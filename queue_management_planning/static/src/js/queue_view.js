odoo.define("queue_management_planning.QueuePlanningView", function(require) {
    "use strict";

    var CalendarListView = require("web_view_calendar_list.CalendarListView");
    var core = require("web.core");
    var QueuePlannningRenderer = require("queue_management_planning.QueuePlannningRenderer");
    var QueuePlanningModel = require("queue_management_planning.QueuePlanningModel");
    var QueuePlanningController = require("queue_management_planning.QueuePlanningController");
    var view_registry = require("web.view_registry");

    var _lt = core._lt;

    var QueuePlanningView = CalendarListView.extend({
        display_name: _lt("Calendar List"),
        icon: "fa-calendar-check-o",
        viewType: "queue_planning_calendar",
        config: _.extend(CalendarListView.prototype.config, {
            Renderer: QueuePlannningRenderer,
            Model: QueuePlanningModel,
            Controller: QueuePlanningController,
        }),
    });

    view_registry.add("queue_planning_calendar", QueuePlanningView);

    return QueuePlanningView;
});
