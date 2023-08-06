from guillotina.auth.users import GuillotinaUser


class LDAPGuillotinaUser(GuillotinaUser):

    async def set_password(self, password):
        util = get_utility(ILDAPUsers)
        await util.set_password(self.id, password)