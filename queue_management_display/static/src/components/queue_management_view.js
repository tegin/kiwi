/** @odoo-module **/;

import QueueDisplayNotificationRenderer from './QueueDisplayNotificationRenderer';

import BasicView from 'web.BasicView';
import core from 'web.core';
import view_registry from 'web.view_registry';


const _lt = core._lt;

const QueueDisplayNotificationView = BasicView.extend({
    accesskey: "p",
    display_name: _lt('Display'),
    icon: 'fa-tachometer',
    viewType: 'queue_display_notification',
    config: _.extend({}, BasicView.prototype.config, {
        // Controller: ActivityController,
        Renderer: QueueDisplayNotificationRenderer,
        // Model: ActivityModel,
    }),
    multi_record: false,
    searchable: false,
    withControlPanel: false,
    init: function () {
        this._super.apply(this, arguments);
        this.controllerParams.mode = 'readonly';
        this.loadParams.type = 'record';
        if (!this.loadParams.res_id && this.loadParams.context.res_id) {
            this.loadParams.res_id = this.loadParams.context.res_id;
        }
    },
});

view_registry.add('queue_display_notification', QueueDisplayNotificationView);

export default QueueDisplayNotificationView;
