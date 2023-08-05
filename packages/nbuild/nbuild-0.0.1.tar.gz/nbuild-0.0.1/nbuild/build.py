
"""
The build module contains the BuildSystem class
"""


import subprocess

from nbuild.util import ask_yn_q

class BuildSystem:
    """
    The BuildSystem class models steps which transform one deliverable
    (such as source code) into another type of deliverable
    (such as a .exe file).

    Many projects will not need a build system, such as
    binary redistributables which are ready to be executed.
    """
    def __init__(self, *args, _type="none", **kwargs):
        self._type = _type
        self.project = None
        self.args = args
        self.kwargs = kwargs

    def build(self, project=None):
        """
        This builds the project.
        For physical projects this prompts the operator to setup their lab environment
        using equipment listed in the Project.
        """
        # Default to self.project
        if self.project and not project:
            project = self.project

        if self._type == "make":
            subprocess.run([
                'make', *self.args
            ], cwd=project.get_cwd(), check=True)

        elif self._type == "npm":
            subprocess.run([
                'npm', 'install'
            ], cwd=project.get_cwd(), check=True)

            subprocess.run([
                'npm', *self.kwargs['cmds']
            ], cwd=project.get_cwd(), check=True)
        
        elif self._type == "physical":
            self._do_physical_build(project)

        elif self._type == "none":
            pass

        else:
            raise Exception("Unknown build type '{}'".format(self._type))

    def _do_physical_build(self, project):
        """
        Internal method which is responsible for prompting operators to
        setup their lab environments.
        """
        print("Please ensure the following items are available at the test site:")
        for item in project.deliverables_in.items:
            print("> {}".format(item))
        
        if ask_yn_q('Are all items available?'):
            for step in list(self.kwargs['steps']):
                print('')
                if step.lower().startswith('q:'):
                    response = ask_yn_q(step[2:])
                    if not response:
                        print('A setup step cannot be completed, test is finished')
                        break
                else:
                    print('> {}'.format(step))
                    response = ask_yn_q('Type "yes" when step completed, or "no" if step cannot be completed.')
                    if not response:
                        print('A setup step cannot be completed, test is finished')
        else:
            print('An item is missing, test is finished.')
