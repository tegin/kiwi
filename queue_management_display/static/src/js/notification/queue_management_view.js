odoo.define("queue_management.QueueDisplayControlView", function(require) {
    "use strict";

    var BasicView = require("web.BasicView");
    var QueueDisplayControlController = require("queue_management.QueueDisplayControlController");
    // Var DashboardModel = require("kpi_dashboard.DashboardModel");
    var QueueDisplayControlRenderer = require("queue_management.QueueDisplayControlRenderer");
    var view_registry = require("web.view_registry");
    var core = require("web.core");

    var _lt = core._lt;

    var QueueDisplayControlView = BasicView.extend({
        accesskey: "p",
        display_name: _lt("Display"),
        icon: "fa-tachometer",
        viewType: "queue_display_control",
        config: _.extend({}, BasicView.prototype.config, {
            Controller: QueueDisplayControlController,
            Renderer: QueueDisplayControlRenderer,
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

    view_registry.add("queue_display_control", QueueDisplayControlView);

    return QueueDisplayControlView;
});
