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


if __name__ == "__main__":
    arr = [5, 6, 1, 2, 3]
    # selection_sort(arr)
    # bubble_sort(arr)
    insertion_sort(arr)
    print(arr)
