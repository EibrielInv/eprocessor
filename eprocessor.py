import os
import sys
import js2py
import logging

from load_bot import bot_script_loader
from watson_sync import watson_sync
from config import Config

logging.basicConfig(filename='eprocessor.log',level=logging.DEBUG)

js_code_template = """
function (context, input_data, text) {{
    goto = null;
    skip = true;
    {code}
    returning = {{
        "context": context,
        "text": text,
        "goto": goto,
        "skip": skip
    }}
    return returning;
}}"""

bot_script_path = sys.argv[1]

bot_loader = bot_script_loader()
bot_script = bot_loader.load(bot_script_path)

watson_syncer = watson_sync(Config.WATSON_USERNAME, Config.WATSON_PASSWORD, "EibrielBot Processor (es)")
watson_syncer.watson_diff(bot_script)

lala()

# Traverse dialog tree

context = {
    "messenger": "telegram"
}
input_data_template = {
    "input_text": None,
    "intents": [],
    "entities": []
}
input_data = input_data_template
continue_loop = True
current_branch = None
input_text = None
watson_analysis = None
while continue_loop:
    if watson_analysis is not None:
        #print (watson_analysis)
        input_data["intents"] = watson_analysis["intents"]
        input_data["entities"] = watson_analysis["entities"]
    if current_branch is None:
        current_branch = tree_folders[1]
    depth_array = current_branch.split("/")
    branch_path = ""
    for depth_item in depth_array:
        if depth_item != "":
            branch_path = os.path.join(branch_path, depth_item)
    #print (branch_path)
    #os.exit()
    logic_path = os.path.join(tree_path, branch_path,"logic.js")
    text_path = os.path.join(tree_path, branch_path, "text")

    with open(logic_path, "r") as txt:
        js_code = js_code_template.format(code=txt.read())
        logic = js2py.eval_js(js_code)

    text = {}
    with open(text_path, "r") as txt:
        lang = None
        for line in txt:
            if line.startswith("es:"):
                lang = "es"
                text[lang] = []
                continue
            if line.strip() == "":
                continue
            text[lang].append(line.strip())

    answer = logic(context, input_data, text["es"])
    if not answer["skip"]:
        for msg in answer["text"]:
            print (msg)
    if answer["skip"] == True:
        current_branch = tree_folders[tree_folders.index(current_branch)+1]
        pass
    elif answer["goto"] is not None:
        current_branch = answer["goto"]
    else:
        current_branch = tree_folders[tree_folders.index(current_branch)+1]
        input_text = input("> ")
        input_data = input_data_template
        watson_analysis = conversation.message(
            workspace_id=workspace_id,
            message_input={
                'text': input_text
            }
        )
