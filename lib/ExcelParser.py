# -*- coding: utf-8 -*-
import xlrd
import re

class ExcelParserCommon(object):

    excelFile = None
    __workbook = None

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

    @property
    def workbook(self):
        return self.__workbook

    def parse_excel(self, **kwargs):
        if 'excelFile' in kwargs.keys() and kwargs['excelFile'] is not None:
            self.__set_file(kwargs['excelFile'])

        if self.excelFile:
            self.__workbook = xlrd.open_workbook(self.excelFile, encoding_override='cp1251')

        if 'excelContent' in kwargs.keys() and kwargs['excelContent'] is not None:
            self.__workbook = xlrd.open_workbook(file_contents=kwargs['excelContent'], encoding_override='cp1251')

    def __set_file(self, file):
        self.__workbook = None
        self.excelFile = file

class DataParser(ExcelParserCommon):

    def parse_file(self, **kwargs):
        self.parse_excel(**kwargs)
        if self.workbook is not None:
            worksheet = self.workbook.sheet_by_index(0)

            result = []
            data = {}

            start_row = 1
            if 'start_row' in kwargs.keys():
                start_row = kwargs['start_row']

            number_col = None
            if 'number_col' in kwargs.keys():
                number_col = kwargs['number_col']

            price_col = None
            if 'price_col' in kwargs.keys():
                price_col = kwargs['price_col']

            # Получаем максимальные значения рядов и колонок
            max_rows = worksheet.nrows
            max_cols = worksheet.ncols

            # columns = self.get_columns(worksheet)
            replace_re = re.compile("[^0123456789\.\-]")
            replace_lz_re = re.compile("^0+")
            for row_number in range(start_row, max_rows):
                order = {}
                number = None
                clean_number = None
                clean_price = None
                for col_number in range(max_cols):
                    cell = worksheet.cell(row_number, col_number)
                    cell_value = cell.value
                    if number_col is not None and col_number == number_col and cell_value:
                        if isinstance(cell_value, float):
                            cell_value = "%d" % cell_value
                        number = cell_value
                        clean_number = str(replace_re.sub("", str(cell_value)))
                        clean_number = str(replace_lz_re.sub("", str(clean_number)))

                    if price_col is not None and col_number == price_col and isinstance(cell_value, float):
                        clean_price = int((float(cell_value) * 100) + 0.5) / 100

                if clean_number is not None and clean_price is not None:
                    # print(row_number, '!!', str(clean_number), clean_price)
                    data[clean_number] = {
                        'row': row_number,
                        'number': number,
                        'price': clean_price
                    }

        return data


class Comparator(object):

    source = {}
    compare = {}

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

    def compare_data(self, **kwargs):
        if 'source' in kwargs.keys() and isinstance(kwargs['source'], dict):
            self.source = kwargs['source']

        if 'compare' in kwargs.keys() and isinstance(kwargs['compare'], dict):
            self.compare = kwargs['compare']

        checked = []
        result = [];
        d_type = 'Наш'
        compare_keys = self.compare.keys()
        for key in self.source.keys():
            can_append = False
            result_string = '';
            if key in compare_keys:
                item = self.compare[key]
                if self.source[key]['price'] > item['price']:
                    can_append = True
                    result_string = 'Переплатили контрагенту'
                    result_string = result_string + ' (Н: ' + \
                                    str(self.source[key]['price']) + \
                                    ' И: ' + str(item['price']) + ')'
                elif self.source[key]['price'] < item['price']:
                    can_append = True
                    result_string = 'Недоплатили контрагенту'
                    result_string = result_string + ' (Н: ' + \
                                    str(self.source[key]['price']) + \
                                    ' И: ' + str(item['price']) + ')'
            else:
                can_append = True
                result_string = 'Отсутствует в файле от контрагента'

            if can_append:
                result.append([d_type, self.source[key]['row'], self.source[key]['number'], result_string])

            checked.append(key)

        d_type = 'Их'
        for key in compare_keys:
            result_string = ''
            if key not in checked:
                result_string = 'Отсутсвует в нашем файле'
                result.append([d_type, self.compare[key]['row'], self.compare[key]['number'], result_string])
                checked.append(key)

        return result