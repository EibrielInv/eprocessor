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
                            if script_example["text"] == watson_example["text"]:
                                exists_example = True
                        if exists_example:
                            pass
                        else:
                            intent_examples_to_add.append([script_intent, script_example])
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
                            if script_example["text"] == watson_example["text"]:
                                exists_example = True
                        if exists_example:
                            pass
                        else:
                            intent_examples_to_remove.append([watson_intent, watson_example])
            if exists_intent:
                pass
            else:
                intents_to_remove.append(watson_intent)
        self.logger.debug("intents_to_add:\n{}".format(self.pp.pformat(intents_to_add)))
        self.logger.debug("intent_examples_to_add:\n{}".format(self.pp.pformat(intent_examples_to_add)))
        self.logger.debug("intents_to_remove:\n{}".format(self.pp.pformat(intents_to_remove)))
        self.logger.debug("intent_examples_to_remove:\n{}".format(self.pp.pformat(intent_examples_to_remove)))

        # Entities
        if 0:
            watson_entities = self.conversation.list_entities(
                workspace_id = self.workspace_id,
                export = True,
                page_limit=9999999
            )
            entities_to_add = []
            entities_to_remove = []
            entity_values_to_add = []
            entity_values_to_remove = []
            # Compare script_entities with watson_entities (to add)
            for script_entity in bot_script["entities"]:
                exists_entity = False
                for watson_entity in watson_entities["entities"]:
                    if script_entity == watson_entity["entity"]:
                        exists_entity = True
                        for script_value in bot_script["entities"][script_entity]:
                            exists_value = False
                            for watson_value in watson_entity["values"]:
                                if script_value == watson_value["metadata"]: # ID stored on Metadata
                                    exists_value = True
                            if exists_value:
                                pass
                            else:
                                entity_values_to_add.append([script_entity, script_value])
                if exists_entity:
                    pass
                else:
                    entity_to_add = {
                        "entity_id": script_entity,
                        "data": bot_script["entities"][script_entity]
                    }
                    entities_to_add.append(entity_to_add)
            # Compare watson_entities with script_entities (to remove)
            for watson_entity in watson_entities["entities"]:
                exists_entity = False
                for script_entity in bot_script["entities"]:
                    if script_entity == watson_entity["entity"]:
                        exists_entity = True
                        for watson_value in watson_entity["values"]:
                            exists_value = False
                            for script_value in bot_script["entities"][script_entity]:
                                if script_value == watson_value["value"]:
                                    exists_value = True
                            if exists_value:
                                pass
                            else:
                                entity_values_to_remove.append([watson_entity, watson_value])
                if exists_entity:
                    pass
                else:
                    entities_to_remove.append(watson_entity)
            self.logger.debug("entities_to_add:\n{}".format(self.pp.pformat(entities_to_add)))
            self.logger.debug("entity_values_to_add:\n{}".format(self.pp.pformat(entity_values_to_add)))
            self.logger.debug("entities_to_remove:\n{}".format(self.pp.pformat(entities_to_remove)))
            self.logger.debug("entity_values_to_remove:\n{}".format(self.pp.pformat(entity_values_to_remove)))

        # Return
        diff = {
            "intents_to_add": intents_to_add,
            "intent_examples_to_add": intent_examples_to_add,
            "intents_to_remove": intents_to_remove,
            "intent_examples_to_remove": intent_examples_to_remove,
            #"entities_to_add": entities_to_add,
            #"entities_to_remove": entities_to_remove,
            #"entity_values_to_add": entity_values_to_add,
            #"entity_values_to_remove": entity_values_to_remove
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

    #def sync_entities(self, diff):
    #    for entity in diff["entities_to_add"]:
    #        values = []
    #        for value in entity["data"]:
    #
    #            value = {
    #                "value": value, #main concept
    #                "metadata": {"value_id": value},
    #                "synonyms": []
    #            }
    #            values.append(value)
    #        response = self.conversation.create_entity(
    #            workspace_id = self.workspace_id,
    #            entity = entity["name"],
    #            values = values
    #        )
