import os
from fastutils import fsutils

def get_base_dn_from_domain(domain):
    dn =  ",".join(["dc="+x for x in domain.split(".")])
    return dn

def get_dn_from_path(path, domain=None):
    paths = path.split(".")
    if not domain:
        domains = paths[-2:]
        paths = paths[:-2]
    else:
        domains = domain.split(".")
    ds = []
    ds += ["cn="+x for x in paths]
    ds += ["dc="+x for x in domains]
    dn = ",".join(ds)
    return dn

def ldapimport(ldap_filepath):
    cmd = "ldapadd -Y EXTERNAL -H ldapi:/// -f {ldap_filepath}".format(ldap_filepath=ldap_filepath)
    return os.system(cmd)

def ldap_template_import(template_filename, context, template_root=None, test=False):
    template_filepath = template_root and os.path.abspath(os.path.join(template_root, template_filename)) or template_filename
    template = fsutils.readfile(template_filepath)
    ldif_content = template.format(**context)
    print(ldif_content)
    with fsutils.TemporaryFile(content=ldif_content) as fileinstance:
        if not test:
            ldapimport(fileinstance.filepath)
