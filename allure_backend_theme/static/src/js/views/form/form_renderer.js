/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { FormRenderer } from "@web/views/form/form_renderer";
import { FormController } from "@web/views/form/form_controller";

const { Component, onWillStart, useEffect, useRef, onRendered, useState, toRaw } = owl;
import __themesDB from 'allure_backend_theme.AllureWebThemes';
import { session } from '@web/session';

patch(FormController.prototype, "allure_backend_theme.FormController", {
    setup() {
        this._super();
        useEffect(() => {
            this._doUpdateActionMenus();
        });
    },
    _doUpdateActionMenus: function() {
        if (this.hasActionMenus) {
            this.$el.toggleClass('o_open_sidebar', (this.$el.find('.o_cp_action_menus').hasClass('o_drw_in')));
        }
    },
});
patch(FormRenderer.prototype, "allure_backend_theme.FormRenderer", {
    /**
     * @Override
     * @param {Object} node
     * @returns {jQueryElement}
     */
    setup() {
        this._super();
        $('.o_menu_systray').hasClass('show') && $('.user_menu')[0].click();
        useEffect(() => {
            this._updateView();
            // this._renderTagNotebook()
        });
    },
    /**
     * @private
     * @param {Object} node
     * @returns {jQueryElement}
     */
    _updateView: function() {
        var self = this;
        var formChatter = document.querySelector('.o_FormRenderer_chatterContainer');
        var formView = document.querySelector('.o_form_view');
        console.log("????????????/*$(formChatter)*/", $('.o_form_editable').children('.o_FormRenderer_chatterContainer'))
        if ($(formChatter).length > 0) {
            $(formView).prepend('<div class="toggle_btn_chatter"><i class="fa fa-comments"/></div>')
            $(formView.querySelector('.toggle_btn_chatter')).on('click', self.toggleChatter.bind(self));
            if ($('.o_xxl_form_view').length > 0 && $('.o_form_editable').children('.o_FormRenderer_chatterContainer').length === 0) {
                // $('.o_form_saved').addClass('flex-column');
                $('.o_FormRenderer_chatterContainer').appendTo($('.o_form_editable'))
                $('.o_form_saved').addClass('flex-column');
                // $('.o_form_view').removeClass('o_xxl_form_view_custom o_xxl_form_view h-100');
                $('.o_form_saved').removeClass('h-100');
                $('.o_form_saved').removeClass('flex-nowrap');
                // $('.o_form_view').removeClass('o_xxl_form_view_scren o_xxl_form_view h-100');
                // $('.o_form_saved').removeClass('h-100');
            }
        }
        // _.each(this.allFieldWidgets[this.state.id], function(widget) {
        //     var idForLabel = self.idsForLabels[widget.name];
        //     var $widgets = self.$('.o_field_widget[name=' + widget.name + ']');
        //     var $label = idForLabel ? self.$('label[for=' + idForLabel + ']') : $();
        //     $label = $label.eq($widgets.index(widget.$el));
        //     if (widget.field.help) {
        //         $label.addClass('o_label_help');
        //     }
        // });
    },
    /**
     * @Override
     * @param {Object} node
     * @returns {jQueryElement}
     */
    _renderTagSheet: function(node) {
        var $sheet = this._super(...arguments);
        $sheet.children().not('.o_notebook').not('.o_chatter.oe_chatter').wrapAll($('<div/>', { class: 'o_cu_panel' }));
        return $sheet;
    },
    /**
     * @private
     * @param {Object} node
     * @returns {jQueryElement}
     */
    toggleChatter: function(ev) {
        $('.o_form_view').toggleClass('side_chatter');
        if ($('.side_chatter').length > 0) {
            $('.o_form_saved').removeClass('flex-column');
            $('.o_form_view').addClass('o_xxl_form_view_custom o_xxl_form_view h-100');
            $('.o_form_saved').addClass('h-100');
        //     $('.o_FormRenderer_chatterContainer').appendTo($('.o_form_editable'))
        //     $('.o_form_editable').removeClass('d-flex');
        //     $('.o_form_editable').removeClass('flex-nowrap');
        } else {
                $('.o_form_saved').addClass('flex-column');
                $('.o_form_view').removeClass('o_xxl_form_view_custom o_xxl_form_view h-100');
                $('.o_form_saved').removeClass('h-100');
        //     console.log("?????????????$('.o_FormRenderer_chatterContainer')", $('.o_FormRenderer_chatterContainer'))
        //     $('.o_FormRenderer_chatterContainer').appendTo($('.o_form_view_container'))
        //     $('.o_form_editable').addClass('d-flex');
        //     $('.o_form_editable').addClass('flex-nowrap');
        }
        if ($('.o_xxl_form_view').length > 0) {
            // $('.o_form_saved').addClass('flex-column');
            $('.o_FormRenderer_chatterContainer').appendTo($('.o_form_editable'))
            $('.o_form_view').removeClass('o_xxl_form_view_scren o_xxl_form_view h-100');
            // $('.o_form_saved').removeClass('h-100');
        }
    },
});
// // odoo Form view inherit for teb view change and form first panel create.
// odoo.define('allure_backend_theme.FormRenderer', function(require) {
//     "use strict";


