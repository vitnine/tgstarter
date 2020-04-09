from typing import (
    Optional,
    Dict,
    Any,
    Callable,
)

import yaml
import jinja2


def load_yamls(*paths: str, loader: yaml.Loader) -> Dict[str, Any]:
    yamls = {}
    for path in paths:
        with open(path) as file:
            yaml_content = yaml.load(stream=file, Loader=loader)
        yamls[path] = yaml_content
    return yamls


def get_template_constructor(jinja2_env: Optional[jinja2.Environment] = None) -> Callable[..., Any]:

    def template_constructor(loader: yaml.Loader, node: yaml.Node) -> jinja2.Template:
        if jinja2_env is not None:
            return jinja2_env.from_string(source=node.value)
        else:
            return jinja2.Template(source=node.value)

    return template_constructor
