""" Application config template
"""
from os import environ
from typing import TypeVar, Union, Dict
from configparser import ConfigParser

ValidatorType = TypeVar("T")


def base_load_config(
    config_path: str,
    validator_cls: ValidatorType = None,
) -> Union[Dict, ValidatorType]:
    """Load and produce AppConfig, setting log level as well
    - Accept INI format only
    - Final value is ALWAYS UPPERCASE
    """
    config = {}
    stage = environ.get("STAGE", "DEVELOPMENT").upper()
    parser = ConfigParser()
    parser.read(config_path)

    for k, val in parser.items(stage):
        key = k.upper()
        value = val or environ.get(key)
        config.update({key: value})

    if validator_cls:
        config = validator_cls(**config)

    return config


def load_config_as_dict(config_path: str = "config.ini") -> Dict:
    """load config and return a dict"""
    return base_load_config(config_path)


def load_config_as_class(
    validator_cls: ValidatorType,
    config_path: str = "config.ini",
) -> ValidatorType:
    """load config and return a class instance,
    maybe Dataclass or a Pydantic Model
    """
    return base_load_config(config_path, validator_cls)
