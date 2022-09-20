odoo.define("queue_management.QueueDisplayView", function(require) {
    "use strict";

    var BasicView = require("web.BasicView");
    var QueueDisplayController = require("queue_management.QueueDisplayController");
    // Var DashboardModel = require("kpi_dashboard.DashboardModel");
    var QueueDisplayRenderer = require("queue_management.QueueDisplayRenderer");
    var view_registry = require("web.view_registry");
    var core = require("web.core");

    var _lt = core._lt;

    var QueueDisplayView = BasicView.extend({
        accesskey: "p",
        display_name: _lt("Display"),
        icon: "fa-tachometer",
        viewType: "queue_display",
        config: _.extend({}, BasicView.prototype.config, {
            Controller: QueueDisplayController,
            Renderer: QueueDisplayRenderer,
            // Model: DashboardModel,
        }),
        multi_record: false,
        searchable: false,
        init: function() {
            this._super.apply(this, arguments);
            this.controllerParams.mode = "readonly";
            this.loadParams.type = "record";
            if (!this.loadParams.res_id && this.loadParams.context.res_id) {
                this.loadParams.res_id = this.loadParams.context.res_id;
            }
        },
    });

    view_registry.add("queue_display", QueueDisplayView);

    return QueueDisplayView;
});
