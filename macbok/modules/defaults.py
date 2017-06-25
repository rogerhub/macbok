from macbok.common import task
from macbok.common import util
from macbok.modules import script


class Defaults(task.Task):
  def __init__(self, domain, key, value=None, value_type=None,
               operation='write'):
    if operation not in ('write', 'delete'):
      raise ValueError('Unknown operation %r' % operation)
    if type(value) == bool:
      check_value = str(int(value))
      value = str(value).lower()
      if value_type is None:
        value_type = 'boolean'
    else:
      check_value = str(value)
    assert type(value) in (int, str), 'Unsupported value type: %s' % repr(value)
    if value_type is None:
      if type(value) is int:
        value_type = 'integer'
      elif type(value) is str:
        value_type = 'string'
    self.domain = domain
    self.key = key
    self.value = value
    self.value_type = value_type
    self.operation = operation
    self._check_value = check_value

  def __repr__(self):
    arguments = [repr(self.domain), repr(self.key)]
    if self.domain:
      arguments.append(repr(self.domain))
    if self.key:
      arguments.append(repr(self.key))
    if self.value:
      arguments.append('value=%s' % repr(self.value))
    if self.value_type:
      arguments.append('value_type=%s' % repr(self.value_type))
    if self.operation:
      arguments.append('operation=%s' % repr(self.operation))
    return 'Defaults(%s)' % (', '.join(arguments))

  def OnlyIf(self):
    command = 'defaults read %s %s' % (util.BashQuote(self.domain),
                                       util.BashQuote(self.key))
    result = yield script.Script(command, _internal=True)
    yield result.strip() != self._check_value

  def Run(self):
    command = 'defaults write %s %s -%s %s' % (
        util.BashQuote(self.domain),
        util.BashQuote(self.key),
        util.BashQuote(self.value_type),
        util.BashQuote(str(self.value)))
    yield script.Script(command)
