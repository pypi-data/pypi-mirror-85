# """遍历列表"""
def print_lol(the_list):
    """遍历普通列表或嵌套列表"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)