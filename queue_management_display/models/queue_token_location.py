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
        location = self.env["queue.location"].browse(
            self.env.context.get("location_id")
        )
        self._action_call(location)

    def _action_call(self, location):
        if not location:
            raise ValidationError(_("Location is required"))
        if self.state != "draft":
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

        previous_call_token = self.search(
            [("expected_location_id", "=", location.id), ("state", "=", "draft")]
        )
        if previous_call_token:
            previous_call_token.write({"expected_location_id": False})

        self.write(self._call_action_vals(location))
        self.env["bus.bus"].sendmany(self._get_channel_notifications(location))

    def _get_channel_notifications(self, location):
        notifications = []
        for display in location.display_ids:
            notifications.append(
                (
                    ("%s_%s" % (display._name, display.id)),
                    {
                        "id": self.id,
                        "token": self.token_id.name,
                        "last_call": fields.Datetime.to_string(self.last_call),
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
