from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse, resolve
from django.core.exceptions import FieldDoesNotExist

from django.views.generic.base import TemplateView
from django.views.generic import View

from .forms import FileUploadedForm

from lib.ExcelParser import DataParser, Comparator
from crispy_forms.layout import Div, HTML

from operator import itemgetter


class Main(TemplateView):

    allowed_to = ['manager_outer']
    raise_exception = True

    template_name = 'checker/home.html'

    form = FileUploadedForm

    def get_context_data(self, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = self.form()

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        form = self.form(request.POST, request.FILES)

        if form.is_valid():
            source_file = request.FILES.get('source_file')
            compare_file = request.FILES.get('compare_file')

            parser = DataParser()
            data = form.cleaned_data
            source_data = parser.parse_file(excelContent=source_file.read(),
                                            sheet_number=data['source_sheet_number']-1,
                                            start_row=data['source_start_row']-1,
                                            number_col=data['source_number_col']-1,
                                            price_col=data['source_price_col']-1)

            compare_data = parser.parse_file(excelContent=compare_file.read(),
                                             sheet_number=data['compare_sheet_number']-1,
                                             start_row=data['compare_start_row']-1,
                                             number_col=data['compare_number_col']-1,
                                             price_col=data['compare_price_col']-1)

            comparator = Comparator()

            result = comparator.compare_data(source=source_data,
                                             compare=compare_data)

            result = sorted(result, key=itemgetter(3,2))

            exit_data = []

            count = 1
            for item in result:
                item.insert(0, str(count))
                # l = tuple(item)
                exit_data.append(item)
                count += 1

            context['exit_data'] = exit_data

        context['form'] = form
        return render(request, self.template_name, context)



