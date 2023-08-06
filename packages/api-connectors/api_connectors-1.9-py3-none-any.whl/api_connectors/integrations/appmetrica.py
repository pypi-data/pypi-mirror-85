from datetime import datetime
from typing import Union

from furl import furl

from api_connectors.templates.base import BaseApi

VERSION = 'v1'


class YandexAuthApi(BaseApi):
    """ Implements Oauth api (Passport) of Yandex services """

    def __init__(self,
                 access_token: str,
                 refresh_token: str,
                 expires_in: int,
                 base_url: Union[str, furl],
                 client_id: str,
                 client_secret: str):
        super().__init__(base_url)

        self.client_id = client_id
        self.client_secret = client_secret
        self.expires_in = expires_in
        self.refresh_token = refresh_token
        self.access_token = access_token

        self.headers = dict(Host=self.host)

    def update_token(self):
        now = datetime.now().timestamp()
        url = furl(self.base_url).add(path='token')
        body = dict(
            grant_type='refresh_token', refresh_token=self.refresh_token, client_id=self.client_id,
            client_secret=self.client_secret
        )

        response: dict = self.make_request('POST', url, data=body, encode='x-www-form-urlencoded')

        self.access_token = response['access_token']
        self.expires_in = now + response['expires_in']

        return self.access_token


class AppmetricaLogsApi(BaseApi):
    """ Implements Logs API section of Appmetrica

    Documentation: https://appmetrica.yandex.ru/docs/mobile-api/logs/about.html
    """

    def __init__(self, base_url: Union[str, furl], oauth_api: 'YandexAuthApi'):
        super().__init__(furl(base_url).set(path=f'/logs/{VERSION}'))

        self.oauth_api = oauth_api
        self.headers = {
            'Authorization': f'OAuth {self.oauth_api.access_token}',
            'Host': self.host
        }

    def paginate_request(self, method: str, url: furl, params: dict):
        ...

    def export_installations(self,
                             application_id: int,
                             start_date: datetime,
                             end_date: datetime,
                             fields: list,
                             fmt='csv'):
        """ Documentation: https://appmetrica.yandex.ru/docs/mobile-api/logs/endpoints.html#installations
        :type fmt: can be csv or json
        """
        fmt = '%Y-%m-%d %H:%M:S'
        params = dict(
            application_id=application_id,
            start_date=start_date.strftime(fmt),
            end_date=end_date.strftime(fmt),
            fields=','.join(fields or [])
        )
        url = furl(self.base_url).add(
            path=f'/export/installations.{fmt}',
            query_params=params
        )

        yield from self.paginate_request('GET', url, params)


class AppmetricaApi(BaseApi):
    """ Groups all APIs of appmetrica into single object. Adds business logic and authentication layer for the API.

        :arg access_token: access token to use till authentication (can be expired)
        :arg refresh_token:
        :arg expires_in: a time when the access token becomes expired

    Documentation:
        Authorization: https://appmetrica.yandex.ru/docs/mobile-api/intro/authorization.html
        Logs API: https://appmetrica.yandex.ru/docs/mobile-api/logs/about.html
    """

    def __init__(self,
                 access_token: str,
                 refresh_token: str,
                 expires_in: int,
                 client_id: str,
                 client_secret: str,
                 appmetrica_url: Union[str, furl] = 'https://api.appmetrica.yandex.ru/',
                 oauth_url: Union[str, furl] = 'https://oauth.yandex.ru/'):
        super().__init__(appmetrica_url)

        # Separated APIs within the general API resource
        self.auth = YandexAuthApi(
            access_token, refresh_token, expires_in, oauth_url, client_id, client_secret
        )
        self.auth.update_token()

        self.logs = AppmetricaLogsApi(appmetrica_url, self.auth)
