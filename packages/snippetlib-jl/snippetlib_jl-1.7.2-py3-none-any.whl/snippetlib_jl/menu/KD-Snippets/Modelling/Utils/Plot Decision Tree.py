# display the decision tree
from IPython.display import SVG
from graphviz import Source
from sklearn.tree import export_graphviz

graph = Source(export_graphviz(clf, out_file=None, 
                               feature_names=attributes, 
                               filled=True, 
                               rounded=True, 
                               rotate=True, 
                               impurity=False))
SVG(graph.pipe(format='svg'))