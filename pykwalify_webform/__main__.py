import os
from os import makedirs

import click
from yaml import safe_load

from pykwalify_webform.renderer import Renderer


@click.command()
@click.argument("schema_file", type=click.File("r"))
@click.argument("out_path", type=click.Path(dir_okay=False, writable=True))
@click.argument("target_schema", default="")
def main(schema_file, out_path: str, target_schema: str):
    schemata = safe_load(schema_file)
    renderer = Renderer(schemata, "templates")
    makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write(renderer.render(target_schema))


if __name__ == "__main__":
    main()
