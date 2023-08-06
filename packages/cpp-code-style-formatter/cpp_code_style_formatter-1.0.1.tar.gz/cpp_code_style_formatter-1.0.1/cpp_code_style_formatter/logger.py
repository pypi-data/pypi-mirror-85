from .WorkingMode import *


class Logger:
    def __init__(self, fix_log_file_name, verify_log_file_name):
        self.fix_log_file = open(fix_log_file_name, 'a', encoding='utf-8')
        self.verify_log_file = open(verify_log_file_name, 'a', encoding='utf-8')

    def __del__(self):
        self.fix_log_file.close()
        self.verify_log_file.close()

    def log(self, file_path, line_num, modification_description, error_code, error_message, mode):
        if mode == WorkingMode.VerifyMode:
            self.log_style_error(file_path, line_num, error_code, error_message)
        else:
            self.log_style_fix(file_path, line_num, modification_description)

    def log_style_fix(self, file_path, line_num, modification_description):
        message = "{}: {} - {}\n".format(file_path, line_num, modification_description)
        self.fix_log_file.write(message)

    def log_style_error(self, file_path, line_num, error_code, error_message):
        message = "{}: {} - {}: {}\n".format(file_path, line_num, error_code.name, error_message)
        self.verify_log_file.write(message)
