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
from flask import render_template
from flask_login import current_user

from .utils import add_link as _add_link
from .utils import remove_link as _remove_link
from kadi.ext.db import db
from kadi.lib.api.core import json_error_response
from kadi.lib.api.core import json_response
from kadi.lib.exceptions import KadiPermissionError
from kadi.modules.accounts.models import User
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.permissions.utils import add_role as _add_role
from kadi.modules.permissions.utils import remove_role as _remove_role


def add_link(relationship, resource, user=None):
    """Convenience function to link two resources together.

    For ease of use in API endpoints. Uses :func:`kadi.lib.resources.utils.add_link`.

    :param relationship: The many-to-many relationship to append the resource to.
    :param resource: The resource to link, an instance of :class:`.Record` or
        :class:`.Collection`.
    :param user: (optional) The user performing the operation. Defaults to the current
        user.
    :return: A JSON response depending on the success of the operation.
    """
    user = user if user is not None else current_user

    try:
        if _add_link(relationship, resource, user=user):
            db.session.commit()
            return json_response(201)

        return json_error_response(409, description="Link already exists.")

    except KadiPermissionError as e:
        return json_error_response(403, description=str(e))


def remove_link(relationship, resource, user=None):
    """Convenience function to remove the link between two resources.

    For ease of use in API endpoints. Uses :func:`kadi.lib.resources.utils.remove_link`.

    :param relationship: The many-to-many relationship to remove the resource from.
    :param resource: The resource to remove, an instance of :class:`.Record` or
        :class:`.Collection`.
    :param user: (optional) The user performing the operation. Defaults to the current
        user.
    :return: A JSON response depending on the success of the operation.
    """
    user = user if user is not None else current_user

    try:
        if _remove_link(relationship, resource, user=user):
            db.session.commit()
            return json_response(204)

        return json_error_response(404, description="Link does not exist.")

    except KadiPermissionError as e:
        return json_error_response(403, description=str(e))


def add_role(subject, resource, role_name):
    """Convenience function to add an existing role to a user or group.

    For ease of use in API endpoints. Uses
    :func:`kadi.modules.permissions.utils.add_role`.

    :param subject: The user or group.
    :param resource: The resource the role refers to, an instance of :class:`.Record`,
        :class:`.Collection`, :class:`.Group` or :class:`.Template`.
    :param role_name: The name of the role to add.
    :return: A JSON response depending on the success of the operation.
    """
    try:
        if _add_role(subject, resource.__tablename__, resource.id, role_name):
            db.session.commit()
            return json_response(201)

        return json_error_response(
            409, description="A role for that resource already exists."
        )

    except ValueError:
        return json_error_response(
            400, description="A role with that name does not exist."
        )


def remove_role(subject, resource):
    """Convenience function to remove an existing role of a user or group.

    For ease of use in API endpoints. Uses
    :func:`kadi.modules.permissions.utils.remove_role`. If the given subject is the
    creator of the given resource, the role will not be removed.

    :param subject: The user or group.
    :param resource: The resource the role refers to, an instance of :class:`.Record`,
        :class:`.Collection`, :class:`.Group` or :class:`.Template`.
    :return: A JSON response depending on the success of the operation.
    """
    if isinstance(subject, User) and subject == resource.creator:
        return json_error_response(409, description="Cannot remove the creator's role.")

    if _remove_role(subject, resource.__tablename__, resource.id):
        db.session.commit()
        return json_response(204)

    return json_error_response(404, description="Role does not exist.")


def change_role(subject, resource, role_name):
    """Convenience function to change an existing role of a user or group.

    For ease of use in API endpoints. If the given subject is the creator of the given
    resource, the role will not be changed. Uses
    :func:`kadi.modules.permissions.utils.remove_role` and
    :func:`kadi.modules.permissions.utils.add_role`.

    :param subject: The user or group.
    :param resource: The resource the role refers to, an instance of :class:`.Record`,
        :class:`.Collection`, :class:`.Group` or :class:`.Template`.
    :param role_name: The name of the role to exchange.
    :return: A JSON response depending on the success of the operation.
    """
    if isinstance(subject, User) and subject == resource.creator:
        return json_error_response(409, description="Cannot change the creator's role.")

    if _remove_role(subject, resource.__tablename__, resource.id):
        try:
            _add_role(subject, resource.__tablename__, resource.id, role_name)
            db.session.commit()
            return json_response(200)

        except ValueError:
            return json_error_response(
                400, description="A role with that name does not exist."
            )

    return json_error_response(404, description="Role does not exist.")


def get_selected_resources(
    model, page=1, term="", exclude=None, actions=None, user=None
):
    """Convenience function to search resources for use in dynamic selections.

    For ease of use in API endpoints. Used in conjunction with "Select2" to dynamically
    populate and search through dropdown menus or similar fields.

    :param model: The resource model to search, one of :class:`.Record`,
        :class:`.Collection` or :class:`.Group`.
    :param page: (optional) The current page.
    :param term: (optional) The search term. Will be used to search the title and
        identifier of the resource (case insensitive).
    :param exclude: (optional) A list of one or multiple resource IDs to exclude in the
        results. Defaults to an empty list.
    :param actions: (optional) One or multiple actions to restrict the returned
        resources to specific permissions of the given user, see :class:`.Permission`.
        Defaults to ``["read"]``.
    :param user: (optional) The user performing the search. Defaults to the current
        user.
    :return: A JSON response containing the results in the following form, assuming the
        search results consist of a single :class:`.Record`:

        .. code-block:: js

            {
                "results": [
                    {
                        "id": 1,
                        "text": "@sample-record-1",
                        "body": "<optional HTML body>",
                    }
                ],
                "pagination": {"more": false},
            }
    """
    exclude = exclude if exclude is not None else []
    actions = actions if actions is not None else ["read"]
    user = user if user is not None else current_user

    queries = []
    for action in actions:
        resources_query = get_permitted_objects(user, action, model.__tablename__)

        if resources_query:
            queries.append(resources_query)

    paginated_resources = (
        queries[0]
        .intersect(*queries[1:])
        .filter(
            db.or_(model.title.ilike(f"%{term}%"), model.identifier.ilike(f"%{term}%")),
            model.id.notin_(exclude),
            model.state == "active",
        )
        .order_by(model.title)
        .paginate(page, 10, False)
    )

    data = {"results": [], "pagination": {"more": paginated_resources.has_next}}
    for resource in paginated_resources.items:
        data["results"].append(
            {
                "id": resource.id,
                "text": "@" + resource.identifier,
                "body": render_template(
                    "snippets/resources/select.html", resource=resource
                ),
            }
        )

    return json_response(200, data)
