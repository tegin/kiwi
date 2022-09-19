# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Queue Management Escpos",
    "summary": """
        module to print tickets""",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca,Odoo Community Association (OCA)",
    "website": "https://github.com/tegin/kiwi",
    "depends": ["queue_management", "printer_escpos"],
    "data": [
        "wizards/queue_token_print_escpos.xml",
        "views/queue_token.xml",
        "data/data.xml",
    ],
    "demo": [],
}
