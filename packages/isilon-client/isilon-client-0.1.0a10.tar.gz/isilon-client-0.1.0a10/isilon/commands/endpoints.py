from cleo import Command

from isilon.commands.exec import Operator


class EndpointsCommand(Command):
    """
    Endpoints.

    endpoints
    """

    def handle(self):
        op = Operator()
        resp = op.execute(op.client.endpoints)
        self.line(f"{resp}")
