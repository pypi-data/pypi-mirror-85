from guillotina import app_settings
from guillotina.auth import authenticate_user
from guillotina.events import UserLogin
from guillotina_ldap.interfaces import ILDAPUsers
from guillotina.component import get_utility
from guillotina.auth.utils import find_user
from guillotina.event import notify
import bonsai


async def run(token_data, payload):
    util = get_utility(ILDAPUsers)

    try:
        await util.add_user(token_data["id"])
    except bonsai.AlreadyExists:
        pass

    if "password" in token_data:
        await util.set_password(token_data["id"], token_data['password'])

    user = util.create_g_user(token_data['id'])

    jwt_token, data = authenticate_user(user.id, timeout=app_settings["jwt"]["token_expiration"])
    await notify(UserLogin(user, jwt_token))

    return {"exp": data["exp"], "token": jwt_token}

