from io import StringIO
from os import listdir, path, mkdir
from os.path import splitext
from typing import TextIO, List

from jinja2 import Environment, FileSystemLoader
from yaml import safe_load


class Generator:
    TYPE_ALIASES = {
        "mapping": "map",
        "sequence": "seq",
    }
    TYPE_TEMPLATE_DIR = "types"
    PAGE_TEMPLATE_FILENAME = "page.jinja2"
    TEMPLATE_EXTENSION = ".jinja2"

    def __init__(self, schemata: dict, templates_dir: str):
        self._schemata = schemata

        self._env = Environment(
            loader=FileSystemLoader(templates_dir)
        )

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

    def generate(self, target_schema: str):
        stream = StringIO()
        self._generate(stream, self._schemata[f"schema;{target_schema}"], [target_schema])
        return self._page_template.render(
            name=target_schema, contents=stream.getvalue()
        )

    def _generate(self, stream: TextIO, schema: dict, names: List[str]):
        # TODO: pattern
        # TODO: req/required
        # TODO: range
        # TODO: desc
        # TODO: example

        schema_type = self.TYPE_ALIASES.get(schema["type"], schema["type"])
        required = schema.get("req", False) or schema.get("required", False)

        # TODO: use template inheritance for composite types
        if schema_type in {"map", "mapping"}:
            # TODO: allowempty
            # TODO: matching-rule
            # TODO: regex;(regex-pattern)/re;(regex-pattern)
            for mapping in schema["mapping"]:
                self._generate(stream, schema["mapping"][mapping], names + [mapping])
        else:
            template = self._templates[schema_type]
            stream.write(
                template.render(
                    name=names[-1],
                    path="".join((f"[{name}]" for name in names[1:])),
                    required=required,
                    schema=schema
                )
            )

        # TODO: bool
        # TODO: date
        # TODO: float
        # TODO: time
        # TODO: timestamp

    def _load_template_file(self, filename: str):
        return self._env.get_template(filename)


def main():
    with open("schema.yaml", "r") as f:
        schemata = safe_load(f)
    target_schema = "game"
    generator = Generator(schemata, "templates")
    mkdir("build")
    with open("build/osgameclones/game.html", "w") as f:
        f.write(generator.generate(target_schema))


if __name__ == "__main__":
    main()
