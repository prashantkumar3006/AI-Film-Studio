"""Repository conventions: skills, configs, secrets."""

import re
import unittest

from studio.orchestrator.config import _simple_yaml, load_config
from tests.helpers import REPO

SKILLS = REPO / ".claude" / "skills"


class Skills(unittest.TestCase):
    def test_every_skill_has_valid_frontmatter(self):
        folders = sorted(p for p in SKILLS.iterdir() if p.is_dir())
        self.assertGreaterEqual(len(folders), 30)
        for folder in folders:
            text = (folder / "SKILL.md").read_text(encoding="utf-8")
            match = re.match(r"^---\nname: (.+)\ndescription: (.+)\n---\n", text)
            self.assertIsNotNone(match, f"{folder.name}: missing frontmatter")
            self.assertEqual(match.group(1), folder.name)
            self.assertLessEqual(len(match.group(2)), 1024, folder.name)
            self.assertNotIn("<", match.group(2), folder.name)

    def test_claude_md_routes_to_existing_skills(self):
        text = (REPO / "CLAUDE.md").read_text(encoding="utf-8")
        for name in re.findall(r"`skill:([a-z0-9-]+)`", text):
            self.assertTrue((SKILLS / name / "SKILL.md").is_file(), f"CLAUDE.md routes to missing skill {name}")


class Config(unittest.TestCase):
    def test_config_parses_without_pyyaml(self):
        text = (REPO / "studio/config.yaml").read_text(encoding="utf-8")
        simple = _simple_yaml(text)
        import yaml

        self.assertEqual(simple, yaml.safe_load(text))
        config = load_config()
        self.assertEqual(config["render"]["fps"], 24)
        self.assertEqual(config["budget"]["per_episode_cap"], 5000)
        self.assertEqual(config["legal"]["mode"], "strict")

    def test_no_secrets_committed(self):
        pattern = re.compile(r"(api[_-]?key|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}", re.IGNORECASE)
        for path in REPO.rglob("*"):
            if ".git" in path.parts or "node_modules" in path.parts or not path.is_file() or path.suffix not in {".py", ".yaml", ".yml", ".json", ".md", ".env", ".example", ".ts", ".tsx"}:
                continue
            self.assertIsNone(pattern.search(path.read_text(encoding="utf-8", errors="ignore")), path)


if __name__ == "__main__":
    unittest.main()
