import os
import unittest
from unittest.mock import patch

from core.openai_reasoner import OpenAIReasoner


class OpenAIReasonerTests(unittest.TestCase):
    def test_missing_key_is_reported(self):
        with patch.dict(os.environ, {}, clear=True):
            ok, message = OpenAIReasoner().available()
        self.assertFalse(ok)
        self.assertTrue(message)

    def test_empty_task_is_rejected_before_network(self):
        brain = OpenAIReasoner()
        with self.assertRaises(ValueError):
            brain.reason("   ")


if __name__ == "__main__":
    unittest.main()
