import json

from cleo import Command

from isilon.commands.exec import Operator


class AccountsCommand(Command):
    """
    Accounts.

    accounts
        {account : Account name.}
        {--meta=* : Metadata.}
        {--s|show : Show account details and list containers.}
        {--u|update : Create, update, or delete account metadata.}
        {--m|metadata : Show account metadata.}
    """

    def handle(self):
        op = Operator()
        account_name = str(self.argument("account"))
        meta = dict()
        for header in self.option("meta"):
            meta.update(json.loads(header))
        if self.option("show"):
            resp = op.execute(op.client.accounts.show, account_name)
            self.line(json.dumps(resp, indent=4, sort_keys=True))
        elif self.option("update"):
            op.execute(op.client.accounts.update, account_name, metadata=meta)
            self.line("<options=bold>metadata updated.</>")
        elif self.option("metadata"):
            resp = op.execute(op.client.accounts.metadata, account_name)
            table = self.table(style="compact")
            metas = []
            for meta_key, meta_value in resp.items():
                metas.append([f"<options=bold>{meta_key}</>", f": {meta_value}"])
            table.set_rows(metas)
            table.render(self.io)
