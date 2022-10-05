# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class QueueTokenLocationAction(models.Model):

    _inherit = "queue.token.location.action"

    action = fields.Selection(selection_add=[("call", "Call")])
