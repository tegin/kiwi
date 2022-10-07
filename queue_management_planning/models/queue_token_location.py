# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class QueueTokenLocation(models.Model):

    _inherit = "queue.token.location"

    expected_date = fields.Datetime()
    planning_date = fields.Datetime(compute="_compute_planning_date", store=True)
    arrival_date = fields.Datetime(related="token_id.arrival_date")

    @api.depends("expected_date", "token_id.arrival_date")
    def _compute_planning_date(self):
        for record in self:
            record.planning_date = record.expected_date or record.token_id.arrival_date
