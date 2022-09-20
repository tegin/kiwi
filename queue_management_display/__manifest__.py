# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Queue Management Display",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "website": "https://github.com/tegin/kiwi",
    "author": "CreuBlanca",
    "depends": ["queue_management", "bus", "base_sparse_field"],
    "data": [
        "views/queue_token_location.xml",
        "views/queue_location.xml",
        "security/ir.model.access.csv",
        "views/queue_display.xml",
        "templates/assets.xml",
    ],
    "qweb": ["static/src/xml/queue_management.xml"],
    "demo": [],
}
