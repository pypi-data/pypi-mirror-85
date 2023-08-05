
"""
The deliverable module contains the Deliverable class
"""

import os
import subprocess
import tempfile

class Deliverable:
    """
    The Deliverable class models anything a contractor could produce, including:
      - A webpage hosted remotely
      - A binary redistributable for software
      - Source code for software
      - A physical item such as a tool, munitions, or a vehicle
      - An image, map, overlay, or any other file we have the tools to measure.
    """
    def __init__(self, _type="file", path="", url="", git_dir=None, items=None):
        self._type = _type
        self.path = path
        self.url = url
        # Type-specific data
        self.git_dir = git_dir
        self.git_dir_obj = None
        self.items = items

    def get_cwd(self):
        """
        Gets the working directory that this Deliverable uses.
        For software this may be an unzipped .zip file,
        for git repositories the repo will be cloned to a temporary directory.
        This is mostly used internally.
        """
        if self._type == "git":
            if self.git_dir and os.path.exists(self.git_dir):
                return self.git_dir

            # Do a clone and return that
            if not self.git_dir:
                self.git_dir_obj = tempfile.TemporaryDirectory(suffix=''.join([x for x in self.url if x.isalnum()]))
                self.git_dir = self.git_dir_obj.name

            subprocess.run([
              'git', 'clone', self.url, self.git_dir
            ], check=True)

            return self.git_dir

        if self._type != "directory":
            raise Exception("get_cwd only makes sense for Deliverable of type 'directory'")
        return self.path

