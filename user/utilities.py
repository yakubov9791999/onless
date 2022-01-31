from io import BytesIO
from typing import Dict, List

import openpyxl as xl
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.styles import numbers


def parse_excel_pupil(file: BytesIO) -> List[Dict]:
    workbook = xl.load_workbook(file, read_only=True, data_only=True)
    worksheet = workbook.active
    datas = []
    first = True

    for row in worksheet.values:
        if first:
            first = False
            continue

        if len(row) < 4 or None in row[0:4]:
            break  # break on bad formatted row

        data = dict(zip(["name", "pasport", "phone"], row[1:4]))
        datas.append(data)
    return datas
