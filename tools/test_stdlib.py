import unittest
import subprocess
import sys
import os


class TestStdlibVerify(unittest.TestCase):
    def test_verify_implementation_runs(self):
        cmd = [sys.executable, "tools/verify_implementation.py"]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        out = proc.stdout + proc.stderr
        self.assertEqual(proc.returncode, 0, msg=f"verify_implementation failed:\n{out}")
        self.assertIn("ALL DOMAIN LIBRARIES SUCCESSFULLY IMPLEMENTED", out)


if __name__ == '__main__':
    unittest.main()
