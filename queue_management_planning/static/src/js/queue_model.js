odoo.define("queue_management_planning.QueuePlanningModel", function(require) {
    "use strict";

    var CalendarListModel = require("web_view_calendar_list.CalendarListModel");
    var Domain = require("web.Domain");

    var QueuePlanningModel = CalendarListModel.extend({
        _recordToCalendarEvent: function(evt) {
            var result = this._super.apply(this, arguments);
            result._evalModifiers = this._evalModifiers;
            result.evalModifiers = this._evalModifiers;
            result.data = result.record;
            return result;
        },
        _evalModifiers: function(element, modifiers) {
            var result = {};
            var self = this;
            var evalContext;
            function evalModifier(mod) {
                if (mod === undefined || mod === false || mod === true) {
                    return Boolean(mod);
                }
                evalContext = evalContext || self._getEvalContext(element);
                return new Domain(mod, evalContext).compute(evalContext);
            }
            if (modifiers === undefined) {
                modifiers = {};
            }
            if ("invisible" in modifiers) {
                result.invisible = evalModifier(modifiers.invisible);
            }
            if ("column_invisible" in modifiers) {
                result.column_invisible = evalModifier(modifiers.column_invisible);
            }
            if ("readonly" in modifiers) {
                result.readonly = evalModifier(modifiers.readonly);
            }
            if ("required" in modifiers) {
                result.required = evalModifier(modifiers.required);
            }
            return result;
        },
    });

    return QueuePlanningModel;
});
