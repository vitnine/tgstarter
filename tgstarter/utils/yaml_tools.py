from typing import (
    Optional,
    Dict,
    Any,
    Callable,
    Union,
)
import json

import yaml
import jinja2
from aiogram import types


def load_yaml_files(*paths: str, loader: yaml.Loader) -> Dict[str, Any]:
    yaml_files = {}
    for path in paths:
        with open(path) as file:
            yaml_content = yaml.load(stream=file, Loader=loader)
        yaml_files[path] = yaml_content
    return yaml_files


def get_template_constructor(
    jinja2_env: Optional[jinja2.Environment] = None
) -> Callable[[yaml.Loader, yaml.Node], jinja2.Template]:

    def template_constructor(loader: yaml.Loader, node: yaml.Node) -> jinja2.Template:
        if jinja2_env is not None:
            return jinja2_env.from_string(source=node.value)
        else:
            return jinja2.Template(source=node.value)

    return template_constructor


def button_from_source(button: Union[str, Dict[str, Any]]) -> types.KeyboardButton:
    if isinstance(button, str):
        return types.KeyboardButton(text=button)
    elif isinstance(button, dict):
        return types.KeyboardButton(**button)
    else:
        assert False


def reply_markup_constructor(loader: yaml.Loader, node: yaml.Node) -> types.ReplyKeyboardMarkup:
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    source = loader.construct_sequence(node=node, deep=True)
    for item in source:
        if isinstance(item, list):
            reply_markup.row(
                *[
                    button_from_source(button) for button in item
                ]
            )
        elif isinstance(item, dict):
            reply_markup.add(types.KeyboardButton(**item))
        elif isinstance(item, str):
            reply_markup.add(types.KeyboardButton(text=item))
        else:
            assert False

    return reply_markup


def get_callback_string_constructor(max_bytes: int = 64) -> Callable[[yaml.Loader, yaml.Node], str]:

    def callback_string_constructor(loader: yaml.Loader, node: yaml.Node) -> str:
        value = node.value
        if not isinstance(value, str):
            value = json.dumps(
                obj=node.value,
                ensure_ascii=False,
                separators=(',', ':'),
                default=str,
            )

        length = len(value.encode())
        if length > max_bytes:
            raise ValueError(f'callback of {value} is too long, {length} > {max_bytes}')
        else:
            return value

    return callback_string_constructor


def inline_keyboard_constructor(loader: yaml.Loader, node: yaml.Node) -> types.ReplyKeyboardMarkup:
    inline_keyboard = types.InlineKeyboardMarkup()
    source = loader.construct_sequence(node=node, deep=True)
    for item in source:
        if isinstance(item, list):
            inline_keyboard.row(
                *[
                    types.InlineKeyboardButton(**button)
                    for button in item
                ]
            )
        elif isinstance(item, dict):
            inline_keyboard.add(types.InlineKeyboardButton(**item))
        else:
            assert False

    return inline_keyboard
