import json
from pathlib import Path

from cleo import Command

from isilon.commands.exec import Operator


class ObjectsCommand(Command):
    """
    Objects.

    objects
        {container : Container name.}
        {object : Object name.}
        {--meta=* : Metadata.}
        {--data=? : Object data.}
        {--c|create : Create or replace object.}
        {--m|metadata : Show object metadata.}
        {--u|update : Create or update object metadata.}
        {--d|delete : Delete object.}
    """

    def handle(self):
        op = Operator()
        container_name = str(self.argument("container"))
        object_name = str(self.argument("object"))
        meta = dict()
        for header in self.option("meta"):
            meta.update(json.loads(header))
        if self.option("create"):
            try:
                data = Path(self.option("data"))
            except TypeError:
                self.line("<error>Please, provides a valid object.</>")
                raise SystemExit(1)
            if not data.is_file():
                self.line("<error>Please, provides a valid object.</>")
                raise SystemExit(1)
            op.execute(
                op.client.objects.create_large,
                container_name,
                object_name,
                data,
                metadata=meta,
            )
            self.line(
                f"<options=bold><comment>{object_name}</comment> object created.</>"
            )
        elif self.option("metadata"):
            resp = op.execute(
                op.client.objects.show_metadata, container_name, object_name
            )
            table = self.table(style="compact")
            metas = []
            for meta_key, meta_value in resp.items():
                metas.append([f"<options=bold>{meta_key}</>", f": {meta_value}"])
            table.set_rows(metas)
            table.render(self.io)
        elif self.option("update"):
            op.execute(
                op.client.objects.update_metadata,
                container_name,
                object_name,
                metadata=meta,
            )
            self.line("<options=bold>metadata updated.</>")
        elif self.option("delete"):
            op.execute(op.client.objects.delete, container_name, object_name)
            self.line(
                f"<options=bold><comment>{object_name}</comment> object deleted.</>"
            )
        else:
            op.execute(
                op.client.objects.get_large, container_name, object_name, object_name
            )
            self.line(
                f"<options=bold><comment>{object_name}</comment> object saved.</>"
            )
