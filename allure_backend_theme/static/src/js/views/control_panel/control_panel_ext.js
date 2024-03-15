/** @odoo-module **/

import { ControlPanel } from "@web/search/control_panel/control_panel";
import { patch } from "@web/core/utils/patch";
import { device } from 'web.config';
const { Component, hooks } = owl;
const { useExternalListener } = owl;
import { registry } from "@web/core/registry";
const systrayRegistry = registry.category("systray");

patch(ControlPanel.prototype, 'allure_backend_theme/static/src/js/views/control_panel/control_panel.js', {

    setup() {
        this._super();
        this.isMobileView = device.isMobile;
        useExternalListener(window, 'click', this._onWindowClick);
    },
    _onClickCpButtons(e) {
        var $oCpBottom = e.target.closest('.o_cp_bottom');
        $oCpBottom.classList.add('cp_open');
    },
    _onShowDropdown(e) {
        if (document) {
            var $modelBody = document.querySelector('.list-inline');
            $($modelBody).toggleClass('show')
        }
    },
    systrayItems() {
        return systrayRegistry
            .getEntries()
            .map(([key, value]) => ({ key, ...value }))
            .filter((item) => ("isDisplayed" in item ? item.isDisplayed(this.env) : true))
            .reverse().filter((item) => 
                item.key === "burger_menu" ? item : false
            );
    },
    _onClickFormCpButtons(e){
        var $oCpBottom = e.target.closest('.o_cp_bottom_right');
        $oCpBottom.classList.add('cp_open');
    },
    _onWindowClick(ev) {
        if (this.isMobileView &&
            this.el && !this.el.contains(document.activeElement) &&
            !this.el.contains(ev.target)) {
            var $oCpBottom = this.el.querySelector('.o_cp_bottom');
            $oCpBottom && $oCpBottom.classList.remove('cp_open');
        };
    }
});