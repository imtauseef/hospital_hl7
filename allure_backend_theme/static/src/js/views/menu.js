/** @odoo-module **/

import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { useService } from "@web/core/utils/hooks";
import { patch } from 'web.utils';
import Widget from 'web.Widget';
import { getCookie } from 'web.utils.cookies';
import { qweb } from 'web.core';
const { useEffect } = owl;


patch(DropdownItem.prototype, '@allure_backend_theme/static/src/js/views/menu.js', {
    setup() {
        this._super();
        // this.cookies = useService('cookie');
        // $('.o_menu_systray').hasClass('show') && $('.__menu_systray').click();
        useEffect(
            () => {
                if (getCookie('color_scheme') && getCookie('color_scheme') === 'dark') {
                    $('body').addClass('oe_night_mode');
                }
                if (this.props.dataset && this.props.dataset.menu) {
                    if (this.props.dataset.menu === "logout") {
                        this.props.onSelected = this._onClickLogout.bind(this);
                    }
                }
            },
            () => []
        );   
    },
    willStart() {
        this._super(...arguments);
        
    },
    _onClickLogout: function(e) {
        let template = $(qweb.render('LogoutMessage', {}));
        var modal = template.appendTo(('body'));
        document.querySelector('.oe_cu_logout_yes').addEventListener('click', this._onClickLogoutBtn, this.el)
        document.querySelector('.mb-control-close').addEventListener('click', this._onClickRemoveBtn, this.el)
        return modal
    },
    _onClickRemoveBtn: function(ev) {
        $('.message-box').remove();
    },
    _onClickLogoutBtn: function(ev) {
        window.location.href = "/web/session/logout?redirect=/web/login";
    },
});
