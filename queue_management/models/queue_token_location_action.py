# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class QueueTokenLocationAction(models.Model):

    _name = "queue.token.location.action"
    _description = "Queue_token_location_action"  # TODO
    _log_access = False

    token_id = fields.Many2one("queue.token", required=True, readonly=True)
    token_location = fields.Many2one("queue.token.location")
    location_id = fields.Many2one("queue.location", readonly=True)
    user_id = fields.Many2one("res.users", readonly=True)
    date = fields.Datetime(readonly=True)
    action = fields.Selection(
        [
            ("cancel", "Cancel"),
            ("assign", "Assign"),
            ("leave", "Leave"),
            ("reopen", "Reopen"),
            ("back_to_draft" , "Back to draft")

        ]
    )
