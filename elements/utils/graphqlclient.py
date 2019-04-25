from functools import partial
from six.moves import urllib
import asyncio
import json
import ssl

class GraphQLClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.token = None
        self.headername = None

    def execute(self, query, variables=None):
        return self._send(query, variables)

    async def async_execute(self, query, variables=None):
        return await self._async_send(query, variables=None)

    def inject_token(self, token, headername='Authorization'):
        self.token = token
        self.headername = headername

    def _send(self, query, variables):
        data = {'query': query,
                'variables': variables}
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        if self.token is not None:
            headers[self.headername] = '{}'.format(self.token)

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(self.endpoint, json.dumps(data).encode('utf-8'), headers)
        try:
            response = urllib.request.urlopen(req, context=ctx)
            return response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            print((e.read(), data, headers, req))
            print('')
            raise e

    async def _async_send(self, query, variables):
        data = {'query': query,
                'variables': variables}
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        if self.token is not None:
            headers[self.headername] = '{}'.format(self.token)

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(self.endpoint, json.dumps(data).encode('utf-8'), headers)
        try:
            response = await self._request(req, ctx)
            return response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            print((e.read(), data, headers, req))
            print('')
            raise e

    @asyncio.coroutine
    def _request(self, req, context):
        loop = asyncio.get_event_loop()
        response = yield from loop.run_in_executor(None, partial(urllib.request.urlopen, req, context=context))
        return response
