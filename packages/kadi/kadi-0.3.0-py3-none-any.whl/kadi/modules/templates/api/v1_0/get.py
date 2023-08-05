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
from functools import partial

from flask import abort
from flask_login import current_user
from flask_login import login_required

from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import json_response
from kadi.lib.api.core import scopes_required
from kadi.lib.api.utils import create_pagination_data
from kadi.lib.api.utils import status
from kadi.lib.conversion import strip
from kadi.lib.web import paginated
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.accounts.models import User
from kadi.modules.groups.models import Group
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.permissions.core import has_permission
from kadi.modules.permissions.core import permission_required
from kadi.modules.permissions.models import Role
from kadi.modules.permissions.schemas import GroupRoleSchema
from kadi.modules.permissions.schemas import UserRoleSchema
from kadi.modules.permissions.utils import get_group_roles
from kadi.modules.permissions.utils import get_object_roles
from kadi.modules.permissions.utils import get_user_roles
from kadi.modules.templates.models import Template
from kadi.modules.templates.schemas import TemplateSchema


route = partial(bp.route, methods=["GET"])


@route("/templates")
@login_required
@scopes_required("template.read")
@paginated
@qparam(
    "filter",
    "",
    parse=strip,
    description="A query to filter the templates by their title or identifier.",
)
@status(
    200,
    "Return a paginated list of templates, sorted by last modification date in"
    " descending order.",
)
def get_templates(page, per_page, qparams):
    """Get all templates."""
    paginated_templates = (
        get_permitted_objects(current_user, "read", "template")
        .filter(
            db.or_(
                Template.title.ilike(f"%{qparams['filter']}%"),
                Template.identifier.ilike(f"%{qparams['filter']}%"),
            )
        )
        .order_by(Template.last_modified.desc())
        .paginate(page, per_page, False)
    )

    data = {
        "items": TemplateSchema(many=True).dump(paginated_templates.items),
        "_actions": {"new_template": url_for("api.new_template")},
        **create_pagination_data(
            paginated_templates.total, page, per_page, "api.get_templates", **qparams
        ),
    }

    return json_response(200, data)


@route("/templates/<int:id>")
@permission_required("read", "template", "id")
@scopes_required("template.read")
@status(200, "Return the template.")
def get_template(id):
    """Get the template specified by the given *id*."""
    template = Template.query.get_or_404(id)
    return json_response(200, TemplateSchema().dump(template))


@route("/templates/identifier/<identifier:identifier>")
@login_required
@scopes_required("template.read")
@status(200, "Return the template.")
def get_template_by_identifier(identifier):
    """Get the template specified by the given *identifier*."""
    template = Template.query.filter_by(identifier=identifier).first_or_404()

    if not has_permission(current_user, "read", "template", object_id=template.id):
        abort(403)

    return json_response(200, TemplateSchema().dump(template))


@route("/templates/<int:id>/roles/users")
@permission_required("read", "template", "id")
@scopes_required("template.read", "user.read")
@paginated
@qparam("exclude", [], multiple=True, type=int, description="User IDs to exclude.")
@status(
    200,
    "Return a paginated list of user roles, sorted by role name and then by user ID in"
    " ascending order. The creator will always be listed first.",
)
def get_template_user_roles(id, page, per_page, qparams):
    """Get the user roles of the template specified by the given *id*."""
    template = Template.query.get_or_404(id)

    when = []
    for index, role in enumerate(get_object_roles("template")):
        when.append((role["name"], index))

    paginated_user_roles = (
        get_user_roles("template", object_id=id)
        .filter(User.id.notin_(qparams["exclude"]))
        .order_by(
            (User.id == template.creator.id).desc(),
            db.case(when, value=Role.name).desc(),
            User.id,
        )
        .paginate(page, per_page, False)
    )

    data = {
        "items": UserRoleSchema(obj=template).dump_from_iterable(
            paginated_user_roles.items
        ),
        **create_pagination_data(
            paginated_user_roles.total,
            page,
            per_page,
            "api.get_template_user_roles",
            id=template.id,
        ),
    }

    return json_response(200, data)


@route("/templates/<int:id>/roles/groups")
@permission_required("read", "template", "id")
@scopes_required("template.read", "group.read")
@paginated
@status(
    200,
    "Return a paginated list of group roles, sorted by role name and then by group ID"
    " in ascending order.",
)
def get_template_group_roles(id, page, per_page):
    """Get the group roles of the template specified by the given *id*."""
    template = Template.query.get_or_404(id)

    when = []
    for index, role in enumerate(get_object_roles("template")):
        when.append((role["name"], index))

    group_ids = get_permitted_objects(current_user, "read", "group").with_entities(
        Group.id
    )

    # Already filtered for active groups.
    paginated_group_roles = (
        get_group_roles("template", object_id=id)
        .filter(Group.id.in_(group_ids))
        .order_by(db.case(when, value=Role.name).desc(), Group.id)
        .paginate(page, per_page, False)
    )

    data = {
        "items": GroupRoleSchema(obj=template).dump_from_iterable(
            paginated_group_roles.items
        ),
        **create_pagination_data(
            paginated_group_roles.total,
            page,
            per_page,
            "api.get_template_group_roles",
            id=template.id,
        ),
    }

    return json_response(200, data)
