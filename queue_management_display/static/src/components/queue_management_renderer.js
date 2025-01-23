/** @odoo-module **/

import BasicRenderer from "web.BasicRenderer";

var QueueDisplayNotificationRenderer = BasicRenderer.extend({
    className: "o_queue_management_display_view",
    _renderView: function () {
        this.template_name = "queue_management_display_" + this.state.res_id;
        var template = "<templates><t t-name='" + this.template_name + "'>";
        template += "<div>hola</div>";
        qweb.add_template(template);
        this.$el.html(
            $(
                qweb.render(this.template_name, {
                    // data: this.state.data,
                    company_id: session.user_companies.current_company[0],
                    company: session.user_companies.current_company[1],
                })
            )
        );
    },

});

return QueueDisplayNotificationRenderer;
