"""Change ownership of files."""

import grp
import os
import pwd
from macbok.common.task import Task
from macbok.common.util import bash_quote
from macbok.modules.script import Script


class Chown(Task):
  def __init__(self, target, user, group=None):
    """Takes ownership of a target. Requires sudo."""
    self.target = target
    self.user = user
    self.group = group

  def __repr__(self):
    return "Chown(%r, %r %r)" % (self.target, self.user, self.group)

  def onlyif(self):
    stat_result = os.lstat(self.target)
    stat_user = pwd.getpwuid(stat_result.st_uid)
    if self.user != stat_user.pw_name:
      return True
    if self.group:
      stat_group = grp.getgrgid(stat_result.st_gid)
      if self.group != stat_group.gr_name:
        return True

  def run(self):
    if self.group:
      family = "%s:%s" % (bash_quote(self.user), bash_quote(self.group))
    else:
      family = bash_quote(self.user)
    command = "sudo chown %s %s" % (family, bash_quote(self.target))
    yield Script(command)