//     var FormRenderer = require('web.FormRenderer');
//     var FormController = require('web.FormController');
//     const session = require('web.session');

//     FormController.include({
//         _doUpdateActionMenus: function() {
//             if (this.hasActionMenus) {
//                 this.$el.toggleClass('o_open_sidebar', (this.mode === 'readonly' && this.$el.find('.o_cp_action_menus').hasClass('o_drw_in')));
//             }
//         },
//         _update: async function() {
//             await this._super(...arguments);
//             this._doUpdateActionMenus();
//         },
//     });

//     FormRenderer.include({
//         events: _.extend({}, FormRenderer.prototype.events, {
//             'click .toggle_btn_chatter': function(e) {
//                 e.preventDefault();
//                 this.$el.parent().find('.o_form_view').toggleClass('side_chatter');
//             },
//         }),
//         init: function() {
//             this._super.apply(this, arguments);
//             this.themeData = __themesDB.get_theme_config_by_uid(session.uid);
//         },
//         _renderTagSheet: function(node) {
//             var $sheet = this._super.apply(this, arguments);
//             $sheet.children().not('.o_notebook').not('.o_chatter.oe_chatter').wrapAll($('<div/>', { class: 'o_cu_panel' }));
//             return $sheet;
//         },
//         _renderTabHeader_new: function(page, page_id) {
//             var $a = $('<a>', {
//                 disable_anchor: 'true',
//                 role: 'tab',
//                 text: page.attrs.string,
//             }).click(function() {
//                 $(this).parent('li')
//                     .toggleClass("ad_close");
//             });
//             return $('<li>').append($a);
//         },
//         _renderTagNotebook: function(node) {
//             var self = this;
//             if (this.themeData && this.themeData.tab_type === 'vertical_tabs') {
//                 var $headers = $('<ul class="panel-ul" role="tablist">');
//                 var autofocusTab = -1;
//                 // renderedTabs is used to aggregate the generated $headers and $pages
//                 // alongside their node, so that their modifiers can be registered once
//                 // all tabs have been rendered, to ensure that the first visible tab
//                 // is correctly activated
//                 var renderedTabs = _.map(node.children, function(child, index) {
//                     var pageID = _.uniqueId('notebook_page_');
//                     var $header = self._renderTabHeader_new(child, pageID);
//                     var $page = self._renderTabPage(child, pageID);
//                     $header.append($page);
//                     if (self.themeData.tab_configration === "close_tabs") {
//                         $header.addClass("ad_close")
//                     }
//                     if (autofocusTab === -1 && child.attrs.autofocus === 'autofocus') {
//                         autofocusTab = index;
//                     }
//                     self._handleAttributes($header, child);
//                     $headers.append($header);
//                     return {
//                         $header: $header,
//                         $page: $page,
//                         node: child,
//                     };
//                 });
//                 if (renderedTabs.length) {
//                     var tabToFocus = renderedTabs[Math.max(0, autofocusTab)];
//                     tabToFocus.$header.addClass('active');
//                     tabToFocus.$page.addClass('active');
//                 }
//                 // register the modifiers for each tab
//                 _.each(renderedTabs, function(tab) {
//                     self._registerModifiers(tab.node, self.state, tab.$header, {
//                         callback: function(element, modifiers) {
//                             // if the active tab is invisible, activate the first visible tab instead
//                             if (modifiers.invisible && element.$el.hasClass('active')) {
//                                 element.$el.removeClass('active');
//                                 tab.$page.removeClass('active');
//                                 var $firstVisibleTab = $headers.find('li:not(.o_invisible_modifier):first()');
//                                 $firstVisibleTab.addClass('active');
//                             }
//                         },
//                     });
//                 });
//                 var $notebook = $('<div class="o_notebook">').append($headers);
//                 $notebook[0].dataset.name = node.attrs.name || '_default_';
//                 this._registerModifiers(node, this.state, $notebook);
//                 this._handleAttributes($notebook, node);
//                 return $notebook;
//             } else {
//                 return this._super.apply(this, arguments);
//             }
//         },
//         _updateView: function() {
//             this._super.apply(this, arguments);
//             var self = this;
//             if (this.$el.find('.o_FormRenderer_chatterContainer').length) {
//                 this.$el.prepend('<div class="toggle_btn_chatter"><i class="fa fa-comments"/></div>')
//             }
//             _.each(this.allFieldWidgets[this.state.id], function(widget) {
//                 var idForLabel = self.idsForLabels[widget.name];
//                 var $widgets = self.$('.o_field_widget[name=' + widget.name + ']');
//                 var $label = idForLabel ? self.$('label[for=' + idForLabel + ']') : $();
//                 $label = $label.eq($widgets.index(widget.$el));
//                 if (widget.field.help) {
//                     $label.addClass('o_label_help');
//                 }
//             });
//         },
//     });
// });
