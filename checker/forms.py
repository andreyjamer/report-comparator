import django.forms as forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Div, HTML, Hidden

# from common import widgets

# from shops.models import Shop

class FileUploadedForm(forms.Form):
    source_file = forms.FileField(label='Загрузите файл сверки', required=True)
    source_sheet_number = forms.IntegerField(label='Лист книги',
                                          required=True,
                                          min_value=1)

    source_start_row = forms.IntegerField(label='Ряд начала данных',
                                          required=True,
                                          min_value=1)
    source_number_col = forms.IntegerField(label='Колонка номеров накладных',
                                           required=True,
                                           min_value=1)
    source_price_col = forms.IntegerField(label='Колонка сумм',
                                          required=True,
                                          min_value=1)

    compare_file = forms.FileField(label='Загрузите файл контрагентов',
                                   required=True)
    compare_sheet_number = forms.IntegerField(label='Лист книги',
                                              required=True,
                                              min_value=1)

    compare_start_row = forms.IntegerField(label='Ряд начала данных',
                                           required=True,
                                           min_value=1)
    compare_number_col = forms.IntegerField(label='Колонка номеров накладных',
                                            required=True,
                                            min_value=1)
    compare_price_col = forms.IntegerField(label='Колонка сумм',
                                           required=True,
                                           min_value=1)


    def __init__(self, *args, **kwargs):
        super(FileUploadedForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.form_action = 'home'

        self.helper.layout = Layout(
            Div(
                Div(
                    Field('source_file'),
                    Field('source_sheet_number'),
                    Field('source_start_row'),
                    Field('source_number_col'),
                    Field('source_price_col'),
                    css_class="col-xs-6"
                ),


                Div(
                    Field('compare_file'),
                    Field('compare_sheet_number'),
                    Field('compare_start_row'),
                    Field('compare_number_col'),
                    Field('compare_price_col'),
                    css_class="col-xs-6"
                ),
                css_class="row"
            ),
        )

        self.helper.add_input(Submit('submit', 'Обработать файлы'))