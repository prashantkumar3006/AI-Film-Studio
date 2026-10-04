"""Regression tests for the engine bugs fixed in this restructure."""

import json
import re
import unittest

from tests.helpers import REPO, RepoCopy


class WorkflowDependencyOrder(unittest.TestCase):
    def test_dependencies_only_point_to_earlier_tasks(self):
        workflow = json.loads((REPO / "scripts/workflows/production_pipeline.json").read_text())
        created = 0
        for step in workflow["steps"]:
            args = step.get("args", [])
            if "task-add" not in args:
                continue
            created += 1
            if "--depends-on" in args:
                for dep in args[args.index("--depends-on") + 1].split(","):
                    number = int(re.match(r"TASK_(\d+)", dep).group(1))
                    self.assertLess(number, created, f"{step['name']} depends on {dep}, which is not created yet")

    def test_ai_workflow_references_existing_scripts(self):
        workflow = json.loads((REPO / "scripts/workflows/ai_generation_pipeline.json").read_text())
        for step in workflow["steps"]:
            for arg in step.get("args", []):
                if arg.startswith("{{REPO_ROOT}}/"):
                    self.assertTrue((REPO / arg.replace("{{REPO_ROOT}}/", "")).is_file(), arg)


class EngineRuns(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = RepoCopy()
        cls.repo.run("scripts/create_project.py", "init", "--title", "Pilot", "--type", "animation", check=True)
        cls.state_path = cls.repo.root / "projects/PROJECT_2026_001/pilot/00_admin/.studio/state.json"
        if not cls.state_path.exists():  # year-dependent id
            cls.state_path = next(cls.repo.root.glob("projects/*/pilot/00_admin/.studio/state.json"))
        cls.project_id = cls.state_path.parents[3].name

    @classmethod
    def tearDownClass(cls):
        cls.repo.cleanup()

    def test_production_pipeline_executes_and_keeps_tasks(self):
        done = self.repo.run("scripts/create_project.py", "workflow-run", self.project_id, "pilot", "--workflow", "scripts/workflows/production_pipeline.json", "--execute")
        self.assertEqual(done.returncode, 0, done.stderr)
        state = json.loads(self.state_path.read_text())
        self.assertEqual(len(state["tasks"]), 22, "tasks created by workflow steps must survive the run record save")
        self.assertEqual(state["workflow_runs"][-1]["status"], "COMPLETE")
        ids = [t["id"] for t in state["tasks"]]
        for task in state["tasks"]:
            for dep in task["dependencies"]:
                self.assertLess(ids.index(dep), ids.index(task["id"]))

    def test_ai_workflow_reports_missing_variables(self):
        done = self.repo.run("scripts/create_project.py", "workflow-run", self.project_id, "pilot", "--workflow", "scripts/workflows/ai_generation_pipeline.json", "--execute")
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("Missing environment variables: SHOT_ID, PROMPT_ID, MODEL_ID", done.stderr + done.stdout)
        state = json.loads(self.state_path.read_text())
        self.assertEqual(state["workflow_runs"][-1]["status"], "FAILED")

    def test_ai_workflow_resolves_variables_from_environment(self):
        env ={"SHOT_ID": "SHOT_X", "PROMPT_ID": "PROMPT_X", "MODEL_ID": "animagine_xl_4"}
        done = self.repo.run("scripts/create_project.py", "workflow-run", self.project_id, "pilot", "--workflow", "scripts/workflows/ai_generation_pipeline.json", env=env)
        self.assertEqual(done.returncode, 0, done.stderr)
        report = json.loads(done.stdout)
        joined = json.dumps(report)
        self.assertNotIn("{{SHOT_ID}}", joined)
        self.assertIn("SHOT_X", joined)
        self.assertIn("09_ai-generation/selected/SHOT_X_v001", joined)
        self.assertFalse(any(r.get("unresolved") for r in report["results"]))


if __name__ == "__main__":
    unittest.main()
