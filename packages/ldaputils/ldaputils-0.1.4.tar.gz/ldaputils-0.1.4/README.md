# ldaputils

Ldap utils library.

## Install

```
pip install ldaputils
```

## Usage

```
# use your own host, port, username and password values.
# username must be a fully qualified dn.
# Use ipython help to see more init parameters.
server = LdapService(
    host="localhost,
    port=389,
    username="cn=admin,dc=example,dc=com",
    password="adminpassword",
)

name = nameutils.get_random_name() # use fastutils.nameutils.get_random_name for test
username = pinyinutils.to_pinyin(name).lower()
user_detail = {
    "cn": name,
    "ou": "AI Tech Group",
    "l": "HangZhou, China",
}
assert self.server.add_user_entry(username, user_detail)
assert self.server.delete_user_entry(username)
```

## Releases

### v0.1.4 2020/11/17

- Add util functions.

### v0.1.0 2020/11/14

- First release.
- Add, update, delete user entry function ready.
- Get user and get users function ready.

