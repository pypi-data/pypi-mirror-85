# use command: pip install -e .
# to install and test it locally before you publish it
import json
import os
import traceback
from zipfile import ZipFile

import pandas as pd
from distutils.dir_util import remove_tree
from predictnow import cert
from pandas import DataFrame, read_parquet

from .notifier import MLTrainingCompletedNotifier
from .find_files_with_specific_extensions import find_files_with_specific_extensions
from uuid import uuid4
from typing import Dict
import requests

# TODO: change the host url to Apigee
# host_api = should call proxy API gee //authentication/authorization
# host = "http://127.0.0.1:8080"
import firebase_admin
from firebase_admin import credentials

from .predict_result import PredictResult
from .training_result import TrainingResult


class PredictNowClient:
    def __init__(self, url, api_key):
        self.api_key = api_key
        self.host = url
        cred = credentials.Certificate(cert)
        if len(firebase_admin._apps) == 0:  # check if firebase is already init
            firebase_admin.initialize_app(cred)

    def create_model(self, username, model_name, params, hyp_dict={}):
        request_params = {
                "params": params,
                "hyp_dict": hyp_dict,
                "model_name": model_name,
                "username": username,  # TODO replace with self.username
            }

        url = self.host + "/models"

        response = requests.post(
            url,
            json=request_params,
        )

        return json.loads(response.content.decode('utf-8'))

    def train(self,
              input_df: DataFrame,
              model_name: str,
              label: str,
              username: str,  # TODO remove
              email: str,  # TODO remove
              return_output: bool = True,
              ):
        try:
            params = {
                'model_name': model_name,
                'train_id': str(uuid4()),
                'username': username,
                'email': email,
                'label': label,
            }

            files = {
                'parquet': self.__df_to_parquet_file__(input_df),
            }

            notifier = MLTrainingCompletedNotifier(
                params['username'], params['train_id'])

            url = self.host + "/trainings"

            response = requests.post(
                url,
                files=files,
                data=params,
                timeout=300,
            )  # prevents TaskCancelled error

            if not return_output:
                return json.loads(response.content.decode('utf-8'))
            notifier.wait_for_result()

            extract_path = os.path.join(os.getcwd(), "temp")
            os.makedirs(extract_path, exist_ok=True)
            self.download_files(
                username=username,
                model_name=model_name,
                output_path=extract_path,
            )

            return self.deserialize(
                path=extract_path,
                username=username,
                model_name=model_name,
            )
        except Exception as e:
            the_error_type = type(e).__name__
            the_traceback = traceback.format_exc()
            print(the_traceback)
            return {
                "success": False,
                "message": the_error_type + ": " + str(e),
            }

    def predict(self,
                input_df: DataFrame,
                model_name: str,
                username: str,  # TODO remove
                eda: str = "no",
                ) -> PredictResult:
        params = {
            'model_name': model_name,
            'username': username,
            'eda': eda,
        }
        files = {
            'parquet':  self.__df_to_parquet_file__(input_df),
        }

        url = self.host + "/predictions"
        response = requests.post(
            url,
            data=params,
            files=files,
        )
        response = json.loads(response.content.decode('utf-8'))
        return PredictResult(
            title=response["title"],
            filename=response["filename"],
            objective=response["objective"],
            eda=response["eda"],
            too_many_nulls_list=response["too_many_nulls_list"],
            suffix=response["suffix"],
            labels=response["labels"],
            probabilities=response["probabilities"],
        )

    # TODO Confirm to Radu, what's the difference between save_to_output, download_all_files(path), and DownloadFiles(model_name, path)
    # Save results output for the model named model_name to the local directory specified by output_path
    # The following are downloaded (the .pkl file for the model itself remains on the server):
    #  - performance metrics file
    #  - feature selection chart
    #  - Feature selection importance score csv file
    #  - In-sample and out-of-sample predictions


    def get_subscription_details(self,
                username: str,  # TODO remove
                ) -> PredictResult:

        url = self.host + "/get_subscription_details/" + username
        response = requests.get(
            url,
        )
        response = json.loads(response.content.decode('utf-8'))
        return response

    def get_account_status(self,
                username: str,  # TODO remove
                ) -> PredictResult:

        url = self.host + "/get_account_status/" + username
        response = requests.get(
            url,
        )
        response = json.loads(response.content.decode('utf-8'))
        return response

    def download_files(self,
                       username: str,
                       output_path: str = None,
                       model_name: str = "",
                       do_not_extract: bool = False,
                       ):
        output_path = output_path if output_path else os.getcwd()
        url = self.host + "/download_files"

        params = {
            'username': username,
            'model_name': model_name
        }
        response = requests.post(
            url,
            data=params,
        )
        response = response.content

        zip_path = os.path.join(output_path, params["username"] + ".zip")
        file = open(zip_path, "wb")
        file.write(response)
        file.close()

        message = "The result " + params["username"] + ".zip has been saved into " + output_path
        if not do_not_extract:
            message += " and extracted with the parquet files converted to CSV"
            with ZipFile(zip_path, 'r') as zipObj:
                zipObj.extractall(output_path)

            parquet_paths = find_files_with_specific_extensions(os.path.join(output_path, "userprofile_api"), "parquet")
            for parquet_path in parquet_paths:
                df = read_parquet(parquet_path)
                csv_path = parquet_path[:-8] + ".csv"
                df.to_csv(csv_path)

        return {
            "success": True,
            "message": message,
        }

    def delete_files(self,
                       username: str,
                       model_name: str = "",
                       delete_all: bool = False,
                       ):
        url = self.host + "/delete_files"

        params = {
            'username': username,
            'model_name': model_name,
            'delete_all': delete_all,
        }
        response = requests.post(
            url,
            data=params,
        )
        response = json.loads(response.content.decode('utf-8'))
        return response

    # # TODO confirm to radu, I think we can merge DeleteAllData and Delete Data.
    # # Just give flag to the params, saying 'all:true'
    # # DeleteAllData: Deletes all input and output files from the current account on the server.
    # # DeleteData(model_name): Deletes input and output files associated with the specified model
    # def delete_data(self, params: Dict[str, str] ):
    #     ...
    #     raise Exception("method is not implemented yet.")
    #
    # # Sends reset password request link to the current account email.
    # def reset_password(self):
    #     ...
    #     raise Exception("method is not implemented yet.")
    #
    # # Sends reset password request link to the current account email.
    # def reset_password(self):
    #     ...
    #     raise Exception("method is not implemented yet.")
    #
    # # Return: dictionary whose keys and values are strings. Keys represent method names, and values
    # # represent description of the corresponding method
    # # use dir(self)???
    # def get_all_methods(self):
    #     ...
    #     raise Exception("method is not implemented yet.")
    def __df_to_parquet_file__(self, input_df: DataFrame):
        df_name = self.__pick_name_from_df__(input_df)
        os.makedirs("temp", exist_ok=True)
        parquet_path = os.path.join("temp", df_name + ".parquet")
        input_df.to_parquet(parquet_path)
        return open(parquet_path, 'rb')  # TODO dont store the files, do it in mem?

    def __pick_name_from_df__(self, input_df: DataFrame):
        if hasattr(input_df, "name") and input_df.name:
            return input_df.name
        print("DF HAS NO NAME, USING A UUID. Assign a name to it e.g df.name = 'myfirstname'")
        if hasattr(input_df, "filename") and input_df.filename:
            return input_df.filename
        return str(uuid4())

    def deserialize(self, path, username, model_name, delete_afterwards=True):
        root_path = path
        zip_path = os.path.join(path, username + ".zip")
        with ZipFile(zip_path, 'r') as zipObj:
            zipObj.extractall(path)

        path = os.path.join(path, "userprofile_api", username, model_name)
        latest_model_date = os.listdir(path)[-1]
        path = os.path.join(path, latest_model_date)
        latest_train_date = [i for i in os.listdir(path) if os.path.isdir(os.path.join(path, i))]
        latest_train_date = latest_train_date[-1]
        path = os.path.join(path, latest_train_date)

        with open(os.path.join(path, "performance_metrics_" + model_name + ".txt")) as f:
            performance_metrics = f.readlines()
            performance_metrics = [i.replace("\n", "") for i in performance_metrics]

        with open(os.path.join(path, "personal_" + model_name + ".json")) as f:
            training_parameters = f.read()
            training_parameters = json.loads(training_parameters)

        csv_files = {
            "dataframe_train_diff_": dict(),
            "dataframe_train_undiff_": dict(),
            "feat_test_": dict(),
            "feat_train_": dict(),
            "feature_importance_": dict(),
            "lab_test_": dict(),
            "lab_train_": dict(),
            "predicted_prob_cv_": dict(),
            "predicted_prob_test_": dict(),
            "predicted_targets_cv_": dict(),
            "predicted_targets_test_": dict(),
        }

        for file_name_prefix in csv_files:
            parquet_path = os.path.join(path, file_name_prefix + model_name + ".parquet")
            dataframe = pd.read_parquet(parquet_path) if os.path.exists(parquet_path) else None
            csv_files[file_name_prefix] = dataframe

        if delete_afterwards:
            os.remove(zip_path)
            remove_tree(os.path.join(root_path, "userprofile_api"))

        return TrainingResult(
            success=True,
            feature_importance=csv_files["feature_importance_"],
            feat_train=csv_files["feat_train_"],
            feat_test= csv_files["feat_test_"],
            lab_test= csv_files["lab_test_"],
            lab_train= csv_files["lab_train_"],
            performance_metrics= performance_metrics,
            dataframe_train_diff=csv_files["dataframe_train_diff_"],
            dataframe_train_undiff=csv_files["dataframe_train_undiff_"],
            training_parameters= training_parameters,
            predicted_prob_cv= csv_files["predicted_prob_cv_"],
            predicted_prob_test= csv_files["predicted_prob_test_"],
            predicted_targets_cv= csv_files["predicted_targets_cv_"],
            predicted_targets_test= csv_files["predicted_targets_test_"],
        )
