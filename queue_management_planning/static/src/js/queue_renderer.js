odoo.define("queue_management_planning.QueuePlannningRenderer", function(require) {
    "use strict";

    var CalendarListRenderer = require("web_view_calendar_list.CalendarListRenderer");
    var BasicRenderer = require("web.BasicRenderer");
    var field_utils = require("web.field_utils");
    var core = require("web.core");
    var viewUtils = require("web.viewUtils");
    var qweb = core.qweb;

    var QueuePlannningRenderer = CalendarListRenderer.extend({
        _getModifiersData: BasicRenderer.prototype._getModifiersData,
        _applyModifiers: BasicRenderer.prototype._applyModifiers,
        _handleAttributes: BasicRenderer.prototype._handleAttributes,
        _registerModifiers: BasicRenderer.prototype._registerModifiers,
        _eventRender: function(event) {
            var qweb_context = {
                event: event,
                record: event.record,
                color: this.getColor(event.color_index),
            };
            this.qweb_context = qweb_context;
            if (_.isEmpty(qweb_context.record)) {
                return "";
            }

            var $el = $(
                qweb.render("queue_management_planning.calendar-box", qweb_context)
            );
            var self = this;
            var $cells = this.columns.map(function(node, index) {
                return self._renderBodyCell(event, node, index, {});
            });
            $el.find(".o_queue_management_planning").append($cells);
            return $el;
        },
        _renderButton: function(record, node) {
            var self = this;
            var nodeWithoutWidth = Object.assign({}, node);
            delete nodeWithoutWidth.attrs.width;
            var $button = viewUtils.renderButtonFromNode(nodeWithoutWidth, {
                extraClass: node.attrs.icon ? "o_icon_button" : undefined,
                textAsTitle: Boolean(node.attrs.icon),
            });
            this._handleAttributes($button, node);
            this._registerModifiers(node, record, $button);

            $button.on("click", function(e) {
                console.log("CLICKING!!!");
                e.stopPropagation();
                self.trigger_up("button_clicked", {
                    attrs: node.attrs,
                    record: record,
                });
            });

            return $button;
        },
        _renderBodyCell: function(record, node, index, options) {
            var tdClassName = "o_data_cell";
            if (node.tag === "button") {
                tdClassName += " o_list_button";
            }
            if (node.attrs.editOnly) {
                tdClassName += " oe_edit_only";
            }
            if (node.attrs.readOnly) {
                tdClassName += " oe_read_only";
            }
            var $td = $("<td>", {class: tdClassName, tabindex: -1});
            // We register modifiers on the <td> element so that it gets the correct
            // modifiers classes (for styling)
            var modifiers = this._registerModifiers(
                node,
                record,
                $td,
                _.pick(options, "mode")
            );
            // If the invisible modifiers is true, the <td> element is left empty.
            // Indeed, if the modifiers was to change the whole cell would be
            // rerendered anyway.
            if (modifiers.invisible && !(options && options.renderInvisible)) {
                return $td;
            }

            if (node.tag === "button") {
                return $td.append(this._renderButton(record, node));
            } else if (node.tag === "widget") {
                return $td.append(this._renderWidget(record, node));
            }
            if (node.attrs.widget || (options && options.renderWidgets)) {
                var $el = this._renderFieldWidget(
                    node,
                    record,
                    _.pick(options, "mode")
                );
                return $td.append($el);
            }
            this._handleAttributes($td, node);
            var name = node.attrs.name;
            var field = this.state.fields[name];
            var value = record.data[name];
            var formatter = field_utils.format[field.type];
            var formatOptions = {
                escape: true,
                data: record.data,
                isPassword: "password" in node.attrs,
                digits: node.attrs.digits && JSON.parse(node.attrs.digits),
            };
            var formattedValue = formatter(value, field, formatOptions);
            var title = "";
            if (field.type !== "boolean") {
                title = formatter(
                    value,
                    field,
                    _.extend(formatOptions, {escape: false})
                );
            }
            return $td.html(formattedValue).attr("title", title);
        },
        willStart: function() {
            this._processColumns();
            return this._super.apply(this, arguments);
        },
        _processColumns: function() {
            this.allModifiersData = [];
            this.columns = [];
            var self = this;
            _.each(this.arch.children, function(c) {
                if (!c.attrs.modifiers.column_invisible) {
                    self.columns.push(c);
                }
            });
        },
    });

    return QueuePlannningRenderer;
});
