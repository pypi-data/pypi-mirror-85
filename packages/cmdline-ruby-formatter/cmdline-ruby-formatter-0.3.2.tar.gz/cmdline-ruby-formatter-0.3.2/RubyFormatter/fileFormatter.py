import os
import logging

from RubyFormatter.analizer import Analizer
from RubyFormatter.rubyCodeParser import RubyCodeParser
from RubyFormatter.rubyFolderVerify import RubyFolderVerify

logger = logging.getLogger('Formatter')


class FileFormatter:
    def __init__(self, my_dict):
        self.dict = my_dict
        self.need_to_fix = False

    @staticmethod
    def is_file_type_supported(file, needed_type=".rb"):
        file_name, type_name = os.path.splitext(file)

        if type_name == needed_type:
            logger.debug(f'{file} is suitable')
            return True
        else:
            logger.debug(f'{file} is NOT suitable')
            return False

    @staticmethod
    def create_formatted_file(file, formatted_str):
        file_name, type_name = os.path.splitext(file)
        # formatted_file = file_name + '_formatted' + type_name
        formatted_file = file_name + type_name

        text_file = open(formatted_file, "wt")
        text_file.write(formatted_str)
        text_file.close()

        logger.debug(f'created formatted file: {formatted_file}')

    def formatting(self, file_name):
        logger.debug(f'formatter works with {file_name}')

        if FileFormatter.is_file_type_supported(file_name):
            logger.debug(f'formatter is checking {file_name}')

            code_parser = RubyCodeParser(file_name)
            code_parser.check_name_of_file(file_name)

            formatted_str = code_parser.parser()

            if self.need_to_fix:
                FileFormatter.create_formatted_file(file_name, formatted_str)

        logger.debug(f'formatter finished work with {file_name} and went to the next')

    def run(self):
        my_list = Analizer.define_item(self.dict)

        if my_list[3] == 'True':
            self.need_to_fix = True

        if my_list[0] == 'project':
            list_of_directories = Analizer.come_across_project(my_list)

            for i in range(len(list_of_directories)):
                list_pro = ['', list_of_directories[i]]
                RubyFolderVerify().check_name_of_folder(list_of_directories[i])
                for file in Analizer.come_across_directory(list_pro):
                    self.formatting(file)

        if my_list[0] == 'directory':
            RubyFolderVerify().check_name_of_folder(my_list[1])

            for file in Analizer.come_across_directory(my_list):
                self.formatting(file)

        elif my_list[0] == 'file':
            self.formatting(my_list[1])
