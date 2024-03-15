/** @odoo-module */

import { ListRenderer } from "@web/views/list/list_renderer";
import { patch } from 'web.utils';
import { useService } from '@web/core/utils/hooks';
import session from 'web.session';
import PdfViewer from 'allure_layout.PdfViewer';
import { device } from 'web.config';
import { evaluateExpr } from "@web/core/py_js/py";
import { useSortable } from "@web/core/utils/sortable";
import { Component, onWillStart, useState, useSubEnv, useEffect, useRef } from "@odoo/owl"; 
patch(ListRenderer.prototype, 'allure_backend_theme.ListRenderer', {
     setup() {
        this._super()
        this.rpc = useService('rpc');
        this.orm = useService('orm');
        onWillStart(async () =>{
            this.state.attachmentsData = await this.orm.call('ir.attachment', "get_attachments", [this.props.list.resModel, [], {}], {}).then(function(data) { return data });
        });
        // return this._super();
    },
    getnbAttachment(record) {
        if (this.state.attachmentsData && this.state.attachmentsData.nbAttahments) {
            var nbAttahments = JSON.parse(JSON.stringify(this.state.attachmentsData.nbAttahments))
            var attachCount = _.filter(nbAttahments, function (attachment) {
                if (attachment[record.resId]) {
                    return attachment[record.resId]
                }
            });
            if (attachCount && attachCount[0]) {
                return attachCount[0][record.resId]
            }
        } else {
            return 0;

        }
    },
    getAttachment(record) {
        if (this.state.attachmentsData && this.state.attachmentsData.displayDensity) {
            var displayDensity = JSON.parse(JSON.stringify(this.state.attachmentsData.displayDensity))
            if (this.state.attachmentsData.attachmentsData && displayDensity.display_density === 'default') {
                var attachmentsData = JSON.parse(JSON.stringify(this.state.attachmentsData.attachmentsData))
                var attachments = _.filter(attachmentsData, function (attachment) {
                    if (attachment[record.resId]) {
                        return attachment[record.resId][0]
                    }
                });
                attachments = attachments && attachments[0] && attachments[0][record.resId] ? attachments[0][record.resId] : false;
                let dictionary = {};
                if (attachments) {
                    dictionary = attachments.map((action) => ({
                        id: action.id,
                        name: action.name,
                        mimetype: action.mimetype,
                        res_id: action.res_id,
                    }));
                }
                return dictionary;
            } else {
                return {};
            }
        } else {
            return {};
        }
    },
    /**Override
     * Returns the classnames to apply to the row representing the given record.
     * @param {Record} record
     * @returns {string}
     */
    getRowClass(record) {
        // classnames coming from decorations
        const classNames = this.props.archInfo.decorations
            .filter((decoration) => evaluateExpr(decoration.condition, record.evalContext))
            .map((decoration) => decoration.class);
        if (record.selected) {
            classNames.push("table-info");
        }
        // "o_selected_row" classname for the potential row in edition
        if (record.isInEdition) {
            classNames.push("o_selected_row");
        }
        if (record.selected) {
            classNames.push("o_data_row_selected");
        }
        if (this.canResequenceRows) {
            classNames.push("o_row_draggable");
        }
        if (this.state.attachmentsData && this.state.attachmentsData.displayDensity) {
            var displayDensity = JSON.parse(JSON.stringify(this.state.attachmentsData.displayDensity))
            if (displayDensity && displayDensity.display_density && displayDensity.display_density === 'default' && this.getAttachment(record).length) {
                classNames.push('o_' + displayDensity.display_density)
            } 

            if (displayDensity.display_density === 'compact' || displayDensity.display_density === 'comfortable') {
                classNames.push('o_' + displayDensity.display_density)
            }
        }
        return classNames.join(" ");
    },
    /**Override
     */
    onClickCapture(record, ev) {
        const { list } = this.props;
        var self = this;
        if ($(ev.target).data('mimetype') && ($(ev.target).data('mimetype') ===  'application/pdf' || $(ev.target).data('mimetype') ===  'image/png' || $(ev.target).data('mimetype') ===  'image/jpg')) {
            self.PdfViewer = new PdfViewer(self, {
                isWebsite: true,
                fullscreen: true,
                size: 'extra-large',
            }, {
                mimetype: $(ev.target).data('mimetype'),
                id: $(ev.target).data('id'),
                name: $(ev.target).data('name'),
            });
            self.PdfViewer.open();
        }
        if ($(ev.target).hasClass('attech_link') || $(ev.target).hasClass('name') || $(ev.target).hasClass('o_image') || $(ev.target).hasClass('o_attachment_download')) {
            ev.stopPropagation();
            // if ($(ev.target).hasClass('o_image')) {
            //     var attachmentsData = JSON.parse(JSON.stringify(this.state.attachmentsData.attachmentsData))
            //     var attachmentVal = _.compact(_.map(attachmentsData, function(data) {
            //         return data[record.resId];
            //     }));
            //     if (attachmentVal) {
            //         var activeAttachmentID = $(ev.target).closest('.o_image_box').data('id');
            //         console.log("?????????????", attachmentVal, activeAttachmentID, AttachmentViewer)
            //         // var attachmentViewer = new DocumentViewer(this, attachmentData[0], activeAttachmentID);
            //         // attachmentViewer.appendTo($('body'));
            //     }
            // }
        } else {
            this._super(...arguments)
        }
    },
    _onAttachmentView: function(ev) {
        // var self = this;
        // ev.stopPropagation();
        // ev.preventDefault();
        // var activeAttachmentID = $(ev.currentTarget).data('id');
        // var res_id = $(ev.currentTarget).closest('tr').data('res_id');
        // if (activeAttachmentID && res_id) {
        //     var attachmentData = _.compact(_.map(this.attachmentsData, function(record) {
        //         return record[res_id];
        //     }));
        //     if (attachmentData) {
        //         // var attachmentViewer = new DocumentViewer(this, attachmentData[0], activeAttachmentID);
        //         attachmentViewer.appendTo($('body'));
        //     }
        // }
    },
    // onAttachmentClick(ev) {
    //     console.log("attachment>>>>>>>>>>>")
    //     // ev.stopPropagation();
    // }
});
// odoo.define('allure_backend_theme.ListRenderer', function(require) {
//     "use strict";

