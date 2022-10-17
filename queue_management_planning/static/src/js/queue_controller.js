odoo.define("queue_management_planning.QueuePlanningController", function(require) {
    "use strict";

    var CalendarListController = require("web_view_calendar_list.CalendarListController");

    var QueuePlannningController = CalendarListController.extend({
        custom_events: _.extend({}, CalendarListController.prototype.custom_events, {
            button_clicked: "_onButtonClicked",
        }),
        _onOpenEvent: function(event) {
            console.log(event);
        },
        _onButtonClicked: function(ev) {
            ev.preventDefault();
            ev.stopPropagation();
            this._callButtonAction(ev.data.attrs, ev.data.record);
        },
    });

    return QueuePlannningController;
});
