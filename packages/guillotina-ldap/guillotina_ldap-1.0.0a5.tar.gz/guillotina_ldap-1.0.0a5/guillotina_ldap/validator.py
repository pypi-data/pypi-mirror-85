from guillotina.component import get_utility
from guillotina_ldap.interfaces import ILDAPUsers
from guillotina.auth import find_user
import bonsai

class LDAPPasswordValidator:
    for_validators = ("basic")

    async def validate(self, token):
        users = get_utility(ILDAPUsers)
        try:
            result = await users.validate_user(token['id'], token['token'])
        except bonsai.AuthenticationError:
            return None

        if result:
            user = users.create_g_user(token['id'])
            return user
        else:
            return None


