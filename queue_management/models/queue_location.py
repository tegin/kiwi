# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import api, fields, models


class QueueLocation(models.Model):
    """'Data model that represents the location of the places where
    it's necessary a queue management."""

    _name = "queue.location"
    _description = "Queue Location"

    name = fields.Char(required=True)
    group_ids = fields.Many2many("queue.location.group")
    token_location_ids = fields.Many2many(
        "queue.token.location", compute="_compute_token_location"
    )
    token_location_done_ids = fields.Many2many(
        "queue.token.location", compute="_compute_token_location_done"
    )

    active = fields.Boolean(default=True)

    @api.depends("group_ids")
    def _compute_token_location(self):
        """
        Fill the token_location_ids field with the tokens and theirs location/group.
        """
        for record in self:
            record.token_location_ids = self.env["queue.token.location"].search(
                [("state", "=", "in-progress"), ("location_id", "=", record.id)]
            ) | self.env["queue.token.location"].search(
                [
                    ("state", "=", "draft"),
                    "|",
                    ("location_id", "=", record.id),
                    ("group_id", "in", record.group_ids.ids),
                ]
            )

    @api.depends()
    def _compute_token_location_done(self):
        """
        Fill the token_status_done field with the tokens and theirs location/group.
        """
        for record in self:
            record.token_location_done_ids = self.env["queue.token.location"].search(
                [
                    ("state", "=", "done"),
                    ("location_id", "=", record.id),
                    ("leave_date", ">=", fields.Datetime.now() + timedelta(days=-2),),
                ],
            )
