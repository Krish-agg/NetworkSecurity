import yaml
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
import os
import sys
import numpy as np
import pandas as pd
import dill
import pickle


def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.
    
    :param file_path: Path to the YAML file.
    :return: Dictionary containing the YAML file content.
    """
    try:
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise NetworkSecurityException(f"Error reading YAML file {file_path}: {e}", sys)
    
def write_yaml_file(file_path: str, data: dict,replace:bool =False) -> None:
    try:
        if replace: 
            if os.path.exists(file_path):
                os.remove(file_path)
        with open(file_path, 'w') as file:
            yaml.dump(data, file)
    except Exception as e:
        raise NetworkSecurityException(f"Error writing YAML file {file_path}: {e}", sys)