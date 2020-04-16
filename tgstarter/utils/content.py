from typing import (
    Any,
    Type,
    Callable,
    TypeVar,
)
import textwrap
import inspect

import jinja2


T = TypeVar('T', bound=Type)


def isbuiltinname(name: str) -> bool:
    return name.startswith('__') and name.endswith('__')


class ContentValidator:
    def __init__(
        self,
        delete_indentation: Callable[[str], str] = textwrap.dedent,
        create_jinja2_template: Callable[[str], jinja2.Template] = jinja2.Template
    ) -> None:
        self.delete_indentation = delete_indentation
        self.create_jinja2_template = create_jinja2_template

    def validated_class(
        self,
        cls: T = None,
        delete_indent: bool = True,
        with_subclasses: bool = True
    ) -> T:
        def wrapper(cls: T) -> T:
            annotations = getattr(cls, '__annotations__', {})
            for field, value in cls.__dict__.items():
                if not isbuiltinname(field):
                    if inspect.isclass(value):
                        if with_subclasses:
                            value = wrapper(value)
                    else:
                        if isinstance(value, str) and delete_indent:
                            value = self.delete_indentation(value)

                        if field in annotations:
                            value_type = annotations[field]
                            if not isinstance(value, value_type):
                                # TODO: take out this logic to a method
                                if value_type == jinja2.Template:
                                    if isinstance(value, str):
                                        value = self.create_jinja2_template(value)
                                    else:
                                        assert False

                    setattr(cls, field, value)
            return cls

        return wrapper if cls is None else wrapper(cls)
