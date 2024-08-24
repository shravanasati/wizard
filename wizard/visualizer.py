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

        self._stalin_write_index = 1

        self.fig, self.axes = plt.subplots()

        self.bar = self.axes.bar(range(1, self.config.elements + 1), self.arr)
        self.axes.set_title(f"Visualizing {config.algorithm.algorithm_name()}")
        self.axes.set_xlim(0, self.config.elements + 1)
        self.axes.set_ylim(0, 110)
        self.axes.get_xaxis().set_visible(False)
        # self.axes.get_yaxis().set_visible(False)

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
