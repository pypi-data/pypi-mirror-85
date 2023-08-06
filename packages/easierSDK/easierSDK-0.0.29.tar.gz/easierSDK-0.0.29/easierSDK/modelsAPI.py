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
import urllib3
import os
import subprocess
import tensorflow as tf
import joblib
from shutil import rmtree
import json
import tensorflow.keras.backend as K

from easierSDK.classes.categories import Categories
from easierSDK.classes.model_metadata import ModelMetadata
from easierSDK.classes.model import Model
import easierSDK.classes.constants as constants


class ModelsAPI():
    """Class to control the Models API of EasierSDK.
    """

    _GLOBAL = 'global'
    _MODELS = 'models'
    _DATASETS = 'datasets'
    _BASE_MODELS_PATH = './models'
    _MAX_FOLDER_SIZE = 2000 # Kbytes = 2M
    _MAX_FOLDER_SIZE_STR = '2MB'

    def __init__(self, minio_client, minio_bucket_public, minio_bucket_private):
        """Constructor for the ModelsAPI.

        Args:
            minio_client (Minio): Minio client object with user session initialized.
            minio_bucket_public (str): Name of the public bucket of the user.
            minio_bucket_private (str): Name of the private bucket of the user.
        """
        if not os.path.isdir(self._BASE_MODELS_PATH): os.mkdir(self._BASE_MODELS_PATH)
        self.minio_client = minio_client
        self.minio_bucket_public = minio_bucket_public
        self.minio_bucket_private = minio_bucket_private

    def _count_model_experiments(self, repo_name:str, category:str, model_name:str) -> int:
        """Count number of experiments in Minio of a model.

        Args:
            repo_name (str): Name of the Minio repository.
            category (str): Category of the model.
            model_name (str): Model name in repository.

        Returns:
            int: number of experiments of the model.
        """
        num_experiments = 0
        already_counted = []
        for item in self.minio_client.list_buckets(repo_name, prefix=self._MODELS + '/' + category.value + '/' + model_name, recursive=True):
            experimentID = item.object_name.split('/')[3]
            if experimentID in already_counted:
                continue
            num_experiments += 1
            already_counted.append(experimentID)
        return num_experiments

    def _print_models(self, repo_name:str, category:Categories=None):
        """List models are under a specific repository and under a specific category.

        Args:
            repo_name (str): Name of the repository.
            category (Categories, optional): Category of the models to list. Defaults to None to show the models under every category.
        """
        if category:
            objects = self.minio_client.list_objects(repo_name, prefix=self._MODELS + '/' + category.value, recursive=True)
        else:
            objects = [] 
            for category in Categories:
                objects += self.minio_client.list_objects(repo_name, prefix=self._MODELS + '/' + category.value, recursive=True)
        
        already_printed = []
        row_format ="{:<30}" * 5
        printed = False
        for item in objects:
            repo_name = item.bucket_name
            model = item.object_name.split('/')[2]
            cat = item.object_name.split('/')[1]
            num_experiments = self._count_model_experiments(repo_name, cat, model)
            if [model, cat] in already_printed:
                continue
            already_printed.append([model, cat])
            size = item.size            
            print(row_format.format(*[repo_name, cat, model, size, str(num_experiments)]))
            printed = True
        
        if not printed and category is None:
            print(row_format.format(*[repo_name, 'None', 'None', '0']))

        if printed: print("\n")

    def show_models(self, repo_name:str=None, category:Categories=None):
        """Show which models are under a specific repository and under a specific model Category.

        Args:
            repo_name (str, optional): Name of the repository to list models. Defaults to None to show all available repositories.
            category (Categories, optional): Category of the model. Defaults to None to show all models under each Category.
        """
        row_format ="{:<30}" * 5
        print(row_format.format(*['Repository', 'Category', 'Name', 'Size', '# Experiments']))
        if repo_name is None:
            for repo in self.minio_client.list_buckets():
                self._print_models(repo.name, category)
        else:
            self._print_models(repo_name, category)
        

    def show_model_info(self, repo_name:str, category:Categories, model_name:str, experimentID:int=-1) -> ModelMetadata:
        """Show metadata information of a specific model and/or a specific experimentID.

        Args:
            repo_name (str): Name of the repository that contains the model.
            category (Categories): Category that contains the model.
            model_name (str): Name of the model.
            experimentID (int, optional): ExperimentID of the model to which information is going to be shown. Defaults to -1 to show contextual model information without references to any experimentID.

        Returns:
            ModelMetadata: object with the model information.
        """
        if not self.minio_client.bucket_exists(repo_name):
            print('ERROR: Repository name does not exist. Please check and try again')
            return None
        if experimentID == -1:
            # Show model metadata instead of experiment metadata
            # experimentID = self._count_model_experiments(repo_name, category.value, model_name) - 1        
            filename = self._MODELS + '/' + category.value + '/' + model_name + '/' + 'metadata.json'
        else:
            filename = self._MODELS + '/' + category.value + '/' + model_name + '/' + str(experimentID) + '/' + 'metadata.json'
        local_path = './models/' + filename
        try:
            minio_obj = self.minio_client.fget_object(repo_name, filename, local_path)
        except minio.error.NoSuchKey as ex:
            print('ERROR: Wrong model information, please check and try again.')
            return None
        
        with open(local_path, 'r') as f:
            metadata = ModelMetadata(json.load(f), minio_obj)
            metadata.pretty_print()

        return metadata

    def download(self, repo_name:str, category:Categories, model_name:str, path_to_download:str, experimentID:int=-1) -> str:
        """Downloads a model and its attached objets in a specific path.

        Args:
            repo_name (str): Name of the repository that contains the model.
            category (Categories): Category that contains the model.
            model_name (str): Name of the model.
            path_to_download (str): Local path in which to store all files.
            experimentID (int, optional): ExperimentID of the model to download. Defaults to -1 to download the last experiment.

        Returns:
            str: path under path_to_download folder where files were stored
        """
        if not self.minio_client.bucket_exists(repo_name):
            print('ERROR: Repository name does not exist. Please check and try again')
            return None
        if experimentID == -1:
            # Download last experiment
            experimentID = self._count_model_experiments(repo_name, category.value, model_name) - 1
        # TODO check if models will be saved in HDF5 .h5 or tf SavedModel format (folder)
        minio_path = self._MODELS + '/' + category.value + '/' + model_name + '/' + str(experimentID)
        local_path = path_to_download + "/" + minio_path
        try:
            objects = self.minio_client.list_objects(repo_name, prefix=minio_path, recursive=True)
            for minio_object in objects:
                minio_obj = self.minio_client.fget_object(repo_name, minio_object.object_name, path_to_download + "/" + minio_object.object_name)
        except minio.error.NoSuchKey as ex:
            print('ERROR: Wrong model name or category, please check and try again.')
            return None
        return local_path

    def _load_file(self, path:str, print_files=False, model:Model=None) -> Model:
        """Loads files from a path onto an EASIER model variable depending on the file's extension.

        Args:
            path (str): path of the file
            print_files (bool, optional): Whether or not to print which files are being loaded. Defaults to False.
            model (Model, optional): EASIER Model variable to to load the files. Defaults to None to create a new model.

        Returns:
            Model: EASIER model variable with file loaded
        """
        if model is None: model = Model()
        for obj in os.listdir(path):
            extension = obj.split(".")[-1]
            # TODO check if models will be saved in HDF5 .h5 or tf SavedModel format (folder)
            if extension == constants.MODEL_EXTENSION:
                model.set_tf_model(tf.keras.models.load_model(path + '/' + obj))
                if print_files: print("Loaded model. File stored in: " + path + '/' + obj)
            elif extension == constants.PICKLE_EXTENSION:
                extension_pkl = obj.split(".")[-2:]
                extension_pkl = '.'.join(extension_pkl)
                if extension == constants.SCALER_EXTENSION:
                    model.set_scaler(joblib.load(path + '/' + obj))
                    if print_files: print("Loaded scaler. File stored in: " + path + '/' + obj)
                elif extension == constants.LABELENCODER_EXTENSION:
                    model.set_label_encoder(joblib.load(path + '/' + obj))
                    if print_files: print("Loaded label encoder. File stored in: " + path + '/' + obj)
                elif extension == constants.ONEHOTENCODER_EXTENSION:
                    model.set_feature_encoder(joblib.load(path + '/' + obj))
                    if print_files: print("Loaded one hot encoder. File stored in: " + path + '/' + obj)
            elif extension == constants.JSON_EXTENSION:
                with open(path + '/' + obj, 'r') as f:
                    metadata = ModelMetadata(f=json.load(f))
                    model.set_metadata(metadata)
                if print_files: print("Loaded model's metadata. File stored in: " + path + '/' + obj)
            elif extension == constants.TF_LITE_EXTENSION: 
                extension_tflite = obj.split("_")[-1]    
                if '_' + extension_tflite == constants.TPU_EXTENSION:
                    model.set_tpu_model_path(path + '/' + obj)
                    if print_files: print("Downloaded tpu model version. File stored in: " + path + '/' + obj)
                else:
                    model.set_tf_lite_model_path(path + '/' + obj)
                    if print_files: print("Downloaded tf lite model version. File stored in: " + path + '/' + obj)
            else:
                if print_files: print("Couldn't load file with extension: ." + str(extension))

        return model

    def load_from_local(self, path:str, print_files=False) -> Model:
        """Loads a model into program from a local path.

        Args:
            path (str): Local path where model files are stored.
            print_files (bool, optional): Whether to print which files are loaded. Defaults to False.

        Returns:
            Model: object with the loaded model and its attached elements like scalers.
        """
        model = self._load_file(path, print_files)
                
        return model

    def load_from_repository(self, repo_name:str, category:Categories, model_name:str, experimentID:int=-1, print_files=False) -> Model:
        """Loads a model into program from a repository.

        Args:
            repo_name (str): Name of the repository that contains the model.
            category (Categories): Category that contains the model.
            model_name (str): Name of the model.
            experimentID (int, optional): ExperimentID of the model to download. Defaults to -1 to load the last experiment.
            print_files (bool, optional): Whether to print which files are loaded. Defaults to False.

        Returns:
            Model:  object with the loaded model and its attached elements like scalers.
        """
        if not os.path.isdir('/tmp/download'): os.mkdir('/tmp/download')

        if experimentID == -1:
            # Load last experiment
            experimentID = self._count_model_experiments(repo_name, category.value, model_name) - 1
        
        path = self.download(repo_name, category, model_name, path_to_download='/tmp/download', experimentID=experimentID)
        if print_files: print("Files are stored in: " + path)
        
        model = self._load_file(path, print_files)
        
        return model

    def upload(self, category:Categories, model:Model, public=False, remove_dir=True) -> bool:
        """Upload a model and its attached elements to the user's repository.

        Args:
            category (Categories): Category that contains the model.
            model (Model): Object with the model and its attached elements.
            public (bool, optional): Whether to upload the model in the public version of the repository. Defaults to False.
            remove_dir (bool, optional): Whether to remove the folder in which the files to be uploaded were created. Defaults to True.

        Returns:
            bool: True if successful upload. False otherwise.
        """
        path = model.store(print_files=False)
        minio_path = self._MODELS + '/' + category.value + '/' + model.metadata.name
        # TODO revise experiment_id
        try:
            for obj in os.listdir(path):
                if public:
                    bucket = self.minio_bucket_public
                else:
                    bucket = self.minio_bucket_private
                
                # Create bucket if doesn't exist
                if not self.minio_client.bucket_exists(bucket): self.minio_client.make_bucket(bucket, location='es')

                # Check last experiment
                last_experimentID = self._count_model_experiments(bucket, category.value, model.metadata.name)
                # TODO check if models will be saved in HDF5 .h5 or tf SavedModel format (folder)
                self.minio_client.fput_object(bucket, minio_path + '/' + str(last_experimentID) + '/' + obj, path + '/' + obj)
            if remove_dir: rmtree(path)
        except Exception as ex:
            print("ERROR: Error uploading model to MINIO: " + str(ex))
            return False
        return True

    def compile_tflite(self, model:Model, calibration_data: list, path:str=_BASE_MODELS_PATH + "/storage/"):
        """Compiles a Tensorflow model to its Lite version.

        Args:
            model (Model): Model object with the Tensorflow model to be compiled.
            calibration_data (list): List with some example data that the model was trained with.
            path (str, optional): Path to store the tflite file. Defaults to "./models/storage/".
        """
        # TODO check model type (h5 vs SavedModel)
        # TODO check usage of path
        if not os.path.isdir(path): os.mkdir(path)
        if not os.path.isdir("/tmp/storage/"): os.mkdir("/tmp/storage/")
        model.set_representative_data(samples = calibration_data)

        if model.tf_model is None and model.tf_model_dir != '':
            converter = tf.lite.TFLiteConverter.from_saved_model(model.tf_model_dir)
        elif model.tf_model is not None:
            if tf.__version__.split(".")[0] == '1':
                model.tf_model.save("/tmp/storage/" + model.metadata.name + "." + constants.MODEL_EXTENSION)
                # Clear graph in prep for next step.
                try:
                    K.clear_session()
                except Exception as e:
                    pass                
                converter = tf.lite.TFLiteConverter.from_keras_model_file("/tmp/storage/" + model.metadata.name + "." + constants.MODEL_EXTENSION)
            else:    
                converter = tf.lite.TFLiteConverter.from_keras_model(model.tf_model)

        converter.representative_dataset = model.representative_dataset_gen
        converter.optimizations = [tf.lite.Optimize.DEFAULT]

        try:
            tflite_model = converter.convert()
        except Exception as e:
            print("Error converting model to tf lite: " + str(e))
            return

        if model.tf_model_dir != '':
            tf_lite_model_path = path + model.tf_model_dir + "/" + model.metadata.name + "." + constants.TF_LITE_EXTENSION
            open(tf_lite_model_path, "wb").write(tflite_model)
            print("Converted tf model " + str(model.tf_model_dir) + " to tf lite")
        else:
            tf_lite_model_path = path + model.metadata.name + "." + constants.TF_LITE_EXTENSION
            open(tf_lite_model_path, "wb").write(tflite_model)
            # Clear graph in prep for next step.
            try:
                K.clear_session()
            except Exception as e:
                pass
            print("Converted keras model " + model.metadata.name + " to tf lite")

        model.set_tf_lite_model_path(tf_lite_model_path)

    def compile_tpu(self,  model:Model, calibration_data, path:str=_BASE_MODELS_PATH + "/storage/"):
        """Compiles a Tensorflow model to its TPU version.

        Args:
            model (Model): Model object with the Tensorflow model to be compiled.
            calibration_data (list): List with some example data that the model was trained with.
            path (str, optional): Path to store the tflite.edge_tpu file. Defaults to "./models/storage/".
        """
        # TODO check model type (h5 vs SavedModel)
        # TODO check usage of path

        if not os.path.isdir(path): os.mkdir(path)
        if not os.path.isdir("/tmp/storage/"): os.mkdir("/tmp/storage/")
        model.set_representative_data(samples = calibration_data)

        if model.tf_model_dir != '':
            converter = tf.lite.TFLiteConverter.from_saved_model(model.tf_model_dir)
        else:
            if tf.__version__.split(".")[0] == '1':
                if not os.path.isfile("/tmp/storage/" + model.metadata.name + "." + constants.MODEL_EXTENSION):
                    model.tf_model.save("/tmp/storage/" + model.metadata.name + "." + constants.MODEL_EXTENSION)
                try:
                    K.clear_session()
                except Exception as e:
                    pass
                converter = tf.lite.TFLiteConverter.from_keras_model_file("/tmp/storage/" + model.metadata.name + "." + constants.MODEL_EXTENSION)
            else:    
                converter = tf.lite.TFLiteConverter.from_keras_model(model.tf_model)

        if tf.__version__.split(".")[0] == '1':
            converter.target_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]        
        else:
            converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.representative_dataset = model.representative_dataset_gen
        converter.inference_input_type = tf.uint8
        converter.inference_output_type = tf.uint8
        converter.optimizations = [tf.lite.Optimize.DEFAULT]

        try:
            tflite_model = converter.convert()
        except Exception as e:
            print("Error converting model to tf lite: " + str(e))
            return

        if model.tf_model_dir is not None:
            open('/tmp/storage/' + model.tf_model_dir + "/" + model.metadata.name + "." + constants.TF_LITE_EXTENSION, "wb").write(
                tflite_model)
            try:
                K.clear_session()
            except Exception as e:
                pass
            print("Converted tf model " + str(model.tf_model_dir) + " to tf lite specific for TPU")
            tpu_model_path = "/tmp/storage/" + model.tf_model_dir + "/" + model.metadata.name + "." + constants.TF_LITE_EXTENSION
            cmd = ['edgetpu_compiler', tpu_model_path, '-o', '/tmp/storage']
            tpu_model_path = "/tmp/storage/" + model.tf_model_dir + "/" + model.metadata.name + "_edgetpu." + constants.TF_LITE_EXTENSION
        else:
            try:
                open('/tmp/storage/' + model.metadata.name + "." + constants.TF_LITE_EXTENSION, "wb").write(
                    tflite_model)
                try:
                    K.clear_session()
                except Exception as e:
                    pass
                print("Converted keras model " + model.metadata.name + " to tf lite specific for TPU")
            except Exception as e:
                print("Error saving tf lite model to file: " + str(e))
                try:
                    K.clear_session()
                except Exception as e:
                    pass
                return
            tpu_model_path = "/tmp/storage/" +  model.metadata.name + "." + constants.TF_LITE_EXTENSION
            cmd = ['edgetpu_compiler', '-o', '/tmp/storage', tpu_model_path]
            tpu_model_path = "/tmp/storage/" +  model.metadata.name + "_edgetpu." + constants.TF_LITE_EXTENSION
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE)
            model.set_tpu_model_path(tpu_model_path)
        except FileNotFoundError as e:
            print('The edge tpu complier is not installed: ' + str(e))
            return
        except Exception as e:
            print('The edge tpu complier throwed an error: ' + str(e))
            return

    # TODO check if necessary
    def _compile_gpu(self):
        pass      
    
    def _dockerize(self, model:Model, image_name:str=None):
        raise NotImplementedError()
    
        if not os.path.isdir("/dockerized_model"): os.mkdir("/dockerized_model")

        model.store(model_path="/dockerized_model", print_files=False)
        if image_name is None: image_name = model.metadata.name + '_' + model._get_random_string()
        cmd = ['docker', 'build', '-f', 'Dockerfile_model', '-t', image_name]
        subprocess.run(cmd, stdout=subprocess.PIPE)

        cmd = ['docker', 'save', image_name, '--output', image_name + '.tar']
        subprocess.run(cmd, stdout=subprocess.PIPE)