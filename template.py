"""
   Copyright 2020 Newlogic

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from jinja2 import Environment, FileSystemLoader

import settings

template_env = None


def get_template_env():
    global template_env
    if template_env is None:
        loader = FileSystemLoader(settings.TEMPLATES_DIR)
        template_env = Environment(loader=loader)
    return template_env


def get_template(template_name):
    env = get_template_env()
    return env.get_template(template_name)


def render_from_template(template_name, **kwargs):
    return get_template(template_name=template_name).render(**kwargs)


def mm_to_px(value, dpi=300):
    """Convert mm to pixel with PPI / DPI
    pixels = millimeters * ( PPI / 25.4 )

    Args:
        value (_type_): _description_
        dpi (int, optional): _description_. Defaults to 300.
    """
    return value * int(dpi / 25.4)


def to_dpi(value, correction=1):
    input_dpi = 96
    output_dpi = 300
    correction = correction  # fix marginal error on DPI conversion
    ratio = output_dpi / input_dpi
    return int(value) * ratio * correction


def add(value, arg):
    """Add the arg to the value."""
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        try:
            return value + arg
        except Exception:
            return ""


get_template_env().filters["add"] = add
get_template_env().filters["to_dpi"] = to_dpi
get_template_env().filters["mm_to_px"] = mm_to_px
