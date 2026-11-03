import json
import os
import re
import unittest

from _load import SKILL

MODULES = {"copycat": "edgar13f", "news": "news", "budget": "size", "pelosi": "ptr",
           "analyst": "facts", "screener": "screen", "risk": "check", "broker": "ticket",
           "tax": "lots", "alerts": "alerts", "rebalance": "rebalance"}


def read(*parts):
    with open(os.path.join(SKILL, *parts), encoding="utf-8") as fh:
        return fh.read()


class Skill(unittest.TestCase):
    def test_one_skill_with_frontmatter(self):
        text = read("SKILL.md")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        self.assertIsNotNone(m)
        self.assertIn("name: traiding\n", m.group(1) + "\n")
        self.assertIn("description: ", m.group(1))

    def test_every_module_has_guide_and_tool(self):
        self.assertEqual(sorted(d for d in os.listdir(SKILL)
                                if os.path.isdir(os.path.join(SKILL, d)) and d != "__pycache__"),
                         sorted(MODULES))
        text = read("SKILL.md")
        for mod, tool in MODULES.items():
            self.assertTrue(os.path.isfile(os.path.join(SKILL, mod, "GUIDE.md")), mod)
            self.assertTrue(os.path.isfile(os.path.join(SKILL, mod, tool + ".py")), mod)
            self.assertIn("`%s`" % mod, text, mod)
            self.assertFalse(read(mod, "GUIDE.md").startswith("---"), mod)

    def test_guides_point_inside_their_module(self):
        for mod in MODULES:
            guide = read(mod, "GUIDE.md")
            for ref in re.findall(r"\$\{CLAUDE_SKILL_DIR\}/([^\s\"`]+)", guide):
                path = os.path.join(SKILL, ref.rstrip("/"))
                self.assertTrue(os.path.exists(path), "%s: %s" % (mod, ref))
            self.assertNotRegex(guide, r"/trader-(%s)\b" % "|".join(MODULES), mod)

    def test_safety_rules(self):
        low = " ".join(read("SKILL.md").lower().split())
        self.assertIn("not financial advice", low)
        self.assertIn("yes", low)
        cfg = json.loads(read("budget", "config.example.json"))
        self.assertIs(cfg["paper"], True)
        self.assertIs(cfg.get("allow_options", False), False)


if __name__ == "__main__":
    unittest.main()
