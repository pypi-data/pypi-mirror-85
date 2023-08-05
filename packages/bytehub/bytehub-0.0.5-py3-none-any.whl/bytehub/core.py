# """
# A feature store client. This module exposes an API for interacting with feature stores in Bytehub.
# It hides complexity and provides utility methods such as:
#     - `configure()`
#     - `create_feature()`
#     - `get_feature()`.
#     #- `project_featurestore()`.
#     #- `get_featuregroup()`.
#     - `get_timeseries()`.
#     #- `sql()`
#     #- `insert_into_featuregroup()`
#     #- `get_featurestore_metadata()`
#     #- `get_project_featurestores()`
#     #- `get_featuregroups()`
#     #- `get_training_datasets()`
# """


import os
import itertools
import operator
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import gzip
from getpass import getpass
import time
import json
import re
import types
import dill
import base64


class FeatureStore():

    """Class for instantiating a ByteHub feature store, with members functions for loading and querying data feeds and configuring metadata.

    Parameters
    ----------
    endpoint : str
        URL for server connection.
    client_id : str, optional
        The client ID of secure feature store account. Can be specified in BYTEHUB_CLIENT_ID environment variable.
    client_secret : str, optional
        Optional client secret (use when a non-interactive login is required). Can be specified in BYTEHUB_CLIENT_SECRET environment variable.
    Returns
    -------
    bh.FeatureStore()
        A ByteHub feature store object

    Examples
    --------
    >>> import bytehub as bh
    >>> fs = bh.FeatureStore()
    """


    def __init__(self, endpoint, client_id=None, client_secret=None):
        # Save the endpoint
        self.endpoint = endpoint
        if endpoint[-1] != '/':
            self.endpoint += '/'
        # Get the Oauth2 URLs
        response = requests.get(self.endpoint + 'auth')
        response.raise_for_status()
        self.urls = response.json()

        # Decide with authentication method to use
        self.client_id = os.environ.get('BYTEHUB_CLIENT_ID', client_id)
        self.client_secret = os.environ.get(
            'BYTEHUB_CLIENT_SECRET', client_secret)
        if self.client_secret:
            # Use client-credentials
            client = BackendApplicationClient(client_id=self.client_id)
            oauth = OAuth2Session(client=client)
            tokens = oauth.fetch_token(
                self.urls['token_url'],
                client_id=self.client_id,
                client_secret=self.client_secret
            )
        else:
            # Use interactive login
            oauth = OAuth2Session(
                client_id, redirect_uri=self.urls['callback_url'])
            authorization_url, state = oauth.authorization_url(
                self.urls['login_url'])
            print(
                f'Please go to {authorization_url} and login. Copy the response code and paste below.')
            code_response = getpass('Response: ')
            tokens = oauth.fetch_token(
                self.urls['token_url'], code=code_response, include_client_id=True
            )
        self.tokens = tokens

    def _check_tokens(self):
        # Check that token hasn't expired
        if time.time() < self.tokens['expires_at'] - 10:
            return True
        else:
            # Token expired... refresh it
            if 'refresh_token' in self.tokens:
                oauth = OAuth2Session(self.client_id, token=self.tokens)
                tokens = oauth.refresh_token(
                    self.urls['token_url'],
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    include_client_id=True
                )
            else:
                # Authenticate again with client credentials
                client = BackendApplicationClient(client_id=self.client_id)
                oauth = OAuth2Session(client=client)
                tokens = oauth.fetch_token(
                    self.urls['token_url'],
                    client_id=self.client_id,
                    client_secret=self.client_secret
                )
            self.tokens = tokens

    def _api_headers(self):
        self._check_tokens()
        return {
            'Authorization': self.tokens['access_token'],
        }
    
    def _decode_function(self, encoded_function):
        if isinstance(encoded_function, str):
            encoded_function = encoded_function.encode('utf-8')
        try:
            decoded_function = base64.b64decode(encoded_function)
            func = dill.loads(decoded_function)
        except Exception as e:
            raise(e)
        if not isinstance(func, types.FunctionType):
            raise ValueError('This payload does not contain a Python function')
        return func

    def _encode_function(self, func):
        return base64.b64encode(dill.dumps(func)).decode('utf-8')

    def list_features(self, feature=None, regex=None, metadata=False):
        """List features in feature store.

        Parameters
        ----------
        feature : str or list[str], optional
            Only return these features.
        regex : str, optional
            Regular expression to filter feature names.
        metadata : bool, default False
            Return metadata with features.

        Returns
        -------
        list[str] or pd.DataFrame
            A list of features or dataframe of features and metadata.

        Examples
        --------
        >>> fs.list_features()

        ['feature1', 'feature2', 'feature3']

        >>> fs.list_features(regex='weather', metadata=True)
            name            metadata
        ------------------------------------------
        0   weather.actual  {'source': 'NOAA GFS'}
        """

        assert type(metadata) is bool, "metadata is type, bool."
        assert regex is None or isinstance(
            regex, str), "Expecting regex of type, str."

        df = self.get_feature_data_frame(feature=feature, regex=regex)

        if metadata:
            return df[['name', 'metadata']]
        else:
            return df.name.tolist()

    def feature_exists(self, feature):
        """Check whether feature(s) exist.

        Parameters
        ----------
        feature : str or list[str]
            A feature or list of features.

        Returns
        -------
        bool or list[bool]
            A boolean or list of booleans indicating whether feature(s) exist.

        Examples
        --------
        >>> fs.feature_exists(['feature1', 'nonsense'])
        [True, False]
        """

        names = self.list_features(feature=feature)
        if isinstance(feature, list):
            return [f in names for f in feature]
        else:
            return feature in names

    def get_feature_data_frame(self, feature=None, regex=None):
        """Get a dataframe of feature metadata.

        Parameters
        ----------
        feature : str or list[str]
            A feature or list of features.
        regex: str
            A regex to filter results with

        Returns
        -------
        pd.DataFrame
            A dataframe containing feature metadata

        Examples
        --------
        >>> fs.get_feature_data_frame(['feature1', 'feature2'])
            id                                      name            metadata
        ----------------------------------------------------------------------------
        0   0341bacc-e161-11ea-a042-0a53e92ebe18    feature1        {'source': NULL}
        1   193177cc-e158-11ea-a042-0a53e92ebe18    feature2        {'source': NULL}
        """

        params = {}
        if feature:
            if not isinstance(feature, list):
                feature = [feature]
            is_str = [isinstance(f, str) for f in feature]
            assert all(is_str), 'Feature names should be type, str.'
            params['name'] = ','.join(feature)
        if regex:
            assert isinstance(regex, str), 'Regex query should be type, str'
            params['query'] = regex

        url = self.endpoint + 'feature'

        response = requests.get(
            url, params=params, headers=self._api_headers())
        response.raise_for_status()

        result = response.json()
        
        df = pd.DataFrame({'id': [r['id'] for r in result],
                           'name': [r['name'] for r in result],
                           'metadata': [r['metadata'] for r in result]})

        return df

    def get_feature_id(self, feature):
        """Get the unique id number of feature(s).

        Parameters
        ----------
        feature : str or list[str]
            A feature or list of features.

        Returns
        -------
        str or list[str]
            Ids for the feature(s).

        Examples
        --------
        >>> fs.get_feature_id(['feature1', 'feature2'])
        ['0341bacc-e161-11ea-a042-0a53e92ebe18',
        '193177cc-e158-11ea-a042-0a53e92ebe18']
        """

        df = self.get_feature_data_frame(feature=feature)
        if isinstance(feature, str):
            assert feature in df.name.tolist(), f'The feature(s), {feature}, is non-existent.'
            return df[df.name == feature]['id'].iloc[0]
        else:
            assert len(feature) == len(
                df), 'One or more features are non-existent.'
            result = [
                df[df.name == f]['id'].iloc[0]
                for f in feature
            ]
            return result

    def get_feature_metadata(self, feature):
        """Get the metadata for feature(s).

        Parameters
        ----------
        feature : str or list[str]
            A feature or list of features.

        Returns
        -------
        pd.DataFrame
            A dataframe of metadata for feature(s).

        Examples
        --------
        >>> fs.get_feature_metadata(['feature1', 'feature2'])
            name            metadata
        ------------------------------------
        0   feature1        {'source': NULL}
        1   feature2        {'source': NULL}
        """

        df = self.get_feature_data_frame(feature)

        return df[['name', 'metadata']]

    def get_first(self, feature):
        """Gets first entry from feature in feature store per entity.

        Parameters
        ----------
        feature : str
            A feature name.

        Returns
        -------
        pd.DataFrame
            A pandas dataframe of first entry of feature per entity.

        Examples
        --------
        >>> fs.get_first('weather.actual')
            time                        entity      value
        -------------------------------------------------
        0   2020-08-19 23:00:00+00:00   London      21780
        1   2020-08-19 23:00:00+00:00   New York    19774

        """

        assert type(feature) is str, 'Feature type is, str.'

        feature_id = self.get_feature_id(feature)

        url = self.endpoint + f'timeseries/{feature_id}/first'
        response = requests.get(url, headers=self._api_headers())
        response.raise_for_status()

        df = pd.DataFrame(response.json())

        df['time'] = pd.to_datetime(df['time'], utc=True, unit='ms')

        return df

    def get_last(self, feature):
        """Gets last entry from feature in feature store per entity.

        Parameters
        ----------
        feature : str
            A feature name.

        Returns
        -------
        pd.DataFrame
            A pandas dataframe of last entry of feature per entity.

        Examples
        --------
        >>> fs.get_last('weather.actual')
            time                        entity      value
        -------------------------------------------------
        0   2020-08-26 22:30:00+00:00   London      23985
        1   2020-08-26 22:30:00+00:00   New York    22895
        """

        assert type(feature) is str, 'Feature type is, str.'

        feature_id = self.get_feature_id(feature)

        url = self.endpoint + f'timeseries/{feature_id}/last'
        response = requests.get(url, headers=self._api_headers())
        response.raise_for_status()

        df = pd.DataFrame(response.json())

        df['time'] = pd.to_datetime(df['time'], utc=True, unit='ms')

        return df

    def get_freq(self, feature):
        """Gets freq of time column of feature in feature store.

        Parameters
        ----------
        feature : str
            A feature name.

        Returns
        -------
        str
            Datetime freq in units of Pandas offset aliases, https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases

        Examples
        --------
        >>> fs.get_freq('weather.actual')
        '30T'
        """

        assert isinstance(feature, str), 'Feature type is, str.'
        assert self.feature_exists(feature), 'Feature does not exist.'

        feature_id = self.get_feature_id(feature)

        url = self.endpoint + f'timeseries/{feature_id}/freq'
        response = requests.get(url, headers=self._api_headers())
        response.raise_for_status()

        return response.json()['freq']

    def get_timeseries(self, feature, entity=None, from_date=None, to_date=None, freq=None):
        """Gets feature timeseries from feature store.

        Parameters
        ----------
        feature : str or list[str]
            Feature or list of features.
        entity : str or list[str] or list[list] or list[list, None, list, ...], optional
            Entities to filter on. If feature is singular, entity is a str, or a list of entities to filter on. If getting list of features, entity is list[str],
            this filter is applied to each feature in list, if entity is list[list] each feature is filtered by corresponding list of entities. To indicate that
            a feature in the list isn't to be filtered by entity, include an empty list ([]) or None.
        from_date : str, optional
            A datetime string.
        to_date : str, optional
            A datetime string.
        freq : str, optional
            A freq string using pandas offset aliases, https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases, e.g. '1H'.

        Returns
        -------
        pd.DataFrame
            A pandas dataframe of specified data from the feed.

        Examples
        --------
        >>> fs.get_timeseries('weather', entity='London', from_date='2020-01-01 9:00', to_date='2020-01-01 17:00', freq='1H')
        """

        if not isinstance(feature, list):
            feature = [feature]
        exists = self.feature_exists(feature)
        assert all(
            exists), f'The feature(s), {", ".join(list(itertools.compress(feature, map(operator.not_, exists))))}, non-existent.'

        assert isinstance(entity, str) or isinstance(
            entity, list) or entity is None, 'Entity should be of type, str or list[str] or None'
        if entity:
            if not isinstance(entity, list):
                entity = [entity]

        assert from_date is not None, 'from_date cannot be, None. Use bytehub.get_first() to define from_date.'

        if to_date is None:
            to_date = pd.Timestamp.utcnow()

        url = self.endpoint + f'timeseries'
        params = {
            'feature': ','.join(feature),
            'from_date': pd.Timestamp(from_date).isoformat(),
            'to_date': pd.Timestamp(to_date).isoformat(),
            'freq': freq,
            'entity': ','.join(entity) if entity else None
        }
        response = requests.get(
            url, params=params, headers=self._api_headers())
        response.raise_for_status()

        df = pd.DataFrame(response.json())
        if df.empty:
            return pd.DataFrame(
                {
                    col: []
                    for col in ['time', 'entity', *feature]
                }
            )

        df['time'] = pd.to_datetime(df.time, utc=True, unit='ms')

        return df

    def save_timeseries(self, feature, df):
        """Saves a dataframe of timeseries values to the feature store.

        Parameters
        ----------
        feature : str
            A feature name.
        df: pd.DataFrame
            A Pandas Dataframe of timeseries values to save.
            Must contain columns: time, value.
            Optionally can contain columns: entity, created_time.

        Examples
        --------
        >>> fs.save_timeseries('weather.actual', df)
        """

        assert isinstance(feature, str), 'Must save to a single feature'
        assert self.feature_exists(feature), 'Feature does not exist.'
        assert isinstance(
            df, pd.DataFrame), 'Must supply a DataFrame of feature values'
        assert 'time' in df.columns, 'No time column available in DataFrame'
        assert 'value' in df.columns, 'No value column available in DataFrame'
        assert not set(df.columns) - set(['time', 'entity', 'value',
                                          'created_time']), 'Extraneous columns in DataFrame'
        assert is_datetime(
            df.time), 'In DataFrame, time column must be a datetime'
        if 'created_time' in df.columns:
            assert is_datetime(
                df.created_time), 'In DataFrame, created_time column must be a datetime'
        
        feature_id = self.get_feature_id(feature)
        url = self.endpoint + f'timeseries/{feature_id}'

        # Convert payload to JSON
        payload = json.loads(df.to_json(orient='records'))
        headers = self._api_headers()

        if len(df) > 10:
            # Compress the payload
            payload = gzip.compress(json.dumps(payload).encode('utf-8'))
            headers['Content-Type'] = 'application/json'
            headers['Content-Encoding'] = 'gzip'
            response = requests.post(
                url, data=payload, headers=headers
            )
        else:
            response = requests.post(
                url, json=payload, headers=headers
            )
        response.raise_for_status()

    def create_feature(self, name, **kwargs):
        """Adds a feature to the feature store.

        Parameters
        ----------
        feature : str
            Feature name.

        kwargs : dict, optional
            Data to be added to metadata.

        Examples
        --------
        >>> fs.create_feature('weather.actuals', source='NOAA GFS')
        """

        assert isinstance(name, str), 'Feature names should be type, str.'
        assert bool(re.match(r'^[a-zA-Z0-9\./#_-]+$', name)), 'Feature name must only contain alphanumeric .#_-'
        assert not self.feature_exists(name), 'Feature already exists.'

        payload = {
            'name': name,
            'metadata': kwargs
        }
        url = self.endpoint + f'feature'
        response = requests.post(
            url, json=payload, headers=self._api_headers())
        response.raise_for_status()

        data = response.json()

    def create_virtual_feature(self, name, transform, derived_from, params={}, **kwargs):
        """Adds a virtual feature to the feature store.

        Parameters
        ----------
        feature : str
            Feature name.
        transform : str
            Transform name (must be defined already in the feature store)
        derived_from : str or list[str]
            Feature(s) from which this virtual feature derives from
        params : dict, optional
            Optional dictionary of kwargs to be passed to the transform

        kwargs : dict, optional
            Data to be added to metadata.

        Examples
        --------
        >>> fs.create_virtual_feature('weather.actuals', source='NOAA GFS')
        """

        assert isinstance(name, str), 'Feature names should be type, str.'
        assert bool(re.match(r'^[a-zA-Z0-9\./#_-]+$', name)), 'Feature name must only contain alphanumeric .#_-'
        assert not self.feature_exists(name), 'Feature already exists.'
        assert self.transform_exists(transform), 'Transform must exist in the feature store'
        assert isinstance(params, dict), 'params should be a dictionary of name: value pairs'
        if isinstance(derived_from, str):
            derived_from = [derived_from]
        elif isinstance(derived_from, list):
            assert len(derived_from) == 1, 'Multiple derived_from features not implemented yet'
            assert self.feature_exists(derived_from[0]), f'Feature {derived_from} does not exist'
        assert isinstance(derived_from, str) or isinstance(derived_from, list), 'derived_from must be string or list of strings'

        payload = {
            'name': name,
            'transform': self.get_transform_id(transform),
            'compute_type': 'virtual',
            'derived_from': [self.get_feature_id(f) for f in derived_from],
            'params': params,
            'metadata': kwargs
        }
        url = self.endpoint + f'feature'
        response = requests.post(
            url, json=payload, headers=self._api_headers())
        response.raise_for_status()

        data = response.json()

    def delete_feature(self, name):
        """Deletes a feature from the feature store.

        Parameters
        ----------
        feature : str
            Feature name.

        Examples
        --------
        >>> fs.delete_feature('weather.actuals')
        """

        assert isinstance(name, str), 'Feature names should be type, str.'
        assert self.feature_exists(name), 'Feature does not exist.'

        feature_id = self.get_feature_id(name)
        url = self.endpoint + f'feature/{feature_id}'
        response = requests.delete(url, headers=self._api_headers())
        response.raise_for_status()

    def update_feature(self, name, **kwargs):
        """Update a feature in the feature store.

        Parameters
        ----------
        feature : str
            Feature name.

        kwargs : dict, optional
            Data to be added to metadata.

        Examples
        --------
        >>> fs.update_feature('weather.actuals', source='NOAA GFS')
        """

        assert isinstance(name, str), 'Feature names should be type, str.'
        assert self.feature_exists(name), 'Feature does not exist.'

        payload = {
            'name': name,
            'metadata': kwargs
        }
        feature_id = self.get_feature_id(name)
        url = self.endpoint + f'feature/{feature_id}'
        response = requests.patch(
            url, json=payload, headers=self._api_headers())
        response.raise_for_status()

        data = response.json()

    def list_transforms(self, transform=None, regex=None, metadata=False):
        """List transforms in feature store.

        Parameters
        ----------
        transform : str or list[str], optional
            Only return these transforms.
        regex : str, optional
            Regular expression to filter transform names.
        metadata : bool, default False
            Return metadata with transform.

        Returns
        -------
        list[str] or pd.DataFrame
            A list of transforms or dataframe of transforms and metadata.

        Examples
        --------
        >>> fs.list_transforms()

        ['transform1', 'transform2', 'transform3']

        >>> fs.list_transforms(regex='extract.', metadata=True)
            name            metadata
        ------------------------------------------
        0   extract-keys  {'source': 'NOAA GFS'}
        """

        assert type(metadata) is bool, "metadata is type, bool."
        assert regex is None or isinstance(
            regex, str), "Expecting regex of type, str."

        df = self.get_transform_data_frame(transform=transform, regex=regex)

        if metadata:
            return df[['name', 'description', 'transform_type', 'metadata']]
        else:
            return df.name.tolist()

    def transform_exists(self, transform):
        """Check whether transform(s) exist.

        Parameters
        ----------
        transform : str or list[str]
            A transform or list of transform.

        Returns
        -------
        bool or list[bool]
            A boolean or list of booleans indicating whether transform(s) exist.

        Examples
        --------
        >>> fs.transform_exists(['transform1', 'nonsense'])
        [True, False]
        """

        names = self.list_transforms(transform=transform)
        if isinstance(transform, list):
            return [t in names for t in transform]
        else:
            return transform in names
    
    def get_transform_data_frame(self, transform=None, regex=None):
        """Get a dataframe of transform metadata.

        Parameters
        ----------
        transform : str or list[str]
            A transform or list of transforms.
        regex: str
            A regex to filter results with

        Returns
        -------
        pd.DataFrame
            A dataframe containing transform metadata

        Examples
        --------
        >>> fs.get_transform_data_frame(['transform1', 'transform2'])
            id                                      name         description      transform_type   metadata
        ---------------------------------------------------------------------------------------------------
        0   0341bacc-e161-11ea-a042-0a53e92ebe18    transform1   Transform 1      simple           {}
        1   193177cc-e158-11ea-a042-0a53e92ebe18    transform2   Transform 2      dataframe        {}
        """

        params = {}
        if transform:
            if not isinstance(transform, list):
                transform = [transform]
            is_str = [isinstance(t, str) for t in transform]
            assert all(is_str), 'Transform names should be type, str.'
            params['name'] = ','.join(transform)
        if regex:
            assert isinstance(regex, str), 'Regex query should be type, str'
            params['query'] = regex

        url = self.endpoint + 'transform'
        response = requests.get(
            url, params=params, headers=self._api_headers())
        response.raise_for_status()

        result = response.json()

        df = pd.DataFrame({'id': [r['id'] for r in result],
                           'name': [r['name'] for r in result],
                           'description': [r['description'] for r in result],
                           'transform_type': [r['transform_type'] for r in result],
                           'metadata': [r['metadata'] for r in result]})

        return df

    def get_transform_id(self, transform):
        """Get the unique id number of transform(s).

        Parameters
        ----------
        transform : str or list[str]
            A transform or list of transforms.

        Returns
        -------
        str or list[str]
            Ids for the transform(s).

        Examples
        --------
        >>> fs.get_transform_id(['transform1', 'transform2'])
        ['0341bacc-e161-11ea-a042-0a53e92ebe18',
        '193177cc-e158-11ea-a042-0a53e92ebe18']
        """

        df = self.get_transform_data_frame(transform=transform)
        if isinstance(transform, str):
            assert transform in df.name.tolist(), f'The transform(s), {transform}, is non-existent.'
            return df[df.name == transform]['id'].iloc[0]
        else:
            assert len(transform) == len(
                df), 'One or more transforms are non-existent.'
            result = [
                df[df.name == t]['id'].iloc[0]
                for t in transform
            ]
            return result

    def get_transform_func(self, transform):
        """Get the function for transform.

        Parameters
        ----------
        transform : str
            A transform or list of transforms.

        Returns
        -------
        function or list[function]

        Examples
        --------
        >>> fs.get_transform_func(['transform1', 'transform2'])
            [<function>, <function>]
        """

        if isinstance(transform, list):
            return [self.get_transform_func(t) for t in transform]
        
        transform_id = self.get_transform_id(transform)

        url = self.endpoint + f'transform/{transform_id}'
        response = requests.get(
            url, headers=self._api_headers()
        )
        response.raise_for_status()
        result = response.json()

        if not result.get('code'):
            # No function return, so return identity function
            return lambda x: x
        return self._decode_function(result['code'])

    def create_transform(self, name, func, transform_type='simple', params={}, **kwargs):
        """Adds a transform to the feature store.

        Parameters
        ----------
        name : str
            Transform name.
        func : function
            A function or lambda, which defines the feature transformation.
        transform_type : str, optional
            Type of transform: either 'simple' or 'dataframe'.
        params : dict, optional
            A dictionary of {"name": default_value} pairs, which may be passed to the transform function.

        kwargs : dict, optional
            Data to be added to metadata.

        Examples
        --------
        >>> fs.create_transform('extract-x', lambda x: x['value'].get('x'))
        """

        assert isinstance(name, str), 'Transform names should be type, str.'
        assert bool(re.match(r'^[a-zA-Z0-9\./#_-]+$', name)), 'Transform name must only contain alphanumeric .#_-'
        assert not self.transform_exists(name), 'Transform already exists.'
        assert isinstance(func, types.FunctionType), 'A valid function must be provided'

        payload = {
            'name': name,
            'description': func.__doc__,
            'transform_type': transform_type,
            'params': params,
            'code': self._encode_function(func),
            'metadata': kwargs
        }
        url = self.endpoint + f'transform'
        response = requests.post(
            url, json=payload, headers=self._api_headers())
        response.raise_for_status()

        data = response.json()

    def delete_transform(self, name):
        """Deletes a transform from the feature store.

        Parameters
        ----------
        feature : str
            Transform name.

        Examples
        --------
        >>> fs.delete_transform('extract-x')
        """

        assert isinstance(name, str), 'Transform names should be type, str.'
        assert self.transform_exists(name), 'Transform does not exist.'

        transform_id = self.get_transform_id(name)
        url = self.endpoint + f'transform/{transform_id}'
        response = requests.delete(url, headers=self._api_headers())
        response.raise_for_status()

    def update_transform(self, name, func=None, transform_type=None, params=None, **kwargs):
        """Update a transform in the feature store.

        Parameters
        ----------
        feature : str
            Feature name.
        func : function, optional
            A function or lambda, which defines the feature transformation.
        transform_type : str, optional
            Type of transform: either 'simple' or 'dataframe'.
        params : dict, optional
            A dictionary of {"name": default_value} pairs, which may be passed to the transform function.

        kwargs : dict, optional
            Data to be added to metadata.

        Examples
        --------
        >>> fs.update_transform('extract-x', transform_type='dataframe')
        """

        assert isinstance(name, str), 'Transform names should be type, str.'
        assert self.transform_exists(name), 'Transform does not exist.'

        payload = {
            'name': name,
            'metadata': kwargs
        }
        if func:
            assert isinstance(func, types.FunctionType), 'A valid function must be provided'
            payload['code'] = self._encode_function(func)
            payload['description'] = func.__doc__
        if transform_type:
            assert transorm_type.lower() in ['simple', 'dataframe'], 'Transform type must be simple or dataframe'
            payload['transform_type'] = transform_type.lower()
        if params:
            assert isinstance(params, dict), 'Params must be a dictionary of name/value pairs'
            payload['params'] = params
        transform_id = self.get_transform_id(name)
        url = self.endpoint + f'transform/{transform_id}'
        response = requests.patch(
            url, json=payload, headers=self._api_headers())
        response.raise_for_status()

        data = response.json()

    def create_feature_group(self, name, **kwargs):
        """Adds a feature group to the feature store.

        Parameters
        ----------
        feature : str
            Feature group name.

        kwargs : dict, optional
            Data to be added to metadata.

        Examples
        --------
        >>> fs.create_feature('weather.actuals', source='NOAA GFS')
        """

        feature_ids = []

        payload = {
            'name': name,
            'feature_ids': feature_ids,
            'metadata': kwargs
        }
        url = self.endpoint + f'feature_group'
        response = requests.post(
            url, json=payload, headers=self._api_headers())
        response.raise_for_status()

        data = response.json()

    def split(target, past, future, include_time, horizon, initial, period,
              offset, max_train_size, cutoffs):
        """
        Generates train, validate, test splits for forecasting
        models. The splits can be based on historical cutoff points, which user
        can input. If not provided, begins from (end - horizon) and works
        backwards, making cutoffs with a spacing of period until initial is
        reached.

		Parameters
		----------
        target: dict
            Dict containing features and timeseries to include as target,
            e.g. {"feature1" : "timeseries1", "feature2" : "timeseries2"...}.
            The combined target will to be split into train, test, validation
            timeseries.

        past: dict
            Dict containing input features and timeseries, usually
            historic actuals, to include in train split,
            e.g. {"feature1" : "timeseries1", "feature2" : "timeseries2"...}.

        future: dict, optional
            Dict containing input features and timeseries, usually forecasts,
            to include in test and validation splits,
            e.g. {"feature1" : "timeseries1", "feature2" : "timeseries2"...}.

        include_time: bool, default True
            Boolean indicating whether to include "time", e.g. timeseries
            timestamps, in inputs.

		horizon: pd.Timedelta, optional
            string with pd.Timedelta compatible style, e.g., '5 days',
		    '3 hours', '10 seconds'. Lookahead period of intended forecasts.

        initial: pd.Timedelta, optional
            string with pd.Timedelta compatible style. The first training
    		period will include at least this much data. If not provided,
    		3 * horizon is used.

        period: pd.Timedelta, optional
            string with pd.Timedelta compatible style. Intend forecasts to be
            done every this period. If not provided, 0.5 * horizon is used.

        offset: pd.Timedelta, default "1{freq}"
            string with pd.Timedelta compatible style. Period betweeen end of
            train set and start of test set. If not provided, "1{freq}".

        max_train_size: pd.Timedelta, optional
            string with pd.Timedelta compatible style. Maximum size for a single
            training set. If not provided, train set grows for each generated
            timeseries without limit.


        cutoffs: list[pd.Timestamp], optional
            list of pd.Timestamp specifying train set end timestamps.
            If not provided, they are generated as described above.

		Yields
		-------
		train: np.array
            train set.
        validation: np.array
            validation set.
        test: np.array
            test set.

		"""
        pass
