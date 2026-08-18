# SWC Visualizer
SWC Visualizer is a Python tool for validating, summarizing, and visualizing neuronal morphology stored in SWC files.

It is designed for people who are new to neuronal morphology and/or programming, who want to explore SWC files from databases such as NeuroMorpho.Org or other sources.

The tool can:

* Validate SWC morphology data.
* Provide basic summary information about neuronal morphology.
* Generate 2D visualizations of neuronal morphology.
* Generate interactive 3D visualizations of neuronal morphology.
* Process SWC files individually or. process all SWC files in a directory sequentially.

## Example 
![See Screenshot](https://raw.githubusercontent.com/danieljosemoca/swc-visualizer/main/docs/3d_visualizer_example.png)

## Basic Usage
After installing the package, import and call ```visualize_swc ```

```python
from swc_visualizer import visualize_swc

visualize_swc("my/neuron/folder", visualization="3d")
```

The visualization argument accepts:

* "2d" — generate a 2D visualization.
* "3d" — generate a 3D visualization.
* "both" — generate both 2D and 3D visualizations.

You can provide either an individual SWC file or a directory containing multiple SWC files:

```python
from swc_visualizer import visualize_swc

# Process a single SWC file
visualize_swc("my/neuron.swc", visualization="2d")

# Process all SWC files in a directory
visualize_swc("my/neuron_folder", visualization="both")
```
Example SWC files from NeuroMorpho are provided in the morphology directory.

## Acknowledgements
Special thanks to Marieke Westendorp for her guidance throughout this project.

## License
This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/)