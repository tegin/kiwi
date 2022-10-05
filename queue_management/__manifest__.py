# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Queue Management",
    "summary": """
        Management of queue""",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca,Odoo Community Association (OCA)",
    "website": "https://github.com/tegin/kiwi",
    "depends": [],
    "category": "Queue management",
    "data": [
        "security/security.xml",
        "views/menu.xml",
        "views/queue_token_location.xml",
        "data/ir_sequence_data.xml",
        "data/ir_cron.xml",
        "views/queue_location_group.xml",
        "views/queue_location.xml",
        "security/ir.model.access.csv",
        "views/queue_token.xml",
        "views/queue_token_location_action.xml",
        "reports/queue_token_location_reporting.xml",
        "templates/assets.xml",
    ],
    "demo": ["demo/security.xml", "demo/data.xml"],
}
