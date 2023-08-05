import json

from cleo import Command

from isilon.commands.exec import Operator


class ContainersCommand(Command):
    """
    Containers.

    containers
        {container : Container name.}
        {--meta=* : Metadata.}
        {--o|objects : Show container details and list objects.}
        {--c|create : Create container.}
        {--m|metadata : Show container metadata.}
        {--u|update : Create, update or delete container metadata.}
        {--d|delete : Delete container.}
    """

    def handle(self):
        op = Operator()
        container_name = str(self.argument("container"))
        meta = dict()
        for header in self.option("meta"):
            meta.update(json.loads(header))
        if self.option("objects"):
            resp = op.execute(op.client.containers.objects, container_name)
            for obj in resp:
                self.line(json.dumps(obj, indent=4, sort_keys=True))
        elif self.option("create"):
            op.execute(op.client.containers.create, container_name, metadata=meta)
            self.line(
                f"<options=bold>container <comment>{container_name}</comment> created.</>"
            )
        elif self.option("delete"):
            op.execute(op.client.containers.delete, container_name)
            self.line(
                f"<options=bold>container <comment>{container_name}</comment> deleted.</>"
            )
        elif self.option("metadata"):
            resp = op.execute(op.client.containers.show_metadata, container_name)
            table = self.table(style="compact")
            metas = []
            for meta_key, meta_value in resp.items():
                metas.append([f"<options=bold>{meta_key}</>", f": {meta_value}"])
            table.set_rows(metas)
            table.render(self.io)
        elif self.option("update"):
            op.execute(
                op.client.containers.update_metadata, container_name, metadata=meta
            )
            self.line("<options=bold>container metadata updated.</>")
