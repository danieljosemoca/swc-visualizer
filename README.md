What could this tool get out of my beloved the SWC...

Indeces for: 
* Dendritic complexity
* Tortuosity 
* Branching complexity
* degeneration score (when comparing neurons)
* Spatial Distribution Changes (as indicator of loss of proper targeting)

numbers: 
- Soma size (if contour or three point soma representation) 
- Branching points number

visualizations: 
- very very nice 2D visualizations
* Color-code differences between swc files (ex: same neuron after a week in epilepsy simulation thing)
- 3D visualizations? not so matplotlib...






== brainstorm ==
slap a randomforest to classify healthy vs abnormal neurons?
- would need lotta classified data which jeez where do I get that
- prolly more accurate if focus on healthy vs specific condition
- could then be used to compare neuron groups statistically that'd be insane
- lotta graphs could be made to communicate the differences to the user


unsupervised learning 
- for initial exploration
- PCA?
- no need for training or healthy vs specific condition
- usually needs a loooot of data but im wondering if swc files could be argued to have more than one data point...
- i dont like dis one anymore


== neuro considerations == 
Schizophrenia = reduced dendritic complexity (less branches and intersections)
Depression = dendritic atrophy (less volume/length)
ASD = atypical branching patterns 
epilepsy = inhibitory neurons pruned, dentate granule cells excitatory self-reinforcing circuits
migraine = decreased neurite growth in headeache-processing regions (decreased neuronal plasticity)




== TO DO == 
-mandatory-
- validation tools (mutant catcher? omaiga)
- remove repeated code in the two visualizations
- turn this into a package 
- change length of node to node depth 
- change depth() to height() question mark


-ideally-
- basic info tools (with graphs too? def input)
- hovering for more info about node (node type)






