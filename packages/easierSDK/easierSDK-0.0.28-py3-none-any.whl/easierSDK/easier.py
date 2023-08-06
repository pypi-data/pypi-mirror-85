#   Copyright  2020 Atos Spain SA. All rights reserved.
 
#   This file is part of EASIER AI.
 
#   EASIER AI is free software: you can redistribute it and/or modify it under the terms of Apache License, either version 2 of the License, or
#   (at your option) any later version.
 
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT ANY WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT,
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#   WHETHER IN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
#   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#   See  LICENSE file for full license information  in the project root.

import minio
from minio import Minio
import os

import easierSDK.modelsAPI, easierSDK.datasetsAPI
from easierSDK.classes.categories import Categories

class EasierSDK():
    """Higher level class to interact with the EASIER platform.
    """

    _MODELS = 'models'
    _DATASETS = 'datasets'
    
    def __init__(self, minio_url: str, minio_user:str, minio_password:str):
        """Initializer for the class.

        Args:
            minio_url (str): URL to an EASIER MINIO deployment.
            minio_user (str): Username.
            minio_password (str): Password.
        """
        self.minio_bucket = minio_user
        self.minio_client = Minio(minio_url, access_key=minio_user, secret_key=minio_password, secure=True, region='es')
        self.minio_bucket_public = minio_user + '-public'
        self.minio_bucket_private = minio_user + '-private' 

        self.models = modelsAPI.ModelsAPI(self.minio_client, self.minio_bucket_public, self.minio_bucket_private)
        self.datasets = datasetsAPI.DatasetsAPI(self.minio_client, self.minio_bucket_public, self.minio_bucket_private)

    def _count_repo_models(self, repo_name:str) -> (int, list):
        """Count number of models under a repository.

        Args:
            repo_name (str): Repository to count models from.

        Returns:
            int: Number of models under the repository.
            list: List of models in the repository.
        """
        num_models = 0
        models_list = []
        for category in Categories:
            for obs in self.minio_client.list_objects(repo_name, prefix=self._MODELS + '/' + category.value, recursive=True):
                experiment_model = obs.object_name.split('/')[0:3]
                experiment_model = repo_name + '/' + '/'.join(experiment_model)
                if experiment_model not in models_list:
                    num_models += 1
                    models_list.append(experiment_model)
        return num_models, models_list
    
    def _count_repo_datasets(self, repo_name:str) -> (int, list):
        """Count number of datasets under a repository.

        Args:
            repo_name (str): Repository to count datasets from.

        Returns:
            int: Number of datasets under the repository.
            list: List of datasets in the repository.
        """
        num_datasets = 0
        datasets_list = []
        for category in Categories:
            for obs in self.minio_client.list_objects(repo_name, prefix=self._DATASETS + '/' + category.value, recursive=True):
                experiment_dataset = obs.object_name.split('/')[0:3]
                experiment_dataset = repo_name + '/' + '/'.join(experiment_dataset)
                if experiment_dataset not in datasets_list:
                    num_datasets += 1
                    datasets_list.append(experiment_dataset)
        return num_datasets, datasets_list

    def show_available_repos(self, deep:bool=False) -> (list, list):
        """Show which repositories are available for the user to interact with.

        Args:
            deep (bool, optional): Whether or not to print more information of the content of each repository. Defaults to False.

        Returns:
            list: List of models in the repository.
            list: List of datasets in the repository.
        """
        repo_list = self.minio_client.list_buckets()
        global_models_list = []
        global_datasets_list = []
        row_format ="{:<30}" * 3
        print(row_format.format(*['Repo Name', '# Models', '# Datasets']))
        for repo in repo_list:
            num_models, models_list = self._count_repo_models(repo.name)
            num_datasets, datasets_list = self._count_repo_datasets(repo.name)
            global_models_list += models_list
            global_datasets_list += datasets_list
            print(row_format.format(*['- ' + repo.name, num_models, num_datasets]))
            if deep:
                for model in models_list:
                    print(row_format.format(*['', '- ' + model.split('/')[-1], '']))
                
                for dataset in datasets_list:
                    print(row_format.format(*['', '', '- ' + dataset.split('/')[-1]]))
        return global_models_list, global_datasets_list

    def _count_category_models(self, category:Categories) -> (int, list):
        """Count all available models under a specific category.

        Args:
            category (Categories): Category to which count the models from.

        Returns:
            int: number of models under the category
            list: list of models under the category
        """
        num_models = 0
        models_list = []
        repo_list = self.minio_client.list_buckets()
        for repo in repo_list:
            for obs in self.minio_client.list_objects(repo.name, prefix=self._MODELS + '/' + category.value, recursive=True):
                experiment_model = obs.object_name.split('/')[0:3]
                experiment_model = repo.name + '/' + '/'.join(experiment_model)            
                if experiment_model not in models_list:
                    num_models += 1
                    models_list.append(experiment_model)
        return num_models, models_list
    
    def _count_category_datasets(self, category:Categories) -> (int, list):
        """Count all available datasets under a specific category.

        Args:
            category (Categories): Category to which count the datasets from.

        Returns:
            int: number of datasets under the category
            list: list of datasets under the category
        """
        num_datasets = 0
        datasets_list = []
        repo_list = self.minio_client.list_buckets()
        for repo in repo_list:
            for obs in self.minio_client.list_objects(repo.name, prefix=self._DATASETS + '/' + category.value, recursive=True):
                experiment_dataset = obs.object_name.split('/')[0:3]
                experiment_dataset = repo.name + '/' + '/'.join(experiment_dataset)
                if experiment_dataset not in datasets_list:
                    num_datasets += 1
                    datasets_list.append(experiment_dataset)
        return num_datasets, datasets_list

    def show_categories(self, deep:bool=False) -> (list, list):
        """Show information of which categories are available to the user.

        Args:
            deep (bool): Whether or not to show more complete information of each category.

        Returns:
            list: list of models available
            list: list of datasets available
        """
        global_models_list = []
        global_datasets_list = []
        row_format ="{:<30}" * 3
        print(row_format.format(*['Category', '# Models', '# Datasets']))
        for category in Categories:
            num_models, models_list = self._count_category_models(category)
            num_datasets, datasets_list = self._count_category_datasets(category)
            global_models_list += models_list
            global_datasets_list += datasets_list
            print(row_format.format(*['- ' + category.value, num_models, num_datasets]))
            if deep:
                for model in models_list:
                    print(row_format.format(*['', '- ' + model.split('/')[-1], '']))
                
                for dataset in datasets_list:
                    print(row_format.format(*['', '', '- ' + dataset.split('/')[-1]]))
        return global_models_list, global_datasets_list