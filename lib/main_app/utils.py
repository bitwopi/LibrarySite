import datetime
import os

import docx

from lib.settings import BASE_DIR
from .models import Rent


def get_month_report():
    rents = Rent.objects.all()
    text = ""
    income = 0
    current_month = datetime.datetime.now().month

    for rent in rents:
        if rent.actual_end_date and int(rent.actual_end_date.__str__().split('-')[1]) == current_month:
            text += "%s дата начала: %s, дата конца: %s, " \
                    "итоговая цена аренды: %s рублей \n\n" % (rent.instance_id,
                                                              rent.start_date,
                                                              rent.actual_end_date,
                                                              rent.get_full_rent_cost())
            income += rent.get_full_rent_cost()
    text += "\nВыручка за месяц: %s рублей" % income
    doc = docx.Document()
    doc.add_paragraph(text)
    doc.save(f'media/reports/{datetime.datetime.now().date()}-report.docx')
    return f'media/reports/{datetime.datetime.now().date()}-report.docx'
