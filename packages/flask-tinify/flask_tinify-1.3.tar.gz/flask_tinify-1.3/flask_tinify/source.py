from .result import Result
from .result_meta import ResultMeta


class Source(object):
    def __init__(self, url, tinify, **commands):
        self.url = url
        self.commands = commands
        self.tinify = tinify

    def preserve(self, *options):
        return type(self)(self.url, **self._merge_commands(preserve=self._flatten(options)))

    def resize(self, **options):
        return type(self)(self.url, **self._merge_commands(resize=options))

    def store(self, **options):
        response = self.tinify.get_client().request('POST', self.url, self._merge_commands(store=options))
        return ResultMeta(response.headers)

    def result(self):
        response = self.tinify.get_client().request('GET', self.url, self.commands)
        return Result(response.headers, response.content)

    def to_file(self, path):
        return self.result().to_file(path)

    def to_buffer(self):
        return self.result().to_buffer()

    def _merge_commands(self, **options):
        commands = self.commands.copy()
        commands.update(options)
        return commands

    def _flatten(self, items, seqtypes=(list, tuple)):
        items = list(items)
        for i, x in enumerate(items):
            while isinstance(items[i], seqtypes):
                items[i:i+1] = items[i]
        return items
