import io
import logging
import re

import pandas as pd
import xlsxwriter
from django.http import HttpResponse
from django.utils.http import urlquote


ua_exp = re.compile(r"(?:\b(MS)?IE\s+|\bTrident\/7\.0;.*\s+rv:)(\d+)")




def render_style_xlsx(workbook, request):
    style_head = workbook.add_format()
    style_head.set_font_name("黑体")
    style_head.set_font_size(10)
    style_head.set_font_color("#ffffff")
    style_head.set_pattern(1)
    bg_color = request.domain.config["theme"]
    style_head.set_bg_color("#00aeef")
    style_head.set_border(1)
    style_head.set_border_color("#808080")
    style_head.set_align("center".encode("utf8"))

    style_content_str = workbook.add_format()
    style_content_str.set_font_name("黑体")
    style_content_str.set_font_size(10)
    style_content_str.set_border(1)
    style_content_str.set_border_color("#808080")
    style_content_str.set_align("left".encode("utf8"))

    style_content_num = workbook.add_format()
    style_content_num.set_font_name("黑体")
    style_content_num.set_font_size(10)
    style_content_num.set_border(1)
    style_content_num.set_border_color("#808080")
    style_content_num.set_align("right".encode("utf8"))

    return style_content_str, style_content_num, style_head



def makeResponse(fd, filename):
    response = HttpResponse(fd)
    attachment = f"attachment; filename={urlquote(filename)}"
    response["Content-Disposition"] = attachment
    response[
        "Content-type"
    ] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return response

def write_sheet(worksheet, sheet, styles, method=None):
    header = sheet["header"]
    matric = sheet["matric"]
    for col, data in enumerate(header.translate()):
        worksheet.write(0, col, data, styles["header"])

    worksheet.set_column(0, len(header.all), 20)

    if matric.empty:
        return
    for col, index in enumerate(header.all):
        style = styles["str"]
        for row, data in enumerate(matric[index], 1):
            if index not in header.datas:
                data = str(data)
            worksheet.write(row, col, data, style)


def PythonXlsx(request, filename: str, sheets: list):
    with io.BytesIO() as fd:
        workbook = xlsxwriter.Workbook(fd)
        styles = dict(
            zip(["str", "num", "header"], render_style_xlsx(workbook, request))
        )
        for sheet in sheets:
            worksheet = workbook.add_worksheet(sheet["name"][:31])
            write_sheet(worksheet, sheet, styles)
        workbook.close()
        fd.seek(0)
        return makeResponse(fd, filename)



def exceler(request, filename, sheets, method=None):
    """
    filename: 文件名
    sheets:  [{"name": sheet_name, header: 表头的keys, cn: 表头的文案显示, matric: 表格对应的dataframe}]
    """
    return PythonXlsx(request, filename, sheets)
