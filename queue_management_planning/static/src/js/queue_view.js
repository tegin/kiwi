odoo.define("queue_management_planning.QueuePlanningView", function (require) {
    "use strict";

    var ListView = require("web.ListView");
    var core = require("web.core");
    var QueuePlanningSearchPanel = require("queue_management_planning.QueuePlanningSearchPanel");
    var QueuePlanningController = require("queue_management_planning.QueuePlanningController");
    var view_registry = require("web.view_registry");

    var _lt = core._lt;

    var QueuePlanningView = ListView.extend({
        display_name: _lt("Queue Planning"),
        icon: "fa-calendar-check-o",
        viewType: "queue_planning",
        config: _.extend(ListView.prototype.config, {
            SearchPanel: QueuePlanningSearchPanel,
            Controller: QueuePlanningController,
        }),
        init: function () {
            this._super.apply(this, arguments);
            // We need this in order to make the system work as a list
            this.fieldsInfo.list = this.fieldsView.fieldsInfo[this.viewType];
        },
    });

    view_registry.add("queue_planning", QueuePlanningView);

    return QueuePlanningView;
});
