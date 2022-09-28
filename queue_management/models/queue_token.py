# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class QueueToken(models.Model):
    """
    Data model that defines the token
    """

    _name = "queue.token"
    _description = "Queue Token"  # TODO

    name = fields.Char(
        required=True, readonly=True, index=True, default=lambda self: _("New")
    )
    location_ids = fields.One2many("queue.token.location", inverse_name="token_id")
    state = fields.Selection(
        [("in-progress", "In Progress"), ("done", "Done")],
        compute="_compute_state",
        store=True,
        index=True,
    )

    active = fields.Boolean(default=True)

    @api.depends("location_ids.state")
    def _compute_state(self):
        for record in self:
            record.state = (
                "done"
                if all(location.state == "done" for location in record.location_ids)
                else "in-progress"
            )

    @api.model_create_multi
    def create(self, mvals):
        """
        Creates the new sequence value of the token when the condition is met.
        """
        for vals in mvals:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self._get_name_sequence(vals)
        return super().create(mvals)

    def _get_name_sequence(self, vals):
        """
        We create this hook in order to fill specific specifications of each implementation
        In some case, we might want to get the sequence from some data, so we keep it this way
        """
        return self.env["ir.sequence"].sudo().next_by_code("queue.token") or _("New")
