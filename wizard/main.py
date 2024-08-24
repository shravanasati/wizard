from wizard.visualizer import SortingAlgorithm, SortingVisualizer, VisualizerConfig


def main():
    config = VisualizerConfig(SortingAlgorithm.SELECTION_SORT, 65, 15)
    wiz = SortingVisualizer(config)
    wiz.animate()
