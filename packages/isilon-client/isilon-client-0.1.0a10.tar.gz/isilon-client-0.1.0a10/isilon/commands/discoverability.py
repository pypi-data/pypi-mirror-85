import json

from cleo import Command

from isilon.commands.exec import Operator


class DiscoverabilityCommand(Command):
    """
    Discoverability.

    discoverability
    """

    def handle(self):
        op = Operator()
        resp = op.execute(op.client.discoverability.info)
        self.line(json.dumps(resp, indent=4, sort_keys=True))
