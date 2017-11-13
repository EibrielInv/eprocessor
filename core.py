import os

from tree_walker import tree_walker


# Traverse dialog tree
class Core:
    def __init__(self, bot_script, analyzer):
        self.walker = tree_walker()
        self.context = {
            "messenger": "telegram"
        }
        self.input_data_template = {
            "input_text": None,
            "intents": [],
            "entities": []
        }
        self.input_data = self.input_data_template
        self.current_branch = None
        self.bot_script = bot_script
        self.analyzer = analyzer

    def iteration(self, input_text):
        tree = self.bot_script.get_tree()
        initial_branch = self.current_branch
        final_answer = []
        while 1:
            self.input_data = self.input_data_template
            # Analize input and apply
            analysis = self.analyzer.analize(input_text)
            if analysis is not None:
                self.input_data["intents"] = analysis["intents"]
                self.input_data["entities"] = analysis["entities"]
            # If first step, set to begining
            if self.current_branch is None:
                self.current_branch = tree[0]
            # Remove / at the begining of current branch path
            branch_id = self.current_branch[1:]
            # Get text for current branch
            text = self.bot_script.get_text()[branch_id]
            # Feed logic with context, input data and text
            answer = self.bot_script.eval_logic(branch_id,
                                                self.context,
                                                self.input_data,
                                                text)
            # If eval, save text
            if answer["evaluate"]:
                final_answer += answer["text"]["es"]
                initial_branch = self.current_branch
            # If goto, continue
            if answer["evaluate"] and answer["goto"] is not None:
                self.current_branch = answer["goto"]
                initial_branch = self.current_branch
                continue
            # Avance step
            self.current_branch = self.walker.step(tree,
                                                   self.current_branch,
                                                   initial_branch)
            # If not eval and not goto, iterate again
            if not answer["evaluate"] and answer["goto"] is None:
                continue
            break
        return final_answer
