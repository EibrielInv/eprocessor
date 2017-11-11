import os
import pprint
import logging

class MissingLanguage(Exception):
    pass

class bot_script_loader:
    def __init__(self):
        # Logging
        self.pp = pprint.PrettyPrinter(indent=4)
        self.logger = logging.getLogger('bot_script_loader')

    def get_tree_files(self, path, folder=""):
        """Return object of files on dir."""
        nodes = []
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                nodes = nodes + self.get_tree_files(entry.path, "{}/{}".format(folder, entry.name))
        nodes.append(folder)
        return sorted(nodes)

    def get_intents_files(self, path):
        """Return file lis on directory"""
        nodes = []
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                nodes += self.get_intents_files(entry.path)
            else:
                nodes.append(entry.name)
        return sorted(nodes)

    def get_entities_files(self, path, folder=[]):
        """Return file lis on directory"""
        nodes = []
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                nodes += self.get_entities_files(entry.path, folder+[entry.name])
            else:
                path_string = ""
                for item in folder:
                    path_string = os.path.join(path_string, item)
                path_string = os.path.join(path_string, entry.name)
                nodes.append(path_string)
        return sorted(nodes)

    def text_reader(self, txt, txt_path):
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
            return self.text_reader(txt, text_path)

    def load(self, bot_script_path):
        tree_path = os.path.join(bot_script_path, "tree")
        tree_folders = self.get_tree_files(tree_path)
        intents_path = os.path.join(bot_script_path, "intents")
        intents_files = self.get_intents_files(intents_path)
        entities_path = os.path.join(bot_script_path, "entities")
        entities_files = self.get_entities_files(entities_path)

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

        if False:
            self.logger.debug("tree:\n{}".format(self.pp.pformat(tree_folders)))
            self.logger.debug("intents:\n{}".format(self.pp.pformat(intents_data)))
            self.logger.debug("entities:\n{}".format(self.pp.pformat(entities_data)))

        bot_script = {
            "tree": tree_folders,
            "intents": intents_data,
            "entities": entities_data
        }
        return bot_script