//     // var DocumentViewer = require('@mail/js/document_viewer')[Symbol.for("default")];
//     var ListRenderer = require('web.ListRenderer');
//     var core = require('web.core');
//     var QWeb = core.qweb;

//     ListRenderer.include({
//         events: _.extend({}, ListRenderer.prototype.events, {
//             'click .o_attachment_view': '_onAttachmentView',
//             'click tbody tr td .attachment-counter': '_onRowClicked',
//             'click tbody tr td .o_attachment_download': '_onAttachmentClick',
//         }),
//         init: function(parent, state, params) {
//             this._super.apply(this, arguments);
//             this.resIDs = state.res_ids;
//             this.resModel = state.model;
//             this.attachmentsData = state.attachmentsData || [];
//             this.nbAttahments = state.nbAttahments || [];
//             this.displayDensity = state.displayDensity;
//             this.records = {};
//         },
//         updateState: function(state) {
//             this._setState(state);
//             this.attachmentsData = this.state.attachmentsData || [];
//             this.nbAttahments = this.state.nbAttahments || [];
//             this.displayDensity = this.state.displayDensity;
//             return this._super.apply(this, arguments);
//         },
//         _renderRow: function(record) {
//             var self = this;
//             var $tr = this._super.apply(this, arguments);
//             if (self.displayDensity && self.displayDensity.display_density !== 'default') {
//                 $tr.addClass('o_' + self.displayDensity.display_density);
//             }
//             _.each(this.attachmentsData, function(values) {
//                 if (values[record.res_id]) {
//                     var $attech = $('<td/>', { class: 'o_attachment' });
//                     if (self.displayDensity) {
//                         $tr.addClass('o_' + self.displayDensity.display_density);
//                     }
//                     $tr.data('res_id', record.res_id);
//                     $tr.find('td:nth-child(2)').append($attech);
//                     $tr.find('.o_attachment').append(QWeb.render('ListView.Attachment', {
//                         values: values[record.res_id],
//                     }));
//                 }
//             });
//             _.each(this.nbAttahments, function(attach) {
//                 if (attach[record.res_id] && attach[record.res_id] > 3) {
//                     $tr.find('.o_attachment').append('<div class="attachment-counter">+' + (attach[record.res_id] - 3) + '</div>')
//                 }
//             });
//             return $tr;
//         },
//         _onAttachmentView: function(ev) {
//             var self = this;
//             ev.stopPropagation();
//             ev.preventDefault();
//             var activeAttachmentID = $(ev.currentTarget).data('id');
//             var res_id = $(ev.currentTarget).closest('tr').data('res_id');
//             if (activeAttachmentID && res_id) {
//                 var attachmentData = _.compact(_.map(this.attachmentsData, function(record) {
//                     return record[res_id];
//                 }));
//                 if (attachmentData) {
//                     // var attachmentViewer = new DocumentViewer(this, attachmentData[0], activeAttachmentID);
//                     attachmentViewer.appendTo($('body'));
//                 }
//             }
//         },
//     });
// });
