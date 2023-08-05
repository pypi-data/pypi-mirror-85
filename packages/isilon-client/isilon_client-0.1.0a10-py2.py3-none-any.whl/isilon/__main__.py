from cleo import Application

from isilon.__version__ import __version__
from isilon.commands import (
    AccountsCommand,
    ContainersCommand,
    DiscoverabilityCommand,
    EndpointsCommand,
    ObjectsCommand,
)

application = Application("isilon-client", f"{__version__}")
application.add(AccountsCommand())
application.add(ContainersCommand())
application.add(DiscoverabilityCommand())
application.add(EndpointsCommand())
application.add(ObjectsCommand())


if __name__ == "__main__":
    application.run()
