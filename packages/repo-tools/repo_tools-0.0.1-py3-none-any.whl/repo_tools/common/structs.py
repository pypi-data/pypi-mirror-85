import json
from dataclasses import dataclass

from enum import Enum


class OutputFormat(Enum):
    table = "table"
    json = "json"


@dataclass
class ProjectFeatures:
    git: bool = False
    circleci: bool = False
    helm: bool = False
    js: bool = False
    python: bool = False
    maven: bool = False
    docker: bool = False

    def get_list(self):
        features = self.__dict__.items()
        feature_names = [feature[0] if feature[1] else "" for feature in features]
        return feature_names

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


@dataclass
class ProjectInfo:
    name: str = ""
    abs_path: str = ""
    features: ProjectFeatures = ProjectFeatures()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
