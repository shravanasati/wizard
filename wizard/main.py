import tkinter as tk
from tkinter import ttk
import sv_ttk
from wizard.visualizer import SortingAlgorithm, SortingVisualizer, VisualizerConfig


def visualize(algo_name: str, elements: int, speed: float):
    # auto in StrEnum generates values as lowered names
    # transforming "Algo Sort" to "algo_sort"
    algo = algo_name.lower().replace(" ", "_")
    config = VisualizerConfig(SortingAlgorithm(algo), elements, speed)
    wiz = SortingVisualizer(config)
    wiz.animate()


def main():
    root = tk.Tk()
    root.title("wizard - Sorting Algorithm Visualizer")
    root.geometry("800x600")
    tk.Label(root, text="wizard 🪄", font=("Segoe UI", 40, "bold")).pack(pady=10)
    tk.Label(root, text="a sorting algorithm visualizer", font=("Segoe UI", 25, "bold")).pack(pady=7)

    algorithms = [a.algorithm_name() for a in SortingAlgorithm]

    algorithm_label = tk.Label(root, text="Select Algorithm:")
    algorithm_label.pack(pady=5)
    algorithm_var = tk.StringVar(value=algorithms[0])
    algorithm_menu = ttk.Combobox(root, textvariable=algorithm_var, values=algorithms)
    algorithm_menu.pack(pady=5)

    speed_label = tk.Label(root, text="Speed:")
    speed_label.pack(pady=5)
    speed_var = tk.DoubleVar(value=1.0)
    speed_slider = ttk.Scale(
        root, from_=1, to=10, orient=tk.HORIZONTAL, variable=speed_var, length=200
    )
    speed_slider.pack(pady=5)

    elements_label = tk.Label(root, text="Number of Elements:")
    elements_label.pack(pady=5)
    elements_var = tk.IntVar(value=50)
    elements_entry = ttk.Entry(root, textvariable=elements_var, width=10)
    elements_entry.pack(pady=5)

    visualize_button = ttk.Button(
        root,
        text="Visualize",
        command=lambda: visualize(
            algorithm_var.get(), elements_var.get(), speed_var.get()
        ),
    )
    visualize_button.pack(pady=20)

    sv_ttk.use_dark_theme(root)
    root.mainloop()
