# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import api, fields, models


class QueueLocation(models.Model):
    """'Data model that represents the location of the places where
    it's necessary a queue management."""

    _name = "queue.location"
    _description = "Queue Location"

    name = fields.Char(required=True)
    group_ids = fields.Many2many("queue.location.group")
    token_location_count = fields.Integer(compute="_compute_token_location_count")
    last_token_assigned = fields.Datetime(compute="_compute_token_location_count")

    token_location_ids = fields.Many2many(
        "queue.token.location", compute="_compute_token_location"
    )
    current_token_location_id = fields.Many2one(
        "queue.token.location", compute="_compute_current_token"
    )
    current_token_id = fields.Many2one("queue.token", compute="_compute_current_token")
    token_location_done_ids = fields.Many2many(
        "queue.token.location", compute="_compute_token_location_done"
    )
    token_location_cancelled_ids = fields.Many2many(
        "queue.token.location", compute="_compute_token_location_cancelled"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [("waiting", "Waiting"), ("working", "Working"), ("warning", "Warning")],
        compute="_compute_state",
    )

    @api.depends()
    def _compute_current_token(self):
        for record in self:
            record.current_token_location_id = self.env["queue.token.location"].search(
                [("location_id", "=", record.id), ("state", "=", "in-progress")],
                limit=1,
            )
            record.current_token_id = record.current_token_location_id.token_id

    @api.depends()
    def _compute_token_location_count(self):
        for record in self:
            record.token_location_count = len(record.token_location_ids)
            record.last_token_assigned = (
                self.env["queue.token.location"]
                .search(
                    [
                        ("location_id", "=", record.id),
                        ("state", "in", ["in-progress", "done"]),
                    ],
                    limit=1,
                    order="assign_date desc",
                )
                .assign_date
            )

    @api.depends("group_ids")
    def _compute_token_location(self):
        """
        Fill the token_location_ids field with the tokens and theirs location/group.
        """
        for record in self:
            record.token_location_ids = self.env["queue.token.location"].search(
                [("state", "=", "in-progress"), ("location_id", "=", record.id)]
            ) | self.env["queue.token.location"].search(
                record._get_token_location_domain(),
                order=record._get_token_location_order(),
            )

    def _get_token_location_order(self):
        """
        We will modify this value when planning is installed
        """
        return "create_date asc"

    def _get_token_location_domain(self):
        return [
            ("state", "=", "draft"),
            "|",
            ("location_id", "=", self.id),
            ("group_id", "in", self.group_ids.ids),
        ]

    @api.depends()
    def _compute_token_location_done(self):
        """
        Fill the token_status_done field with the tokens and theirs location/group.
        """
        for record in self:
            record.token_location_done_ids = self.env["queue.token.location"].search(
                [
                    ("state", "=", "done"),
                    ("location_id", "=", record.id),
                    (
                        "leave_date",
                        ">=",
                        fields.Datetime.now() + timedelta(days=-2),
                    ),
                ],
            )

    @api.depends()
    def _compute_token_location_cancelled(self):
        """
        Fill the token_location_cancelled field with the tokens and theirs location/group.
        """
        for record in self:
            record.token_location_cancelled_ids = self.env[
                "queue.token.location"
            ].search(
                [
                    ("state", "=", "cancelled"),
                    ("location_id", "=", record.id),
                    (
                        "cancel_date",
                        ">=",
                        fields.Datetime.now() + timedelta(days=-2),
                    ),
                ],
            )

    @api.depends()
    def _compute_state(self):
        """
        We will get a different color according to the following:
        green: It is working (it has an assigned token)
        orange: It should be working (some tokens are waiting but it has nothing assigned)
        blue: It is not working (no tokens waiting, nothing assigned)
        """
        for record in self:
            if record.current_token_id:
                record.state = "working"
            elif record.token_location_ids:
                record.state = "warning"
            else:
                record.state = "waiting"

    def action_reload(self):
        self.ensure_one()
        return {"type": "ir.actions.act_view_reload"}

    def access_location(self):
        return self.get_formview_action()
