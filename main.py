import os
import glob

from visualization import plot_2d, plot_3d
from processing import swc_to_dataframe, dataframe_to_tree

def visualize_swc(visualization = "3d") -> None:
    """Main function to run the program."""
    # locate all swc files in the 'morphology' folder
    swc_files = glob.glob("morphology/*.swc")
    if not swc_files:
        print("No .swc files found in a 'morphology' folder.")
        return
    
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
    visualize_swc()
