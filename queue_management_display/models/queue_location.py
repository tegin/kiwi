# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class QueueLocation(models.Model):

    _inherit = "queue.location"

    display_ids = fields.Many2many("queue.display")
