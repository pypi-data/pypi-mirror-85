from guillotina import configure
import glob
import yaml
import logging
import bonsai

bonsai.utils.set_connect_async(True)

logger = logging.getLogger('guillotina_ldap')


app_settings = {
    "load_utilities": {
        "ldap": {
            "provides": "guillotina_ldap.interfaces.ILDAPUsers",
            "factory": "guillotina_ldap.utility.LDAPUtility",
            "settings": {},
        }
    },
    "auth_validation_tasks": {
        "register_user": {
            "executor": "guillotina_ldap.register_user",
            "schema": {"title": "Register new user", "type": "object", "properties": {}},
        },
    },
}

def includeme(root, settings):
    configure.scan("guillotina_ldap.utility")

