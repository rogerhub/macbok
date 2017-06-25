import re

from macbok.common import util
from macbok.common import task
from macbok.modules import script


class Pmset(task.Task):
  def __init__(self, setting, value, mode='a'):
    """Sets a power-management setting."""
    if mode not in 'abc':
      raise ValueError('Unrecognized mode %r' % mode)
    self.setting = setting
    self.value = value
    self.mode = mode

  def __repr__(self):
    return 'Pmset(setting=%r, value=%r, mode=%r)' % (self.setting, self.value,
                                                     self.mode)

  def _CurrentSettings(self):
    with self.TaskLock():
      result = yield script.Script('pmset -g custom', _internal=True)
      match = re.match(r'^Battery Power:\n(.*)AC Power:\n(.*)', result,
                       re.DOTALL)
      if not match:
        raise ValueError('Unrecognized output: %s' % result)
      yield {
        'battery_power': self._ParseKeyValue(match.group(1)),
        'ac_power': self._ParseKeyValue(match.group(2)),
      }

  def _ParseKeyValue(self, payload):
    """Turns a multi-line string of '  key value' into a dict."""
    return dict(re.findall(r'^ *([a-z]+) +(.*)$', payload, re.MULTILINE))

  def OnlyIf(self):
    current_settings = yield self._CurrentSettings()
    if self.mode == 'a':
      yield not all(s[self.setting] == self.value for s in current_settings)
    elif self.mode == 'b':
      yield current_settings['battery_power'][self.setting] != self.value
    elif self.mode == 'c':
      # Mode 'c' means 'charger'.
      yield current_settings['ac_power'][self.setting] != self.value
    else:
      raise ValueError('Unrecognized pmset mode %r' % self.mode)

  def Run(self):
    with self.task_lock():
      yield script.Script('sudo pmset -%s %s %s' %
                          (self.mode, util.BashQuote(self.setting),
                           util.BashQuote(self.value)))
