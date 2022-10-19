odoo.define("queue_management.Clock", function(require) {
    "use strict";

    var config = require("web.config");
    // Var core = require("web.core");
    var Widget = require("web.Widget");
    // Var _t = core._t;
    var clockTemp = null;

    var Clock = Widget.extend({
        template: "queue_management.Clock",
        /**
         * @override
         */
        init: function() {
            this._super.apply(this, arguments);
            this.isMobile = config.device.isMobile;
        },
        /**
         * @override
         */
        willStart: function() {
            clockTemp = this;
            return this._super();
        },
        /**
         * @override
         */
        start: function() {
            this.renderTime();
            setInterval(this.renderTime, 1000);
            return this._super();
        },

        renderTime: function() {
            this.$(".main_clock").text(clockTemp.getTime());
            this.$(".main_clock_date").text(clockTemp.getDate());
        },
        getDate: function() {
            var today = new Date();
            var dd = String(today.getDate()).padStart(2, "0");
            var mm = String(today.getMonth() + 1).padStart(2, "0");
            var yyyy = today.getFullYear();
            var date = dd + "/" + mm + "/" + yyyy;
            return date;
        },
        getTime: function() {
            var today = new Date();
            var h = today.getHours();
            var m = today.getMinutes();
            // Var s = today.getSeconds();
            h = this.checkTime(h);
            m = this.checkTime(m);
            // S = this.checkTime(s);
            var time = h + ":" + m;
            return time;
        },
        checkTime: function(i) {
            if (i < 10) {
                i = "0" + i;
            }
            return i;
        },
    });
    return Clock;
});
