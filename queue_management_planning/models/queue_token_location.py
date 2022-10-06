# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class QueueTokenLocation(models.Model):

    _inherit = "queue.token.location"

    expected_date = fields.Datetime()
