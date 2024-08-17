from wizard.visualizer import SortingAlgorithm, SortingVisualizer


def main():
    wiz = SortingVisualizer(SortingAlgorithm.SELECTION_SORT, 12)
    wiz.animate()
