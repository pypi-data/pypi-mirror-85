import logging
import requests
from .Type import Type
from ..environment import environment
from ..variables.Variable import variable_helper
from ..common.common_funcs import get_query_string, get_authorization_token


class Types:
    def __init__(self):
        """
        Types object

        This class implements the API for getting types from the TSI.
        Not to be confused with Type, which holds the actual types.
        """
        self.__types = None

    def __call__(self, *args, **kwargs):
        """
        Return the list of types in the TSI, optionally refreshing the list

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
        List [ Type ] : The list of type
        """
        if kwargs.get('force_refresh', False):
            self.__refresh_types()

        return self._types

    @property
    def _types(self):
        if self.__types is None:
            self.__refresh_types()

        return self.__types

    def __refresh_types(self):
        """
        Download the list of types from the TSI
        """
        url = f'https://{environment.ENVIRONMENT_ID}.env.timeseries.azure.com/timeseries/types'
        payload = ''
        headers = {
            'x-ms-client-application-name': environment.APPLICATION_NAME,
            'Authorization': get_authorization_token(),
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        try:
            response = requests.request(
                "GET",
                url,
                data=payload,
                headers=headers,
                params=get_query_string(),
                timeout=10
            )
            response.raise_for_status()

        except requests.exceptions.ConnectTimeout:
            logging.error('pyTSI: The request to the TSI API timed out.')
            raise
        except requests.exceptions.HTTPError:
            logging.error('pyTSI: The request to the TSI API returned an unsuccessful status code.')
            raise

        self.__types = []
        for t in response.json()['types']:
            self.__types.append(Type(type_id=t['id'],
                                     name=t['name'],
                                     description=t.get('description'),
                                     vars=[variable_helper(k, v)
                                           for k, v in t['variables'].items()]))
