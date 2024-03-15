/** @odoo-module */

import { ListController } from '@web/views/list/list_controller';
import { Dialog } from "@web/core/dialog/dialog";
import { patch } from 'web.utils';
import { useService } from '@web/core/utils/hooks';
import session from 'web.session';
import { device } from 'web.config';
import { Component, onWillStart, useState, useSubEnv, useEffect, useRef } from "@odoo/owl";

export const TABS = {
    DEFAULT: {
        id: 'DEFAULT',
        title: "Default",
        // Component: Defaultselector,
    },
    COMFORATBLE: {
        id: 'COMFORATBLE',
        title: "Comfortable",
        // Component: ComfortableSelector,
    },
    COMPAT: {
        id: 'COMPAT',
        title: "Compat",
        // Component: CompatSelector,
    },
};
    // var default_density;  
    export class DensityDialog extends Component {
         setup() {
            var self = this;
            this.contentClass = 'o_select_density_dialog';
            this.size = 'lg';
            this.parent = parent;
            this.title = this.env._t("Customize List");
            this.state = useState({
                default_density: this.density,
            });
            this.state = useState({
                default_density: this.density,
            });
            this.widget = useState({
                default_density: this.displayDensity,
            });
            this.tabs = [];
            this.rpc = useService('rpc');
            this.orm = useService('orm');
            this.action = useService('action');
            // var state = this.model.root;
            // this.default_density = state.displayDensity &&
            // state.displayDensity.display_density || false;

        }
        get displayDensity() {

            if (this.state.default_density) {
                return this.state.default_density;
            }
            if (this.props.media) {
                const correspondingTab = Object.keys(TABS).find(id => TABS[id].Component.tagNames.includes(this.props.media.tagName));
                if (correspondingTab) {
                    return correspondingTab;
                }
            }
            return this.props && this.props.density || 'default';
        }
        default() {
            this.widget.default_density = 'default'
        }
        comfortable() {
            this.widget.default_density = 'comfortable';
        }
        compact() {
            this.widget.default_density = 'compact'
        }
        async save() {
            var self = this;
            const action = await this.orm.call('res.users', 'write', [session.uid, {display_density: this.widget.default_density}]
            )
            this.props.close();
            this.action.doAction({
                'type': 'ir.actions.client',
                'tag': 'reload',
            });
        }
    }
DensityDialog.template = 'CustomizeList';
DensityDialog.components = {Dialog};

patch(ListController.prototype, 'allure_backend_theme.ListController', {
     setup() {
        this._super.apply(this, arguments);
        const _Super = this._super(...arguments);
        this.dialogs = useService('dialog');
        this.group_display_density = false;
        this.rpc = useService('rpc');
        this.orm = useService('orm');
        onWillStart(async () => {
            var self = this;
            const acl = session.user_has_group('allure_backend_theme.group_display_density').then(hasGroup => {
                this.group_display_density = hasGroup;
            });
            var density = await self.orm.call('ir.attachment', "get_attachments", [self.model.rootParams.resModel, [], {}], {}).then(function(record) {
                _.extend(self, record);
                return record;
            });
            this.density = density && density.displayDensity && density.displayDensity.display_density;
            return Promise.all([_Super, acl, density]);
        });
        useEffect(
            () => {
                if (!device.isMobile) { this._doToggleActionMenu(); };
            }
        );
     },
     _onAttachmentView: function(ev) {
        // var self = this;
        // ev.stopPropagation();
        // ev.preventDefault();
        console.log(">?????????????????", PdfViewer)
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
     onClickDisplayDensity(ev) {
        var dialog = new DensityDialog(this)
        const state = this.model.root;
        var default_density = state.displayDensity &&
        state.displayDensity.display_density || false;
        var $customize_list = new DensityDialog(this, state);
        default_density = $customize_list
        console.log("???????????this", this)
        this.dialogs.add(DensityDialog, this);
       
     },
    renderButtons: function($node) {
        alert("render button")
        this._super.apply(this, arguments);
        var state = this.model.get(this.handle);
        state.group_display_density = this.group_display_density;
        this.state = state;
        if (this.group_display_density && this.$buttons.find('.o_display_density').length === 0) {
            this.$buttons.prepend(QWeb.render('DisplayDensityList.buttons'));
        };
        if (this.$buttons) {
            this.$buttons.on('click', '.o_display_density', this._onOpenSetting.bind(this));
        }
    },
    _reRenderAttachments: function(state, recordID) {
        var record = _.findWhere(state.data, { id: recordID });
        if (record) {
            var rowIndex = _.findIndex(state.data, { id: recordID });
            var attachmentsData = _.filter(state.attachmentsData, function(rec) {
                return rec[record.res_id];
            });
            var nbAttahments = _.filter(state.nbAttahments, function(rec) {
                return rec[record.res_id];
            });
            if (attachmentsData.length !== 0) {
                var $row = this.$('.o_data_row:nth(' + rowIndex + ')');
                var $attech = $('<td/>', { class: 'o_attachment' });
                if (this.state.displayDensity) {
                    $row.addClass('o_' + state.displayDensity.display_density);
                }
                $row.data('res_id', record.res_id);
                var $td = $row.find('td:nth-child(2)');
                $td.append($attech);
                $td.addClass('has_attachment');
                $row.find('.o_attachment').append(QWeb.render('ListView.Attachment', {
                    values: attachmentsData[0][record.res_id],
                }));
                if (nbAttahments.length !== 0 && nbAttahments[0][record.res_id] && nbAttahments[0][record.res_id] > 3) {
                    $row.find('.o_attachment').append('<div class="attachment-counter">' + (nbAttahments[0][record.res_id] - 3) + '</div>')
                }
            }
        }
    },
    _onSaveLine: function(ev) {
        alert("call on save")
        var recordID = ev.data.recordID;
        var state = this.model.get(this.handle);
        var default_density = this.widget.default_density;

        this.saveRecord(recordID)
            .then(ev.data.onSuccess)
            .guardedCatch(ev.data.onFailure);
        if (default_density && default_density === 'default') {
            this._reRenderAttachments(state, recordID);
        }
    },
    _confirmSave: function(id) {
        var self = this;
        var state = this.model.get(this.handle);
        var default_density = state.displayDensity &&
            state.displayDensity.display_density || false;
        return this._super.apply(this, arguments).then(function() {
            if (default_density && default_density === 'default') {
                self._reRenderAttachments(state, id);
            }
        });
    },
    _doToggleActionMenu: function() {
        if (this.model.root.selection.length > 0) {
            $('.o_action').addClass('o_open_sidebar');
            $('.o_cp_action_menus').addClass('o_drw_in');
            if ($('.o_form_view').hasClass('.o_xxl_form_view') === false) {
                $('.o_form_view').addClass('o_xxl_form_view_custom o_xxl_form_view h-100');
            }
            $('.o_cp_action_menus').find('.o_action_allure').removeClass('d-none')
        } else {
            $('.o_action').removeClass('o_open_sidebar');
            $('.o_cp_action_menus').removeClass('o_drw_in');
            $('.o_cp_action_menus').find('.o_action_allure').addClass('d-none')
        };
    },
    _onSelectionChanged: function(ev) {
        this.selectedRecords = ev.data.selection;
        this.isPageSelected = ev.data.allChecked;
        this.isDomainSelected = false;
        this.$('.o_list_export_xlsx').toggle(!this.selectedRecords.length);
        this._updateSelectionBox();
        this._updateControlPanel();
    },
});
