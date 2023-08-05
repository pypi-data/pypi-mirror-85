from typing import Union, List

import time
from tqdm import tqdm

from pyrasgo.connection import Connection
from pyrasgo.enums import ModelType
from pyrasgo.feature import Feature, FeatureList
from pyrasgo.member import Member
from pyrasgo.monitoring import track_usage
from pyrasgo.namespace import Namespace


class Model(Connection):
    """
    Stores all the features for a model
    """

    def __init__(self, api_object, **kwargs):
        self._namespace = Namespace(**api_object)
        super().__init__(**kwargs)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Model(id={self.id}, name={self.name})"

    def __getattr__(self, item):
        try:
            return self._namespace.__getattribute__(item)
        except KeyError:
            raise AttributeError(f"No attribute named {item}")

    @property
    @track_usage
    def type(self):
        """
        Returns the model type of the model
        """
        return ModelType(self._namespace.type)

    @property
    @track_usage
    def features(self):
        """
        Returns the features within the model
        """
        return FeatureList([feature.dict() for feature in self._namespace.features])

    @features.setter
    def features(self, features: Union[List[Feature], FeatureList, Feature]):
        # Update the namespace
        self._namespace.__setattr__('features',
                                    [Namespace(**feature.dict()) for feature in self.features + features])

    def get(self):
        """
        Updates the Model object's attributes from the API
        """
        self._namespace = Namespace(**self._get(f"/models/{self.id}").json())

    def get_author(self):
        """
        Returns the full author object of the model (including credentials)
        """
        return Member(self.author.to_dict())

    @track_usage
    def add_feature(self, feature: Feature) -> None:
        """
        Adds a single feature to the model
        """
        self.features = feature
        self._patch(f"/models/{self.id}/features", api_version=1,
                    _json={"featureIds": [str(feature.id)]})

    @track_usage
    def add_features(self, features: Union[List[Feature], FeatureList]) -> None:
        """
        Adds a FeatureList or a list of Features to the model.
        """
        self.features = features
        self._patch(f"/models/{self.id}/features", api_version=1,
                    _json={"featureIds": [str(feature.id) for feature in features]})

    @track_usage
    def is_data_ready(self) -> bool:
        """
        Performs check against API for training data readiness, if true, a dataframe can be pulled down.
        :return:
        """
        r = self._get("/trainings/latest")
        if any([model['state'] == 'done' for model in r.json() if model['model']['id'] == self.id]):
            return True
        if any([model['state'] == 'error' for model in r.json() if model['model']['id'] == self.id]):
            raise SystemError("There's been an issue with the training data generation")
        return False

    @track_usage
    def generate_training_data(self) -> None:
        """
        Triggers the generation of the model's training data.
        """
        self._post(f"/trainings/", _json={"modelId": int(self.id),
                                          "userId": self._profile['id']},
                   api_version=0)
        for _ in tqdm(range(0, 10)):
            if self.is_data_ready():
                break
            time.sleep(1)

    def snowflake_table_metadata(self, creds):
        metadata = {
            "database": creds.get("database", "rasgoalpha"),
            "schema": creds.get("schema", "public"),
            "table": self._snowflake_table_name(),
        }
        return metadata

    def _snowflake_table_name(self):
        table_name = self.dataTableName
        if table_name is None:
            raise ValueError("No table found for model '{}'".format(self.id))
        return table_name
