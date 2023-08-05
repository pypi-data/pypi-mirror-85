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
from authlib.integrations.flask_client import OAuth
from flask_login import current_user

from kadi.ext.db import db
from kadi.lib.oauth.core import update_oauth2_token


def _update_token(name, token, access_token=None, refresh_token=None):
    oauth2_token = None

    if access_token:
        oauth2_token = current_user.oauth2_tokens.filter_by(
            name=name, access_token=access_token
        ).first()
    elif refresh_token:
        oauth2_token = current_user.oauth2_tokens.filter_by(
            name=name, refresh_token=refresh_token
        ).first()

    if oauth2_token is not None:
        update_oauth2_token(
            oauth2_token,
            access_token=token.get("access_token"),
            refresh_token=token.get("refresh_token"),
            expires_at=token.get("expires_at"),
            expires_in=token.get("expires_in"),
        )
        db.session.commit()


oauth = OAuth(update_token=_update_token)
