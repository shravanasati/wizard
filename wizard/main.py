from wizard.visualizer import SortingAlgorithm, SortingVisualizer, VisualizerConfig


def main():
    config = VisualizerConfig(SortingAlgorithm.INSERTION_SORT, 82, 5)
    wiz = SortingVisualizer(config)
    wiz.animate()
