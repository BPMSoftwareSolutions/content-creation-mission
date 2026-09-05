"""Include the production JavaScript scheduler's tests in the repository proof."""
import subprocess
import unittest

from infographic_contract import ROOT


class CircuitFlowTests(unittest.TestCase):
    def test_silver_ball_scheduler(self):
        result = subprocess.run(['node', '--test', 'scripts/circuit-flow.test.cjs'], cwd=ROOT,
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
