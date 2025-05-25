import os
import sys

"""Defining common constants for training pipeline data ingestion module."""

TARGAT_COLUMN="Result"
PIPELINE_NAME = "NetworkSecurityML"
ARTIFACT_DIR =  "Artifacts"
FILE_NAME = "phishingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

SCHEMA_FILE_PATH= os.path.join("data_schema","schema.yaml")


"""Data Ingestion Configuration for Network Security Project.
This module defines the configuration for data ingestion, including the paths for raw data"""

DATA_INGESTION_COLLECTION_NAME = "phishingData"
DATA_INGESTION_DATABASE_NAME = "NetworkSecurityML"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2


""" Data Validation Configuration for Network Security Project."""

DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_VALID_DIR="validated"
DATA_VALIDATION_INVALID_DIR="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME = "report.yaml"