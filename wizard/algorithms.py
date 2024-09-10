import random


def selection_sort(arr: list[int]):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        print(min_idx)
        arr[i], arr[min_idx] = arr[min_idx], arr[i]


def bubble_sort(arr: list[int]):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def insertion_sort(arr: list[int]):
    n = len(arr)
    for i in range(1, n):
        j = i - 1
        while arr[j] > arr[j + 1] and j >= 0:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
            j -= 1


def _is_sorted(arr: list[int]):
    if len(arr) < 2:
        # 0 or 1 elements
        return True

    for i in range(1, len(arr)):
        if arr[i] < arr[i - 1]:
            return False

    return True


def bogo_sort(arr: list[int]):
    while not _is_sorted(arr):
        random.shuffle(arr)
        continue

    return arr


def stalin_sort(arr: list[int]) -> None:
    if len(arr) < 2:
        return

    write_index = 1
    for read_index in range(1, len(arr)):
        if arr[read_index] >= arr[write_index - 1]:
            arr[write_index] = arr[read_index]
            write_index += 1

    del arr[write_index:]


def partition(arr, l, h):
    i = l - 1
    x = arr[h]

    for j in range(l, h):
        if arr[j] <= x:

            # increment index of smaller element
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[h] = arr[h], arr[i + 1]
    return i + 1


def quickSortIterative(arr, l, h):

    # Create an auxiliary stack
    size = h - l + 1
    stack = [0] * (size)

    # initialize top of stack
    top = -1

    # push initial values of l and h to stack
    top = top + 1
    stack[top] = l
    top = top + 1
    stack[top] = h

    # Keep popping from stack while is not empty
    while top >= 0:

        # Pop h and l
        h = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1

        # Set pivot element at its correct position in
        # sorted array
        p = partition(arr, l, h)

        # If there are elements on left side of pivot,
        # then push left side to stack
        if p - 1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1

        # If there are elements on right side of pivot,
        # then push right side to stack
        if p + 1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h


arr = [4, 3, 5, 2, 1, 3, 2, 3]
n = len(arr)
quickSortIterative(arr, 0, n - 1)
print("Sorted array is:")
for i in range(n):
    print("%d" % arr[i]),


if __name__ == "__main__":
    arr = [5, 6, 1, 2, 3]
    # selection_sort(arr)
    # bubble_sort(arr)
    # insertion_sort(arr)
    # bogo_sort(arr)
    stalin_sort(arr)
    print(arr)
