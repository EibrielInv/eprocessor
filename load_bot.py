import os
import js2py
import pprint
import logging

class MissingLanguage(Exception):
    pass

class bot_script_loader:
    def __init__(self):
        # Logging
        self.pp = pprint.PrettyPrinter(indent=4)
        self.logger = logging.getLogger('bot_script_loader')
        with open("template.js", "r") as txt:
            self.js_code_template = txt.read()

    def get_tree_files_(self, path, folder=""):
        """Return object of files on dir."""
        nodes = []
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                nodes = nodes + self.get_tree_files_(entry.path, "{}/{}".format(folder, entry.name))
        nodes.append(folder)
        return sorted(nodes)

    def get_intents_files_(self, path):
        """Return file lis on directory"""
        nodes = []
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                nodes += self.get_intents_files_(entry.path)
            else:
                nodes.append(entry.name)
        return sorted(nodes)

    def get_entities_files_(self, path, folder=[]):
        """Return file lis on directory"""
        nodes = []
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                nodes += self.get_entities_files_(entry.path, folder+[entry.name])
            else:
                path_string = ""
                for item in folder:
                    path_string = os.path.join(path_string, item)
                path_string = os.path.join(path_string, entry.name)
                nodes.append(path_string)
        return sorted(nodes)

    def text_reader_(self, txt, txt_path):
        items = {}
        title = "default"
        lang = None
        items[title] = {}
        for line in txt:
            if line.startswith("#"):
                # Is a comment
                continue
            if line.strip() == "":
                # Is an empty line
                continue
            if line.startswith("set_title:"):
                title = line[10:].strip()
                items[title] = {}
                lang = None
                continue
            if line.startswith("set_lang:"):
                lang = line[9:].strip()
                items[title][lang] = []
                continue
            if lang is None:
                raise MissingLanguage("Missing language on file {}".format(txt_path))
            item = {
                "text": line.strip()
            }
            items[title][lang].append(item)
        return items

    def load_text_file(self, text_path):
        with open(text_path, "r") as txt:
            return self.text_reader_(txt, text_path)

    def get_tree(self):
        return self.bot_script_["tree"]

    def get_intents(self):
        return self.bot_script_["intents"]

    def get_entities(self):
        return self.bot_script_["entities"]

    def get_text(self):
        return self.bot_script_["text"]

    def get_logic(self):
        return self.bot_script_["logic_eval"]

    def eval_logic(self, branch, context, input_data, text):
        answer = self.bot_script_["logic_eval"][branch](context, input_data, text)
        answer = answer.to_dict()
        return answer

    def load(self, bot_script_path):
        tree_path = os.path.join(bot_script_path, "tree")
        tree_folders = self.get_tree_files_(tree_path)[1:]
        intents_path = os.path.join(bot_script_path, "intents")
        intents_files = self.get_intents_files_(intents_path)
        entities_path = os.path.join(bot_script_path, "entities")
        entities_files = self.get_entities_files_(entities_path)
        self.tree_path = tree_path
        self.tree_folders = tree_folders

        intents_data = {}
        for inf in intents_files:
            intent_path = os.path.join(intents_path, inf)
            intents_data[inf] = self.load_text_file(intent_path)

        entities_data = {}
        for inf in entities_files:
            intent_path = os.path.join(entities_path, inf)
            head = None
            tail = inf
            inf_splitted = []
            while head != "":
                tail, head = os.path.split(tail)
                if head != "":
                    inf_splitted.append(head)
            if not inf_splitted[-1] in entities_data:
                entities_data[inf_splitted[-1]] = {}
            entities_data[inf_splitted[-1]][inf_splitted[-2]] = self.load_text_file(intent_path)

        logic_code_data = {}
        logic_eval_data = {}
        text_data = {}
        for branch_path in tree_folders:
            # Removing starting /
            # Otherwise os.path.join will interpret that as an absolute path
            branch_path = branch_path[1:]
            logic_path = os.path.join(tree_path, branch_path, "logic.js")
            if os.path.isfile(logic_path):
                with open(logic_path, "r") as txt:
                    js_code = self.js_code_template.replace("/*code*/", txt.read())
                    logic_code_data[branch_path] = js_code
                    logic = js2py.eval_js(js_code)
                    logic_eval_data[branch_path] = logic
            text_path = os.path.join(tree_path, branch_path, "text")
            if os.path.isfile(text_path):
                with open(text_path, "r") as txt:
                    text = self.text_reader_(txt, text_path)
                    text_data[branch_path] = text

        if False:
            self.logger.debug("tree:\n{}".format(self.pp.pformat(tree_folders)))
            self.logger.debug("intents:\n{}".format(self.pp.pformat(intents_data)))
            self.logger.debug("entities:\n{}".format(self.pp.pformat(entities_data)))

        self.bot_script_ = {
            "tree": tree_folders,
            "intents": intents_data,
            "entities": entities_data,
            "logic_code": logic_code_data,
            "logic_eval": logic_eval_data,
            "text": text_data
        }
        return True
