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
from pluggy import HookspecMarker


hookspec = HookspecMarker("kadi")


@hookspec
def kadi_register_blueprints(app):
    """Hook for registering blueprints.

    :param app: The application object.
    """


@hookspec
def kadi_template_index_before():
    """Template hook for prepending HTML snippets to the index page.

    Used in :file:`modules/main/templates/main/index.html`.
    """


@hookspec
def kadi_template_home_before():
    """Template hook for prepending HTML snippets to the home page.

    Used in :file:`modules/main/templates/main/home.html`.
    """


@hookspec
def kadi_get_translations_paths():
    """Hook for collecting translation folders.

    Note that currently translations of the main application and plugins are simply
    merged together. Translations of the main application will always take precedence.
    """


@hookspec
def kadi_register_oauth2_providers(registry):
    """Hook for registering OAuth2 providers.

    Currently, only the authorization code grant is supported, which a provider must
    support as well. Each provider needs to register itself to the given registry
    provided by the Authlib library using a unique name.

    :param registry: The OAuth2 provider registry.
    """


@hookspec
def kadi_get_oauth2_providers():
    """Hook for collecting OAuth2 providers.

    The providers have to be returned as either a single dictionary or a list of
    dictionaries, containing various information about the provider, but at least the
    unique name that was also used to register it.

    For example:

    .. code-block:: python3

        {
            "name": "my_provider",
            "title": "My provider",
            "website": "https://example.com",
            "description": "My provider.",
        }
    """
