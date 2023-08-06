import logging


logger = logging.getLogger('Formatter')


class RubyFolderVerify:
    def __init__(self):
        self.type_of_file = '.rb'

    def check_name_of_folder(self, full_name_of_folder):
        name_of_folder = RubyFolderVerify._get_only_name_of_folder(full_name_of_folder)
        name_of_folder = self._check_snake_case_format(name_of_folder, isFile=False)

    def _check_snake_case_format(self, name_of_folder, isFile):
        logger.debug(f'verify {name_of_folder}')

        self.list_char_name = RubyFolderVerify._get_chars_from_str(name_of_folder)

        recommend_new_name = ''

        for i in range(len(self.list_char_name)):

            if self.list_char_name[i].isnumeric():
                recommend_new_name += self.list_char_name[i]

            elif self.list_char_name[i].isalpha():

                if self.list_char_name[i].isupper():
                    recommend_new_name += self._verify_big_letter(i)
                else:
                    recommend_new_name += self.list_char_name[i]

            elif self.list_char_name[i] == '_':
                recommend_new_name += self._verify_under_line(i)

        if isFile:
            name_of_folder += self.type_of_file
            recommend_new_name += self.type_of_file

        if recommend_new_name != name_of_folder:
            logger.debug(f'You should name {name_of_folder} to {recommend_new_name}')
        else:
            logger.debug(f'name {name_of_folder} is ok')


        return recommend_new_name

    def _verify_big_letter(self, index):
        recommend_new_name_of_folder = ''
        logger.debug(f'find upper letter --> {self.list_char_name[index]}')
        if index > 0:
            if self.list_char_name[index - 1] != '_':
                recommend_new_name_of_folder += '_'
            recommend_new_name_of_folder += self.list_char_name[index].lower()
            return recommend_new_name_of_folder
        else:
            return self.list_char_name[index].lower()

    def _verify_under_line(self, index):
        recommend_new_name_of_folder = ''
        if index <= len(self.list_char_name):

            if self.list_char_name[index + 1].isnumeric():
                logger.debug(f'find number after {self.list_char_name[index]}')
            else:
                recommend_new_name_of_folder += self.list_char_name[index]
        return recommend_new_name_of_folder

    @staticmethod
    def _get_only_name_of_folder(full_name_of_folder):
        list_chars = RubyFolderVerify._get_chars_from_str(full_name_of_folder)
        list_name_of_folder = []

        i = len(list_chars) - 1
        while list_chars[i] != '/':
            list_name_of_folder.append(list_chars[i])
            i -= 1

        list_name_of_folder.reverse()
        return RubyFolderVerify._get_str_from_chars(list_name_of_folder)

    @staticmethod
    def _get_only_name_of_file(full_name_of_folder):
        list_chars = RubyFolderVerify._get_chars_from_str(full_name_of_folder)
        list_name_of_folder = []

        j = 0
        i = len(list_chars) - 1
        while list_chars[i] != '.':
            i -= 1
            j += 1
        j += 1

        i = len(list_chars) - 1 - j
        while list_chars[i] != '/':
            # print(list_chars[i])
            list_name_of_folder.append(list_chars[i])
            i -= 1

        list_name_of_folder.reverse()
        return RubyFolderVerify._get_str_from_chars(list_name_of_folder)

    @staticmethod
    def _get_chars_from_str(str):
        return [char for char in str]

    @staticmethod
    def _get_str_from_chars(chars_list):
        str = ""

        for char in chars_list:
            str += char

        return str

    @staticmethod
    def _convert_list_to_string(org_list, seperator='\n'):
        return seperator.join(org_list)
