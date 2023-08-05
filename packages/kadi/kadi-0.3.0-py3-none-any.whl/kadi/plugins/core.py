# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask import current_app
from jinja2 import Markup


def run_hook(name, _flatten_results=True, **kwargs):
    r"""Run the plugin hook with the given name for all registered plugins.

    :param name: The name of the hook.
    :param _flatten_results: (optional) A bool indicating whether the results (which are
        not ``None``) of each plugin should be flattened into a single, non-nested list.
    :param \**kwargs: Additional keyword arguments that will be passed to the hook.
    :return: The results of all hooks as a list or an empty list if the given hook was
        not found.
    """
    try:
        hook = getattr(current_app.plugin_manager.hook, name)
        results = hook(**kwargs)

        if _flatten_results:
            flattened_results = []

            for result in results:
                if isinstance(result, list):
                    flattened_results += result
                else:
                    flattened_results.append(result)

            results = flattened_results

    except AttributeError:
        results = []

    return results


def template_hook(name, **kwargs):
    r"""Run the plugin hook with the given name inside a template.

    Uses :func:`run_hook` and also joins all results together as a string ready to be
    inserted into a template.

    :param name: The name of the hook.
    :param \**kwargs: Additional keyword arguments that will be passed to the hook.
    :return: The template string or an empty string if the given hook was not found.
    """
    results = run_hook(name, **kwargs)
    return Markup("\n".join(results))


def get_plugin_config(name):
    """Get the configuration of a plugin.

    :param name: The name of the plugin.
    :return: The plugin configuration or an empty dictionary if none could be found or
        none was specified.
    """
    return current_app.config["PLUGIN_CONFIG"].get(name, {})
