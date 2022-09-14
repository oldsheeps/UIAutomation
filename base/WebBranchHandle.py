from base.WebOperation import condition_handle

"""
if（如果）、elif（或者）、else（否则）分支的处理思路：
    1.测试用例中8号索引（kwargs['branch']）以‘如果、或者、否则’开头，则截取文字后的数字判断缩进位置决定执行测试步骤；
    2.假设‘如果n’的n等于1，则执行条件判断，并将结果作为状态绑定‘如果n’；
    3.假设‘如果n’的n大于1，则需要判断‘如果n-1’的状态，判断是否存在‘或者n-1’,再考虑下面三种场景；
    4.如遇’或者n‘，则检查’如果n‘的状态，状态为False则执行条件判断，并将结果作为状态绑定‘或者n’；
    5.如遇‘否则n’，则先检查‘如果n’、‘或者n’的状态；再判断n是否大于1；再考虑下面三种场景；
        ‘如果’、‘否则’的n大于1需要考虑的三种场景：
            # 1.上一个if状态为True 且 elif状态为None
            # 2.上一个if、elif状态都为True
            # 3.上一个if为False 且 上一个elif为True
            # 注：如果仅仅判断两者不可以同时为False，则会出现‘如果1’不成立，‘如果2’成立仍执行
"""


def if_branch_handle(self, **kwargs):
    """
    处理if（如果）分支
    :param self: 将WebCommand.Command对象引入，为了获取其数据字典：if_handles_status、elif_handles_status、global_variable_list等等
    :param kwargs: 当前测试步骤中的数据，详情查看ScriptEnhance.params_filter()方法
    :return: 返回if条件处理的结果
    """
    # 当前‘如果’分支的缩进位置数字
    # 如：kwargs['branch'] = '如果1' ，kwargs['branch'][2:] = '1'
    index = int(kwargs['branch'][2:])

    # 若此时的缩进位置数字等于1，说明是该测试用例中的第一个if分支，则直接记录条件结果即可
    if index == 1:
        last_if_status = condition_handle(self.global_variable_list, **kwargs)
        # 如：if_handles_status['如果1'] = True
        self.if_handles_status[kwargs['branch']] = last_if_status
        return last_if_status
    # 若此时的缩进位置数字大于1，则说明并不是第一个if分支，需要考虑到多重分支的场景
    elif index > 1:
        # 1.先获取上一个if分支的状态
        last_if_status = self.if_handles_status['如果' + str(index - 1)]
        # 2.再检查上一个if分支是否存在elif分支，如果存在则拿到它的状态，不存在则标志为None
        if '或者' + str(index - 1) in self.elif_handles_status.keys():
            last_elif_status = self.elif_handles_status['或者' + str(index - 1)]
        else:
            last_elif_status = None
        # 3.接着检查上一个if和elif的状态，再考虑三种可执行的场景。
        if (last_if_status and last_elif_status is None) \
                or (last_if_status and last_elif_status) \
                or (last_if_status is False and last_elif_status):
            # 处理if条件
            current_if_status = condition_handle(self.global_variable_list, **kwargs)
            # 记录if条件处理结果
            self.if_handles_status[kwargs['branch']] = current_if_status
        else:
            # kwargs['branch'] = '如果n'
            # 将‘如果n’当作key，False当作value添加到if_handles_status字典中
            current_if_status = self.if_handles_status[kwargs['branch']] = False
        return current_if_status


def elif_branch_handle(self, **kwargs):
    # 碰到‘或者’测试步骤，需要如下处理
    # 首先获取当前缩进位置，假设当前是‘或者n’那么就需要先查‘如果n’的状态
    current_if_branch = '如果' + kwargs['branch'][2:]
    current_if_status = self.if_handles_status[current_if_branch]
    # 假设当前‘或者’对应的‘如果’为True，则只需要记录状态即可，跳过‘或者n’的步骤
    if current_if_status:
        # kwargs['branch'] = '否则n'
        # 将‘或者n’当作key，False当作value添加到elif_handles_status字典中
        current_elif_status = self.elif_handles_status[kwargs['branch']] = False
    else:
        # 当前‘或者’对应的‘如果’为False，则需要执行或者条件
        current_elif_status = condition_handle(self.global_variable_list, **kwargs)
        # 将条件处理结果记录到字典中
        self.elif_handles_status[kwargs['branch']] = current_elif_status
    return current_elif_status


def else_branch_handle(self, **kwargs):
    # 获取当前否则n分支所对应的如果n、或者n分支的状态
    current_if_branch = '如果' + kwargs['branch'][2:]
    current_elif_branch = '或者' + kwargs['branch'][2:]
    current_if_status = self.if_handles_status[current_if_branch]
    current_elif_status = False
    if current_elif_branch in self.elif_handles_status.keys():
        current_elif_status = self.elif_handles_status[current_elif_branch]
    # 当前‘否则’分支对应状态，默认False
    current_else_status = False
    # 当前‘否则’分支的缩进位置数字
    # 如：kwargs['branch'] = '否则1' ，kwargs['branch'][2:] = '1'
    index = int(kwargs['branch'][2:])

    # 开始处理else分支
    # 若此时的缩进位置数字等于1，则根据对应的‘如果’、‘或者’的状态决定当前‘否则’的状态
    if index == 1:
        # 若‘如果’、‘或者’都是False，说明条件均不成立，则将当前‘否则’分支的状态设置为True来执行
        if current_if_status is False and current_elif_status is False:
            current_else_status = self.else_handles_status[kwargs['branch']] = True
        else:
            current_else_status = self.else_handles_status[kwargs['branch']] = False

    # 若此时的缩进位置数字大于1，则需要确认上一个‘如果’、‘或者’的状态，且需要考虑多重分支的场景
    elif index > 1:
        # 检查上一个‘如果’分支是否存在，存在就获取对应的状态，不存在则标志为None
        if '如果' + str(index - 1) in self.if_handles_status.keys():
            last_if_status = self.if_handles_status['如果' + str(index - 1)]
        else:
            last_if_status = None
        # 检查上一个‘或者’分支是否存在，存在就获取对应的状态，不存在则标志为None
        if '或者' + str(index - 1) in self.elif_handles_status.keys():
            last_elif_status = self.elif_handles_status['或者' + str(index - 1)]
        else:
            last_elif_status = None

        # 检查上一个if和elif的状态，再考虑三种可执行的场景。
        if (last_if_status and last_elif_status is None) \
                or (last_if_status and last_elif_status) \
                or (last_if_status is False and last_elif_status):
            current_else_status = self.else_handles_status[kwargs['branch']] = True
        else:
            current_else_status = self.else_handles_status[kwargs['branch']] = False

    return current_else_status
