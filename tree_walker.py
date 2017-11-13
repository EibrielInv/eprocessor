class tree_walker:
    def step(self, tree, current_branch, initial_branch=None):
        # If no current branch, just start from the begining
        if current_branch is None:
            return tree[0]
        # If initial branch is above the current branch
        # means that the tree is being iterated again from the begining
        # then, we must reset the initial branch value
        if initial_branch is not None:
            if tree.index(current_branch) < tree.index(initial_branch):
                initial_branch = None
        starting_branch = current_branch
        depth = len(current_branch.split("/"))-1
        if initial_branch is not None:
            initial_branch_position = current_branch.split("/")[-1]
        while 1:
            index = tree.index(current_branch)+1
            if index > len(tree)-1:
                current_branch = tree[1]
                break
            current_branch = tree[index]
            new_depth = len(current_branch.split("/"))-1
            if new_depth < depth:
                current_branch = tree[1]
                break

            if new_depth == depth+1 and initial_branch is not None:
                if initial_branch_position == current_branch.split("/")[-2]:
                    if current_branch.startswith(initial_branch):
                        break
            if new_depth == depth:
                break
        return current_branch
