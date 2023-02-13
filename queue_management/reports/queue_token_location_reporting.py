# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools


class QueueTokenLocationReporting(models.Model):

    _name = "queue.token.location.reporting"
    _description = "Queue Token Location Reporting"
    _auto = False
    _rec_name = "assign_date"
    _order = "assign_date desc"

    token_location_id = fields.Many2one("queue.token.location", readonly=True)
    token_id = fields.Many2one("queue.token", required=True, readonly=True)
    location_id = fields.Many2one("queue.location", readonly=True)
    assign_date = fields.Datetime(readonly=True)
    leave_date = fields.Datetime(readonly=True)
    create_date = fields.Datetime(readonly=True)
    time_to_assign = fields.Float(readonly=True, string="Time to assign (hours)")
    time_to_assign_average = fields.Float(
        readonly=True, group_operator="avg", string="Average time to assign (min)"
    )
    time_to_leave = fields.Float(readonly=True, string="Time to leave (hours)")
    time_to_leave_average = fields.Float(
        readonly=True, group_operator="avg", string="Average time to leave (min)"
    )
    time_total = fields.Float(readonly=True, string="Total time (hours)")
    time_total_average = fields.Float(readonly=True, string="Average total time (min)")
    state = fields.Selection("_get_state")

    def _get_state(self):
        return self.env["queue.token.location"]._fields["state"].selection

    @api.model
    def _select(self):
        return """
            SELECT %s
        """ % ",".join(
            "%s as %s" % (value, key) for key, value in self._select_fields().items()
        )

    @api.model
    def _select_fields(self):
        return {
            "id": "qtl.id",
            "token_location_id": "qtl.id",
            "token_id": "qtl.token_id",
            "location_id": "qtl.location_id",
            "leave_date": "qtl.leave_date",
            "assign_date": "qtl.assign_date",
            "create_date": "qtl.create_date",
            "state": "qtl.state",
            "time_to_assign": "EXTRACT(EPOCH FROM qtl.assign_date - qtl.create_date)/3600",
            "time_to_assign_average": "EXTRACT(EPOCH FROM qtl.assign_date "
            " - qtl.create_date)/60",
            "time_to_leave": "EXTRACT(EPOCH FROM qtl.leave_date - qtl.assign_date)/3600",
            "time_to_leave_average": "EXTRACT(EPOCH FROM qtl.leave_date - qtl.assign_date)/60",
            "time_total": "EXTRACT(EPOCH FROM qtl.leave_date - qtl.create_date)/3600",
            "time_total_average": "EXTRACT(EPOCH FROM qtl.leave_date - qtl.create_date)/60",
        }

    @api.model
    def _from(self):
        return """
            FROM queue_token_location qtl
        """

    @api.model
    def _where(self):
        return """
            WHERE TRUE
        """

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(  # pylint: disable=E8103
            """
            CREATE OR REPLACE VIEW %s AS (
                %s %s %s
            )
        """
            % (self._table, self._select(), self._from(), self._where())
        )
