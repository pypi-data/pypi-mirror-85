from django.urls import reverse
from operator import attrgetter

import datetime
import xlsxwriter

def get_params_for_search(request, Obj, ObjForm, search_fields, result_fields, \
        relational_obj_values={}, translations={}):
    print('trk = ', translations)
    if not search_fields:
        search_fields = [field.name for field in Obj._meta.fields]
    fields = []
    charfield_exists = False
    datetimefield_exists = False
    booleanfield_exists = False
    for field in search_fields:
        remaining = {}
        remaining['label'] = field
        if field in translations:
            remaining['label'] = translations[field]
        internal_type = Obj._meta.get_field(field).get_internal_type()
        if internal_type in ('IntegerField', 'FloatField', 'DecimalField'):
            fields.append((field, 'number', 'ltgt', remaining))
            charfield_exists = True
        elif internal_type in ('CharField', 'TextField'):
            fields.append((field, 'text', 'text', remaining))
            charfield_exists = True
        elif internal_type in ('DateField', 'DateTimeField'):
            fields.append((field, 'date', 'ltgt', remaining))
            datetimefield_exists = True
        elif internal_type == 'ForeignKey':
            values = []
            if field in relational_obj_values:
                remaining['relational_obj_values'] = relational_obj_values[field]
            fields.append((field, 'relation', 'relation', remaining))
        elif internal_type == 'BooleanField':
            fields.append((field, 'boolean', 'text', remaining))
            booleanfield_exists = True
    print(fields)
    class_name = Obj._meta.object_name
    class_name_lower = class_name.lower()
    ajax_url = reverse('ajax_get_%s_list' % class_name.lower())
    return (fields, class_name, class_name_lower, ajax_url, charfield_exists, \
            datetimefield_exists, booleanfield_exists)


def generate_xlsx(object_list, REPORT, filename=False):
    data = []
    for obj in object_list:
        data_inline = []
#        if not report_name:
#            report_name = obj.__class__.__name__
        class_name = obj.__class__.__name__
        if 'parameters' in REPORT:
            for attr in REPORT['parameters']:
                _value = attrgetter(attr)(obj)
                if _value == None:
                    _value = ''
                data_inline.append(_value)
            data.append(data_inline)
    print(data)

    if not filename:
        now = datetime.datetime.now()
        filename = '/tmp/generate_xlsx_%s_%s.xlsx' % (class_name, now.strftime('%Y_%m_%d__%H_%M_%S'))

    wb = xlsxwriter.Workbook(filename)
    ws = wb.add_worksheet()

    row = 0
    col = 0
    try:
        _header = REPORT['header']
    except:
        _header = REPORT['parameters']
    for attr in _header:
        ws.write(row, col, str(attr)[:1].upper() + str(attr)[1:])
        col = col + 1

    row = 1
    for line in data:
        col = 0
        for item in line:
            ws.write(row, col, str(item))
            col = col + 1
        row = row + 1
    wb.close()

    return filename


def apply_translations(form, translations=False):
    if translations:
        for field in form.fields:
            sfield = form.fields[field]
            if field in translations:
                sfield.label = translations[field]
        return form
    return form