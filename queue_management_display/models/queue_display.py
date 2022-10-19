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
    kind = fields.Selection(
        [("notification", "Notification screen"), ("control", "Control Screen")],
        default="notification",
        required=True,
    )
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
            </div>
        """

    def open_display(self):
        """
        Open XML id depending on wich type os self.kind you have choosed.
        """
        self.ensure_one()
        action = self.env.ref(
            "queue_management_display.queue_display_fullscreen_%s_act_window"
            % self.kind
        ).read()[0]
        action["res_id"] = self.id
        return action

    @api.depends()
    def _compute_items(self):
        for record in self:
            record.items = {"tokens": record._get_display_tokens()}

    def _get_display_tokens(self):
        actions = self.env["queue.token.location.action"].search(
            [
                ("location_id", "in", self.location_ids.ids),
                ("date", ">", fields.Datetime.now() + timedelta(hours=-self.max_time),),
            ],
            order="date desc",
        )
        token_locations = self.env["queue.token.location"]
        final_actions = self.env["queue.token.location.action"]
        for action in actions:
            if action.token_location_id not in token_locations:
                token_locations |= action.token_location_id
                final_actions |= action
                if len(token_locations) >= self.show_items:
                    break
        return [
            {
                "id": action.token_location_id.id,
                "token": action.token_id.name,
                "location": action.location_id.name,
                "last_call": fields.Datetime.to_string(action.date),
            }
            for action in final_actions
        ]
