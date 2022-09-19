# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class QueueToken(models.Model):

    _inherit = "queue.token"

    def action_print_escpos(self):
        self.ensure_one()
        action = self.env.ref(
            "queue_management_escpos.queue_token_print_escpos_act_window"
        ).read()[0]
        action["context"] = {"default_token_id": self.id}
        return action
