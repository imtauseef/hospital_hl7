/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { Notebook } from '@web/core/notebook/notebook';
import __themesDB from 'allure_backend_theme.AllureWebThemes';
import { session } from '@web/session';
import { Component, onWillDestroy, onWillUpdateProps, useEffect, useRef, useState } from "@odoo/owl";

patch(Notebook.prototype, "allure_backend_theme.Notebook", {
    setup() {
        this._super();
        var themeData = __themesDB.get_theme_config_by_uid(session.uid);
        if (themeData && themeData.tab_type === 'vertical_tabs') {
            this.state.tab_type = 'vertical_tabs';
        } else {
            this.state.tab_type = 'horizontal_tabs';
        }
        useEffect(
            () => {
                this.props.onPageUpdate(this.state.tab_type);
            },
            () => [this.state.tab_type]
        );
        onWillUpdateProps((nextProps) => {
            const activateDefault =
                this.props.defaultPage !== nextProps.defaultPage || !this.defaultVisible;
            this.pages = this.computePages(nextProps);
            this.state.currentPage = this.computeActivePage(nextProps.defaultPage, activateDefault);
            if (themeData && themeData.tab_type === 'vertical_tabs') {
                this.state.tab_type = 'vertical_tabs';
            } else {
                this.state.tab_type = 'horizontal_tabs';
            }
        });
    },
});