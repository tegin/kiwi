/** @odoo-module **/

import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";

const {Component, useState, onWillStart} = owl;

export class QueueDisplayDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            title: "",
        });

        onWillStart(async () => {
            console.log("onWillStart");
            this.state.title = "Greetings Dashboard";
            console.log("this.state.title", this.state.title);
        });
    }
}

QueueDisplayDashboard.template = "queue_management_display.QueueDisplayDashboard";

registry
    .category("actions")
    .add("queue_management_display.queue_display_dashboard", QueueDisplayDashboard);
