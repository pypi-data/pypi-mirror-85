import logging
from collections import UserList
from datetime import date, datetime
from typing import List

import httplib2
from apiclient import discovery
from oauth2client.client import OAuth2Credentials


class GoogleListResponse(UserList):
    """ Default wrapper for  """

    def __init__(self, api_response: dict):
        super().__init__(initlist=api_response.pop('items'))

        self.kind = api_response.pop('kind', None)
        self.username = api_response.pop('username', None)
        self.total_results = api_response.pop('totalResults', None)
        self.start_index = api_response.pop('startIndex', None)
        self.items_per_page = api_response.pop('itemsPerPage', None)

        self.others = api_response


class GoogleAnalyticsAPI_V4:
    """ Google Analytics API is a proxy sub-library for an origin Python API library of Google.
        So it is rather different from other APIs.

        :arg credentials:

        For now, here supports only Core API v3
        Documentation: https://developers.google.com/analytics/devguides/reporting/core/v3?hl=ru
    """

    def __init__(self, credentials: dict):
        if isinstance(credentials['token_expiry'], str):
            token_expiry = datetime.strptime(credentials['token_expiry'], '%Y-%m-%dT%H:%M:%SZ')
        else:
            token_expiry = credentials['token_expiry']

        self.oauth_creds = OAuth2Credentials(
            credentials['access_token'],
            credentials['client_id'],
            credentials['client_secret'],
            credentials['refresh_token'],
            token_expiry,
            credentials['token_uri'],
            credentials['user_agent'],
            revoke_uri=credentials.get('revoke_uri', None),
            id_token=credentials.get('id_token', None),
            token_response=credentials.get('token_response', None)
        )

        self.oauth_creds.invalid = credentials['invalid']
        self.refresh()
        http_auth = self.oauth_creds.authorize(httplib2.Http(timeout=360))
        self.client = discovery.build('analyticsreporting', 'v4', http=http_auth)

    def refresh(self):
        if self.oauth_creds.access_token_expired:
            http = httplib2.Http(timeout=360)
            self.oauth_creds.refresh(http)

    def get_report(self,
                     profile_id: str,
                     metrics: List[str],
                     dimensions: List[str],
                     start_date: date,
                     end_date: date,
                     filters: List[dict],
                     max_results=10_000,
                     batch_limit=0):
        params = {
                'reportRequests': [
                    {
                        'viewId': f'ga:{profile_id}',
                        'dateRanges': [
                            {
                                'startDate': start_date.strftime('%Y-%m-%d'),
                                'endDate': end_date.strftime('%Y-%m-%d')
                            }],
                        'metrics': [{'expression': metr} for metr in metrics],
                        'dimensions': [{'name': dim} for dim in dimensions],
                        "samplingLevel": 'LARGE',
                        'pageSize': max_results,
                        "metricFilterClauses": [{
                            "filters": [{
                                "metricName": f_r['metric'],
                                "operator": f_r['op'],
                                "comparisonValue": f_r['value']
                            } for f_r in filters]
                        }]

                    }
                ]
            }

        first_response = self.client.reports().batchGet(body=params).execute()['reports'][0]
        total_results = int(first_response['data']['totals'][0]['values'][0])

        yield_handler = lambda x: [*x['dimensions'], *[y['values'][0] for y in x['metrics']]]
        rows = first_response['data'].get('rows', [])
        yield from map(yield_handler, rows)

        batch_limit -= 1
        if total_results > max_results:
            params['reportRequests'][0]['pageToken'] = first_response['nextPageToken']
            while batch_limit != 0:
                response = self.client.reports().batchGet(body=params).execute()['reports'][0]

                yield from map(yield_handler, rows)
                batch_limit -= 1

                start_index = int(response['nextPageToken'])
                cur_index = max_results + start_index
                if total_results > cur_index and batch_limit != start_index // max_results:
                    params['reportRequests'][0]['pageToken'] = response['nextPageToken']
                else:
                    break

