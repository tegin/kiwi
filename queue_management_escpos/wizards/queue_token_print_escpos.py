# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class QueueTokenPrintEscpos(models.TransientModel):

    _name = "queue.token.print.escpos"
    _description = "token escpos"

    token_id = fields.Many2one("queue.token", required=True)
    printer_id = fields.Many2one(
        "printing.printer", required=True, default=lambda r: r._default_printer()
    )
    escpos_id = fields.Many2one(
        "printing.escpos",
        required=True,
        domain=[("model_id.model", "=", "queue.token")],
        default=lambda r: r._default_escpos(),
    )

    # TODO: Add defaults, for printer we can review printer_escpos/wizards/....py

    @api.model
    def _default_printer(self):
        printers = self.env["printing.printer"].search(
            [("id", "=", self.env.context.get("printer_escpos_id"))]
        )
        if not printers:
            printers = self.env.user.printing_printer_id
        if not printers:
            printers = self.env["printing.printer"].search([])
        if len(printers) == 1:
            return printers[0].id

    @api.model
    def _default_escpos(self):
        escpos = self.env.ref(
            "queue_management_escpos.queue_token_escpos", raise_if_not_found=False
        )

        return escpos and escpos.id

    def print_escpos(self):
        self.ensure_one()
        self.escpos_id.print_escpos(
            self.printer_id, self.token_id,
        )
