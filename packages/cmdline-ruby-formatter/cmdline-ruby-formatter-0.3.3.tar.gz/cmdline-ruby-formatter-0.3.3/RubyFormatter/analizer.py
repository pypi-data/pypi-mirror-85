import os
import logging

logger = logging.getLogger('Formatter')


class Analizer:
    """
    Analizer

    define_item():
        analyzing dictionary from class CmdParser
        return list of key aspects for further analysis

    come_across_directory():
        go over all files in current directory

    come_across_project():
        go over all directories in current project

    run():
        go over all project by every file
        apply FileFormatter by every file

    """

    def __init__(self):
        pass

    @staticmethod
    def define_item(my_dict):
        my_list = []

        if my_dict['file'] is not None:
            my_list.append('file')
            my_list.append(my_dict['file'])

        if my_dict['directory'] is not None:
            my_list.append('directory')
            my_list.append(my_dict['directory'])

        if my_dict['project'] is not None:
            my_list.append('project')
            my_list.append(my_dict['project'])

        if my_dict['fixed'] is not None:
            my_list.append('fixed')
            my_list.append(my_dict['fixed'])

        my_list.append('verify')
        my_list.append(my_dict['verify'])

        logger.debug(f'{my_list}')
        return my_list

    @staticmethod
    def come_across_directory(my_list):
        folder = []
        list_of_files = []

        for i in os.walk(my_list[1]):
            folder.append(i)

        for i in folder[0][2]:
            list_of_files.append(my_list[1] + '/' + i)

        logger.debug(f'{list_of_files}')

        return list_of_files

    @staticmethod
    def come_across_project(list):
        folder = []
        for i in os.walk(list[1]):
            folder.append(i)

        list_of_directory = []

        for i in range(len(folder)):
            list_of_directory.append(folder[i][0])

        logger.debug(f'{list_of_directory}')
        return list_of_directory
