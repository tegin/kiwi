# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class QueueLocationGroup(models.Model):
    """
    Data model that represents the groups of locations
    """

    _name = "queue.location.group"
    _description = "Queue Location Groups"  # TODO

    name = fields.Char(required=True)
    location_ids = fields.Many2many("queue.location",)
