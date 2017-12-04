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
        self.current_episode = None
        self.current_episode_id = None
        self.current_scene = None
        self.current_scene_id = None
        self.current_cut = None
        self.current_cut_id = None
        self.bot_script = bot_script
        self.analyzer = analyzer

        self.episodes_id_n = 0
        self.scenes_id_n = 0
        self.cuts_id_n = 0

        self.episodes_ids_count = 0
        self.scenes_ids_count = 0
        self.cuts_ids_count = 0

        self.first_time = True
        self.last_interaction = None

    def iteration(self, input_text):
        final_answer = []
        while 1:
            if input_text is not None:
                self.input_data = self.input_data_template
                # Analize input and apply
                analysis = self.analyzer.analize(input_text)
                input_text = None
                if analysis is not None:
                    self.input_data["interactions"] = analysis["interactions"]
                interactions = self.bot_script.get_interactions()
                if len(analysis["interactions"]) > 0:
                    interaction = analysis["interactions"][0]["interaction"]
                    answers = interactions[interaction]["answers"][0]
                    print(self.current_cut_id)
                    answer = interactions[interaction]["logic"](
                                                        self.last_interaction,
                                                        self.current_cut_id)

                    answer_id = answer["answer_id"]
                    if answer_id is not None:
                        answer_txt = answers[
                            "answer_id:{}".format(answer_id)][
                                "lang_id:es"]["text"][0]
                        final_answer.append([answer_txt])
                        self.last_interaction = interaction
                        if answer["pause"]:
                            break

            # If first step, set to begining
            if not self.first_time:
                self.cuts_id_n += 1
                if self.cuts_id_n >= self.cuts_ids_count:
                    self.scenes_id_n += 1
                    self.cuts_id_n = 0
                if self.scenes_id_n >= self.scenes_ids_count:
                    self.episodes_ids_count += 1
                    self.scenes_id_n = 0
            else:
                self.first_time = False

            episodes, episodes_ids = self.bot_script.get_episodes()
            self.current_episode_id = episodes_ids[self.episodes_id_n]
            self.current_episode = episodes[self.current_episode_id]
            self.current_scene_id = \
                self.current_episode["scenes_ids"][self.scenes_id_n]
            scene_id = self.current_scene_id
            self.current_scene = self.current_episode["scenes"][scene_id]
            self.current_cut_id = \
                self.current_scene["cuts_ids"][self.cuts_id_n]
            cut_id = "cut_id:{}".format(self.current_cut_id)
            self.current_cut = self.current_scene["cuts"][cut_id]
            #
            self.episodes_ids_count = len(episodes_ids)
            self.scenes_ids_count = len(self.current_episode["scenes_ids"])
            self.cuts_ids_count = len(self.current_scene["cuts_ids"])

            final_answer.append(self.current_cut["lang_id:es"]["text"])
            if "[user_input]" in final_answer[-1]:
                break
        return final_answer
