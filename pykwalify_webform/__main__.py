import os
from distutils.dir_util import copy_tree
from os import makedirs
from pathlib import Path

import click
from yaml import safe_load

from pykwalify_webform.renderer import Renderer

HERE = Path(__file__).parent


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.argument("schema_file", type=click.File("r"))
@click.argument("out_path", type=click.Path(dir_okay=False, writable=True))
@click.argument("static_path", type=click.Path(dir_okay=True, writable=True))
@click.argument("target_schema", default="")
@click.option("--value-file", type=click.File("r"))
@click.pass_context
def main(
    ctx, schema_file, out_path: str, static_path: str, target_schema: str, value_file
):
    kwargs = {kv.split("=")[0].lstrip("--"): kv.split("=")[1] for kv in ctx.args}
    schemata = safe_load(schema_file)
    value = None
    if value_file:
        value = safe_load(value_file)
    renderer = Renderer(schemata, HERE / "templates")
    makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write(renderer.render(target_schema, value, **kwargs))

    # Copy static files
    copy_tree(str(HERE / "static"), static_path)


if __name__ == "__main__":
    main()
