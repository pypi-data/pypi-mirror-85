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
from flask_login import current_user

from kadi.ext.db import db
from kadi.ext.oauth import oauth
from kadi.lib.exceptions import KadiDecryptionKeyError
from kadi.plugins.core import run_hook


def get_oauth2_token(name, user=None, delete_on_error=False):
    """Get an OAuth2 token of a user by its name.

    :param name: The name of the token.
    :param user: (optional) The user the token belongs to. Defaults to the current user.
    :param delete_on_error: (optional) Flag indicating whether the token should be
        deleted from the database if either the access token or refresh token cannot be
        decrypted due to an invalid decryption key.
    :return: The OAuth2 token or ``None`` if no token can be found or if some either the
        access token or refresh token cannot be decrypted.
    """
    user = user if user is not None else current_user
    oauth2_token_query = user.oauth2_tokens.filter_by(name=name)

    try:
        return oauth2_token_query.first()
    except KadiDecryptionKeyError:
        if delete_on_error:
            oauth2_token_query.delete()

    return None


def get_oauth2_providers(user=None):
    """Get a list of registered and connected OAuth2 providers.

    Uses the ``"kadi_get_oauth2_providers"`` plugin hook.

    :param user: (optional) The user that should be checked for whether they are
        connected with an OAuth2 provider, in which case ``"is_connected"`` will be set
        to ``True`` for the respective provider. Defaults to the current user.
    :return: A list of provider dictionaries in the following form, sorted by whether
        the provider is connected first and the name of the provider second:

        .. code-block:: python3

            [
                {
                    "name": "example",
                    "title": "Example provider",
                    "website": "https://example.com",
                    "description": "An example provider.",
                    "is_connected": True,
                },
            ]
    """
    user = user if user is not None else current_user
    providers = []

    for provider in run_hook("kadi_get_oauth2_providers"):
        provider_name = provider.get("name")

        if provider_name is None or provider_name not in oauth._clients:
            continue

        oauth2_token = get_oauth2_token(provider_name, user=user, delete_on_error=True)
        db.session.commit()

        providers.append(
            {
                "name": provider_name,
                "title": provider.get("title", provider_name),
                "website": provider.get("website", ""),
                "description": provider.get("description", ""),
                "is_connected": oauth2_token is not None,
            }
        )

    return sorted(
        providers, key=lambda provider: (not provider["is_connected"], provider["name"])
    )
