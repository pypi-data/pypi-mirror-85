
"""
The test module contains the TestSystem class.
The Test class is not used externally.
"""


import os
import subprocess
import platform
import shutil

from nbuild.util import ask_yn_q

class Test:
    """
    An internal class to track some test task,
    a description of the task, and the task success state.
    """

    @staticmethod
    def no_task_task():
        """
        Default task which crashes the program because someone
        forgot to specify work to be done/tested
        """
        raise Exception("No task specified!")

    def __init__(self, description="No Description", task=no_task_task):
        self.description = description
        self.task = task
        self.passed = False

    def test(self, *args):
        """Runs this test and records if it passed"""
        p = self.task(*args)
        if not isinstance(p, (bool)):
            raise Exception("test tasks MUST return a boolean (True or False). Good examples may be a lambda that returns 'x == 5' or 'output.startswith(\"completed\")'")
        self.passed = p


class TestSystem:
    """
    The TestSystem class represents an entire test routine.
    After using a method in `nbuild` to create a test system,
    chained methods may be used to specify any number of
    individual test cases for the project.
    """

    def __init__(self, *args, _type="execute", **kwargs):
        self._type = _type
        self.args = args
        self.kwargs = kwargs
        self.project = None
        # Holds Test objects
        self.tests = []
        # Holds any generated report files
        self.reports = []
        # These are _type-dependent flags
        self.execute_stdout = ""
        self.execute_process_crashed = False
        self.execute_process_crashed_msg = None
        self.physical_test_notes = ""
      

    def with_stdout(self, description, task):
        """
        Only valid for executable files.
        `task` receives the program's standard output as a string
        and must return True if the test passed, otherwise False.
        """
        if self._type != "execute":
            raise Exception("Cannot call with_stdout unless task type is 'execute'")
        self.tests.append(Test(
            description=description,
            task=task
        ))
        return self

    def default_npm(self):
        """
        Only valid for NPM tests, used internally.
        """
        if self._type != "npm":
            raise Exception("Cannot call default_npm unless task type is 'npm'")
        
        def inner_npm():
            
            subprocess.run([
                'npm', *self.kwargs['cmds']
            ], cwd=self.project.get_cwd(), check=True)

            return True

        self.tests.append(Test(
            description='NPM Test; see the test report generated below for details.',
            task=inner_npm
        ))

        return self

    def default_physical(self):
        """
        Only valid for physical tests, used internally.
        """
        if self._type != "physical":
            raise Exception("Cannot call default_physical unless task type is 'physical'")
      
        def inner_physical(step):
            
            print('')
            if step.lower().startswith('q:'):
                return ask_yn_q(step[2:].strip())
              
            print('> {}'.format(step))
            return ask_yn_q('Type "yes" when step completed, or "no" if step cannot be completed.')
            
        for step in list(self.kwargs['steps']):
            self.tests.append(Test(
                description=step,
                task=(lambda istep: lambda: inner_physical(istep))(step) # 1 level of indirection so we save THIS iteration's step value
            ))

        return self
      

    def run_pretest_tasks(self, project):
        """
        Internal method which sets up for tests; at the moment
        only the "execute" type uses this to collect program
        output before running tests on the output.
        """
        if self._type == "execute":
            try:
                self.execute_stdout = subprocess.run(
                    self.kwargs['exec_args'],
                    cwd=project.get_cwd(),
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                ).stdout.decode('utf-8')
            except subprocess.CalledProcessError as e:
                self.execute_process_crashed = True
                self.execute_process_crashed_msg = e.output.decode('utf-8') + os.linesep + os.linesep + str(e)


    def test(self, project):
        """Runs all tests"""
        self.run_pretest_tasks(project)
        if len(self.tests) < 1:
            raise Exception("No tests specified!")
        if self._type == "execute":
            for t in self.tests:
                t.test(self.execute_stdout)

        elif self._type == "npm":
            for t in self.tests:
                t.test()

        elif self._type == "physical":
            for t in self.tests:
                t.test()
            self.physical_test_notes = input('Write any additional notes here, typing enter when complete: ')

        else:
            raise Exception("Unknown testing procedure for TestSystem._type = {}".format(self._type))

    def write_reports_to(self, project, directory):
        """
        Generates a file "nbuild_test_report.html" in the specified directory.
        May also copy in results of 3rd-party test reports from Unit testing frameworks
        and other automated test suites.
        """
        test_rep_path = os.path.join(directory, 'nbuild_test_report.html')
        with open(test_rep_path, 'w') as test_rep:
            # test_table is a bunch of <tr> rows with <td> columns
            test_table = ""
            for t in self.tests:
                test_table += '<tr><td class="{_class}">{passed}</td><td>{description}</td></tr>'.format(
                    _class='passed' if t.passed else 'failed',
                    passed='Passed' if t.passed else 'Failed',
                    description=t.description
                )

            closing_remarks = ""
            if self.execute_process_crashed:
                closing_remarks = "<p>The program crashed during execution. Output is shown below.</p><pre>{output}</pre>".format(
                    output=self.execute_process_crashed_msg
                )
            elif self.execute_stdout:
                closing_remarks = "<p>Program Output:</p><pre>{output}</pre>".format(output=self.execute_stdout)

            elif self._type == "npm":
                test_res_dir = os.path.join(self.project.get_cwd(), 'build', 'test-results')
                if os.path.exists(test_res_dir):
                    # Grab first .html file, copy to "directory", then add <iframe> pointint to it
                    copied_report_prefix = 'nbuild_cp_'
                    first_report_f = None
                    for report_f in os.listdir(test_res_dir):
                        if report_f.endswith('.html'):
                            first_report_f = copied_report_prefix+report_f
                            shutil.copy(os.path.join(test_res_dir, report_f), os.path.join(directory, first_report_f))
                            break

                if first_report_f:
                    closing_remarks = '<iframe src="{first_report_f}" width="100%" height="900pt" style="border: 1px solid black;"></iframe>'.format(first_report_f=first_report_f)

            elif self._type == "physical":
                closing_remarks = "<p>Additional test comments:</p><pre>{notes}</pre>".format(notes=self.physical_test_notes)

            test_rep.write("""<DOCTYPE html>
<html lang="en">
  <head>
    <title>{name} Test Report</title>
    <style>
table, th, td {{
  border: 1px solid black;
  border-collapse: collapse;
}}
th, td {{
  padding: 4pt 8pt;
}}
.passed {{
  background-color: #90ee90; /* light green */
}}
.failed {{
  background-color: #ffcccb; /* light red */
}}
pre {{
  overflow-x: auto;
  white-space: pre-wrap;
  white-space: -moz-pre-wrap;
  white-space: -pre-wrap;
  white-space: -o-pre-wrap;
  word-wrap: break-word;
}}

    </style>
  </head>
  <body>
    <h1>{name} Test Report</h1>
     <table>
      <tr>
        <th>Status</th>
        <th>Description</th>
      </tr>
      {test_table}
    </table>
    {closing_remarks}
  </body>
</html>
  """.format(
            name=project.name,
            test_table=test_table,
            closing_remarks=closing_remarks
          ))

        self.reports.append(test_rep_path)

    def open_reports(self):
        """
        Must be called after write_reports_to has been called.
        Opens all report files in their default programs, for example
        Chrome will usually open .html files and Adobe products will usually open .pdf files.
        """
        for filepath in self.reports:
            if platform.system() == 'Darwin':
                subprocess.call(('open', filepath))
            elif platform.system() == 'Windows':
                # pylint: disable=no-member
                os.startfile(filepath)
            else:
                subprocess.call(('xdg-open', filepath))

