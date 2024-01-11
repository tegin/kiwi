odoo.define("queue_management.QueueDisplayNotificationController", function (require) {
    "use strict";

    var BasicController = require("web.BasicController");
    var core = require("web.core");
    var field_utils = require("web.field_utils");
    var qweb = core.qweb;

    var QueueDisplayNotificationController = BasicController.extend({
        custom_events: _.extend({}, BasicController.prototype.custom_events, {
            notification_received: "_onNotificationReceived",
            render_token: "_onRenderToken",
        }),
        init: function () {
            this._super.apply(this, arguments);
            this.queue_data = {};
        },
        _onNotificationReceived: function (ev) {
            var token = ev.data.notification;
            var last_call = field_utils.parse
                .datetime(token.last_call, null, {
                    timezone: false,
                })
                .unix();
            if (token.last_call !== last_call) {
                token.last_call = last_call;
                if (ev.data.audio !== undefined) {
                    ev.data.audio.play();
                }
            }
            this.queue_data[ev.data.notification.id] = token;
        },
        _onRenderToken: function () {
            this.$(".o_queue_management_display_body_content_body").empty();
            var self = this;
            // Sort the list by last call date
            var list = Object.entries(this.queue_data).sort(function (a, b) {
                return a[1].last_call > b[1].last_call ? -1 : 1;
            });
            var shiny_max_time =
                Date.now() / 1000 - this.initialState.data.shiny_time * 3600;
            _.each(list.slice(0, 10), function (token) {
                var $row = $(
                    qweb.render("queue_management_display.queue_display_token_shiny", {
                        token: token[1].token,
                        location: token[1].location,
                        shiny: token[1].last_call > shiny_max_time,
                    })
                );
                self.$(".o_queue_management_display_body_content_body").append($row);
            });
        },
        getState: function () {
            const state = this._super.apply(this, arguments);
            const env = this.model.get(this.handle, {env: true});
            state.id = env.currentId;
            return state;
        },
    });
    return QueueDisplayNotificationController;
});
