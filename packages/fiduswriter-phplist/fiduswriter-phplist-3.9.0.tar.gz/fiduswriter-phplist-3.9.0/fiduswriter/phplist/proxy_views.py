from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.escape import json_decode
from base.django_handler_mixin import DjangoHandlerMixin
from urllib.parse import urlencode
from django.conf import settings
from allauth.account.models import EmailAddress
from urllib.parse import urljoin


class Proxy(DjangoHandlerMixin, RequestHandler):

    async def post(self, relative_url):
        if not hasattr(settings, 'PHPLIST_BASE_URL'):
            self.finish()
        self.url = urljoin(
            settings.PHPLIST_BASE_URL,
            '/admin/?page=call&pi=restapi'
        )
        self.relative_url = relative_url
        await self.login()

    async def login(self):
        post_data = {
            'cmd': 'login',
            'login': settings.PHPLIST_LOGIN,
            'password': settings.PHPLIST_PASSWORD
        }
        if hasattr(settings, 'PHPLIST_SECRET'):
            post_data['secret'] = settings.PHPLIST_SECRET
        http = AsyncHTTPClient()
        try:
            response = await http.fetch(
                HTTPRequest(
                    self.url,
                    'POST',
                    None,
                    urlencode(post_data)
                )
            )
        except ConnectionRefusedError:
            self.set_status(404)
            self.finish()
            return
        if response.error:
            self.set_status(404)
            self.finish()
            return
        self.session_cookie = response.headers['Set-Cookie']
        if self.relative_url == 'subscribe_email':
            await self.subscribe_email()
        else:
            self.set_status(401)
            self.finish()
            return

    async def subscribe_email(self):
        email = self.get_argument('email')
        email_object = EmailAddress.objects.filter(email=email).first()
        if not email_object:
            self.finish()
            return
        post_data = {
            'cmd': 'subscriberAdd',
            'email': email,
            'foreignkey': '',
            'confirmed': 1,
            'htmlemail': 1,
            'disabled': 0
        }
        if hasattr(settings, 'PHPLIST_SECRET'):
            post_data['secret'] = settings.PHPLIST_SECRET
        http = AsyncHTTPClient()
        response = await http.fetch(
            HTTPRequest(
                self.url,
                'POST',
                {'Cookie': self.session_cookie},
                urlencode(post_data)
            )
        )
        if response.error:
            response.rethrow()
        response_json = json_decode(response.body)
        if response_json['status'] == 'error':
            # could not create user with this email
            self.finish()
            return
        subscriber_id = response_json['data']['id']
        post_data = {
            'cmd': 'listSubscriberAdd',
            'list_id': settings.PHPLIST_LIST_ID,
            'subscriber_id': subscriber_id
        }
        if hasattr(settings, 'PHPLIST_SECRET'):
            post_data['secret'] = settings.PHPLIST_SECRET
        http = AsyncHTTPClient()
        response = await http.fetch(
            HTTPRequest(
                self.url,
                'POST',
                {'Cookie': self.session_cookie},
                urlencode(post_data)
            )
        )
        if response.error:
            response.rethrow()
        self.finish()
