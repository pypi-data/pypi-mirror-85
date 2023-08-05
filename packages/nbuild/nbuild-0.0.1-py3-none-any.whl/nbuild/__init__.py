
"""
The nbuild module provides functions which
model, build, test, and report the status
of any given project.
"""

import os
import sys
import subprocess
import platform
import tempfile
import shutil

from nbuild.project import Project
from nbuild.deliverable import Deliverable
from nbuild.build import BuildSystem
from nbuild.test import TestSystem

# Deliverable constructors
def src_directory(path):
    """Creates a "directory" Deliverable"""
    return Deliverable(_type="directory", path=path)

def src_file(path):
    """Creates a "file" Deliverable"""
    return Deliverable(_type="file", path=path)

def executable(path):
    """Creates a "file" Deliverable (identical to src_file, named to aid readability)"""
    return Deliverable(_type="file", path=path)

def git_repository(url, git_dir=None):
    """Creates a "git" Deliverable. Optional 2nd argument is a persistent directory to store git repo in."""
    return Deliverable(_type="git", url=url, git_dir=git_dir)

def physical_items(*items):
    """Creates an "items" Deliverable"""
    return Deliverable(_type="items", items=list(items))

# Build system constructors
def make(*args):
    """Creates a "make" BuildSystem, suitable for building c/c++ code"""
    return BuildSystem(_type="make", targets=list(args))

def npm_build(*args):
    """Creates a "npm" BuildSystem, suitable for building npm projects in javascript"""
    return BuildSystem(_type="npm", cmds=list(args))

def physical_prep(*steps):
    """Creates a "physical" BuildSystem, suitable for non-code setup procedures"""
    return BuildSystem(_type="physical", steps=list(steps))


# Test system constructors
def execute(*args):
    """Creates an "execute" TestSystem (tests receive output as string data)"""
    return TestSystem(
        _type="execute",
        exec_args=list(args)
    )

def npm_test(*args):
    """Creates an "npm" TestSystem (# TODO ensure all npm projects place test files in the same place)"""
    return TestSystem(_type="npm", cmds=list(args)).default_npm()

def physical_test(*steps):
    """
    Creates a "physical" TestSystem (steps are a list of tasks to perform during testing,
    with possible questions about system status along the way. Each task
    becomes one row in the output report.
    """
    return TestSystem(_type="physical", steps=list(steps)).default_physical()


# nbuild cares a great deal about it's public API;
# to prevent people from using/reading about internals they
# have no business using we explicitly define __all__,
# the behaviour of which is documented here: https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
__all__ = [
    # Classes
    'Project',
    'Deliverable',
    'BuildSystem',
    'TestSystem',

    # fns to create deliverables
    'src_directory',
    'src_file',
    'executable',
    'git_repository',
    'physical_items',
    
    # fns to create build/assembly instructions
    'make',
    'npm_build',
    'physical_prep',
    
    # fns to perform tests
    'execute',
    'npm_test',
    'physical_test',

]

# The __pdoc__ dictionary contains
# details for pdoc to respect when
# generating documentation.
# See https://pdoc3.github.io/pdoc/doc/pdoc/#overriding-docstrings-with-__pdoc__&gsc.tab=0
__pdoc__ = {
    'project': False,
    'deliverable': False,
    'build': False,
    'test': False,
    'http_test_server': False,
    'util': False,
    'flowchart_gen': False,
}



