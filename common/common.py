def sort_by_second_tuple_element(my_list):
    my_list.sort(key=lambda x: x[1])
    return my_list


def select_list_average(my_list):
    return sum(my_list) / len(my_list)
