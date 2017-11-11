import pprint
import logging
import watson_developer_cloud

class watson_sync:
    def __init__(self, username, password, workspace_name):
        # Get Watson Workspace
        self.conversation = watson_developer_cloud.ConversationV1(
            username = username,
            password = password,
            version = '2017-05-26'
        )
        watson_workspaces = self.conversation.list_workspaces()
        self.workspace_id = None
        for workspace in watson_workspaces["workspaces"]:
            if workspace["name"] == workspace_name:
                self.workspace_id = workspace["workspace_id"]
        # Logging
        self.pp = pprint.PrettyPrinter(indent=4)
        self.logger = logging.getLogger('watson_sync({})'.format(workspace_name))

    def watson_diff(self, bot_script):
        # Intents
        watson_intents = self.conversation.list_intents(
            workspace_id = self.workspace_id,
            export = True,
            page_limit=9999999
        )
        intents_to_add = []
        intents_to_remove = []
        intent_examples_to_add = []
        intent_examples_to_remove = []
        # Compare script_intents with watson_intents (to add)
        for script_intent in bot_script["intents"]:
            exists_intent = False
            for watson_intent in watson_intents["intents"]:
                if script_intent == watson_intent["intent"]:
                    exists_intent = True
                    for script_example in bot_script["intents"][script_intent]["default"]["es"]:
                        exists_example = False
                        for watson_example in watson_intent["examples"]:
                            if script_example["text"].lower() == watson_example["text"].lower():
                                exists_example = True
                        if exists_example:
                            pass
                        else:
                            intent_example_to_add = {
                                "intent_id": script_intent,
                                "text": script_example["text"]
                            }
                            intent_examples_to_add.append(intent_example_to_add)
            if exists_intent:
                pass
            else:
                intent_to_add = {
                    "intent_id": script_intent,
                    "intent_data": bot_script["intents"][script_intent]
                }
                intents_to_add.append(intent_to_add)
        # Compare watson_intents with script_intents (to remove)
        for watson_intent in watson_intents["intents"]:
            exists_intent = False
            for script_intent in bot_script["intents"]:
                if script_intent == watson_intent["intent"]:
                    exists_intent = True
                    for watson_example in watson_intent["examples"]:
                        exists_example = False
                        for script_example in bot_script["intents"][script_intent]["default"]["es"]:
                            if script_example["text"].lower() == watson_example["text"].lower():
                                exists_example = True
                        if exists_example:
                            pass
                        else:
                            intent_example_to_remove = {
                                "intent_id": watson_intent["intent"],
                                "text": watson_example["text"]
                            }
                            intent_examples_to_remove.append(intent_example_to_remove)
            if exists_intent:
                pass
            else:
                intent_to_remove = {
                    "intent_id": watson_intent["intent"],
                }
                intents_to_remove.append(intent_to_remove)
        self.logger.debug("intents_to_add:\n{}".format(self.pp.pformat(intents_to_add)))
        self.logger.debug("intent_examples_to_add:\n{}".format(self.pp.pformat(intent_examples_to_add)))
        self.logger.debug("intents_to_remove:\n{}".format(self.pp.pformat(intents_to_remove)))
        self.logger.debug("intent_examples_to_remove:\n{}".format(self.pp.pformat(intent_examples_to_remove)))

        # Return
        diff = {
            "intents_to_add": intents_to_add,
            "intent_examples_to_add": intent_examples_to_add,
            "intents_to_remove": intents_to_remove,
            "intent_examples_to_remove": intent_examples_to_remove,
        }
        self.sync_intents(diff)
        return diff


    def sync_intents(self, diff):
        for intent in diff["intents_to_add"]:
            response = self.conversation.create_intent(
                workspace_id = self.workspace_id,
                intent = intent["intent_id"],
                examples = intent["intent_data"]["default"]["es"]
            )
        for intent in diff["intents_to_remove"]:
            response = self.conversation.create_intent(
                workspace_id = self.workspace_id,
                intent = intent["intent_id"],
            )
        for intent_example in diff["intent_examples_to_add"]:
            response = self.conversation.create_example(
                workspace_id = self.workspace_id,
                intent = intent_example["intent_id"],
                text = intent_example["text"]
            )
        for intent_example in diff["intent_examples_to_remove"]:
            response = self.conversation.delete_example(
                workspace_id = self.workspace_id,
                intent = intent_example["intent_id"],
                text = intent_example["text"]
            )
