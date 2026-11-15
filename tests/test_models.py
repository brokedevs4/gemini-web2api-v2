"""Test model resolution and thinking level mappings."""
import unittest
from gemini_web2api.models import MODELS, resolve_model, REASONING_EFFORT_MAP


class TestModels(unittest.TestCase):
    def test_ui_models_present(self):
        # 1. Everyday help: 4 Hydrogen
        self.assertIn("gemini-4-hydrogen", MODELS)
        self.assertEqual(MODELS["gemini-4-hydrogen"]["mode"], 1)

        # 2. Code & analysis: 4 Argon
        self.assertIn("gemini-4-argon", MODELS)
        self.assertEqual(MODELS["gemini-4-argon"]["mode"], 2)
        self.assertEqual(MODELS["gemini-4-argon"]["think"], 0)

        # 3. Detailed research: 3.1 Pro
        self.assertIn("gemini-3.1-pro", MODELS)
        self.assertEqual(MODELS["gemini-3.1-pro"]["mode"], 3)

        # 4. Quick answers: 3.5 Flash-Lite
        self.assertIn("gemini-3.5-flash-lite", MODELS)
        self.assertEqual(MODELS["gemini-3.5-flash-lite"]["mode"], 6)

    def test_aliases_resolution(self):
        # Everyday aliases
        for alias in ["gemini-hydrogen", "gemini-everyday", "gemini-4-everyday"]:
            name, mode, think, err, _ = resolve_model(alias)
            self.assertIsNone(err)
            self.assertEqual(mode, 1)

        # Argon / Code aliases
        for alias in ["gemini-argon", "gemini-code", "gemini-4-code"]:
            name, mode, think, err, _ = resolve_model(alias)
            self.assertIsNone(err)
            self.assertEqual(mode, 2)
            self.assertEqual(think, 0)

        # Pro / Research aliases
        for alias in ["gemini-pro", "gemini-research"]:
            name, mode, think, err, _ = resolve_model(alias)
            self.assertIsNone(err)
            self.assertEqual(mode, 3)

        # Flash-Lite / Quick aliases
        for alias in ["gemini-flash-lite", "gemini-quick"]:
            name, mode, think, err, _ = resolve_model(alias)
            self.assertIsNone(err)
            self.assertEqual(mode, 6)

    def test_think_suffix_override(self):
        # @think=0 (deep)
        name, mode, think, err, _ = resolve_model("gemini-4-hydrogen@think=0")
        self.assertIsNone(err)
        self.assertEqual(name, "gemini-4-hydrogen")
        self.assertEqual(think, 0)

        # @think=2 (medium)
        name, mode, think, err, _ = resolve_model("gemini-4-argon@think=2")
        self.assertIsNone(err)
        self.assertEqual(name, "gemini-4-argon")
        self.assertEqual(think, 2)

        # @think=invalid
        name, mode, think, err, _ = resolve_model("gemini-4-argon@think=abc")
        self.assertIsNotNone(err)

    def test_reasoning_effort_parameter(self):
        # high -> 0
        name, mode, think, err, _ = resolve_model("gemini-4-hydrogen", reasoning_effort="high")
        self.assertIsNone(err)
        self.assertEqual(think, 0)

        # medium -> 2
        name, mode, think, err, _ = resolve_model("gemini-4-hydrogen", reasoning_effort="medium")
        self.assertIsNone(err)
        self.assertEqual(think, 2)

        # low -> 4
        name, mode, think, err, _ = resolve_model("gemini-4-argon", reasoning_effort="low")
        self.assertIsNone(err)
        self.assertEqual(think, 4)

    def test_unknown_model_fallback(self):
        name, mode, think, err, _ = resolve_model("nonexistent-model-xyz")
        self.assertIsNone(err)
        self.assertEqual(name, "gemini-4-hydrogen")
        self.assertEqual(mode, 1)


if __name__ == "__main__":
    unittest.main()
