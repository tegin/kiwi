/** @odoo-module **/

import {qweb} from "web.core";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";

const {Component, useState, onWillStart, useRef, onMounted} = owl;

export class QueueDisplayDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.bus_service = useService("bus_service");
        this.state = useState({
            title: "",
            items: {},
            data: {},
        });
        this.res_id = this.props.action.context.active_id;
        this.audio = useRef("audio");
        this.channel = "queue.display:" + this.res_id;
        this.env.services.bus_service.addChannel(this.channel);
        this.env.services.bus_service.addEventListener(
            "notification",
            this._onNotificationsReceived.bind(this)
        );
        this.env.services.bus_service.start();
        this.container = useRef("container");

        onWillStart(async () => {
            const data = await this.orm.call("queue.display", "get_data", [
                [parseInt(this.res_id, 10)],
            ]);
            this.data = data;
            const tokens = {};
            for (let i = 0; i < data.items.tokens.length; i++) {
                const token = data.items.tokens[i];
                tokens[token.id] = token;
            }
            this.state.items = tokens;
        });
        onMounted(() => {
            this.container.el.innerHTML = this.data.parsed_qweb;
            this._parseItems();
            setInterval(this._parseItems.bind(this), 15000);
        });
    }
    _onNotificationsReceived({detail: notifications}) {
        for (const notification of notifications) {
            if (notification.type === this.channel) {
                this._onNotificationReceived(notification.payload);
            }
        }
    }
    _onNotificationReceived(payload) {
        this.state.items[payload.id] = payload;
        this._parseItems();
        if (this.audio.el) {
            this.audio.el.play().catch((error) => {
                console.error("Audio play error:", error);
            });
        }
    }
    _parseItems() {
        const body = $(this.container.el).find(
            ".o_queue_management_display_body_content_body"
        );
        body.empty();
        const shiny_max_time = Date.now() / 1000 - this.data.shiny_time * 3600;
        const min_time = Date.now() / 1000 - this.data.max_time * 3600;
        let shown = 0;
        const items = {};
        for (const item of Object.values(this.state.items)
            .filter((a) => a.last_call_int > min_time)
            .sort(function (a, b) {
                return a.last_call_int > b.last_call_int ? -1 : 1;
            })) {
            if (shown < this.data.show_items) {
                items[item.id] = item;
                shown += 1;
                const $item = $(
                    qweb.render("queue_management_display.QueueDisplayItem", {
                        item,
                        shiny: item.last_call_int > shiny_max_time,
                    })
                );
                body.append($item);
            }
        }
        this.state.items = items;
    }
}

QueueDisplayDashboard.template = "queue_management_display.QueueDisplayDashboard";

registry
    .category("actions")
    .add("queue_management_display.queue_display_dashboard", QueueDisplayDashboard);
