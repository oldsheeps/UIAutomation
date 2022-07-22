import os

from openpyxl.styles import PatternFill, Font


def _cell_style(cell, row, column, fgColor):
    """
    单元格样式处理
    :param cell: 单元格
    :param row: 行
    :param column: 列
    :param fgColor: 前景颜色（AACF91：绿色、FF0000：红色）
    :return: 作用到工作簿
    """
    cell(row=row, column=column).fill = PatternFill(patternType='solid', fgColor=fgColor)
    cell(row=row, column=column).font = Font(bold=True)


# Pass样式配置
def pass_(cell, row, column):
    cell(row=row, column=column).value = 'Pass'
    _cell_style(cell, row, column, 'AACF91')


# Failed样式配置
def failed_(cell, row, column):
    cell(row=row, column=column).value = 'Failed'
    _cell_style(cell, row, column, 'FF0000')


# 自定义回填value样式配置
def value_(cell, row, column, value, fgColor='AACF91'):
    cell(row=row, column=column).value = value
    _cell_style(cell, row, column, fgColor)


def hyperlink_(cell, row, column, path, fgColor='AACF91'):
    """
    超链接样式配置 ADD8E6,87CECB,B0E0E6,AFEEEE
    :param cell: 单元格
    :param row: 行
    :param column: 列
    :param path: 作用工作簿的路径
    :param fgColor: 前景颜色（AACF91：绿色、FF0000：红色）
    :return: 作用于指定工作簿的单元格
    """
    global name
    current_path = os.path.abspath(os.path.dirname(__file__)).split('common')[0][0:-1] + '\picture\\'
    if not str(path).find('/') == '-1':
        name = str(path)[str(path).rindex('/') + 1:]
    cell(row=row, column=column).value = f'=HYPERLINK("{current_path + name}","Screenshot")'
    _cell_style(cell, row, column, fgColor)