class GoogleAnalyticsAPI_V3:
    """ Google Analytics API is a proxy sub-library for an origin Python API library of Google.
        So it is rather different from other APIs.

        :arg credentials:

        For now, here supports only Core API v3
        Documentation: https://developers.google.com/analytics/devguides/reporting/core/v3?hl=ru
    """

    def __init__(self, credentials: dict):
        self.oauth_creds = OAuth2Credentials(
            credentials['access_token'],
            credentials['client_id'],
            credentials['client_secret'],
            credentials['refresh_token'],
            credentials['token_expiry'],
            credentials['token_uri'],
            credentials['user_agent'],
            revoke_uri=credentials.get('revoke_uri', None),
            id_token=credentials.get('id_token', None),
            token_response=credentials.get('token_response', None)
        )

        self.oauth_creds.invalid = credentials['invalid']
        self.refresh()
        http_auth = self.oauth_creds.authorize(httplib2.Http(timeout=360))
        self.client = discovery.build('analytics', 'v3', http=http_auth)

    def refresh(self):
        if self.oauth_creds.access_token_expired:
            http = httplib2.Http(timeout=360)
            self.oauth_creds.refresh(http)

    def list_accounts(self):
        response = self.client.management().accounts().list().execute()
        return GoogleListResponse(response)

    def list_webproperties(self, account_id):
        response = self.client.management().webproperties().list(
            accountId=account_id
        ).execute()

        return GoogleListResponse(response)

    def list_profiles(self, account_id, webproperty_id):
        response = self.client.management().profiles().list(
            accountId=account_id,
            webPropertyId=webproperty_id
        ).execute()

        return GoogleListResponse(response)

    def list_data_sources(self, account_id, webproperty_id):
        response = self.client.management().customDataSources().list(
            accountId=account_id,
            webPropertyId=webproperty_id
        ).execute()

        return GoogleListResponse(response)

    def list_dimensions(self, account_id, webproperty_id):
        response = self.client.management().customDimensions().list(
            accountId=account_id,
            webPropertyId=webproperty_id
        ).execute()

        return GoogleListResponse(response)

    def data_request(self,
                     profile_id: str,
                     metrics: List[str],
                     dimensions: List[str],
                     start_date: date,
                     end_date: date,
                     filters: List[str],
                     is_accessed_sampling=True,
                     sampling_level='HIGHER_PRECISION',
                     max_results=9999,
                     batch_limit=0):
        """ Executes request to Google Analytics for data.

        :param profile_id:
        :param metrics:
        :param dimensions:
        :param start_date:
        :param end_date:
        :param filters:
        :param is_accessed_sampling:
        :param sampling_level:
        :param max_results:
        :param batch_limit:

        :rtype: list
        """
        if len(dimensions) > 7:
            raise Exception('Only 8 dimensions are allowed')

        params = dict(
            ids=f'ga:{profile_id}',
            max_results=max_results,
            samplingLevel=sampling_level,
            metrics=','.join(metrics),
            dimensions=','.join(dimensions),
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            filters=';'.join(filters),
        )
        first_response = self.client.data().ga().get(**params).execute(num_retries=3)
        total_results = first_response['totalResults']

        if not is_accessed_sampling and first_response['containsSampledData']:
            raise Exception(f'Contains sampled data. Request: {params}')

        if batch_limit == 1:
            rows = first_response.get('rows', [])
            logging.info(f'Received {total_results} records')
            yield from rows

        if total_results > first_response['itemsPerPage']:
            params['start_index'] = max_results - 1
            yield from rows
            while True:
                response = self.client.data().ga().get(**params).execute(num_retries=3)

                start_index = response['query']['start-index']

                yield from response['rows']

                cur_index = max_results + start_index
                if total_results > cur_index and batch_limit != start_index // max_results:
                    params['start_index'] = cur_index
                else:
                    break
