import csv


class PostReader:
    '''Класс для работы с CSV'''
    def __init__(self, chrome=False, web_driver=None) -> None:
        self.path = './2021-12-11.csv'

    def create_reader(self):
        with open(self.path) as csvfile:
            for row in csv.reader(csvfile):
                if row[1] == 'date':
                    continue
                yield row


# reader_manager = PostReader()
# reader = reader_manager.create_reader()
#
# for row in reader:
#     print(row)
