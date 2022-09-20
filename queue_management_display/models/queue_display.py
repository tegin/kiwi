# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import api, fields, models


class QueueDisplay(models.Model):

    _name = "queue.display"
    _description = "Queue Display"  # TODO

    name = fields.Char()
    description = fields.Text()
    location_ids = fields.Many2many("queue.location")
    show_items = fields.Integer(default=10)
    max_time = fields.Float(default=24)  # Time maximum
    shiny_time = fields.Float(default=0.05)  # By default, 3 minutes
    items = fields.Serialized(compute="_compute_items")
    qweb = fields.Text(default=lambda r: r._default_qweb())
    css = fields.Text()

    def _default_qweb(self):
        return """
        <div class="row o_queue_management_display_header">
            <div class="col-2 queue_logo">
                <img t-attf-src="/logo.png?company=#{company_id}" t-attf-alt="#{company}" />
            </div>
            <div class="col-8 o_queue_management_display_header_title">
                <h1 t-esc="data.description" />
            </div>
            <div class="col-2 o_queue_management_display_header_datetime">
                <div class="o_queue_management_display_header_clock" />
            </div>
        </div>
        <div class="row o_queue_management_display_body">
            <div class="col-4 o_queue_management_display_body_content">
                <div class="o_queue_management_display_body_content_header row">
                    <t t-call="queue_management_display.queue_display_token">
                        <t t-set="token">Token</t>
                        <t t-set="location">Location</t>
                    </t>

                </div>
                <div class="o_queue_management_display_body_content_body row" />
            </div>
            <div class="col-8  o_queue_management_display_advertising">
                <!-- TODO: Add your video here -->
            </div>
        </div>
        <div class="row o_queue_management_display_footer">
            <!-- TODO: Add Your Social Media data here -->
        </div>"""

    def open_display(self):
        self.ensure_one()
        action = self.get_formview_action()
        action["name"] = self.display_name
        action["views"] = [
            (
                self.env.ref(
                    "queue_management_display.queue_display_form_queue_display_view"
                ).id,
                "form",
            )
        ]
        return action

    @api.depends()
    def _compute_items(self):
        for record in self:
            record.items = {
                "tokens": [
                    {
                        "id": token.id,
                        "token": token.token_id.name,
                        "location": token.expected_location_id.name,
                        "last_call": fields.Datetime.to_string(token.last_call),
                    }
                    for token in record._get_display_tokens()
                ]
            }

    def _get_display_tokens(self):
        return self.env["queue.token.location"].search(
            [
                ("expected_location_id", "in", self.location_ids.ids),
                (
                    "last_call",
                    ">",
                    fields.Datetime.now() + timedelta(hours=-self.max_time),
                ),
            ],
            limit=self.show_items,
            order="last_call desc",
        )
