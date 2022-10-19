# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class QueueTokenLocation(models.Model):

    _inherit = "queue.token.location"
    last_call = fields.Datetime(readonly=True)
    expected_location_id = fields.Many2one("queue.location")

    def action_call(self):
        self.ensure_one()
        if self.expected_location_id and not self.env.context.get(
            "ignore_expected_location"
        ):
            action = self.env.ref(
                "queue_management_display.queue_token_location_force_call_act_window"
            ).read()[0]
            action["res_id"] = self.id
            action["context"] = self.env.context
            return action
        location = self.env["queue.location"].browse(
            self.env.context.get("location_id")
        )
        self._action_call(location)

    def _action_call(self, location):
        if not location:
            raise ValidationError(_("Location is required"))
        if self.token_id.state != "in-progress":
            raise ValidationError(_("You cannot call a non draft item"))
        if self.group_id and location not in self.group_id.location_ids:
            raise ValidationError(_("Location is not in the assigned group"))
        if self.location_id and self.location_id != location:
            raise ValidationError(
                _(
                    "You cannot call a token from a different location \
                    than the assigned location"
                )
            )
        any_assing_token = self.search(
            [("state", "=", "in-progress"), ("location_id", "=", location.id)]
        )
        previous_call_token = self.search(
            [("expected_location_id", "=", location.id), ("state", "=", "draft")]
        )
        if previous_call_token:
            previous_call_token.write({"expected_location_id": False})
        if any_assing_token:
            raise ValidationError(
                _("There is a token assigned in this location. PLease, close it first.")
            )

        # We cannot call an already assigned token
        for record in self:
            if self.search(
                [("token_id", "=", record.token_id.id), ("state", "=", "in-progress")],
                limit=1,
            ):
                raise ValidationError(
                    _(
                        "Token %s already has an assigned location.\
                             You cannot call it, close it first"
                    )
                    % record.token_id.name
                )
        self.write(self._call_action_vals(location))
        action = self._add_action_log("call", location)
        self.env["bus.bus"].sendmany(
            self._get_channel_call_notifications(location, action)
        )

    def _get_channel_call_notifications(self, location, action):
        notifications = []
        for display in location.display_ids:
            if display.kind == "notification":
                notifications.append(
                    (
                        ("%s_%s" % (display._name, display.id)),
                        {
                            "id": self.id,
                            "token": self.token_id.name,
                            "last_call": fields.Datetime.to_string(action.date),
                            "location": location.name,
                        },
                    )
                )
        return notifications

    def _call_action_vals(self, location):
        return {
            "expected_location_id": location.id,
            "last_call": fields.Datetime.now(),
        }
