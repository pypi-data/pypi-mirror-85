import os
import datetime
import pandas as pd
import pickle
from .checks import CheckConditions


class Utils(object):
    """
    # Create the utilities methods to be used in the pipeline
    """

    @staticmethod
    def generate_file_name(prefix):
        """
        The generator method to produce a unique name includes date and time
        Args:
            prefix(string): the prefix for the file name concatenated with data and time
        Returns:
            (string):the generated file name with timestamp
        """

        return prefix + '_' + str(datetime.datetime.now().date()) + '_' + str(
            datetime.datetime.now().time()).replace(':', '-').replace('.', '-')

    @staticmethod
    def save_pipeline( file_name):
        """
        Save the model object in the file system
        Args:
            model_name(string): the model object's name that produced from the clustering
            file_name(string): the model file's name to be renamed in the file system

        Returns:
            pickle_path(string): the model full path 
        """
        model_path = os.path.abspath(os.path.join(os.path.dirname('__file__'), '..',file_name ))

        if not (CheckConditions().is_path_exist(model_path)):
            # print('model_path: ', model_path)
            os.mkdir(model_path)
            # print(model_path, ' is created successfully\n')
        return model_path


    @staticmethod
    def load_pipeline(full_file_name):
        """
        Load the pre-trained model to be predicted
        Args:
            full_file_name(string): full path for the file name

        Returns:
            model(binary object): model pickle serialized file

        """
        try:
            # if the model file is exist
            with open(full_file_name, 'rb') as handle:
                model = pickle.load(handle)
            return Utils().with_success(model)

        except Exception as err:
            return Utils().with_error(2, 'The pickle file does not exist !!', err)

    @staticmethod
    def read_csv_file(full_file_name):
        """
        read csv file as a data frame
        Args:
            full_file_name(string): full file name with the path

        Returns:
            df(data frame): data frame after reading the csv file
        """
        try:
            df = pd.read_csv(full_file_name, index_col=None, encoding='utf-8')
            # print('Data in csv format has been loaded successfully !!\n')
            return Utils().with_success(df)
        except Exception as err:
            return Utils().with_error(1, 'The input file does not exist', err)

    @staticmethod
    def write_csv_file(df):
        """
        Save the data frame to csv file
        Args:
            df(data frame): data frame to be write with the after scoring

        Returns:
            prediction_full_file_name(file): full path for the results
        """
        output_file_name = '\\' + Utils().generate_file_name('results') + '.csv'

        output_path = os.path.abspath(os.path.join(os.path.dirname('__file__'), '..', 'results'))
        if not (CheckConditions().is_path_exist(output_path)):
            os.mkdir(output_path)
            # print(output_path, ' is created successfully')

        prediction_full_file_name = output_path + output_file_name

        df.to_csv(prediction_full_file_name, index=False, header=True)

        return prediction_full_file_name

    @staticmethod
    def with_success(data):
        return {'isSuccess': True, 'data': data}

    @staticmethod
    def with_error(error_code: int, error_message: str = None, exception: Exception = None):
        return {
            'isSuccess': False, 'error': {'code': error_code, 'message': error_message, 'exception': exception}
        }
