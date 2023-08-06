from guillotina.interfaces import IPrincipal
from guillotina.component import get_utility
from guillotina_ldap.interfaces import ILDAPUsers

import typing


class LDAPUserIdentifier:
    async def get_user(self, token: typing.Dict) -> typing.Optional[IPrincipal]:
        """Returns the current user associated with the token and None if user
        could not be found.

        """
        users = get_utility(ILDAPUsers)

        user_id = token.get("id", "")
        if not user_id:
            # No user id in the token
            return None

        if not await users.exists(user_id):
            # User id does not correspond to any existing user folder
            return None

        user = users.create_g_user(user_id)
        return user
