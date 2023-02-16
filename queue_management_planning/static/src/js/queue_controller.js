odoo.define("queue_management_planning.QueuePlanningController", function (require) {
    "use strict";

    var ListController = require("web.ListController");

    var QueuePlannningController = ListController.extend({
        custom_events: _.extend({}, ListController.prototype.custom_events, {
            changeDate: "_onChangeDate",
        }),
        _onChangeDate: function (event) {
            this._searchPanel.setDate(event.data.date);
            // With the parameters on reload, we are able to update the domain using the new date
            this.reload({
                controllerState: {
                    spState: {},
                },
            });
        },
    });

    return QueuePlannningController;
});
