# """遍历列表"""
def print_lol(the_list, indent=False, level=0):  # level=0 赋值让其变成了可选
    """遍历普通列表或嵌套列表"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    # end = “” 表示对象以什么结尾，默认是\n也就是换行
                    print("\t", end='')
            print(each_item)