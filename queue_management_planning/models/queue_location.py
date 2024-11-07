# Copyright 2023 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class QueueLocation(models.Model):

    _inherit = "queue.location"

    def _get_token_location_order(self):
        order = super()._get_token_location_order()
        return "planning_date asc, " + order
