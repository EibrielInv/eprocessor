import os

from config import Config
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
        self.continue_loop = True
        self.current_branch = None
        self.input_text = None
        self.analysis = None
        self.bot_script = bot_script
        self.analyzer = analyzer

    def iteration(self, input_text):
        initial_branch = self.current_branch
        current_branch = self.walker.step(self.bot_script.get_tree(),
                                          self.current_branch, initial_branch)

        self.input_data = self.input_data_template
        analysis = self.analyzer.analize(input_text)

        if analysis is not None:
            # print (watson_analysis)
            self.input_data["intents"] = analysis["intents"]
            self.input_data["entities"] = analysis["entities"]
        if current_branch is None:
            current_branch = bot_script["tree"][0]
            initial_branch = None
        depth_array = current_branch.split("/")
        branch_path = ""
        for depth_item in depth_array:
            if depth_item != "":
                branch_path = os.path.join(branch_path, depth_item)

        text = self.bot_script.get_text()[branch_path]
        answer = self.bot_script.eval_logic(branch_path,
                                            self.context,
                                            self.input_data,
                                            text)
        if answer["evaluate"] is False:
            initial_branch = None
            current_branch = walker.step(bot_script["tree"],
                                         current_branch, initial_branch)
            pass
        elif answer["goto"] is not None:
            current_branch = answer["goto"]

        return answer["text"]["es"]
