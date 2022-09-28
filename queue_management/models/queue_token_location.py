# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class QueueTokenLocation(models.Model):
    """

    Data model that represents the relation between a token with its location/group.
    Also, we can change the token's state (assing/leave methods).
    """

    _name = "queue.token.location"
    _description = "Queue Token-Location"

    group_id = fields.Many2one("queue.location.group")
    location_id = fields.Many2one("queue.location")
    token_id = fields.Many2one("queue.token", required=True)
    state = fields.Selection(
        [
            ("draft", "Pending"),
            ("in-progress", "In Progress"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        required=True,
        readonly=True,
    )

    active = fields.Boolean(default=True)

    assign_date = fields.Datetime(readonly=True)
    assign_user_id = fields.Many2one("res.users", readonly=True)

    leave_date = fields.Datetime(readonly=True)
    leave_user_id = fields.Many2one("res.users", readonly=True)

    @api.constrains("state", "token_id")
    def _check_token_state(self):
        for record in self:
            if record.state != "in-progress":
                continue
            if self.search(
                [
                    ("id", "!=", record.id),
                    ("token_id", "=", record.token_id.id),
                    ("state", "=", "in-progress"),
                ],
                limit=1,
            ):
                raise ValidationError(
                    _("Token %s already has an assigned location. Close it first")
                    % record.token_id.name
                )

    def action_assign(self):
        self.ensure_one()
        location = self.env["queue.location"].browse(
            self.env.context.get("location_id")
        )
        self._action_assign(location)

    def _action_assign(self, location):
        if not location:
            raise ValidationError(_("Location is required"))
        if self.state != "draft":
            raise ValidationError(_("You cannot assign a non draft item"))
        if self.group_id and location not in self.group_id.location_ids:
            raise ValidationError(_("Location is not in the assigned group"))
        if self.location_id and self.location_id != location:
            raise ValidationError(_("Location is different to the assigned location"))
        # We well leave all previous tokens. We might want to close
        previous_token = self.search(
            [("location_id", "=", location.id), ("state", "=", "in-progress")]
        )
        if previous_token:
            previous_token._action_leave(location)
        self.write(self._assign_action_vals(location))

    def _assign_action_vals(self, location):
        """
        We create this hook in order to change some fields values.
        """
        return {
            "state": "in-progress",
            "location_id": location.id,
            "assign_date": fields.Datetime.now(),
            "assign_user_id": self.env.user.id,
        }

    def action_leave(self):
        self.ensure_one()
        location = self.env["queue.location"].browse(
            self.env.context.get("location_id")
        )
        self._action_leave(location)

    def _action_leave(self, location):
        if self.state != "in-progress":
            raise ValidationError(_("You cannot close a not assigned item"))
        if not location:
            raise ValidationError(_("Location is required"))
        if location != self.location_id:
            raise ValidationError(_("Location is not the same"))
        self.write(self._action_leave_vals(location))

    def _action_leave_vals(self, location):
        return {
            "state": "done",
            "leave_date": fields.Datetime.now(),
            "leave_user_id": self.env.user.id,
        }

    def action_cancel(self):
        self.ensure_one()
        location = self.env["queue.location"].browse(
            self.env.context.get("location_id")
        )
        self._action_cancel(location)

    def _action_cancel(self, location):
        if self.state not in ["draft", "in-progress"]:
            raise ValidationError(_("You cannot cancelled an already cancelled item"))
        if (
            self.group_id
            and location not in self.group_id.location_ids
            and not self.env.user.has_group("queue_management.group_queue_planner")
        ):
            raise ValidationError(_("Location is not in the assigned group"))
        if (
            self.location_id
            and self.location_id != location
            and not self.env.user.has_group("queue_management.group_queue_planner")
        ):
            raise ValidationError(_("Location is different to the assigned location"))

        self.write(self._action_cancel_vals(location))

    def _action_cancel_vals(self, location):
        result = {
            "state": "cancelled",
        }
        if self.group_id:
            result["location_id"] = False
        return result

    def action_back_to_draft(self):
        self.ensure_one()
        location = self.env["queue.location"].browse(
            self.env.context.get("location_id")
        )
        self._action_back_to_draft(location)

    def _action_back_to_draft(self, location):
        if self.state != "in-progress":
            raise ValidationError(_("You cannot return to draft a not assigned item"))
        if not location:
            raise ValidationError(_("Location is required"))
        if location != self.location_id:
            raise ValidationError(_("Location is not the same"))
        self.write(self._assign_back_to_draft_vals(location))

    def _assign_back_to_draft_vals(self, location):
        """
        We create this hook in order to change some fields values.
        """
        result = {
            "state": "draft",
        }
        if self.group_id:
            result["location_id"] = False
        return result

    def action_reopen_cancelled(self):
        self.ensure_one()
        location = self.env["queue.location"].browse(
            self.env.context.get("location_id")
        )
        self._action_reopen_cancelled(location)

    def _action_reopen_cancelled(self, location):
        if self.state != "cancelled":
            raise ValidationError(_("You cannot reopen a reopened item again"))

        if not self.location_id and not self.group_id:
            raise ValidationError(_("Location or group is required"))
        self.write(self._assign_reopen_cancelled_vals(location))

    def _assign_reopen_cancelled_vals(self, location):
        """
        We create this hook in order to change some fields values.
        """
        result = {
            "state": "draft",
        }

        return result
