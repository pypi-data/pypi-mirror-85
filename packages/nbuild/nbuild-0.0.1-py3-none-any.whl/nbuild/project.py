
"""
The project module holds the Project class.
"""


import os

from nbuild.deliverable import Deliverable
from nbuild.build import BuildSystem
from nbuild.test import TestSystem
from nbuild.http_test_server import run_http_server

class Project:
    """
    The Project class represents one project,
    and is constructed with the project's:

     - Name
     - Input Deliverables
     - Build System (optional)
     - Output Deliverables (optional)
     - Test System

    once constructed the project
    may be built, tested, and reports generated
    in any given directory.
    """
    def __init__(
        self,
        name="Unnamed Project",
        deliverables_in=None,
        build_system=BuildSystem(_type="none"),
        deliverables_out=None,
        test_system=None,
    ):
        self.name = name
        
        if not isinstance(deliverables_in, (Deliverable)):
            raise Exception("deliverables_in must be a Deliverable")
        self.deliverables_in = deliverables_in

        if not isinstance(build_system, (BuildSystem)):
            raise Exception("build_system must be a BuildSystem")
        self.build_system = build_system
        self.build_system.project = self

        if deliverables_out is None:
            deliverables_out = self.deliverables_in
        if not isinstance(deliverables_out, (Deliverable)):
            raise Exception("deliverables_out must be a Deliverable")
        self.deliverables_out = deliverables_out

        if not isinstance(test_system, (TestSystem)):
            raise Exception("test_system must be a TestSystem")
        self.test_system = test_system
        self.test_system.project = self
    
    def run_test_server(self, port=8080):
        """
        Runs a self-serve webpage where deliverables
        may be uploaded and reports downloaded.
        """
        run_http_server(self, port=port)

    def build(self):
        """Instructs the build system to perform a build (defaults to nothing)"""
        self.build_system.build(self)

    def test(self):
        """Instructs the test system to test the project"""
        self.test_system.test(self)
    
    def write_flowcharts_to(self, directory):
        """Instructs the build and test system to use graphviz to generate a flowchart for the entire project"""
        from nbuild.flowchart_gen import write_flowcharts_to # pylint: disable=import-outside-toplevel
        write_flowcharts_to(self, directory)


    def write_reports_to(self, directory):
        """Creates and fills a directory with report files (usually .html)"""
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.test_system.write_reports_to(self, directory)

    def open_reports(self):
        """Opens any generated reports in their default applications (browser for .html, adobe for .pdf, etc.)"""
        self.test_system.open_reports()

    # Utilities for build + test systems to use,
    # answers common questions about projects.

    def get_cwd(self):
        """Asks the input deliverables for their CWD. Mostly used internally."""
        return self.deliverables_in.get_cwd()

