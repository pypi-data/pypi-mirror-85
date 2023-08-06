import os


class CheckConditions(object):

    @staticmethod
    def is_path_exist(path):
        """

        Args:
            path(string): File system path to be checked if it is exist or not

        Returns:
            (bool): True if the path is exist and False otherwise
        """
        is_dir = os.path.isdir(path)  # True or False
        if is_dir:
            # print('path of the file : ', os.path.exists(path))
            return is_dir  # True or False
        else:
            # print('path: ', path)
            # print('This path does not exist, We will created for you ....')
            return False

