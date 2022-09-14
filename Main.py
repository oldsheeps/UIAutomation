from case import Server_Test_Runner
from common.LoggerConfig import *


def _main(dataSet):
    cut_line = '-'*60
    left_line = '-'*18
    result = []
    stepNum = 1
    for case_group in dataSet:
        log.info(cut_line)
        log.info(cut_line)
        log.info('{} 测试用例所属组号：[{: ^5}] {}'.format(left_line,case_group[0],left_line))
        for case_suite in case_group[1]:
            if type(case_suite) is int:
                log.info('{} 测试用例所属编号：[{: ^5}] {}'.format(left_line,case_suite,left_line))
                log.info(cut_line)
                log.info(cut_line)
                continue
            for case_info in case_suite:
                status = Server_Test_Runner.excel_ruuner(case_info[0],case_info[1],case_info[2],case_info[3],case_info[4],case_info[5])
                log.info(f'执行用例第{stepNum}步骤：{case_info[4]}')
                stepNum +=1
                result.append(status)
    return result

def _main2(execute_func,loc_func,loc_path,input_text,steps_desc,expect_result):
    cut_line = '-'*60
    left_line = '-'*18
    stepNum = 1
    log.info(cut_line)
    log.info(cut_line)
    log.info('{} 测试用例所属组号：[{: ^5}] {}'.format(left_line,'测试用例组号',left_line))
    log.info('{} 测试用例所属编号：[{: ^5}] {}'.format(left_line,'测试用例序号',left_line))
    log.info(cut_line)
    log.info(cut_line)
    status = Server_Test_Runner.excel_ruuner(execute_func,loc_func,loc_path,input_text,steps_desc,expect_result)
    log.info(f'执行用例第{stepNum}步骤：{input_text}')
    stepNum +=1
    return status

if __name__ == '__main__':
    dicts = [
            [1001,
                [10, [
                    ['创建浏览器对象',  None, None, 'Chrome', '打开浏览器',  None,None],
                    ['访问', None,  None, 'http://www.baidu.com/',  '打开百度',None,None],
                    ['输入', 'id', 'kw', 'python','百度搜索python', None,None],
                    ['点击', 'id', 'su',  None, '点击百度一下',  None,None],
                    ['文本断言', 'xpath', '//*[@id="1"]/div/div/h3/a', None, '检查搜索内容', 'Python(计算机编程语言) - 百度百科', None],
                    ['截图', None,  None, '搜索后截图存根', '搜索后截图存根', None,None],
                    ],
                ]
            ]
            ]

    # rs = _main(dicts)
    # print('当前测试用例每一步骤结果：',rs)

    step = [
        ['创建浏览器对象', None, None, 'Chrome', '打开浏览器', None],
        ['访问', None, None, 'http://www.baidu.com/', '打开百度',None],
        ['输入', 'id', 'kw', 'python', '百度搜索python', None],
        ['点击', 'id', 'su', None, '点击百度一下', None,],
        ['文本断言', 'xpath', '//*[@id="1"]/div/div/h3/a', None, '检查搜索内容', 'Python(计算机编程语言) - 百度百科'],
        ['截图', None, None, '搜索后截图存根', '搜索后截图存根', None],
    ]
    rs2 = []
    for i in step:
        # print(i)
        # status = _main2('创建浏览器对象',None,None,'Chrome','打开浏览器',None)
        status = _main2(*i)
        rs2.append(status)
    print('当前测试用例每一步骤结果：',rs2)

