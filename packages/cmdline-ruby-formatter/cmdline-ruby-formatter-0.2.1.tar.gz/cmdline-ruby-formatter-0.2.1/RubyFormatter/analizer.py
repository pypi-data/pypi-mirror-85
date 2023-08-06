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
    def define_item(dict):
        list = []

        if dict['file'] is not None:
            list.append('file')
            list.append(dict['file'])

        if dict['directory'] is not None:
            list.append('directory')
            list.append(dict['directory'])

        if dict['project'] is not None:
            list.append('project')
            list.append(dict['project'])

        if dict['fixed'] is not None:
            list.append('fixed')
            list.append(dict['fixed'])

        list.append('verify')
        list.append(dict['verify'])

        logger.debug(f'{list}')
        return list

    @staticmethod
    def come_across_directory(list):
        folder = []
        list_of_files = []

        for i in os.walk(list[1]):
            folder.append(i)

        for i in folder[0][2]:
            list_of_files.append(list[1] + '/' + i)

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
