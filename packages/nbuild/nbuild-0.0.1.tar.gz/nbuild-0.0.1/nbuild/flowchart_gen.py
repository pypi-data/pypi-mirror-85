
"""
This module is optional and is only imported when
Project.write_flowcharts_to is invoked.
It depends on having graphviz installed
(python -m pip install --user graphviz)
and uses graphviz to generate deliverable/build/test
flowcharts given a Project.
"""

try:
    import graphviz # pylint: disable=import-error,unused-import
except Exception as e:
    from nbuild import util
    util.print_banner(
        "You need 'graphviz' installed to run Project.write_flowcharts_to",
        "Install using pip: python -m pip install --user graphviz"
    )
    raise e

from graphviz import Digraph

def write_flowcharts_to(project, directory):
    pass
