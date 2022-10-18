odoo.define("queue_management.QueueDisplayNotificationView", function(require) {
    "use strict";

    var BasicView = require("web.BasicView");
    var QueueDisplayNotificationController = require("queue_management.QueueDisplayNotificationController");
    // Var DashboardModel = require("kpi_dashboard.DashboardModel");
    var QueueDisplayNotificationRenderer = require("queue_management.QueueDisplayNotificationRenderer");
    var view_registry = require("web.view_registry");
    var core = require("web.core");

    var _lt = core._lt;

    var QueueDisplayNotificationView = BasicView.extend({
        accesskey: "p",
        display_name: _lt("Display"),
        icon: "fa-tachometer",
        viewType: "queue_display_notification",
        config: _.extend({}, BasicView.prototype.config, {
            Controller: QueueDisplayNotificationController,
            Renderer: QueueDisplayNotificationRenderer,
            // Model: DashboardModel,
        }),
        multi_record: false,
        searchable: false,
        withControlPanel: false,
        init: function() {
            this._super.apply(this, arguments);
            this.controllerParams.mode = "readonly";
            this.loadParams.type = "record";
            if (!this.loadParams.res_id && this.loadParams.context.res_id) {
                this.loadParams.res_id = this.loadParams.context.res_id;
            }
        },
    });

    view_registry.add("queue_display_notification", QueueDisplayNotificationView);

    return QueueDisplayNotificationView;
});
