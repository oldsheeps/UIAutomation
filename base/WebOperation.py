import random
import re
import string
import time
from common.LoggerConfig import *

def input_text_handle(params: str, global_variable_list: dict):
    """
    输入值处理：检查输入值是否含有变量，如果有变量则通过变量名从变量集合中取出对应数据替换之；
    如：$hello$你好，则使用hello到变量字典中获取对应的数据代替$hello$。
    params: 必填项，字符类型，需要输入的值
    global_variable_list:必填项，字典类型，变量集合
    return: 处理后的params值
    """
    pattern = re.compile(f'\$(.*?)\$', re.S)
    search = re.findall(pattern, params)
    for i in search:
        # 将text文本值中的变量替换对应的数据，一次替换一个，形成逐个替换
        params = re.sub(pattern, str(global_variable_list[i]), params, count=1)
    return str(params)


def variable_handle(**kwargs: dict):
    """
    变量处理
    name：   必填项，字符类型，变量处理的方式；如：字符串截取、字符串替换、字符串拼接、字符串计数、仅保留数字、金额格式化、日期赋值、重新赋值、随机数字、随机字母、数学运算
    value：  非必填，常规类型，变量处理的截取索引值、拼接值、年月日生成规则、随机数的保留位数、数学运算方式
    expect： 非必填，常规类型，变量重新赋值、字符串的替换值、字符串拼接的位置、数学运算的运算数
    :return: 处理后的变量值
    """
    method = kwargs['method']
    value = kwargs["value"] if "value" in kwargs else 0 if "value" in kwargs and kwargs["value"] == 0 else ""
    params = "params" in kwargs and kwargs["params"] or ""
    expect = kwargs["expect"] if "expect" in kwargs else 0 if "expect" in kwargs and kwargs["expect"] == 0 else ""
    if method == '字符串截取':
        # 如：value = '7,14' 或 value = '首,尾'
        start, end = value.split(',')
        # 场景1：切割后得出截取范围均是数字，则直接强转加切片完成截取
        if str(start).isdigit() and str(end).isdigit():
            final_params = params[int(start):int(end)]
        # 场景2：切割后得出截取范围不是数字，则需要先查询起始字符的索引加上起始字符的长度和结束字符的索引，后再使用切片
        else:
            start = params.find(start) + len(start)
            end = params.find(end)
            final_params = params[start:end]
        log.info(f"webdriver：在[{params}]文本中截取[{start}-{end}]之间的值，结果为[{final_params}]!")
        return final_params

    elif method == '字符串替换':
        # 将字符串中的 value 值全部替换为 expect 值
        final_params = params.replace(str(value), str(expect))
        log.info(f"webdriver：将[{params}]文本中的[{value}]全部替换为[{expect}]，结果为[{final_params}]!")
        return final_params

    elif method == '字符串拼接':
        # 场景1：如果指定在0号索引处拼接，则在变量文本值的开头拼接
        if int(expect) == 0:
            final_params = value + params
        # 场景2：如果并未指定索引，则在变量文本值的末尾拼接
        elif expect == "":
            final_params = params + value
        # 场景3：在变量文本值的指定索引处插入拼接值
        else:
            final_params = params[:int(expect)] + value + params[int(expect):]
        log.info(f"webdriver：在[{params}]文本的[{expect}]位置拼接上[{value}]，结果为[{final_params}]!")
        return final_params

    elif method == '字符串计数':
        # 以字符串类型返回字符串的数量
        final_params = str(len(params))
        log.info(f"webdriver：计算[{params}]字符数量，结果为[{final_params}]!")
        return final_params

    elif method == '仅保留数字':
        # 保留字符串中所有的数字
        final_params = ""
        for item in str(params):
            if item.isdigit():
                final_params += item
        log.info(f"webdriver：仅保留[{params}]的数字，结果为[{final_params}]!")
        return final_params

    elif method == '金额格式化':
        # 将金额按照千分位分隔格式化
        final_params = "{:,.2f}".format(float(params))
        log.info(f"webdriver：将[{params}]金额格式化，结果为[{final_params}]!")
        return final_params

    elif method == '日期赋值':
        # 根据 value 值获取当前年、月、日、年月日
        final_params = ''
        if value == '年':
            final_params = time.strftime('%Y', time.localtime(time.time()))
        elif value == '月':
            final_params = time.strftime('%m', time.localtime(time.time()))
        elif value == '日':
            final_params = time.strftime('%d', time.localtime(time.time()))
        elif value == '年月日':
            final_params = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        log.info(f"webdriver：获取当前[{value}]，结果为[{final_params}]!")
        return final_params

    elif method == '重新赋值':
        # 将expect作为新数据返回给当前变量，完成重新赋值
        log.info(f"webdriver：将[{expect}]赋值给[%{kwargs['key']}%]变量!")
        return str(expect)

    elif method == '随机数字':
        # 根据 value 值确定返回的随机数字位数（最大30位）
        random_1 = str(random.random())[2:][::-1]
        random_2 = str(random.random())[2:][::-1]
        random_3 = random_1[:15] + random_2[:15]
        final_params = random_3[:int(value)]
        log.info(f"webdriver：随机获取[{value}]位数字，结果为[{final_params}]!")
        return final_params

    elif method == '随机字母':
        # 根据 value 值确定返回的随机字母位数
        final_params = "".join(random.sample(string.ascii_letters, value))
        log.info(f"webdriver：随机获取[{value}]位字母，结果为[{final_params}]!")
        return final_params

    elif method == '数学运算':
        final_params = math_operation(method=value, variable=params, expect=expect)
        log.info(f"webdriver：运算[{params}{value}{expect}]，结果为[{final_params}]!")
        return final_params


