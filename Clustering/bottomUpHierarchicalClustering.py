"""
    Algorithm for Bottom-up Hierarchical Clustering:

        1. Make each input its own cluster of one
        2. As long as there are multiple clusters remaining,
            find the two closest clusters and merge them.

    At the end we'll have one giant cluster containing all the inputs. If we keep
        track of the merge order, we can recreate any number of clusters by unmerging.
        For example, if we want three clusters, we can just undo the last two mergest.

"""

