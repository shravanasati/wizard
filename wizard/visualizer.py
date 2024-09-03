from math import floor, log2
import random
from typing import NamedTuple
from enum import StrEnum, auto
from typing import Callable
from matplotlib.container import BarContainer
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


class SortingAlgorithm(StrEnum):
    """
    Enum representing a sorting algorithm.
    """

    BUBBLE_SORT = auto()
    SELECTION_SORT = auto()
    INSERTION_SORT = auto()
    BOGO_SORT = auto()
    QUICK_SORT = auto()
    MERGE_SORT = auto()

    def algorithm_name(self):
        """
        Returns algorithm name in format 'Name Sort'.
        """
        name = self.name
        splitt = name.split("_")
        return " ".join(map(lambda x: x.capitalize(), splitt))


class VisualizerConfig(NamedTuple):
    algorithm: SortingAlgorithm
    elements: int
    speed: float  # speed factor


# type alias for a matplotlib.animation.FuncAnimation update func
AnimationUpdaterFunc = Callable[[int], BarContainer]


class SortingVisualizer:
    def __init__(self, config: VisualizerConfig) -> None:
        self.config = config

        self.arr = np.random.randint(1, 101, self.config.elements)
        self.sorted_arr = sorted(self.arr)
        self._is_sorted = list(self.arr) == self.sorted_arr

        self.fig, self.axes = plt.subplots()

        self.bar = self.axes.bar(range(1, self.config.elements + 1), self.arr)
        self.axes.set_title(f"Visualizing {config.algorithm.algorithm_name()}")
        self.axes.set_xlim(0, self.config.elements + 1)
        self.axes.set_ylim(0, 110)
        self.axes.get_xaxis().set_visible(False)
        # self.axes.get_yaxis().set_visible(False)

        # quick sort setup
        self._qs_stack = [0] * (self.config.elements)
        self._qs_top = 0
        self._qs_stack[self._qs_top] = 0
        self._qs_top += 1
        self._qs_stack[self._qs_top] = self.config.elements - 1

    def _reset_bars_to_arr(self):
        for i, b in enumerate(self.bar):
            b.set_height(self.arr[i])

    def _set_bars_to_color(self, color: str):
        for b in self.bar:
            b.set_color(color)

    def _set_bars_blue(self):
        self._set_bars_to_color("#1f77b4")

    def _set_bars_green(self):
        self._set_bars_to_color("green")

    def _swap(self, i: int, j: int):
        """
        Helper function to swap elements in self.arr, along with setting colors of changed bars to red.
        """
        self.arr[i], self.arr[j] = self.arr[j], self.arr[i]
        self.bar[i].set_color("red")
        self.bar[j].set_color("red")

    def selection_sort_update(self, frame):
        self._set_bars_blue()

        size = len(self.arr)
        ind = frame
        min_index = ind
        for j in range(ind + 1, size):
            if self.arr[j] < self.arr[min_index]:
                min_index = j

        self._swap(ind, min_index)

        self._reset_bars_to_arr()

        if frame == size - 1:
            self._set_bars_green()

        return self.bar

    def bubble_sort_update(self, frame):
        self._set_bars_blue()

        size = len(self.arr)
        ind = frame
        for j in range(size - ind - 1):
            if self.arr[j] > self.arr[j + 1]:
                self._swap(j, j + 1)

        self._reset_bars_to_arr()

        if frame == size - 1:
            self._set_bars_green()

        return self.bar

    def insertion_sort_update(self, frame):
        self._set_bars_blue()

        size = len(self.arr)
        ind = frame
        j = ind - 1
        while self.arr[j] > self.arr[j + 1] and j >= 0:
            self._swap(j, j + 1)
            j -= 1

        self._reset_bars_to_arr()

        if frame == size - 1:
            self._set_bars_green()

        return self.bar

    def bogo_sort_update(self, frame):
        np.random.shuffle(self.arr)
        self._reset_bars_to_arr()
        self._is_sorted = list(self.arr) == self.sorted_arr
        if self._is_sorted:
            self._set_bars_green()
        return self.bar

    def _bogo_sort_frames(self):
        while not self._is_sorted:
            yield 1

    def __partition_arr(self, low: int, high: int):
        self._set_bars_blue()
        pivot_index = random.randrange(low, high + 1)
        self.bar[pivot_index].set_color("orange")
        self._swap(pivot_index, high)
        self._reset_bars_to_arr()
        pivot = self.arr[high]

        smaller = low - 1
        for j in range(low, high):
            if self.arr[j] <= pivot:
                smaller += 1
                self._swap(smaller, j)
                self._reset_bars_to_arr()

        self._swap(smaller + 1, high)
        return smaller + 1

    def quick_sort_update(self, frame):
        h = self._qs_stack[self._qs_top]
        self._qs_top -= 1
        l = self._qs_stack[self._qs_top]
        self._qs_top -= 1

        # Set pivot element at its correct position in
        # sorted array
        p = self.__partition_arr(l, h)
        self._reset_bars_to_arr()

        # If there are elements on left side of pivot,
        # then push left side to self.stack
        if p - 1 > l:
            self._qs_top += 1
            self._qs_stack[self._qs_top] = l
            self._qs_top += 1
            self._qs_stack[self._qs_top] = p - 1

        # If there are elements on right side of pivot,
        # then push right side to self.stack
        if p + 1 < h:
            self._qs_top += 1
            self._qs_stack[self._qs_top] = p + 1
            self._qs_top += 1
            self._qs_stack[self._qs_top] = h

        if self._qs_top < 0:
            self._set_bars_green()

        return self.bar

    def _quick_sort_frames(self):
        while self._qs_top >= 0:
            yield 1

        yield 1

    def __merge(self, left: int, mid: int, right: int):
        # Initialize pointers for the two subarrays
        i = left
        j = mid + 1

        # Merge the two subarrays in place
        while i <= mid and j <= right:
            if self.arr[i] <= self.arr[j]:
                i += 1
            else:
                # Element at j is smaller; shift elements to the right
                value = self.arr[j]
                index = j

                # Shift all elements between i and j to the right by one
                while index != i:
                    self.arr[index] = self.arr[index - 1]
                    self.bar[index].set_color("red")
                    index -= 1

                # Place the value at the correct location
                self.arr[i] = value

                # Update the visualization after each shift
                self._reset_bars_to_arr()

                # Update pointers
                i += 1
                mid += 1
                j += 1

    def merge_sort_update(self, frame):
        n = self.config.elements
        for left in range(0, n, 2 * frame):
            mid = min(left + frame - 1, n - 1)
            right = min(left + 2 * frame - 1, n - 1)

            # Merge subarrays arr[left...mid] and arr[mid+1...right]
            self.__merge(left, mid, right)

        if frame == 2 ** (floor(log2(n))):
            self._set_bars_green()

        return self.bar

    def _merge_sort_frames(self):
        curr_size = 1
        while curr_size < self.config.elements:
            yield curr_size
            curr_size *= 2

    def _get_update_func(self) -> AnimationUpdaterFunc:
        update_func: AnimationUpdaterFunc | None = None
        match self.config.algorithm:
            case SortingAlgorithm.BUBBLE_SORT:
                update_func = self.bubble_sort_update
            case SortingAlgorithm.INSERTION_SORT:
                update_func = self.insertion_sort_update
            case SortingAlgorithm.SELECTION_SORT:
                update_func = self.selection_sort_update
            case SortingAlgorithm.BOGO_SORT:
                update_func = self.bogo_sort_update
            case SortingAlgorithm.QUICK_SORT:
                update_func = self.quick_sort_update
            case SortingAlgorithm.MERGE_SORT:
                update_func = self.merge_sort_update

            case _:
                raise ValueError(
                    f"unknown sorting algorithm={self.config.algorithm.value}"
                )

        return update_func

    def _get_frames(self):
        match self.config.algorithm:
            case (
                SortingAlgorithm.BUBBLE_SORT
                | SortingAlgorithm.SELECTION_SORT
                | SortingAlgorithm.INSERTION_SORT
            ):
                return self.config.elements

            case SortingAlgorithm.BOGO_SORT:
                return self._bogo_sort_frames

            case SortingAlgorithm.QUICK_SORT:
                return self._quick_sort_frames

            case SortingAlgorithm.MERGE_SORT:
                return self._merge_sort_frames

            case _:
                raise ValueError(
                    f"unknown sorting algorithm={self.config.algorithm.value}"
                )

    def animate(self):
        update_func = self._get_update_func()
        frames = self._get_frames()
        interval = 500 / self.config.speed  # milliseconds

        self.anim = animation.FuncAnimation(
            fig=self.fig,
            func=update_func,
            frames=frames,
            interval=interval,
            repeat=False,
            blit=True,
        )
        plt.show()


# if __name__ == "__main__":
#     visualizer = SortingVisualizer()
#     visualizer.animate()  # Show the animation
#     # visualizer.save_animation()  # Save the animation
