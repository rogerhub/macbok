import re
from macbok.common.util import bash_quote
from macbok.common.task import Task
from macbok.modules.script import Script


class Pmset(Task):
    def __init__(self, setting, value, mode='a'):
        """Sets a power-management setting."""
        if mode not in 'abc':
            raise ValueError('Unrecognized mode %r' % mode)
        self.setting = setting
        self.value = value
        self.mode = mode

    def __repr__(self):
        return 'Pmset(setting=%r, value=%r, mode=%r)' % (self.setting,
                                                         self.value, self.mode)

    def _current_settings(self):
        with self.task_lock():
            result = yield Script('pmset -g custom', _internal=True)
            match = re.match(r'^Battery Power:\n(.*)AC Power:\n(.*)', result,
                             re.DOTALL)
            if not match:
                raise ValueError('Unrecognized output: %s' % result)
            yield {
                'battery_power': self._parse_key_value(match.group(1)),
                'ac_power': self._parse_key_value(match.group(2)),
            }

    def _parse_key_value(self, payload):
        """Turns a multi-line string of '  key value' into a dict."""
        return dict(re.findall(r'^ *([a-z]+) +(.*)$', payload, re.MULTILINE))

    def onlyif(self):
        current_settings = yield self._current_settings()
        if self.mode == 'a':
            yield not all(s[self.setting] == self.value for s in current_settings)
        elif self.mode == 'b':
            yield current_settings['battery_power'][self.setting] != self.value
        elif self.mode == 'c':
            # Mode 'c' means 'charger'.
            yield current_settings['ac_power'][self.setting] != self.value
        else:
            raise ValueError('Unrecognized pmset mode %r' % self.mode)

    def run(self):
        with self.task_lock():
            yield Script('sudo pmset -%s %s %s' %
                         (self.mode, bash_quote(self.setting),
                          bash_quote(self.value)))
