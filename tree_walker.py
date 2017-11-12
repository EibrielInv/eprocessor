class tree_walker:
    def step(self, tree, current_branch, initial_branch=None):
        if current_branch is None:
            return tree[0]
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
                    break
            if new_depth == depth:
                break
        return current_branch
