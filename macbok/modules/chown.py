"""Change ownership of files."""

import grp
import os
import pwd
from macbok.common import task
from macbok.common import util
from macbok.modules import script


class Chown(task.Task):
  def __init__(self, target, user, group=None):
    """Takes ownership of a target. Requires sudo."""
    self.target = target
    self.user = user
    self.group = group

  def __repr__(self):
    return "Chown(%r, %r %r)" % (self.target, self.user, self.group)

  def OnlyIf(self):
    stat_result = os.lstat(self.target)
    stat_user = pwd.getpwuid(stat_result.st_uid)
    if self.user != stat_user.pw_name:
      return True
    if self.group:
      stat_group = grp.getgrgid(stat_result.st_gid)
      if self.group != stat_group.gr_name:
        return True

  def Run(self):
    if self.group:
      family = "%s:%s" % (util.BashQuote(self.user), util.BashQuote(self.group))
    else:
      family = util.BashQuote(self.user)
    command = "sudo chown %s %s" % (family, util.BashQuote(self.target))
    yield script.Script(command)