def condition_handle(global_variable_list: dict, **kwargs: dict):
    """
    条件处理
    global_variable_list: 必填项，字典类型，变量集合
    method: 必填项，字符类型，条件处理的方式，如：比较运算、表达式运算
    expect: 必填项，常规类型，预期比较对象
    params: 必填项，常规类型，1.变量名；2.表达式
            1.变量名：$hello$、$world$...
            2.表达式：$计算结果$==0,或,$计算结果$!=20,且,$计算结果$<1
    return: 运算结果为True或False
    """
    expect = "expect" in kwargs and kwargs["expect"]
    # 判断条件类型
    if kwargs['method'] == '比较运算':
        # 处理变量名，去除变量前后缀，当作key到变量字典中取value
        if str(kwargs['params']).startswith('$') and str(kwargs['params']).endswith('$'):
            params = kwargs['params'][1:-1]
        else:
            params = kwargs['params']
        variable = global_variable_list[params]
        # 将获取对应的数据传递给比较运算函数进行运算，返回最终结果
        return compare_operation(method=str(kwargs['value']), variable=variable, expect=expect)

    elif kwargs['method'] == '表达式运算':
        # 将条件以,分割得出列表；如：['$计算结果$==0', '或', '$计算结果$!=20', '且', '$计算结果$<1']
        condition = str(kwargs['params']).split(',')
        # 记录每个条件表达式的状态
        once_condition_status = []
        # 记录最终状态
        final_status = False
        for i in range(len(condition)):
            # 在偶数中(条件表达式)寻找比较运算的符号
            if i % 2 == 0:
                symbol_index,symbol_len,symbol_str = symbol_handle(condition[i])
                # 符号左边的数据
                variable_key = condition[i][:symbol_index][1:-1]
                # 去除首尾的$符号，到变量字典中取数据
                variable = int(global_variable_list[variable_key])
                # 运算的符号
                symbol = condition[i][symbol_index:symbol_index + symbol_len]
                # 符号右边的数据
                expect_data = int(condition[i][symbol_index + symbol_len:])
                # 将每一个条件的结果添加到列表
                status = compare_operation(symbol_str, variable, expect_data)
                once_condition_status.append(status)
            # 如果奇数说明是条件连接符，在当前位置插入到列表中即可
            if i % 2 != 0:
                if condition[i] == '且':
                    once_condition_status.insert(i, 'and')
                elif condition[i] == '或':
                    once_condition_status.insert(i, 'or')
        # 将列表中的每一个元素连接得出原类型，当作最终状态返回
        final_status = eval(" ".join([str(i) for i in once_condition_status]))
        return final_status
    else:
        raise NameError(f"变量处理方式不存在！")


def symbol_handle(condition:str):
    """
    condition_handle函数的拆分函数，用来切割条件表达式；
    从条件中查找比较运算符号的位置，记录比较方式，和比较方式的长度
    condition:  必填项，字符类型，条件表达式
    return:     符号索引位置，比较方式长度，比较方式名称
    """
    symbol_index = 0
    symbol_len = 1
    symbol_str = '等于'
    if condition.find('>') != -1:
        symbol_index = condition.find('>')
        symbol_str = '大于'
    elif condition.find('>=') != -1:
        symbol_index = condition.find('>=')
        symbol_str = '大于等于'
        symbol_len = 4
    elif condition.find('<') != -1:
        symbol_index = condition.find('<')
        symbol_str = '小于'
    elif condition.find('<=') != -1:
        symbol_index = condition.find('<=')
        symbol_str = '小于等于'
        symbol_len = 4
    elif condition.find('==') != -1:
        symbol_index = condition.find('==')
        symbol_len = 2
        symbol_str = '等于'
    elif condition.find('!=') != -1:
        symbol_index = condition.find('!=')
        symbol_len = 2
        symbol_str = '不等于'
    return symbol_index,symbol_len,symbol_str


def compare_operation(method: str, variable: float, expect: float):
    """
    比较运算
    method:   必填项，字符类型，数据进行数学运算的方式，如：大于、大于等于、小于、小于等于、等于、不等于
    variable: 必填项，字符类型，变量值
    expect:   必填项，字符类型，运算值
    return:   返回变量值与运算值得出的结果
    """
    variable = float(variable)
    expect = float(expect)
    if method == '大于':
        return variable > expect
    elif method == '大于等于':
        return variable >= expect
    elif method == '小于':
        return variable < expect
    elif method == '小于等于':
        return variable <= expect
    elif method == '等于':
        return variable == expect
    elif method == '不等于':
        return variable != expect
    else:
        raise NameError(f"比较运算方式不存在！")


def math_operation(method: str, variable: str, expect: str):
    """
    数学运算
    method:   必填项，字符类型，数据进行数学运算的方式，如：加、减、乘、除
    variable: 必填项，字符类型，变量值
    expect:   必填项，字符类型，运算值
    return:   返回变量值与运算值得出的结果
    """
    variable = float(variable)
    expect = float(expect)
    result = 0
    if method == '加':
        result = variable + expect
    elif method == '减':
        result = variable - expect
    elif method == '乘':
        result = variable * expect
    elif method == '除':
        result = variable / expect
    result = str(result)
    if result.find('.'):
        if int(result[result.find('.') + 1:]) > 0:
            pass
        else:
            result = result[:result.find('.')]
    return str(result)