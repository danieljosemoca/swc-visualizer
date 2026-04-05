import os
import glob

from visualization import plot_2d, plot_3d
from processing import swc_to_dataframe, dataframe_to_tree


def main() -> None:
    """Main function to run the program."""
    # locate all swc files in the 'morphology' folder
    swc_files = glob.glob("morphology/*.swc")
    if not swc_files:
        print("No .swc files found in a 'morphology' folder.")
        return

    # ask user which visualization(s) they want
    print("Which visualization(s) would you like?")
    print("1: 2D only")
    print("2: 3D only")
    print("3: Both 2D and 3D")
    choice = input("Enter 1, 2, or 3: ").strip()
    do_2d = choice == "1" or choice == "3"  # do_2d is True is 2D selected for
    do_3d = choice == "2" or choice == "3"  # do_3d is True is 3D selected for

    # process each file
    for filepath in swc_files:
        print(f"\n--- Processing: {os.path.basename(filepath)} ---")
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


if __name__ == "__main__":
    main()
