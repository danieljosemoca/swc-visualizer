import os
from pathlib import Path

from visualization import plot_2d, plot_3d
from processing import swc_to_dataframe, dataframe_to_tree


def visualize_swc(path, visualization="3d") -> None:
    """Main function to run the program."""
    path = Path(path)
    if path.is_file() and path.suffix.lower() == ".swc":
        if not path.exists():
            msg = "provided SWC file path not found."
            raise FileNotFoundError(msg)
        swc_files = [path]
    elif path.is_dir():
        swc_files = list(path.glob("*.swc"))  # locate all swc files in directory
        if not swc_files:
            msg = "No .swc files found in provided directory."
            raise FileNotFoundError(msg)
        print(f"Found {len(swc_files)} SWC files in '{path}' directory.")

    else:
        msg = "No folder exists at the location specified."
        raise FileNotFoundError(msg)

    len_dir = len(swc_files)  # total number of files to process
    # determine visualization
    visualization = visualization.upper()
    if visualization == "2D":
        do_2d = True
        do_3d = False
    elif visualization == "3D":
        do_2d = False
        do_3d = True
    elif visualization == "BOTH":
        do_2d = True
        do_3d = True
    else:
        msg = "Expected '2d', '3d', or 'both' for visualization argument"
        raise ValueError(msg)

    print("\n\nStarting Processing...")
    # process each file
    for file_num, filepath in enumerate(swc_files, start=1):
        if len_dir > 1:
            print(f"\n--- Processing {file_num}/{len_dir}: {os.path.basename(filepath)} ---")
        try:
            df = swc_to_dataframe(filepath)  # dataframe
            root_node, nodes = dataframe_to_tree(df)  # tree construction
            root_node.neuron_summary()  # validation + basic stats

            if do_2d:
                plot_2d(nodes,  title=f"Neuron Morphology 2D: {os.path.basename(filepath)}")
            if do_3d:
                plot_3d(nodes, title=f"Neuron Morphology 3D: {os.path.basename(filepath)}")
        except Exception as e:
            # catch and report any error processing a specific file,
            # and proceed with processing other files
            print(f"Error processing {filepath}: {e}")


def main():
    """
    Entry point into the project.
    Processes all neurons in the example morphology directory, visualizing in 3D.
    """
    visualize_swc("morphology")


if __name__ == "__main__":
    main()
