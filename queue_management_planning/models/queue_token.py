# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class QueueToken(models.Model):

    _inherit = "queue.token"

    arrival_date = fields.Datetime(readonly=True)

    def action_check_token(self):
        self.ensure_one()
        if not self.arrival_date:
            self._check_token()
        elif self.arrival_date:
            self._uncheck_token()

    def _check_token(self):
        self.write({"arrival_date": fields.Datetime.now()})

    def _uncheck_token(self):
        self.write({"arrival_date":False})

