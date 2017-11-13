test_tree = [
    "/0100_root",
    "/0200_two",
    "/0300_three",
    "/0300_three/0100_one",
    "/0300_three/0100_one/0100_one_one",
    "/0300_three/0200_two",
    "/0400_four",
    "/0500_five"
]

test_intents = {
    'one': {
        'default': {
            'en': [{'text': 'one'}],
            'es': [{'text': 'uno'}]}
        },
    'two': {
        'default': {
            'en': [{'text': 'two'}],
            'es': [{'text': 'dos'}]}
        },
    'three': {
        'default': {
            'en': [{'text': 'three'}],
            'es': [{'text': 'tres'}]}
        },
    'four': {
        'default': {
            'en': [{'text': 'four'}],
            'es': [{'text': 'cuatro'}]}
        },
    'five': {
        'default': {
            'en': [{'text': 'five'}],
            'es': [{'text': 'cinco'}]}
        }
    }

test_entities = {
    'animals': {
        'cat': {
            'default': {
                    'en': [{'text': 'cat'}, {'text': 'cats'}],
                    'es': [{'text': 'gato'}, {'text': 'gatos'}]
                }
            },
        'dog': {
            'default': {
                    'en': [{'text': 'dog'}, {'text': 'dogs'}],
                    'es': [{'text': 'perro'}, {'text': 'perros'}]
                }
            }
        }
    }

test_context = {
    "messenger": "telegram"
}

test_input_data = {
    "input_text": None,
    "intents": [],
    "entities": []
}

test_answer = {
    'text': {'es': [{'text': 'Esto es la raíz'}],
             'en': [{'text': 'This is the root'}]},
    'evaluate': True,
    'context': {'messenger': 'telegram'},
    'goto': None
}
