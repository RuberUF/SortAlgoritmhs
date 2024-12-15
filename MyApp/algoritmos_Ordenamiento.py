import csv
import random
import time

def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return [float(item[0]) for item in data if item]

def generate_random_data(start_range, end_range, data_count):
    return [random.randint(start_range, end_range) for _ in range(data_count)]

def bubble_sort(arr, order_type='asc'):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if (order_type == 'asc' and arr[j] > arr[j + 1]) or (order_type == 'desc' and arr[j] < arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def quick_sort(arr, order_type='asc'):
    if len(arr) <= 1:
        return arr
    pivot = arr[-1]
    left = [x for x in arr[:-1] if (order_type == 'asc' and x < pivot) or (order_type == 'desc' and x > pivot)]
    right = [x for x in arr[:-1] if (order_type == 'asc' and x >= pivot) or (order_type == 'desc' and x <= pivot)]
    return quick_sort(left, order_type) + [pivot] + quick_sort(right, order_type)

def insertion_sort(arr, order_type='asc'):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and ((order_type == 'asc' and arr[j] > key) or (order_type == 'desc' and arr[j] < key)):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def cocktail_sort(arr, order_type='asc'):
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if (order_type == 'asc' and arr[i] > arr[i + 1]) or (order_type == 'desc' and arr[i] < arr[i + 1]):
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end -= 1
        for i in range(end - 1, start - 1, -1):
            if (order_type == 'asc' and arr[i] > arr[i + 1]) or (order_type == 'desc' and arr[i] < arr[i + 1]):
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        start += 1
    return arr

def bucket_sort(arr, order_type='asc'):
    if len(arr) == 0:
        return arr
    bucket_count = int(max(arr)) - int(min(arr)) + 1
    buckets = [[] for _ in range(bucket_count)]
    for num in arr:
        index = int(num) - int(min(arr))
        buckets[index].append(num)
    for i in range(bucket_count):
        buckets[i].sort(reverse=(order_type == 'desc'))
    return [num for bucket in buckets for num in bucket]

def counting_sort(arr, order_type='asc'):
    max_val = int(max(arr))
    min_val = int(min(arr))
    range_of_elements = max_val - min_val + 1
    count_arr = [0] * range_of_elements
    output_arr = [0] * len(arr)
    for num in arr:
        count_arr[int(num) - min_val] += 1
    if order_type == 'asc':
        for i in range(1, len(count_arr)):
            count_arr[i] += count_arr[i - 1]
    else:
        for i in range(len(count_arr) - 2, -1, -1):
            count_arr[i] += count_arr[i + 1]
    for num in arr:
        output_arr[count_arr[int(num) - min_val] - 1] = num
        count_arr[int(num) - min_val] -= 1
    return output_arr

def merge_sort(arr, order_type='asc'):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid], order_type)
    right_half = merge_sort(arr[mid:], order_type)
    return merge(left_half, right_half, order_type)

def merge(left, right, order_type):
    result = []
    while left and right:
        if (order_type == 'asc' and left[0] <= right[0]) or (order_type == 'desc' and left[0] >= right[0]):
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result.extend(left or right)
    return result

def binary_tree_sort(arr, order_type='asc'):
    if len(arr) == 0:
        return arr
    root = TreeNode(arr[0])
    for num in arr[1:]:
        insert(root, num)
    sorted_arr = []
    inorder_traversal(root, sorted_arr, order_type == 'asc')
    return sorted_arr

class TreeNode:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

def insert(node, value):
    if value < node.value:
        if node.left is None:
            node.left = TreeNode(value)
        else:
            insert(node.left, value)
    else:
        if node.right is None:
            node.right = TreeNode(value)
        else:
            insert(node.right, value)

def inorder_traversal(node, result, ascending=True):
    if node is not None:
        inorder_traversal(node.left if ascending else node.right, result, ascending)
        result.append(node.value)
        inorder_traversal(node.right if ascending else node.left, result, ascending)

def radix_sort(arr, order_type='asc'):
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        arr = counting_sort_radix(arr, exp, order_type)
        exp *= 10
    return arr

def counting_sort_radix(arr, exp, order_type):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for num in arr:
        index = num // exp
        count[int(index % 10)] += 1
    if order_type == 'asc':
        for i in range(1, 10):
            count[i] += count[i - 1]
    else:
        for i in range(8, -1, -1):
            count[i] += count[i + 1]
    for i in range(n - 1, -1, -1):
        index = arr[i] // exp
        output[count[int(index % 10)] - 1] = arr[i]
        count[int(index % 10)] -= 1
    return output

def shell_sort(arr, order_type='asc'):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and ((order_type == 'asc' and arr[j - gap] > temp) or (order_type == 'desc' and arr[j - gap] < temp)):
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

def comb_sort(arr, order_type='asc'):
    n = len(arr)
    gap = n
    shrink = 1.3
    sorted = False
    while not sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True
        i = 0
        while i + gap < n:
            if (order_type == 'asc' and arr[i] > arr[i + gap]) or (order_type == 'desc' and arr[i] < arr[i + gap]):
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False
            i += 1
    return arr

def heap_sort(arr, order_type='asc'):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, order_type)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0, order_type)
    return arr

def heapify(arr, n, i, order_type):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and ((order_type == 'asc' and arr[i] < arr[left]) or (order_type == 'desc' and arr[i] > arr[left])):
        largest = left

    if right < n and ((order_type == 'asc' and arr[largest] < arr[right]) or (order_type == 'desc' and arr[largest] > arr[right])):
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest, order_type)

def heap_sort(arr, order_type='asc'):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, order_type)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0, order_type)
    return arr

def selection_sort(arr, order_type='asc'):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if (order_type == 'asc' and arr[j] < arr[min_idx]) or (order_type == 'desc' and arr[j] > arr[min_idx]):
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def shell_sort(arr, order_type='asc'):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and ((order_type == 'asc' and arr[j - gap] > temp) or (order_type == 'desc' and arr[j - gap] < temp)):
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

def gnome_sort(arr, order_type='asc'):
    index = 0
    n = len(arr)
    while index < n:
        if index == 0:
            index += 1
        if (order_type == 'asc' and arr[index] >= arr[index - 1]) or (order_type == 'desc' and arr[index] <= arr[index - 1]):
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1
    return arr


