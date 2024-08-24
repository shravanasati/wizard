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


if __name__ == "__main__":
    arr = [5, 6, 1, 2, 3]
    # selection_sort(arr)
    # bubble_sort(arr)
    # insertion_sort(arr)
    # bogo_sort(arr)
    stalin_sort(arr)
    print(arr)
