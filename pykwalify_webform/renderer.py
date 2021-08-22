from io import StringIO
from os import listdir, path
from os.path import splitext
from typing import TextIO, List

from jinja2 import Environment, FileSystemLoader
from yaml import safe_dump


class Renderer:
    TYPE_ALIASES = {
        "mapping": "map",
        "sequence": "seq",
    }
    TYPE_TEMPLATE_DIR = "types"
    PAGE_TEMPLATE_FILENAME = "page.jinja2"
    TEMPLATE_EXTENSION = ".jinja2"

    def __init__(self, schemata: dict, templates_dir: str):
        self._schemata = schemata

        self._env = Environment(loader=FileSystemLoader(templates_dir))

        # Load type templates
        self._templates = {}
        for filename in listdir(path.join(templates_dir, self.TYPE_TEMPLATE_DIR)):
            basename, extension = splitext(filename)
            if extension != self.TEMPLATE_EXTENSION:
                continue
            self._templates[basename] = self._load_template_file(
                path.join(self.TYPE_TEMPLATE_DIR, filename)
            )
        self._page_template = self._load_template_file(self.PAGE_TEMPLATE_FILENAME)

    def render(self, target_schema: str):
        stream = StringIO()
        if target_schema:
            name = target_schema
            schema = self._schemata[f"schema;{target_schema}"]
            target_schema = f"schema;{target_schema}"
        else:
            name = ""
            schema = self._schemata["sequence"][0]
            target_schema = "sequence"
        self._render(stream, schema, [target_schema])
        return self._page_template.render(
            name=name, contents=stream.getvalue(), schema=safe_dump(self._schemata)
        )

    def _render(self, stream: TextIO, schema: dict, names: List[str]):
        # TODO: pattern
        # TODO: range
        # TODO: example

        if "include" in schema:
            self._include(schema)

        schema_type = schema.get("type", "str")
        schema_type = self.TYPE_ALIASES.get(schema_type, schema_type)
        # TODO: multiple sequences
        if schema_type == "seq":
            schema_seq = schema["sequence"]
            if "include" in schema_seq[0]:
                self._include(schema_seq[0])
        required = schema.get("req", False) or schema.get("required", False)

        # TODO: use template inheritance for composite types
        sub_stream = StringIO()
        if schema_type == "map":
            # TODO: allowempty
            # TODO: matching-rule
            # TODO: regex;(regex-pattern)/re;(regex-pattern)
            for mapping in schema["mapping"]:
                self._render(sub_stream, schema["mapping"][mapping], names + [mapping])
        template = self._templates[schema_type]
        stream.write(
            template.render(
                name=names[-1],
                path="".join((f"[{name}]" for name in names[1:])),
                required=required,
                contents=sub_stream.getvalue(),
                schema=schema,
            )
        )

        # TODO: bool
        # TODO: float
        # TODO: time
        # TODO: timestamp

    def _include(self, schema):
        # Copy partial schema in
        for k, v in self._schemata[f"schema;{schema['include']}"].items():
            schema[k] = v

    def _load_template_file(self, filename: str):
        return self._env.get_template(filename)
