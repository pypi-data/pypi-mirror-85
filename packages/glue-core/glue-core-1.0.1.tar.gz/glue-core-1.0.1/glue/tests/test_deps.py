import sys
from subprocess import check_call

from glue.tests.helpers import requires_qt

from .._deps import Dependency, categories


class TestDependency(object):

    def test_installed(self):
        d = Dependency('math', 'the math module')
        assert d.installed

    def test_uninstalled(self):
        d = Dependency('asdfasdf', 'Non-existent module')
        assert not d.installed

    def test_installed_str(self):
        d = Dependency('math', 'info')
        assert str(d) == "                math:\tINSTALLED (unknown version)"

    def test_noinstalled_str(self):
        d = Dependency('asdfasdf', 'info')
        assert str(d) == "            asdfasdf:\tMISSING (info)"

    def test_failed_str(self):
        d = Dependency('asdfasdf', 'info')
        d.failed = True
        assert str(d) == "            asdfasdf:\tFAILED (info)"


@requires_qt
def test_optional_dependency_not_imported():
    """
    Ensure that a GlueApplication instance can be created without
    importing any non-required dependency
    """
    optional_deps = categories[5:]
    deps = [dep.module for cateogry, deps in optional_deps for dep in deps]

    code = """
class ImportDenier(object):
    __forbidden = set(%s)

    def find_module(self, mod_name, pth=None):
        if pth:
            return
        if mod_name in self.__forbidden:
            return self

    def load_module(self, mod_name):
        raise ImportError("Importing %%s" %% mod_name)

import sys
sys.meta_path.append(ImportDenier())

from glue.app.qt import GlueApplication
from glue.core import data_factories
ga = GlueApplication()
""" % deps

    cmd = [sys.executable, '-c', code]
    check_call(cmd)
