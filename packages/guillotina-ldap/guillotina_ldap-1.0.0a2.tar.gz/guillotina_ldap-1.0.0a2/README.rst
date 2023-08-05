GUILLOTINA_LDAP
===============

LDAP Auth backend for guillotina.


Example config.json entry:

.. code-block:: json

    ...
    "applications": ["guillotina_ldap"],
    "ldap": {
        "host": "ldap://myldap.example.com",
        "tls": true,
        "attribute_users": "uid",
        "objecttype": "inetOrgPerson",
        "managerdn": "CM=MANAGER,DC=DOMAIN,DC=ORG",
        "managerpwd": "secret",
        "usersdn": "OU=USERS,DC=DOMAIN,DC=ORG",
        "managers": ["bob"]
    }



Getting started with development
--------------------------------

Using pip (requires Python > 3.7):

.. code-block:: shell

    python3.7 -m venv .
    ./bin/pip install -e .[test]
    pre-commit install
