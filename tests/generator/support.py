import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


class GeneratorTestCase(unittest.TestCase):
    def temporary_directory(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        return Path(directory.name)

    def write_fixture(self, content, name="fixture.txt"):
        path = self.temporary_directory() / name
        path.write_text(content, encoding="utf-8")
        return path
