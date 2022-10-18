odoo.define("queue_management_planning.QueuePlanningSearchPanel", function(require) {
    "use strict";

    var SearchPanel = require("web.SearchPanel");

    function dateToServer(date) {
        return date
            .clone()
            .utc()
            .locale("en")
            .format("YYYY-MM-DD HH:mm:ss");
    }

    var QueuePlanningSearchPanel = SearchPanel.extend({
        init: function(parent, params) {
            this._super.apply(this, arguments);
            // Forcing a new class
            this.className = params.classes
                .concat(["o_search_panel", "o_queue_planning_search_panel"])
                .join(" ");
        },
        setDate: function(date) {
            this.date = date;
        },
        _fetchCategories: function() {
            // Making it as not working
            return new Promise(resolve => {
                resolve();
            });
        },
        _fetchFilters: function() {
            // Making it as not working
            return new Promise(resolve => {
                resolve();
            });
        },
        _render: function() {
            if (!this.calendar_initialized) {
                // We will initialize the calendar just once.
                this._initCalendarMini();
            }
            return;
        },
        getDomain: function() {
            return [
                ["planning_date", ">=", dateToServer(this.date)],
                ["planning_date", "<", dateToServer(this.date.add(1, "days"))],
            ];
        },
        _initCalendarMini: function() {
            this.calendar_initialized = true;
            var start = moment(new Date())
                .utc()
                .locale("en")
                .startOf("day");
            this.date = start.add(-this.getSession().getTZOffset(start), "minutes");
            var self = this;
            this.monthNames = moment.months();
            this.monthNamesShort = moment.monthsShort();
            this.dayNames = moment.weekdays();
            this.dayNamesShort = moment.weekdaysShort();
            this.$el.append($('<div class="o_calendar_mini"/>'));
            this.$small_calendar = this.$(".o_calendar_mini");
            this.$small_calendar.datepicker({
                onSelect: function(datum, obj) {
                    self.trigger_up("changeDate", {
                        date: moment(
                            new Date(
                                Number(obj.currentYear),
                                Number(obj.currentMonth),
                                Number(obj.currentDay)
                            )
                        ),
                    });
                },
                showOtherMonths: true,
                dayNamesMin: this.dayNamesShort,
                monthNames: this.monthNamesShort,
                firstDay: this.firstDay,
            });
        },
    });

    return QueuePlanningSearchPanel;
});
