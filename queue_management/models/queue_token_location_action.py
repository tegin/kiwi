# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from datetime import timedelta

from odoo import api, fields, models, registry

_logger = logging.getLogger(__name__)


class QueueTokenLocationAction(models.Model):

    _name = "queue.token.location.action"
    _description = "Queue_token_location_action"
    _log_access = False
    _order = "date desc"

    token_id = fields.Many2one("queue.token", required=True, readonly=True)
    token_location_id = fields.Many2one("queue.token.location")
    location_id = fields.Many2one("queue.location", readonly=True)
    user_id = fields.Many2one("res.users", readonly=True)
    date = fields.Datetime(readonly=True)
    action = fields.Selection(
        [
            ("cancel", "Cancel"),
            ("assign", "Assign"),
            ("leave", "Leave"),
            ("reopen", "Reopen"),
            ("back_to_draft", "Back to draft"),
        ]
    )

    def name_get(self):
        result = []
        for record in self:
            result.append(
                (
                    record.id,
                    "%s-%s %s"
                    % (record.token_id.name, record.location_id.name, record.action),
                )
            )
        return result

    @api.model
    def autovacuum(self, days=30):
        self.search(self._search_autovacuum_domain(days=days)).batch_unlink()

    def _search_autovacuum_domain(self, days=30):
        return [(("date", "<", fields.Datetime.now() + timedelta(days=-days)))]

    def batch_unlink(self):
        with api.Environment.manage():
            with registry(self.env.cr.dbname).cursor() as new_cr:
                new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                try:
                    while self:
                        batch_delete = self[0:1000]
                        self -= batch_delete
                        # do not attach new env to self because it may be
                        # huge, and the cache is cleaned after each unlink
                        # so we do not want to much record is the env in
                        # which we call unlink because odoo would prefetch
                        # fields, cleared right after.
                        batch_delete.with_env(new_env).unlink()
                        new_env.cr.commit()
                except Exception as e:
                    _logger.exception(
                        "Failed to delete records : {} - {}".format(self._name, str(e))
                    )
