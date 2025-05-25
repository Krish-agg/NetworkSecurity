from NetworkSecurity.components.data_ingestion import NetworkDataIngestion
from NetworkSecurity.entity.data_ingestion_config import DataIngestionConfig, TrainingPipelineConfig
from NetworkSecurity.entity.data_validation_entity import DataValidationConfig
from NetworkSecurity.entity.data_transformation_config import DataTransformationConfig

from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.components.data_validation import NetworkDataValidation
from NetworkSecurity.components.data_transformation import DataTransformation
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)

        dataingestionartifact=NetworkDataIngestion(data_ingestion_config).initialize_data_ingestion()
        logging.info("Network Data Ingestion Module Initialized")
        print(dataingestionartifact)
        data_validation_config=DataValidationConfig(training_pipeline_config)
        data_validation = NetworkDataValidation(data_validation_config, dataingestionartifact)
        logging.info("Network Data Validation Module Initialized")
        data_validation_artifact = data_validation.initiate_validate_data()
        print(data_validation_artifact)
        logging.info("Network Data Validation Completed")
        DataTransformationConfig= DataTransformationConfig(training_pipeline_config)
        logging.info("Network Data Transformation Module Initialized")
        data_transformation = DataTransformation(data_validation_artifact, DataTransformationConfig)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("Network Data Transformation Completed")
    except Exception as e:
        raise NetworkSecurityException(e, sys)    


