from bonsai import LDAPEntry
from bonsai import LDAPClient
from bonsai import LDAPModOp
from bonsai.errors import ConnectionError
from guillotina_ldap.model import LDAPGuillotinaUser
from guillotina_ldap import logger
from guillotina import app_settings
from lru import LRU
import time

USER_CACHE_DURATION = 100
LOCAL_CACHE = LRU(100)


def get_user_cache_key(login):
    return '{}-{}'.format(login, int(time.time() // USER_CACHE_DURATION))

class LDAPUtility:
    client = None
    app = None

    def __init__(self, settings={}, loop=None):
        self.loop = loop
        self.ldap = app_settings['ldap']
        self.host = self.ldap.get('host')
        self.tls = self.ldap.get('tls', False)
        self.attribute_users = self.ldap.get('attribute_users', 'uid')
        self.managers = self.ldap.get('managers', [])
        self.objecttype = self.ldap.get('objecttype', 'inetOrgPerson')
        self.base_users = self.ldap.get('usersdn')
        self.managerdn = self.ldap.get('managerdn')
        self.managerpwd = self.ldap.get('managerpwd')
        self.initialized = False

    async def initialize(self, app):
        self.app = app

        if self.host is None:
            raise KeyError("Host is not defined on app settings")

        self.client = LDAPClient(self.host, self.tls)
        if  self.managerdn is not None:
            self.client.set_credentials("SIMPLE", user=self.managerdn, password=self.managerpwd)
            retries = 0
            conected = None
            while(retries < 3 and conected is None):
                try:
                    async with self.client.connect(is_async=True) as conn:
                        conected = await conn.whoami()
                        logger.info(f"Connected with user {conected}")
                        self.initialized = True
                except ConnectionError:
                    pass
                retries += 1
        if self.initialized is False:
            logger.error(f"NOT connected to LDAP server {self.host}")

    async def finalize(self, app):
        pass

    async def exists(self, login):
        cache_key = get_user_cache_key(login)
        try:
            return LOCAL_CACHE[cache_key]
        except KeyError:
            pass

        exist = False
        async with self.client.connect(is_async=True) as conn:
            results = await conn.search(self.user(login), 1)
            if len(results) > 0:
                exist = True
        LOCAL_CACHE[cache_key] = exist
        return exist

    def create_g_user(self, login): 
        user = LDAPGuillotinaUser(user_id=login)
        user._roles['guillotina.Member'] = 1

        if login in self.managers:
            user._roles['guillotina.ContainerAdmin'] = 1
        
        user._ldap_provider = 1
        return user

    def user(self, login):
        if self.base_users is None:
            raise KeyError("Base users should be defined")
        assert "=" not in login
        assert "," not in login
        return f"{self.attribute_users}={login},{self.base_users}"

    async def search_user(self, login):
        async with self.client.connect(is_async=True) as conn:
            results = await conn.search(self.user(login), 1)
            for res in results:
                print(res['givenName'][0])

    async def set_password(self, login, password):
        async with self.client.connect(is_async=True) as conn:
            search = await conn.search(self.user(login), 0)
            entry = search[0]
            entry.change_attribute("userPassword", LDAPModOp.REPLACE, password)
            await entry.modify()

    async def add_user(self, login):
        obj = LDAPEntry(self.user(login))
        obj['objectClass'] = ['top', self.objecttype] # Must set schemas to get a valid LDAP entry.
        obj[self.attribute_users] = login
        if self.objecttype == 'inetOrgPerson' and self.attribute_users != 'sn':
            obj['sn'] = login
        if self.objecttype == 'inetOrgPerson' and self.attribute_users != 'cn':
            obj['cn'] = login
        obj[self.attribute_users] = login
        async with self.client.connect(is_async=True) as conn:
            await conn.add(obj)

    async def validate_user(self, login, password):
        client = LDAPClient(self.host, self.tls)
        client.set_credentials("SIMPLE", user=self.user(login), password=password)
        result = False
        async with self.client.connect(is_async=True) as conn:
            user = await conn.whoami()
            logger.info(f"Authentication {user}")
            result = True
        return result
