# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Queue Management Planning",
    "summary": """
        new module for planning""",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca,Odoo Community Association (OCA)",
    "website": "https://github.com/tegin/kiwi",
    "depends": ["queue_management", "web_view_calendar_list"],
    "data": [
        "views/queue_token.xml",
        "views/queue_token_location.xml",
        "templates/assets.xml",
    ],
    "demo": [],
}
