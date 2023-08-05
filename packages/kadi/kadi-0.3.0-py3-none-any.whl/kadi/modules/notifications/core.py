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

from kadi.ext.db import db
from kadi.lib.tasks.models import Task
from kadi.modules.records.models import TemporaryFile


def create_notification_data(notification):
    """Create a notification suitable for presenting to a client.

    :param notification: A :class:`.Notification` object, currently only of type
        ``"task_status"``.
    :return: A tuple containing the title and the HTML body of the notification.
    """
    title = body = notification.name

    if notification.name == "task_status":
        task = Task.query.get(notification.data["task_id"])

        if task.name == "kadi.records.package_files":
            title = "Packaging files"

            if task.state == "running":
                body = render_template(
                    "notifications/snippets/packaging_files_running.html",
                    progress=task.progress,
                )
            elif task.state == "success":
                temporary_file = TemporaryFile.query.get(
                    task.result["temporary_file_id"]
                )

                if (
                    not temporary_file
                    or temporary_file.state != "active"
                    or temporary_file.record.state != "active"
                ):
                    body = "The download link has expired."
                else:
                    body = render_template(
                        "notifications/snippets/packaging_files_success.html",
                        temporary_file=temporary_file,
                    )
            else:
                body = "Error while packaging files."

        if task.state == "pending":
            body = "Waiting for available resources..."

        title = f"{title} ({task.state})"

    return title, body


def dismiss_notification(notification):
    """Dismiss a notification.

    If the notification is of type "task_status", the referenced task will be revoked as
    well.

    :param notification: The :class:`.Notification` to dismiss.
    """
    if notification.name == "task_status":
        task = Task.query.get(notification.data["task_id"])
        task.revoke()

    db.session.delete(notification)
