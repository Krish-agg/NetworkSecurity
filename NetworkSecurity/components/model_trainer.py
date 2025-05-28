import os
import sys

from NetworkSecurity.exception.exception import NetworkSecurityException 
from NetworkSecurity.logging.logger import logging

from NetworkSecurity.entity.artifact import DataTransformationArtifact,ModelTrainerArtifact
from NetworkSecurity.entity.model_train_config import ModelTrainerConfig

import mlflow

from NetworkSecurity.utils.ml_utils.model.estimator import NetworkModel
from NetworkSecurity.utils.main_utils.utils import save_object,load_object
from NetworkSecurity.utils.main_utils.utils import load_numpy_array_data, evaluate_models
from NetworkSecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)   

    def track_mlflow(self,best_model,classificationmetric):
        try:
            with mlflow.start_run():
                f1_score=classificationmetric.f1_score
                precision_score=classificationmetric.precision_score
                recall_score=classificationmetric.recall_score

                mlflow.log_metric("f1_score",f1_score)
                mlflow.log_metric("precision",precision_score)
                mlflow.log_metric("recall_score",recall_score)
                mlflow.sklearn.log_model(best_model, "model")
        except Exception as e:
            raise NetworkSecurityException(e,sys)     
        
    def train_model(self,Xtrain,ytrain,Xtest,ytest)->ModelTrainerArtifact:
        try:
            models={
                "LogisticRegression": LogisticRegression(verbose=1),
                "KNeighborsClassifier": KNeighborsClassifier(),
                "DecisionTreeClassifier": DecisionTreeClassifier(),
                "RandomForestClassifier": RandomForestClassifier(verbose=1),
                "GradientBoostingClassifier": GradientBoostingClassifier(verbose=1),
                "AdaBoostClassifier": AdaBoostClassifier()
            }
            params={
                "DecisionTreeClassifier": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "RandomForestClassifier":{
                    # 'criterion':['gini', 'entropy', 'log_loss'],
                    
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,128,256]
                },
                "GradientBoostingClassifier":{
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "LogisticRegression":{},
                "AdaBoostClassifier":{
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "KNeighborsClassifier":{
                    'n_neighbors': [3, 5, 7, 9, 11],
                    'weights': ['uniform', 'distance'],
                    #'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']
                }
            
            }
            model_report,report_param = evaluate_models(X_train=Xtrain, y_train=ytrain, X_test=Xtest, y_test=ytest,
                                       models=models, param=params)
            logging.info(f"Model Report: {model_report}")
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]
            logging.info(f"Best Model Name: {best_model_name} with score: {best_model_score}")
            best_model.set_params(**report_param[best_model_name])
            best_model.fit(Xtrain, ytrain)
            y_train_pred = best_model.predict(Xtrain)
            classification_train_metric = get_classification_score(y_true=ytrain, y_pred=y_train_pred)
            logging.info(f"Classification Train Metric: {classification_train_metric}") 

            self.track_mlflow(best_model, classification_train_metric)
            logging.info(f"Tracking MLflow for model: {best_model_name}")
            y_test_pred = best_model.predict(Xtest)
            classification_test_metric = get_classification_score(y_true=ytest, y_pred=y_test_pred)
            logging.info(f"Classification Test Metric: {classification_test_metric}")
            self.track_mlflow(best_model, classification_test_metric)

            preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)
            Network_Model= NetworkModel(preprocessor=preprocessor, model=best_model)

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,train_metric_artifact=classification_train_metric,test_metric_artifact=classification_test_metric)
            logging.info(f"Model Artifact created.")
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=Network_Model)
            save_object("final_model/model.pkl",best_model)
            logging.info(f"Model saved at: {self.model_trainer_config.trained_model_file_path}")
            return model_trainer_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
        
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            logging.info("Entered initiate_model_trainer method of ModelTrainer class")
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path
            transformed_object_file_path=self.data_transformation_artifact.transformed_object_file_path
            
            logging.info(f"train file path: {train_file_path}")
            logging.info(f"test file path: {test_file_path}")   

            train_arr= load_numpy_array_data(file_path=train_file_path)
            test_arr= load_numpy_array_data(file_path=test_file_path)

            x_train,y_train, x_test,y_test = train_arr[:,:-1],train_arr[:,-1],test_arr[:,:-1],test_arr[:,-1]
            logging.info(f"x_train shape: {x_train.shape}, y_train shape: {y_train.shape}")

            model=self.train_model(x_train,y_train,x_test,y_test)





        except Exception as e:
            raise NetworkSecurityException(e,sys)        