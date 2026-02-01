import unittest
import subprocess
import sys
import os
import shutil


class TestToCLI(unittest.TestCase):
    pkg = "tmp_test_pkg"

    def setUp(self):
        # cleanup any previous leftovers
        for d in (self.pkg, os.path.join("packages", self.pkg), os.path.join("vendor", self.pkg)):
            if os.path.isdir(d):
                shutil.rmtree(d)
        if os.path.exists("tombo_packages.txt"):
            os.remove("tombo_packages.txt")

    def test_init_publish_install_info_integrate(self):
        python = sys.executable
        # init
        proc = subprocess.run([python, "tools/to.py", "init", self.pkg], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(os.path.isdir(self.pkg))

        # publish
        proc = subprocess.run([python, "tools/to.py", "publish", self.pkg], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(os.path.isdir(os.path.join("packages", self.pkg)))

        # list
        proc = subprocess.run([python, "tools/to.py", "list"], capture_output=True, text=True)
        self.assertIn(self.pkg, proc.stdout)

        # install
        proc = subprocess.run([python, "tools/to.py", "install", self.pkg], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(os.path.isdir(os.path.join("vendor", self.pkg)))

        # info
        proc = subprocess.run([python, "tools/to.py", "info", self.pkg], capture_output=True, text=True)
        self.assertIn("name = \"", proc.stdout)

        # integrate
        proc = subprocess.run([python, "tools/to.py", "integrate", self.pkg], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(os.path.exists("tombo_packages.txt"))
        with open("tombo_packages.txt", "r", encoding="utf-8") as f:
            data = f.read()
        self.assertIn(os.path.abspath(os.path.join("vendor", self.pkg)), data)

    def tearDown(self):
        for d in (self.pkg, os.path.join("packages", self.pkg), os.path.join("vendor", self.pkg)):
            if os.path.isdir(d):
                shutil.rmtree(d)
        if os.path.exists("tombo_packages.txt"):
            os.remove("tombo_packages.txt")


if __name__ == '__main__':
    unittest.main()
