from wizard.visualizer import SortingAlgorithm, SortingVisualizer


def main():
    wiz = SortingVisualizer(SortingAlgorithm.BUBBLE_SORT, 42)
    wiz.animate()
