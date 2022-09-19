# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import mock

from odoo.tests.common import TransactionCase

model = "odoo.addons.base_report_to_printer.models.printing_server"


class TestQueueEscpos(TransactionCase):
    def setUp(self):
        super().setUp()
        self.server = self.env["printing.server"].create({})
        self.printer = self.env["printing.printer"].create(
            {
                "name": "Printer",
                "server_id": self.server.id,
                "system_name": "Sys Name",
                "default": True,
                "status": "unknown",
                "status_message": "Msg",
                "model": "res.users",
                "location": "Location",
                "uri": "URI",
            }
        )
        self.token_1 = self.env["queue.token"].create({})

    @mock.patch("%s.cups" % model)
    def test_print_ticket(self, cups):
        action = self.token_1.action_print_escpos()
        wizard = (
            self.env[action["res_model"]]
            .with_context(**action["context"])
            .create({"printer_id": self.printer.id})
        )
        self.assertTrue(wizard.printer_id)
        self.assertEqual(wizard.printer_id, self.printer)
        cups.Connection().printFile.assert_not_called()
        wizard.print_escpos()
        cups.Connection().printFile.assert_called_once()

    @mock.patch("%s.cups" % model)
    def test_printer_not_defined(self, cups):
        pass

    @mock.patch("%s.cups" % model)
    def test_printer_forced(self, cups):
        pass

    @mock.patch("%s.cups" % model)
    def test_printer_context_forced(self, cups):
        pass
