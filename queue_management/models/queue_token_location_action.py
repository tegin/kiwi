# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class QueueTokenLocationAction(models.Model):

    _name = "queue.token.location.action"
    _description = "Queue_token_location_action"
    _log_access = False
    _order = "date desc"

    token_id = fields.Many2one("queue.token", required=True, readonly=True)
    token_location_id = fields.Many2one("queue.token.location")
    location_id = fields.Many2one("queue.location", readonly=True)
    user_id = fields.Many2one("res.users", readonly=True)
    date = fields.Datetime(readonly=True)
    action = fields.Selection(
        [
            ("cancel", "Cancel"),
            ("assign", "Assign"),
            ("leave", "Leave"),
            ("reopen", "Reopen"),
            ("back_to_draft", "Back to draft"),
        ]
    )

    def name_get(self):
        result = []
        for record in self:
            result.append(
                (
                    record.id,
                    "%s-%s %s"
                    % (record.token_id.name, record.location_id.name, record.action),
                )
            )
        return result
