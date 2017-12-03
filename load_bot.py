import os
import js2py
import pprint
import logging


class bot_script_loader:
    def __init__(self):
        # Logging
        self.pp = pprint.PrettyPrinter(indent=4)
        self.logger = logging.getLogger('bot_script_loader')
        with open("template.js", "r") as txt:
            self.js_code_template = txt.read()

    def is_line_command_(self, line):
        """Returns de command name, otherwise returns False"""
        commands = [
            "cut_id",
            "lang_id",
            "answer_id"
        ]
        ordered_commands = [
            "cut_id",
            "answer_id"
        ]
        for command in commands:
            if line.startswith(command):
                value = str(line[len(command)+1:]).strip()
                ordered = command in ordered_commands
                return command, value, ordered
        return False

    def set_to_dict(self, dict_, keys, value, empty_line):
        tmp_dict = dict_
        count = 0
        for key in keys:
            if key not in tmp_dict:
                tmp_dict[key] = {}
            if count == len(keys)-1:
                if "text" in tmp_dict[key]:
                    if empty_line:
                        tmp_dict[key]["text"].append(value)
                    else:
                        tmp_dict[key]["text"][-1] += " " + value
                else:
                    tmp_dict[key] = {"text": [value]}
            else:
                tmp_dict = tmp_dict[key]
            count += 1

    def text_reader_(self, txt_path):
        """Loads text files data"""
        levels = []
        levels_values = []
        data = {}
        command_values = {}
        txt = []
        ordered_ids = []
        empty_line = False
        with open(txt_path, "r") as txt_lines:
            for line in txt_lines:
                txt.append(line)
        for line in txt:
            if line.startswith("#"):
                # Is a comment
                continue
            if line.strip() == "":
                # Is an empty line
                empty_line = True
                continue
            is_line_command = self.is_line_command_(line)
            # If the line contains a command
            if is_line_command is not False:
                line_command, value, ordered = is_line_command
                if ordered:
                    ordered_ids.append(value)
                command_values[line_command] = value
                command_value = "{}:{}".format(line_command,
                                               command_values[line_command])
                if line_command in levels:
                    level_list_index = levels.index(line_command)
                    del(levels[level_list_index:])
                    del(levels_values[level_list_index:])
                    levels.append(line_command)
                    levels_values.append(command_value)
                else:
                    levels.append(line_command)
                    levels_values.append(command_value)
                continue
            # If the line is text add to data
            self.set_to_dict(data, levels_values, line.strip(), empty_line)
            empty_line = False
        return data, ordered_ids

    def get_scenes_(self, path):
        scenes = {}
        scenes_ids = []
        for entry in os.scandir(path):
            if not entry.is_dir(follow_symlinks=False):
                cuts, cuts_ids = self.text_reader_(entry.path)
                scene = {
                    "scene_id": entry.name,
                    "cuts": cuts,
                    "cuts_ids": cuts_ids
                }
                scenes[entry.name] = scene
                scenes_ids.append(entry.name)
        scenes_ids.sort()
        return scenes, scenes_ids

    def get_episodes_(self, path):
        episodes = {}
        episodes_ids = []
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                scenes, scenes_ids = self.get_scenes_(entry.path)
                episode = {
                    "episode_id": entry.name,
                    "scenes": scenes,
                    "scenes_ids": scenes_ids
                }
                episodes[entry.name] = episode
                episodes_ids.append(entry.name)
        episodes_ids.sort()
        return episodes, episodes_ids

    def get_interactions_(self, path):
        interactions = {}
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                answers_path = os.path.join(entry.path, "answers")
                examples_path = os.path.join(entry.path, "examples")
                logic_path = os.path.join(entry.path, "logic.js")
                if os.path.isfile(logic_path):
                    with open(logic_path, "r") as txt:
                        partial_code = txt.read()
                        js_code = self.js_code_template.replace("/*code*/",
                                                                partial_code)
                        logic = js2py.eval_js(js_code)
                interaction = {
                    "interaction_id": entry.name,
                    "answers": self.text_reader_(answers_path),
                    "examples": self.text_reader_(examples_path),
                    "logic_code": partial_code,
                    "logic": logic,
                }
                interactions[entry.name] = interaction
        return interactions

    def load(self, bot_script_path):
        episodes_path = os.path.join(bot_script_path, "episodes")
        episodes, episodes_ids = self.get_episodes_(episodes_path)
        interactions_path = os.path.join(bot_script_path, "interactions")
        interactions = self.get_interactions_(interactions_path)
        self.bot_script_ = {
            "episodes": episodes,
            "episodes_ids": episodes_ids,
            "interactions": interactions
        }
        return True

    def get_episodes(self):
        return self.bot_script_["episodes"], self.bot_script_["episodes_ids"]

    def get_interactions(self):
        return self.bot_script_["interactions"]
