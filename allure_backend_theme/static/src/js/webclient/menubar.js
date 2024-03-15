/** @odoo-module **/

import { NavBar } from "@web/webclient/navbar/navbar";
import { useService } from "@web/core/utils/hooks";
const { hooks, useState } = owl;
const core = require('web.core');
const config = require('web.config');
const { useListener } = require("@web/core/utils/hooks");
import { registry } from "@web/core/registry";
const { useExternalListener } = owl;
const systrayRegistry = registry.category("systray");
const __themesDB = require('allure_backend_theme.AllureWebThemes');

export class CustiomizeMenuBar extends NavBar {
    setup() {
        super.setup();
        this.CustomMenu = useService("custom_menu");
        this.menuService = useService("menu");
        this.orm = useService("orm");
        this.debug = config.isDebug() ? '?debug' : '';
        this.isTouchDevice = config.device.touch;
        this.state = useState({
            favoriteMenuNameById: {},
            menus: [],
            activeSystray: false,

        });
        core.bus.on('click_favorite_menu', this, this._getFavMenuData);
        this._getFavMenuData();
        // useExternalListener(window, "click", this._getfullScreen);
    }
    // async willStart() {
    //     return super.willStart();
    // }
    get systrayItemsCustom() {
        return systrayRegistry
            .getEntries()
            .map(([key, value]) => ({ key, ...value }))
            .filter((item) => ("isDisplayed" in item ? item.isDisplayed(this.env) : true))
            .reverse();
    }
    _getfullScreen(ev) {
        // alert("menubar js")
        if (this.isTouchDevice && !this.el.contains(ev.target) &&
            !document.body.classList.contains('ad_full_view')) {
            $('body').toggleClass('ad_full_view');
        }
    }
    // async toggle(custom_action) {
    //     $('.o_menu_systray').removeClass('show');
    //     const homeMenu = document.querySelector(".__home_menu");
    //     if (!homeMenu) {
    //         const menuToggle = document.querySelector("nav.o_main_navbar > a.__menu_toggle");
    //         console.log(">>>>>>menuToggle>>>>>>>>", menuToggle)
    //         if (menuToggle) {
    //             await ev.services.action.doAction("acs_menu");
    //         }
    //         if (!custom_action) {
    //             ev.services.action.custom_action = true;
    //             //menuToggle.classList.add('__has_action');
    //         }
    //     } else if (ev.services.action.custom_action) {
    //         ev.services.action.restore();
    //     }
    // }
    getGlobalSearchMenu(menu) {
        if (menu.xmlid === 'allure_backend_theme.menu_global_search') {
            return __themesDB.default_web_theme.base_menu_icon === 'base_icon' && '/allure_backend_theme/static/src/img/global_search.png'
            || __themesDB.default_web_theme.base_menu_icon === '2d_icon' && '/allure_backend_theme/static/src/img/menu_2d/global_search.png'
            || __themesDB.default_web_theme.base_menu_icon === '3d_icon' && '/allure_backend_theme/static/src/img/menu/global_search.png';
        }
    }
    async _getFavMenuData() {
        var self = this;
        var favorites = await this.orm.call("ir.favorite.menu", "get_favorite_menus");
        if (favorites) {
            favorites.forEach(function(menu) {
                if (menu.xmlid === 'allure_backend_theme.menu_global_search') {
                    menu.theme_icon_data = __themesDB.default_web_theme.base_menu_icon === 'base_icon' && '/allure_backend_theme/static/src/img/global_search.png'
                    || __themesDB.default_web_theme.base_menu_icon === '2d_icon' && '/allure_backend_theme/static/src/img/menu_2d/global_search.png'
                    || __themesDB.default_web_theme.base_menu_icon === '3d_icon' && '/allure_backend_theme/static/src/img/menu/global_search.png';
                }
                self.state.favoriteMenuNameById[menu.favorite_menu_id[0]] = menu.favorite_menu_id[1];
            });
            self.state.menus = favorites.map(function(favMenu) {
                $('.o_menu_systray').removeClass('show');
                return _.extend(favMenu, {
                    theme_icon_data: favMenu.theme_icon_data && ('data:image/png;base64,' + favMenu.theme_icon_data).replace(/\s/g, "") || favMenu.web_icon_data && ('data:image/png;base64,' + favMenu.web_icon_data).replace(/\s/g, "") || false,
                    actionID: favMenu.favorite_menu_action_id,
                    xmlid: favMenu.favorite_menu_xml_id,
                    parents: "",
                    appID: favMenu.favorite_menu_id[0],
                    action() {
                        self.menuService.selectMenu(favMenu);
                    },
                });
            });
        }
    }
    async render() {
        await super.render();
        var self = this;
        const favorite_menu = $('.oe_apps_menu');
        if (favorite_menu) {
            $(favorite_menu).sortable({
                items: "> .oe_favorite",
                axis: 'y',
                stop: (event, ui) => {
                    $(favorite_menu).children().each(function(index) {
                        var vals = {};
                        var menu_id = $(this).data('id');
                        vals['sequence'] = index;
                        vals['favorite_menu_id'] = $(this).data('menu-id');
                        self.orm.call("ir.favorite.menu", "write", [
                            [menu_id], vals
                        ]);
                    });
                },
            });
        }
    }
    onOpenMenu() {
        return this.state.menus;
    }
    OpenMenu(menu) {
        this.menuService.setCurrentMenu(menu.appID);
        menu.action();
    }
    onFullViewClicked() {
        $('body').toggleClass('ad_full_view');
    }
    onFullScreen() {
        document.fullScreenElement && null !== document.fullScreenElement || !document.mozFullScreen &&
            !document.webkitIsFullScreen ? document.documentElement.requestFullScreen ? document.documentElement.requestFullScreen() :
            document.documentElement.mozRequestFullScreen ? document.documentElement.mozRequestFullScreen() :
            document.documentElement.webkitRequestFullScreen && document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT) :
            document.cancelFullScreen ? document.cancelFullScreen() :
            document.mozCancelFullScreen ? document.mozCancelFullScreen() :
            document.webkitCancelFullScreen && document.webkitCancelFullScreen()
    }
}
CustiomizeMenuBar.template = "allure_backend_theme.CustomMenu";
registry.category("actions").add("fav_menu_item", CustiomizeMenuBar);