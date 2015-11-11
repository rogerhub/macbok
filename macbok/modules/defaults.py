from macbok.common.task import Task
from macbok.common.util import bash_quote
from macbok.modules.script import Script


class Defaults(Task):
    def __init__(self, domain, key, value=None, value_type=None, operation="write"):
        assert operation in ("write", "delete"), "Unknown operation"
        if type(value) == bool:
            check_value = str(int(value))
            value = str(value).lower()
            if value_type is None:
                value_type = "boolean"
        else:
            check_value = str(value)
        assert type(value) in (int, str), "Unsupported value type: %s" % repr(value)
        if value_type is None:
            if type(value) is int:
                value_type = "integer"
            elif type(value) is str:
                value_type = "string"
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
            arguments.append("value=%s" % repr(self.value))
        if self.value_type:
            arguments.append("value_type=%s" % repr(self.value_type))
        if self.operation:
            arguments.append("operation=%s" % repr(self.operation))
        return "Defaults(%s)" % (", ".join(arguments))

    def onlyif(self):
        command = "defaults read %s %s" % (bash_quote(self.domain), bash_quote(self.key))
        result = yield Script(command, _internal=True)
        yield result.strip() != self._check_value

    def run(self):
        yield Script("defaults write %s %s -%s %s" % (bash_quote(self.domain),
                                                      bash_quote(self.key),
                                                      bash_quote(self.value_type),
                                                      bash_quote(str(self.value))))
