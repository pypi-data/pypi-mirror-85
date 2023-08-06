from guillotina import configure
from guillotina.interfaces import IResource
from guillotina.api.service import Service
from guillotina.component import get_utility


@configure.service(
    context=IResource, method='POST',
    permission='guillotina.AccessContent', name='@setpassword',
    summary='Set password for user',
    responses={
        "200": {
            "description": "Result results on workflows",
            "schema": {
                "properties": {}
            }
        }
    })
class PasswordSet(Service):

    async def __call__(self):
        util = get_utility(ILDAPUsers)
        await util.set_password(user, password)
