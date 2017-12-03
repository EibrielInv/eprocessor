import unittest
from core import Core
from load_bot import bot_script_loader
from tree_walker import tree_walker
from simple_analyzer import SimpleAnalyzer

if 0:
    class TestTreeWalker(unittest.TestCase):
        def setUp(self):
            self.walker = tree_walker()
            from test_values import test_tree
            self.test_tree = test_tree

        def test_simple(self):
            current_branch = "/0100_root"
            step_branch = self.walker.step(self.test_tree, current_branch)
            self.assertEqual(step_branch, "/0200_two")

        def test_with_depth(self):
            current_branch = "/0300_three/0100_one"
            step_branch = self.walker.step(self.test_tree, current_branch)
            self.assertEqual(step_branch, "/0300_three/0200_two")

        def test_branch_end(self):
            current_branch = "/0300_three/0200_two"
            step_branch = self.walker.step(self.test_tree, current_branch)
            self.assertEqual(step_branch, "/0200_two")

        def test_end(self):
            current_branch = self.test_tree[-1]
            step_branch = self.walker.step(self.test_tree, current_branch)
            self.assertEqual(step_branch, "/0200_two")

        def test_bifurcation_outside(self):
            current_branch = "/0300_three"
            initial_branch = "/0100_root"
            step_branch = self.walker.step(self.test_tree, current_branch)
            self.assertEqual(step_branch, "/0400_four")

        def test_bifurcation_inside(self):
            current_branch = "/0300_three"
            initial_branch = "/0300_three"
            step_branch = self.walker.step(self.test_tree,
                                           current_branch, initial_branch)
            self.assertEqual(step_branch, "/0300_three/0100_one")

        def test_bifurcation_leaving(self):
            current_branch = "/0300_three"
            initial_branch = "/0300_three/0100_one/0100_one_one"
            step_branch = self.walker.step(self.test_tree,
                                           current_branch, initial_branch)
            self.assertEqual(step_branch, "/0400_four")

        def test_bifurcation_jump(self):
            current_branch = "/0400_four"
            initial_branch = "/0200_two"
            step_branch = self.walker.step(self.test_tree,
                                           current_branch, initial_branch)
            self.assertEqual(step_branch, "/0500_five")


class TestScriptLoader(unittest.TestCase):
    def setUp(self):
        self.bot_loader = bot_script_loader()
        self.bot_loader.load("test_bot")
        from test_values import test_episodes
        self.test_episodes = test_episodes
        from test_values import test_interactions
        self.test_interactions = test_interactions

    def test_get_episodes(self):
        episodes = self.bot_loader.get_episodes()
        self.assertEqual(episodes, self.test_episodes)

    def test_get_interactions(self):
        interactions = self.bot_loader.get_interactions()
        for interaction in interactions:
            # Remove compiled code
            del(interactions[interaction]["logic"])
        self.assertEqual(interactions, self.test_interactions)

    if 0:
        def test_intents(self):
            intents = self.bot_loader.get_intents()
            self.assertEqual(intents, self.test_intents)

        def test_entities(self):
            entities = self.bot_loader.get_entities()
            self.assertEqual(entities, self.test_entities)

        def test_logic(self):
            input_data = self.test_input_data
            context = self.test_context
            text = self.bot_loader.get_text()["0100_root"]
            answer = self.bot_loader.eval_logic("0100_root",
                                                context, input_data, text)
            self.assertDictEqual(answer, self.test_answer)

if 0:
    class TestCore(unittest.TestCase):
        def setUp(self):
            self.bot_loader = bot_script_loader()
            self.bot_loader.load("test_bot")
            analyzer = SimpleAnalyzer(self.bot_loader)
            self.core = Core(self.bot_loader, analyzer)
            self.test_answer = [{'text': 'Esto es la raíz'}]

        def test_start(self):
            answer = self.core.iteration("one")
            self.assertEqual(answer, self.test_answer)


if __name__ == '__main__':
    unittest.main()
