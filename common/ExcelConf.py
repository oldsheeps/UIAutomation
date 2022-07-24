from openpyxl.styles import PatternFill, Font

PASS_VALUE = 'Pass'  # 单元格文本-Pass
FAILED_VALUE = 'Failed'  # 单元格文本-Failed
HYPERLINK_VALUE = 'Picture'  # 超链接文本-Screenshot
CELL_STYLE_RED = 'FF0000'  # 单元格样式-红色填充
CELL_STYLE_GREEN = 'AACF91'  # 单元格样式-绿色填充
CELL_STYLE_FONT = 'solid'  # 单元格样式-字体加粗


def _cell_style(cell, row, column, fgColor):
    """
    单元格样式处理
    :param cell: 单元格
    :param row:  行
    :param column: 列
    :param fgColor: 前景颜色（AACF91：绿色、FF0000：红色）
    :return: 作用到工作簿
    """
    cell(row=row, column=column).fill = PatternFill(patternType=CELL_STYLE_FONT, fgColor=fgColor)
    cell(row=row, column=column).font = Font(bold=True)


# Pass样式配置
def pass_(cell, row, column):
    cell(row=row, column=column).value = PASS_VALUE
    _cell_style(cell, row, column, CELL_STYLE_GREEN)


# Failed样式配置
def failed_(cell, row, column):
    cell(row=row, column=column).value = FAILED_VALUE
    _cell_style(cell, row, column, CELL_STYLE_RED)


# 自定义回填value样式配置
def value_(cell, row, column, value, fgColor=CELL_STYLE_GREEN):
    cell(row=row, column=column).value = value
    _cell_style(cell, row, column, fgColor)


def hyperlink_(cell, row, column, path, link_name=HYPERLINK_VALUE, fgColor=CELL_STYLE_GREEN):
    """
    超链接样式配置 ADD8E6,87CECB,B0E0E6,AFEEEE
    :param cell: 单元格
    :param row: 行
    :param column: 列
    :param path: 作用工作簿的路径
    :param fgColor: 前景颜色（AACF91：绿色、FF0000：红色）
    :return: 作用于指定工作簿的单元格
    """
    cell(row=row, column=column).value = f'=HYPERLINK("{path}","{link_name}")'
    _cell_style(cell, row, column, fgColor)
