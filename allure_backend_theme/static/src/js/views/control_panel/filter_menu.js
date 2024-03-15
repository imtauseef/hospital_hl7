/** @odoo-module **/
import { patch } from '@web/core/utils/patch';

import { FilterMenu } from "@web/search/filter_menu/filter_menu";
import { GroupByMenu } from "@web/search/group_by_menu/group_by_menu";

patch(FilterMenu.prototype, 'allure_backend_theme.FilterMenu', {

    setup() {
        this._super();
        this.props.class = 'o_dropdown_allure';
    }
});

patch(GroupByMenu.prototype, 'allure_backend_theme.GroupByMenu', {

    setup() {
        this._super();
        this.props.class = 'o_dropdown_allure';
        $('.o_menu_systray').hasClass('show') && $('.user_menu')[0].click();
        $('.o_menu_sections_more').hasClass('show') && $('.o_menu_sections_more button')[0].click();
    }
});