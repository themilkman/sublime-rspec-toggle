import sublime, sublime_plugin
import re
import os

def log(message):
  print("=> RSpec Toggle: %s" % (message))

CREATE_IMPLEMENTATION_FILE_MESSAGE = """
The implementation file doesn't exist.
Do you want to create it?
"""

CREATE_SPEC_FILE_MESSAGE = """
The spec file doesn't exist.
Do you want to create it?
"""

SPEC_TEMPLATE = """\
# frozen_string_literal: true

require 'spec_helper'

"""

RAILS_SPEC_TEMPLATE = """\
# frozen_string_literal: true

require 'rails_helper'

"""

class RspecToggleCommand(sublime_plugin.WindowCommand):
  def run(self):
    folders = self.window.folders()

    if len(folders) == 0:
      return

    current_file = self.window.active_view().file_name()
    current_folder = None

    for folder in folders:
      if current_file.startswith(folder):
        current_folder = folder
        break

    if not current_folder:
      return

    relative_path = current_file.replace("%s/" % current_folder, "")

    current_subdir = ''
    sub_dirs = ["shared"] # TODO setting
    for subdir in sub_dirs:
      if relative_path.startswith(subdir):
        current_subdir = subdir
        relative_path = relative_path.replace(subdir + '/', "")

    if relative_path.startswith("spec"):
      self._open_implementation_file(current_folder, relative_path, current_subdir)
    else:
      self._open_spec_file(current_folder, relative_path, current_subdir)

  def _open_implementation_file(self, folder, file, current_subdir):
    base_path = re.sub(r"^spec\/(.*?)_spec\.rb$", "\\1.rb", file)
    candidates = [base_path, "lib/%s" % base_path, "app/%s" % base_path]

    for path in candidates:
      fullpath = os.path.join(folder, current_subdir, path)

      if os.path.isfile(fullpath):
        return self.window.open_file(fullpath)

    if not sublime.ok_cancel_dialog(CREATE_IMPLEMENTATION_FILE_MESSAGE):
      return

    candidates = [
      os.path.join(current_subdir,  "app"),
      os.path.join(current_subdir,  "lib"),
      os.path.join(folder, "app"),
      os.path.join(folder, "lib"),
    ]

    for dir in candidates:
      fullpath = os.path.join(dir, base_path)
      if current_subdir == '':
        basedir = os.path.dirname(fullpath)
      else:
        basedir = folder   + "/" + os.path.dirname(fullpath)

        fullpath = os.path.join(folder, os.path.dirname(fullpath),  os.path.basename(fullpath))


      if os.path.isdir(basedir):
        open(fullpath, "w+").close()
        self.window.open_file(fullpath)
        break

  def _is_rails(self, folder):
    return os.path.isdir(os.path.join(folder, "app")) and \
           os.path.isdir(os.path.join(folder, "config"))

  def _open_spec_file(self, folder, file, current_subdir):
    if self._is_rails(folder):
      regex = r"^(?:app\/)?(.*?)\.rb$"
    else:
      regex = r"^lib\/(.*?)\.rb$"

    base_path = re.sub(regex, "spec/\\1_spec.rb", file)
    fullpath = os.path.join(folder, current_subdir, base_path)
    rails_helper = os.path.join(folder, "spec/rails_helper.rb")

    if os.path.isfile(rails_helper):
      template = RAILS_SPEC_TEMPLATE
    else:
      template = SPEC_TEMPLATE

    if os.path.isfile(fullpath):
      self.window.open_file(fullpath)
    elif sublime.ok_cancel_dialog(CREATE_SPEC_FILE_MESSAGE):
      self._make_dir_for_path(fullpath)
      handler = open(fullpath, "w+")
      handler.write(template)
      handler.close()
      self.window.open_file(fullpath)

  def _make_dir_for_path(self, filepath):
    basedir = os.path.dirname(filepath)

    if not os.path.isdir(basedir):
      os.makedirs(basedir)
