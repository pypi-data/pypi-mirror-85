#!/usr/bin/env python
# -*-coding:utf-8-*-

"""

pandas的dataframe结构是为了更清晰的表达


"""

import pandas as pd
from my_python_module.algorithm.tree.binary_decision_tree import BinaryDecisionTree


class Knapsack(object):
    def __init__(self, capacity, items=None):
        self.capacity = capacity
        self.items = [] if items is None else items
        self.freespace = self.capacity

    def add_item(self, item):
        if self.freespace - item.weight >= 0:
            self.freespace -= item.weight
            self.items.append(item)
            return True
        else:
            return False

    def all_items_value(self):
        value = 0
        for item in self.items:
            value += item.value
        return value

    def __repr__(self):
        return '<Knapsack: {0}>'.format(self.items)


class Item(object):
    def __init__(self, name, value, weight):
        self.value = value
        self.weight = weight
        self.name = name

    def __repr__(self):
        return '<Item: {0}>'.format(self.name)

    def __eq__(self, other):
        if self.name == other.name and self.value == other.value and self.weight == other.weight:
            return True
        else:
            return False


def greedy_algorithm(knapsack, items):
    """
    贪婪法求解
    :return:
    """
    items_copy = items.copy()
    found = True

    while found:
        max_value = 0
        choosed_item = None
        for item in items_copy:
            if item.value > max_value:
                choosed_item = item
                max_value = choosed_item.value

        if knapsack.add_item(choosed_item):
            found = True
            items_copy.remove(choosed_item)
        else:
            found = False
    return knapsack


def dynamic_programming(knapsack, items):
    """
    动态规划法求解
    :return:
    """
    len_i = len(items)
    len_j = knapsack.freespace

    df = pd.DataFrame(index=[item.name for item in items],
                      columns=range(1, len_j + 1))
    for i in range(len_i):
        for j in range(1, len_j + 1):
            if i == 0:  # 第一行
                item = items[i]
                test_knapsack = Knapsack(capacity=j)
                test_knapsack.add_item(item)
                df.iloc[i][j] = test_knapsack
            else:
                upper_item_value = df.iloc[i - 1][j].all_items_value()
                rightnow_item_value = items[i].value

                if j - items[i].weight == 0:
                    check_value = rightnow_item_value
                elif j - items[i].weight >= 1:
                    check_value = rightnow_item_value + df.iloc[i - 1][
                        j - items[i].weight].all_items_value()
                else:
                    check_value = 0

                test_knapsack = Knapsack(capacity=j)
                if upper_item_value >= check_value:  # 和上面的背包状态一样
                    for item in df.iloc[i - 1][j].items:
                        test_knapsack.add_item(item)
                    df.iloc[i][j] = test_knapsack
                else:
                    if j - items[i].weight == 0:
                        test_knapsack.add_item(items[i])
                    else:
                        test_knapsack.add_item(items[i])
                        for item in df.iloc[i - 1][j - items[i].weight].items:
                            test_knapsack.add_item(item)
                    df.iloc[i][j] = test_knapsack

    return df.iloc[len_i - 1][len_j]


item_a = Item('a', 6, 3)
item_b = Item('b', 7, 3)
item_c = Item('c', 8, 2)
item_d = Item('d', 9, 5)
items = [item_a, item_b, item_c, item_d]

from queue import PriorityQueue


def dynamic_programming2(items, max_node=None):
    """
    利用决策树来进行动态规划

    引入优先级队列来减少决策树构建成本
    :param knapsack:
    :param items:
    :return:
    """

    tree = BinaryDecisionTree(data={
        'pre': [],
        'post': items,
        'value': 0,
        'freespace': 5
    })

    q = PriorityQueue()
    q.put((0, tree))

    node_num = 1
    while not q.empty():
        if max_node and node_num > max_node:
            break

        _, target = q.get()
        import copy
        data = copy.deepcopy(target.data)
        data_pre = data['pre']
        data_post = data['post']
        data_value = data['value']
        data_freespace = data['freespace']

        try:
            item = data_post.pop(0)

            data = {
                'pre': data_pre,
                'post': data_post,
                'value': data_value,
                'freespace': data_freespace
            }
            node = target.append(data, new_decision=(item.name, False))
            node_num += 1
            q.put((-data_value, node))

            data_pre = data_pre + [item]
            data_value += item.value
            data_freespace -= item.weight

            data = {
                'pre': data_pre,
                'post': data_post,
                'value': data_value,
                'freespace': data_freespace
            }
            if data_freespace < 0:
                pass
            else:
                node = target.append(data, new_decision=(item.name, True))
                node_num += 1
                q.put((-data_value, node))
        except IndexError:
            pass

    max_value = 0
    target_node = None
    for node in tree.introspection():
        value = node.data['value']
        if value > max_value:
            target_node = node
            max_value = value

    return target_node


def test_priority_queue():
    """
    因为认为数字越大越优先出来，所以实践中最好都带上负号
    这样数字越大越优先出来
    权重相同的会按照插入的顺序先插先出
    :return:
    """
    q = PriorityQueue()
    q.put((-1, '1'))
    q.put((-20, '20'))
    q.put((-2, '2'))
    q.put((-3, '3-1'))
    q.put((-3, '3-2'))
    q.put((-3, '3-3'))

    while not q.empty():
        _, data = q.get()
        print(data)


if __name__ == '__main__':
    best_node = dynamic_programming2(items, max_node=10)
