from enum import StrEnum, auto
from typing import Callable
from matplotlib.container import BarContainer
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


class SortingAlgorithm(StrEnum):
    BUBBLE_SORT = auto()
    SELECTION_SORT = auto()
    INSERTION_SORT = auto()


AnimationUpdaterFunc = Callable[[int], BarContainer]


class SortingVisualizer:
    def __init__(self, algorithm: SortingAlgorithm, elements: int) -> None:
        self.N_ELEMENTS = elements
        self.algorithm = algorithm
        self.arr = np.random.randint(1, 101, self.N_ELEMENTS)
        self.fig, self.axes = plt.subplots()
        self.bar = self.axes.bar(range(1, self.N_ELEMENTS + 1), self.arr)
        self.axes.set_xlim(0, self.N_ELEMENTS + 1)
        self.axes.set_ylim(0, 110)
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)

    def selection_sort_update(self, frame):
        for i, b in enumerate(self.bar):
            b.set_color("#1f77b4")

        size = len(self.arr)
        ind = frame
        min_index = ind
        for j in range(ind + 1, size):
            if self.arr[j] < self.arr[min_index]:
                min_index = j

        self.arr[ind], self.arr[min_index] = self.arr[min_index], self.arr[ind]
        self.bar[ind].set_color("red")
        self.bar[min_index].set_color("red")

        for i, b in enumerate(self.bar):
            b.set_height(self.arr[i])

        if frame == size - 1:
            for i, b in enumerate(self.bar):
                b.set_color("green")

        return self.bar

    def bubble_sort_update(self, frame):
        for i, b in enumerate(self.bar):
            b.set_color("#1f77b4")

        size = len(self.arr)
        ind = frame
        for j in range(size - ind - 1):
            if self.arr[j] > self.arr[j + 1]:
                self.arr[j], self.arr[j + 1] = self.arr[j + 1], self.arr[j]
                self.bar[j].set_color("red")
                self.bar[j + 1].set_color("red")

        for i, b in enumerate(self.bar):
            b.set_height(self.arr[i])

        if frame == size - 1:
            for i, b in enumerate(self.bar):
                b.set_color("green")

        return self.bar

    def insertion_sort_update(self, frame):
        for i, b in enumerate(self.bar):
            b.set_color("#1f77b4")

        size = len(self.arr)
        ind = frame
        j = ind - 1
        while self.arr[j] > self.arr[j + 1] and j >= 0:
            self.arr[j], self.arr[j + 1] = self.arr[j + 1], self.arr[j]
            self.bar[j].set_color("red")
            self.bar[j + 1].set_color("red")
            j -= 1

        for i, b in enumerate(self.bar):
            b.set_height(self.arr[i])

        if frame == size - 1:
            for i, b in enumerate(self.bar):
                b.set_color("green")

        return self.bar

    def animate(self):
        update_func: AnimationUpdaterFunc | None = None
        match self.algorithm:
            case SortingAlgorithm.BUBBLE_SORT:
                update_func = self.bubble_sort_update
            case SortingAlgorithm.INSERTION_SORT:
                update_func = self.insertion_sort_update
            case SortingAlgorithm.SELECTION_SORT:
                update_func = self.selection_sort_update

            case _:
                raise ValueError(f"unknown sorting algorithm={self.algorithm.value}")

        self.anim = animation.FuncAnimation(
            fig=self.fig,
            func=update_func,
            frames=self.N_ELEMENTS,
            interval=100,
            repeat=False,
            blit=True,
        )
        plt.show()

    def save_animation(self):
        # Create a new animation for saving
        save_anim = animation.FuncAnimation(
            fig=self.fig,
            func=self.insertion_sort_update,
            frames=self.N_ELEMENTS,
            interval=100,
            repeat=False,
        )
        save_anim.save(filename="demo.html", writer="html")


# if __name__ == "__main__":
#     visualizer = SortingVisualizer()
#     visualizer.animate()  # Show the animation
#     # visualizer.save_animation()  # Save the animation
