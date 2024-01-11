odoo.define("queue_management.QueueDisplayNotificationRenderer", function (require) {
    "use strict";

    var BasicRenderer = require("web.BasicRenderer");
    var session = require("web.session");
    var core = require("web.core");
    var qweb = core.qweb;
    var Clock = require("queue_management.Clock");

    var QueueDisplayNotificationRenderer = BasicRenderer.extend({
        className: "o_queue_management_display_view",
        _renderView: function () {
            this.channel = "queue.display_" + this.state.res_id;
            this.template_name = "queue_management_display_" + this.state.res_id;
            var template = "<templates><t t-name='" + this.template_name + "'>";
            template +=
                "<style type='text/css'><![CDATA[" +
                this.state.data.css +
                "]]></style>";
            template += this.state.data.qweb;
            template += "</t></templates>";
            qweb.add_template(template);
            this.$el.html(
                $(
                    qweb.render(this.template_name, {
                        data: this.state.data,
                        company_id: session.user_companies.current_company[0],
                        company: session.user_companies.current_company[1],
                    })
                )
            );
            this.audio = false;
            if (this.state.data.audio_file) {
                this.audio = $(
                    '<audio class="audio_file" style="display:none" src="data:audio/mp3;base64,' +
                        this.state.data.audio_file +
                        '" type="audio/mp3"/>'
                );
                this.$el.append(this.audio);
            }
            new Clock(this).appendTo(
                this.$(".o_queue_management_display_header_clock")
            );

            var self = this;
            _.each(this.state.data.items.tokens, function (token) {
                self.trigger_up("notification_received", {
                    notification: token,
                });
            });
            this.trigger_up("render_token");
            this.call("bus_service", "addChannel", this.channel);
            this.call("bus_service", "startPolling");
            this.call("bus_service", "onNotification", this, this._onNotification);

            return $.when();
        },
        _onNotification: function (notifications) {
            var self = this;
            _.each(notifications, function (notification) {
                if (notification[0] === self.channel) {
                    self.trigger_up("notification_received", {
                        notification: notification[1],
                        audio: self.audio[0],
                    });
                }
            });
            this.trigger_up("render_token");
        },
    });

    return QueueDisplayNotificationRenderer;
});
