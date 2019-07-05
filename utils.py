import csv_nickname_parser
import os

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
root_dir = scriptDirectory.rsplit(os.sep, 1).pop(0)


class Names:
    def __init__(self):
        self.name_dict = csv_nickname_parser.NameDenormalizer(root_dir + r'/names.csv')
