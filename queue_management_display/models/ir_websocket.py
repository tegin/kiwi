import re

from odoo import models
from odoo.exceptions import AccessDenied


class IrWebsocket(models.AbstractModel):
    _inherit = "ir.websocket"

    def _build_bus_channel_list(self, channels):
        if self.env.uid:
            # Do not alter original list.
            channels = list(channels)
            for channel in channels:
                if isinstance(channel, str):
                    match = re.match(r"queue.display:(\d+)", channel)
                    if match:
                        res_id = int(match[1])

                        # Verify access to the edition channel.
                        if not self.env.user._is_internal():
                            raise AccessDenied()

                        document = self.env["queue.display"].browse([res_id])
                        if not document.exists():
                            continue

                        document.check_access_rights("read")
                        document.check_access_rule("read")
                        document.check_access_rights("write")
                        document.check_access_rule("write")

                        channels.append(
                            (self.env.registry.db_name, document._name, document.id)
                        )
        return super()._build_bus_channel_list(channels)
