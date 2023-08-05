import requests
from ..environment import environment
from ..instance_types.Types import Types
from ..common.common_funcs import get_query_string, get_authorization_token
from .TimeSeriesInstance import TimeSeriesInstance


class TimeSeries:
    def __init__(self, types):
        """
        Time Series object

        This class implements the API for getting time series.
        Not to be confused with TimeSeriesInstance, which holds the actual
        instances.

        Parameters
        ----------
        types : Types
                The list of types available for the current TSI series
        """
        self._types = types

        self.__time_series = None

    def get_by_id(self, series_id, force_refresh=False):
        """
        Get the instances that match the given ID, optionally querying the server

        Parameters
        ----------
        series_id : List [ str ]
                    A list of IDs providing a unique key for the series.
        force_refresh : bool
                        Flag indicating whether the server should be queried or
                        cached data should be used

        Returns
        -------
        TimeSeriesInstance or None

        """
        if force_refresh:
            self.__refresh_series()

        instance = [i for i in self._time_series if i.series_id == series_id]
        if len(instance) == 1:
            return instance[0]

        return None

    def __call__(self, *args, **kwargs):
        """
        Return the list of instances in the TSI, optionally refreshing the list

        Parameters
        ----------
        args : ignored
        kwargs : keyword args
                 Supported vars are:

                    * force_refresh : bool
                                      Flag indicating whether the list should be
                                      forcefully re-read from the TSI.

        Returns
        -------
        List [ TimeSeriesIntance ] : The list of time series instances
        """
        if kwargs.get('force_refresh', False):
            self.__refresh_series()

        return self._time_series

    @property
    def _time_series(self):
        if self.__time_series is None:
            self.__refresh_series()

        return self.__time_series

    def __refresh_series(self):
        """
        Download the list of Time Series Instances from the TSI
        """
        base_url = f'https://{environment.ENVIRONMENT_ID}.env.timeseries.azure.com/' \
                   f'timeseries/instances/'
        authorizationToken = get_authorization_token()

        querystring = get_query_string()
        payload = ""

        headers = {
            'x-ms-client-application-name': environment.APPLICATION_NAME,
            'Authorization': authorizationToken,
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        response = requests.request('GET', base_url, data=payload,
                                    headers=headers, params=querystring)

        json_response = response.json()
        result = response.json()

        while len(json_response['instances']) > 999 and 'continuationToken' in list(json_response.keys()):
            headers = {
                'x-ms-client-application-name': environment.APPLICATION_NAME,
                'Authorization': authorizationToken,
                'x-ms-continuation': json_response['continuationToken'],
                'Content-Type': "application/json",
                'cache-control': "no-cache"
            }
            response = requests.request('GET', base_url, data=payload,
                                        headers=headers, params=querystring)
            json_response = response.json()

            result['instances'].extend(json_response['instances'])

        self.__time_series = [TimeSeriesInstance(series_type=[t for t in self._types(force_refresh=True)
                                                              if ts['typeId'] == t.type_id][0],
                                                 series_id=ts['timeSeriesId'],
                                                 name=ts.get('name'),
                                                 description=ts.get('description'),
                                                 instance_fields=ts.get('instanceFields'))
                              for ts in result['instances']]
