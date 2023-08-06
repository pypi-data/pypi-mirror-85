import json
import uuid
import random
import logging

import ldap3
from fastutils import hashutils
from fastutils import nameutils


logger = logging.getLogger(__name__)


class LdapService(object):

    # used to break dead loop while something unknown happen
    LDAP_MAX_ENTRIES = 100 * 10000

    DEFAULT_USER_BASE_DN_TEMPLATE = "cn=users,{base_dn}"
    DEFAULT_USER_DN_TEMPLATE = "uid={username},{user_base_dn}"
    DEFAULT_USER_SEARCH_TEMPLATE = "(&(objectclass=inetOrgPerson)(uid={username}))"
    DEFAULT_USER_ATTR_OBJECT_CLASSES = [
        "top",
        "inetOrgPerson",
        "posixAccount",
    ]
    DEFAULT_USER_ATTR_HOME_DIRECTORY_TEMPLATE = "/home/{username}"
    DEFAULT_USER_ATTR_UID_NUMBER = 9999999
    DEFAULT_USER_ATTR_GID_NUMBER = 9999999
    DEFAULT_USER_ATTR_OU = "Default Department"
    DEFAULT_USER_ATTR_L = "Default Location"

    def __init__(self,
            host="localhost",
            port=389,
            username=None,
            password=None,
            base_dn=None,
            server_params=None,
            connection_params=None,
            raise_error=False,
            default_user_base_dn_template=None,
            default_user_dn_template=None,
            default_user_search_template=None,
            default_user_attr_object_classes=None,
            default_user_attr_home_directory_template=None,
            default_user_attr_uid_number=None,
            default_user_attr_gid_number=None,
            default_user_attr_ou=None,
            default_user_attr_l=None,
            ):
        self.user_base_dn_template = default_user_base_dn_template or self.DEFAULT_USER_BASE_DN_TEMPLATE
        self.user_dn_template = default_user_dn_template or self.DEFAULT_USER_DN_TEMPLATE
        self.user_search_template = default_user_search_template or self.DEFAULT_USER_SEARCH_TEMPLATE
        self.user_attr_object_classes = default_user_attr_object_classes or self.DEFAULT_USER_ATTR_OBJECT_CLASSES
        self.default_user_attr_home_directory_template = default_user_attr_home_directory_template or self.DEFAULT_USER_ATTR_HOME_DIRECTORY_TEMPLATE
        self.default_user_attr_uid_number = default_user_attr_uid_number or self.DEFAULT_USER_ATTR_UID_NUMBER
        self.default_user_attr_gid_number = default_user_attr_gid_number or self.DEFAULT_USER_ATTR_GID_NUMBER
        self.default_user_attr_ou = default_user_attr_ou or self.DEFAULT_USER_ATTR_OU
        self.default_user_attr_l = default_user_attr_l or self.DEFAULT_USER_ATTR_L
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.raise_error = raise_error
        self.server_params = {
            "get_info": ldap3.ALL,
        }
        self.server_params.update(server_params or {})
        self.connection_params = {}
        self.connection_params.update(connection_params or {})
        if username and password:
            self.connection_params.update({
                "user": username,
                "password": password,
            })
        self.base_dn = base_dn or self.auto_get_base_dn()

    def auto_get_base_dn(self):
        connection = self.get_connection()
        base_dns = [x for x in connection.server.info.naming_contexts if "dc=" in x]
        if base_dns:
            return base_dns[0]
        else:
            return None

    def get_connection(self):
        server = ldap3.Server(self.host, self.port, **self.server_params)
        connection = ldap3.Connection(server, **self.connection_params)
        connection.start_tls()
        connection.bind()
        return connection

    def get_user_base_dn(self, username):
        return self.user_base_dn_template.format(base_dn=self.base_dn)

    def get_user_dn(self, username):
        return self.user_dn_template.format(username=username, user_base_dn=self.get_user_base_dn(username))

    def get_user_search_filter(self, username):
        return self.user_search_template.format(username=username)

    def get_user_object_classes(self, username, user_detail=None):
        return self.user_attr_object_classes

    def get_default_user_attr_home_directory(self, username, user_detail=None):
        user_detail = user_detail or {}
        if "homeDirectory" in user_detail:
            return user_detail["homeDirectory"]
        else:
            return self.default_user_attr_home_directory_template.format(username=username, user_detail=user_detail)

    def get_default_user_attr_uid_number(self, username, user_detail=None):
        return self.default_user_attr_uid_number

    def get_default_user_attr_gid_number(self, username, user_detail=None):
        user_detail = user_detail or {}
        if "uidNumber" in user_detail:
            return user_detail["uidNumber"]
        return self.default_user_attr_gid_number

    def get_default_user_attr_user_password(self, username, user_detail=None):
        # bad sha password
        return "{BAD}RESET_YOUR_PASSWORD" + hashutils.get_sha1_base64(str(uuid.uuid4()))

    def get_default_user_attr_cn(self, username, user_detail=None):
        return username

    def get_default_user_attr_sn(self, username, user_detail=None):
        user_detail = user_detail or {}
        cn = user_detail.get("cn", username)
        return nameutils.guess_surname(cn)

    def get_default_user_attr_ou(self, username, user_detail=None):
        return self.default_user_attr_ou

    def get_default_user_attr_l(self, username, user_detail=None):
        return self.default_user_attr_l
    @classmethod
    def entry_to_json(cls, user_entry):
        user_detail = json.loads(user_entry.entry_to_json())
        data = {
            "dn": user_detail["dn"],
        }
        data.update(user_detail["attributes"])
        for key in data.keys():
            value = data[key]
            if isinstance(value, (list, set, tuple)) and len(value) == 1:
                data[key] = value[0]
        return data

    def get_user(self, username, connection=None):
        user_entry = self.get_user_entry(username, connection)
        if not user_entry:
            return None
        return self.entry_to_json(user_entry)

    def get_user_entry(self, username, connection=None):
        connection = connection or self.get_connection()
        connection.search(
            search_base=self.get_user_base_dn(username),
            search_filter=self.get_user_search_filter(username),
            attributes=[ldap3.ALL_ATTRIBUTES, ldap3.ALL_OPERATIONAL_ATTRIBUTES],
            )
        if len(connection.entries):
            return connection.entries[0]
        else:
            return None

    def get_users(self, paged_size=200, connection=None):
        entries = self.get_user_entries(paged_size=paged_size, connection=connection)
        return list(map(self.entry_to_json, entries))

    def get_user_entries(self, paged_size=200, connection=None):
        entries = []
        connection = connection or self.get_connection()
        extra_params = {}
        counter = 0
        while True:
            counter += 1
            if counter > self.LDAP_MAX_ENTRIES / paged_size:
                error_message = "LdapService.get_user_entries hit the max limit: {0}".format(self.LDAP_MAX_ENTRIES)
                logger.error(error_message)
                raise RuntimeError(error_message)
            connection.search(
                search_base=self.get_user_base_dn("*"),
                search_filter=self.get_user_search_filter("*"),
                attributes=[ldap3.ALL_ATTRIBUTES, ldap3.ALL_OPERATIONAL_ATTRIBUTES],
                paged_size=paged_size,
                **extra_params
                )
            entries += connection.entries
            paged_cookie = connection.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
            if paged_cookie:
                extra_params["paged_cookie"] = paged_cookie
            else:
                break
        return entries

    def update_user_entry(self, username, user_changes, connection=None):
        dn = self.get_user_dn(username)
        connection = connection or self.get_connection()
        changes = {}
        for key, value in user_changes.items():
            if isinstance(value, (list, set, tuple)):
                values = list(value)
            else:
                values = [value]
            changes[key] = [(ldap3.MODIFY_REPLACE, values)]
        logger.info("update user entry: dn={0}, connection={1}, changes={2}".format(dn, connection, changes))
        success = connection.modify(dn, changes)
        logger.info("update user entry: dn={0}, success={1}, result={2}".format(dn, success, connection.result))
        if success:
            return True
        else:
            if not self.raise_error:
                return False
            else:
                raise RuntimeError(connection.result)

    def delete_user_entry(self, username, connection=None):
        dn = self.get_user_dn(username)
        connection = connection or self.get_connection()
        logger.info("delete user entry: dn={0}, connection={1}".format(dn, connection))
        success = connection.delete(dn)
        logger.info("delete user entry: dn={0}, success={1}, result={2}".format(dn, success, connection.result))
        if success:
            return True
        else:
            if not self.raise_error:
                return False
            else:
                raise RuntimeError(connection.result)

    def modify_user_password(self, username, new_password, connection=None):
        dn = self.get_user_dn(username)
        connection = connection or self.get_connection()
        logger.info("modify user password: dn={0}, connection={1}".format(dn, connection))
        success = connection.extend.standard.modify_password(user=dn, new_password=new_password)
        logger.info("modify user password: dn={0}, success={1}, result={2}".format(dn, success, connection.result))
        if success:
            return True
        else:
            if not self.raise_error:
                return False
            else:
                raise RuntimeError(connection.result)

    def modify_user_password_by_encoded_password(self, username, password_encoded, connection=None):
        dn = self.get_user_dn(username)
        connection = connection or self.get_connection()
        logger.info("modify user password: dn={0}, connection={1}".format(dn, connection))
        user_changes = {
            "userPassword": password_encoded,
        }
        success = self.update_user_entry(username, user_changes=user_changes, connection=connection)
        logger.info("modify user password: dn={0}, success={1}, result={2}".format(dn, success, connection.result))
        if success:
            return True
        else:
            if not self.raise_error:
                return False
            else:
                raise RuntimeError(connection.result)

    def add_user_entry(self, username, user_detail=None, user_object_classes=None, connection=None):
        user_detail = user_detail or {}
        dn = self.get_user_dn(username)
        connection = connection or self.get_connection()
        self.set_default_entry_attrs(username, user_detail)
        if user_object_classes:
            user_detail["objectClass"] = user_object_classes
        logger.info("add user entry: dn={0}, connection={1}, user_object_classes={2}, user_detail={3}".format(dn, connection, user_object_classes, user_detail))
        success = connection.add(dn, user_object_classes, user_detail)
        logger.info("add user entry: dn={0}, success={1}, result={2}".format(dn, success, connection.result))
        if success:
            return True
        else:
            if not self.raise_error:
                return False
            else:
                raise RuntimeError(connection.result)

    def set_default_entry_attrs(self, username, user_detail):
        if not "objectClass" in user_detail:
            user_detail["objectClass"] = self.get_user_object_classes(username, user_detail)
        if not "uid" in user_detail:
            user_detail["uid"] = username
        if not "homeDirectory" in user_detail:
            user_detail["homeDirectory"] = self.get_default_user_attr_home_directory(username, user_detail)
        if not "uidNumber" in user_detail:
            user_detail["uidNumber"] = self.get_default_user_attr_uid_number(username, user_detail)
        if not "gidNumber" in user_detail:
            user_detail["gidNumber"] = self.get_default_user_attr_gid_number(username, user_detail)
        if not "userPassword" in user_detail:
            user_detail["userPassword"] = self.get_default_user_attr_user_password(username, user_detail)
        if not "cn" in user_detail:
            user_detail["cn"] = self.get_default_user_attr_cn(username, user_detail)
        if not "sn" in user_detail:
            user_detail["sn"] = self.get_default_user_attr_sn(username, user_detail)
        if not "ou" in user_detail:
            user_detail["ou"] = self.get_default_user_attr_ou(username, user_detail)
        if not "l" in user_detail:
            user_detail["l"] = self.get_default_user_attr_l(username, user_detail)

    def authenticate(self, username, password):
        dn = self.get_user_dn(username)
        connection = self.get_connection()
        success = connection.rebind(dn, password)
        if success:
            return True
        else:
            if not self.raise_error:
                return False
            else:
                raise RuntimeError(connection.result)

