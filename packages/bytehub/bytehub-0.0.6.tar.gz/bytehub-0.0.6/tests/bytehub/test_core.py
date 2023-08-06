import pandas as pd
import bytehub as bh
import random
from uuid import UUID
import string


# To run tests without interactive login, set environment variables:
# BYTEHUB_CLIENT_ID and BYTEHUB_CLIENT_SECRET


def random_string(n):
    return ''.join(random.choice(string.ascii_lowercase) for x in range(n))


def is_valid_uuid(uuid_to_test, version=None):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


class TestByteHub():
    def setup_class(self):
        print('Connecting to Feature Store')
        self.fs = bh.FeatureStore(
            endpoint='https://api.dev.bytehub.ai/v1'
        )
        # Create test features
        num_test_features = 3
        self.features = [
            'pytest.' + random_string(8)
            for x in range(num_test_features)
        ]
        self.feature_ids = [
            self.fs.create_feature(
                feature, source='pytest', test_idx=idx)
            for idx, feature in enumerate(self.features)
        ]
        self.features_df = pd.DataFrame(
            {
                'name': self.features,
                'metadata': [
                    {'source': 'pytest', 'test_idx': idx}
                    for idx in range(num_test_features)
                ]
            }
        )
        # Add dummy data to test features
        dts = pd.date_range('2020-08-01', '2020-08-10', freq='3H')
        self.dataframes = [
            # Simple DataFrame of scalar values
            pd.DataFrame(
                {
                    'time': dts,
                    'value': [random.randint(0, 100) for x in dts]
                }
            ),
            # DataFrame with two entities
            pd.concat([
                pd.DataFrame(
                    {
                        'time': dts,
                        'value': [random.randint(0, 100) for x in dts],
                        'entity': ['entity-1'] * len(dts)
                    }
                ),
                pd.DataFrame(
                    {
                        'time': dts,
                        'value': [random.randint(0, 100) for x in dts],
                        'entity': ['entity-2'] * len(dts)
                    }
                ),
            ]),
        ]
        for f, df in zip(self.features[:2], self.dataframes):
            self.fs.save_timeseries(f, df)

    def teardown_class(self):
        print('Finished: tearing down...')
        # Delete test features
        for feature in self.fs.list_features(regex=r'pytest\..'):
            self.fs.delete_feature(feature)

    def test_list_features(self):
        fs = self.fs

        # List all of the features in the system
        feature_list = fs.list_features()
        for feature in self.features:
            assert feature in feature_list

        # Use regex search on features
        feature_list = fs.list_features(regex=r'pytest\..', metadata=False)
        assert sorted(feature_list) == sorted(self.features)

        # Retrieve metadata
        df = fs.list_features(regex=r'pytest\..', metadata=True)
        assert df.sort_values('name').equals(
            self.features_df.sort_values('name'))

    def test_feature_exists(self):
        fs = self.fs

        # Test that a single feature exists
        assert fs.feature_exists(self.features[0])
        # Test that a list of features exists
        assert all(fs.feature_exists(self.features))
        # Try with some non-existent features
        assert fs.feature_exists(
            [random_string(10), self.features[0], random_string(10)]
        ) == [False, True, False]

    def test_get_feature_id(self):
        fs = self.fs

        assert is_valid_uuid(fs.get_feature_id(self.features[0]), version=None)

        # Check non-existent features
        error = ''
        try:
            fs.get_feature_id('junk')
        except AssertionError as e:
            error = e.args[0]
        assert error == 'The feature(s), junk, is non-existent.'

        error = ''
        try:
            fs.get_feature_id(['junk1', 'junk2'])
        except AssertionError as e:
            error = e.args[0]
        assert error == 'One or more features are non-existent.'

    def test_create_feature(self):
        fs = self.fs

        # Try to create a feature that already exists
        error = ''
        try:
            fs.create_feature(self.features[0])
        except AssertionError as e:
            error = e.args[0]
        assert error == 'Feature already exists.'

        # Try a bad feature name
        error = ''
        try:
            fs.create_feature(1)
        except AssertionError as e:
            error = e.args[0]

        assert error == 'Feature names should be type, str.'

        # Create a new feature
        feature_name = 'pytest.' + random_string(8)
        fs.create_feature(feature_name, source='test')
        assert fs.feature_exists(feature_name)
        # Now delete this feature and check it has gone
        fs.delete_feature(feature_name)
        assert not fs.feature_exists(feature_name)

    def test_get_timeseries(self):
        fs = self.fs

        # Check returned timeseries for feature
        f = self.features[0]
        expected_df = self.dataframes[0]
        df = fs.get_timeseries(
            f, from_date=expected_df.time.iloc[0].isoformat(), to_date=expected_df.time.iloc[-1].isoformat(), freq='3H'
        )
        assert all(df.iloc[:, -1].values == expected_df.value.values)
        assert df.columns[-1] == f
        # Upsample
        df = fs.get_timeseries(
            f, from_date=expected_df.time.iloc[0].isoformat(), to_date=expected_df.time.iloc[-1].isoformat(), freq='1H'
        )
        assert all(
            df.iloc[:, -1].values == expected_df.set_index(
                'time').resample('1H').asfreq().ffill().value.values
        )
        # Downsample
        df = fs.get_timeseries(
            f, from_date=expected_df.time.iloc[0].isoformat(), to_date=expected_df.time.iloc[-1].isoformat(), freq='6H'
        )
        assert all(
            df.iloc[:, -1].values == expected_df.set_index(
                'time').resample('6H').asfreq().ffill().value.values
        )

        # Test timeseries filtered by entity
        f = self.features[1]
        expected_df = self.dataframes[1]
        df = fs.get_timeseries(
            f, entity='entity-1', from_date=expected_df.time.iloc[0].isoformat(), to_date=expected_df.time.iloc[-1].isoformat(), freq='3H'
        )
        assert all(
            df.iloc[:, -1].values == expected_df[expected_df.entity ==
                                                 'entity-1'].value.values
        )

        # Test multiple timeseries
        df = fs.get_timeseries(
            self.features[:2], from_date=expected_df.time.iloc[0].isoformat(), to_date=expected_df.time.iloc[-1].isoformat(), freq='3H'
        )
        print(df.head())
        df1 = df[[self.features[0]]].dropna()
        expected_df = self.dataframes[0]
        assert all(
            df1.iloc[:, -1].values == expected_df.value.values
        )
        df2 = df[df.entity == 'entity-2'][[self.features[1]]].dropna()
        expected_df = self.dataframes[1]
        assert all(
            df2.iloc[:, -1].values == expected_df[expected_df.entity ==
                                                  'entity-2'].value.values
        )

        # Test empty timeseries
        df = fs.get_timeseries(
            self.features[2], from_date=pd.Timestamp.utcnow(), to_date=pd.Timestamp.utcnow(), freq='3H'
        )
        assert df.columns[-1] == self.features[2]
        assert df.empty

    def test_save_feature(self):
        fs = self.fs

        # Create new feature
        feature_name = 'pytest.' + random_string(8)
        fs.create_feature(feature_name, source='test')
        # Save some test data
        dts = pd.date_range('2020-10-04', '2020-10-05', freq='1H')
        expected_df = pd.DataFrame(
            {
                'time': dts,
                'value': [random.randint(0, 100) for x in dts]
            }
        )
        fs.save_timeseries(feature_name, expected_df)
        # Read back and check
        df = fs.get_timeseries(
            feature_name, from_date=expected_df.time.iloc[0].isoformat(), to_date=expected_df.time.iloc[-1].isoformat(), freq='1H'
        )
        assert all(df.iloc[:, -1].values == expected_df.value.values)
        # Overwrite with new data
        expected_df = pd.DataFrame(
            {
                'time': dts,
                'value': [random.randint(0, 100) for x in dts]
            }
        )
        fs.save_timeseries(feature_name, expected_df)
        # Read back and check
        df = fs.get_timeseries(
            feature_name, from_date=expected_df.time.iloc[0].isoformat(), to_date=expected_df.time.iloc[-1].isoformat(), freq='1H'
        )
        assert all(df.iloc[:, -1].values == expected_df.value.values)

    def test_update_feature(self):
        fs = self.fs

        # Add some new metadata
        fs.update_feature(self.features[0], new_meta='test')
        df = fs.get_feature_data_frame(self.features[0])
        metadata = df.metadata.iloc[0]
        assert metadata.get('new_meta') == 'test'

        # Remove the metadata
        fs.update_feature(self.features[0], new_meta=None)
        df = fs.get_feature_data_frame(self.features[0])
        metadata = df.metadata.iloc[0]
        assert 'new_meta' not in metadata
