/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { fuzzyLookup } from "@web/core/utils/search";
import { NavBar } from "@web/webclient/navbar/navbar";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { _lt } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { computeAppsAndMenuItems } from "./menus/menu_helpers";
const { Component, hooks } = owl;
const { useExternalListener, useState, useRef, onWillStart} = owl;
const session = require('web.session');
import { sprintf } from "@web/core/utils/strings";
var core = require('web.core');
const __themesDB = require('allure_backend_theme.AllureWebThemes');



export const customMenu = {
    start(ev) {
        var self = this;
        export class NewMenu extends Component {
            setup() {
                this.menuService = useService("menu");
                this.orm = useService("orm");
                this.companyService = useService("company");
                this.actionService = useService("action");
                this.notification = useService("notification");
                this.rpc = useService('rpc')
                this.inputRef = useRef("input");
                let { apps, menuItems } = computeAppsAndMenuItems(this.menuService.getMenuAsTree("root"));
                apps.forEach((app) => {
                    if (app.xmlid === 'allure_backend_theme.menu_global_search') {
                        app.webIconData = __themesDB.default_web_theme.base_menu_icon === 'base_icon' && '/allure_backend_theme/static/src/img/global_search.png'
                        || __themesDB.default_web_theme.base_menu_icon === '2d_icon' && '/allure_backend_theme/static/src/img/menu_2d/global_search.png'
                        || __themesDB.default_web_theme.base_menu_icon === '3d_icon' && '/allure_backend_theme/static/src/img/menu/global_search.png';
                    }
                });
                this.menuApps = apps;
                this.menuLinks = [];
                this.apps = apps;
                this.menuItems = menuItems;
                this.router = useService("router");
                this.state = useState({
                    query: "",
                    favoriteMenuById: {},
                    menuEdit: false,
                });
                owl.onMounted(() => {
                    this.updateCustomizeMenu(true);
                });
                owl.onWillUnmount(() => {
                    this.updateCustomizeMenu(false);
                    document.querySelector("nav.o_main_navbar > a.__menu_toggle").classList.remove('__has_action');
                });
                onWillStart(async () =>{
                    this.router.pushState({ menu_id: undefined });
                    ev.services.action.custom_action = false;
                    $('body').addClass('oe_home_menu');
                });
                useExternalListener(window, "keydown", this._onKeydown);
            }
            _onKeydown(e) {
                var self = this;
                var switchmenu = $(document.getElementsByClassName("select_app")),
                    pre_focused = switchmenu.filter(".__active") || $(switchmenu[0]),
                    offsetval = switchmenu.index(pre_focused);
                switch (e.which) {
                    case $.ui.keyCode.ENTER:
                        e.preventDefault();
                        const menu = this.menuApps[offsetval];
                        if (menu) {
                            this.menuService.selectMenu(menu);
                        } else {
                            var itmeoffset = offsetval - this.menuApps.length;
                            const Items = this.menuLinks[itmeoffset];
                            if (Items) {
                                this.menuService.selectMenu(Items);
                            }
                        }
                        break;
                    case $.ui.keyCode.DOWN:
                        offsetval++;
                        e.preventDefault();
                        break;
                    case $.ui.keyCode.UP:
                        offsetval--;
                        e.preventDefault();
                        break;
                    case $.ui.keyCode.RIGHT:
                        offsetval++;
                        e.preventDefault();
                        break;
                    case $.ui.keyCode.LEFT:
                        offsetval--;
                        e.preventDefault();
                        break;
                    case $.ui.keyCode.TAB:
                        offsetval++;
                        e.preventDefault();
                        break;
                }
                var new_focused = $(switchmenu[offsetval]);
                var $main_menu = $('.__home_menu');
                pre_focused.removeClass("__active");
                new_focused.addClass("__active");
                if (new_focused.length) {
                    $main_menu.scrollTo(new_focused, {
                        offset: {
                            top: $main_menu.height() * -0.5,
                        },
                    });
                }
            }
            getCurrentCompany() {
                const company = this.companyService.currentCompany;
                if (company && company.id) {
                    const url = '/web/image/res.company/' + company.id + '/logo/180x55';
                    return url;
                }
                return false;
            }
            _filterapps(value) {
                this.filterapps(value);
            }
            _fuzzy(value, apps) {
                return fuzzyLookup(value, apps, (el) =>
                    (el.parents + " / " + el.label).split("/").reverse().join("/")
                );
            }

            filterapps(value) {
                this.state.query = value;
                this.inputRef.el.value = this.state.query;
                if (value === "") {
                    this.menuApps = this.apps;
                    this.menuLinks = [];
                } else {
                    this.menuApps = this._fuzzy(value, this.apps);
                    this.menuLinks = this._fuzzy(value, this.menuItems);
                }
            }
            async _getFavMenuData() {
                self = this
                var favorites = await this.orm.call("ir.favorite.menu", "get_favorite_menus")
                if (favorites) {
                    favorites.forEach(function(menu) {
                        self.state.favoriteMenuById[menu.favorite_menu_id[0]] = menu.id;
                    });
                }
            }
            onEditMenu(ev) {
                var inputval = this.inputRef.el.value;
                if (inputval) {
                    this.inputRef.el.value = '';
                    this.state.query = '';
                    this.menuApps = this.apps;
                    this.menuLinks = [];
                };
                this.state.menuEdit = !this.state.menuEdit;
                const $favorite = $('.o_favorite');
                const $searchmenu = $('.__search_menu');
                $searchmenu.toggleClass('d-md-flex', !this.state.menuEdit).toggleClass('d-none', !!this.state.menuEdit);
                Promise.all([this._getFavMenuData()])
            }
            onNavBarDropdownItemSelection(menu) {
                if (this.state.menuEdit) { return; }
                if (menu) {
                    return this.menuService.selectMenu(menu);
                }
            }
            getMenuItemHref(payload) {
                const parts = [`menu_id=${payload.id}`];
                if (payload.action) {
                    parts.push(`action=${payload.action.split(",")[1]}`);
                }
                return "#" + parts.join("&");
            }
            async _onClickFavorite(payload) {
                var self = this;
                if (_.has(this.state.favoriteMenuById, payload.id)) {
                    var favoriteMenuId = this.state.favoriteMenuById[payload.id]
                    self.bindToRemoveOnUnFavorited(payload, favoriteMenuId);
                } else {
                    self._makeFavourited(payload.label, {
                        favorite_menu_id: payload.id,
                        favorite_menu_xml_id: payload.xmlid,
                        favorite_menu_action_id: payload.actionID,
                        user_id: session.uid
                    });
                }
            }
            // _onAppClick() {
            //     if (this.state.menuEdit) { return; }
            //     this._super(...arguments);
            // }
            async _makeFavourited(name, values) {
                const value = await this.orm.create("ir.favorite.menu", [values]);
                this.state.favoriteMenuById[values.favorite_menu_id] = value;
                core.bus.trigger('click_favorite_menu');
                const message = sprintf(this.env._t('%s added to favorite.'), name);
                this.notification.add(message, { type: "success" }, );
            }
            async bindToRemoveOnUnFavorited(values, favoriteMenuId) {
                const value = await this.orm.unlink("ir.favorite.menu", [favoriteMenuId]);
                if (value) {
                    delete this.state.favoriteMenuById[values.appID]
                    core.bus.trigger('click_favorite_menu');
                    const message = sprintf(this.env._t('%s removed to favorite.'), values.label);
                    this.notification.add(message, { type: "danger" });
                }
            }
            updateCustomizeMenu(type) {
                $('body').toggleClass('oe_home_menu', type);
            }
            // mounted() {
            //     this.updateCustomizeMenu(true);
            // }

            // willUnmount() {
            //     this.updateCustomizeMenu(false);
            //     document.querySelector("nav.o_main_navbar > a.__menu_toggle").classList.remove('__has_action');
            // }
        }
        // import { DropdownItem } from "@web/core/dropdown/dropdown_item";
        NewMenu.components = { NavBar, DropdownItem };
        NewMenu.template = "allure_backend_theme.CustomMenuLayout";
        registry.category("actions").add("acs_menu", NewMenu);
        return {
            async toggle(custom_action) {
                $('.o_menu_systray').removeClass('show');
                const homeMenu = document.querySelector(".__home_menu");
                if (!homeMenu) {
                    const menuToggle = document.querySelector("nav.o_main_navbar > a.__menu_toggle");
                    if (menuToggle) {
                        await ev.services.action.doAction("acs_menu");
                    }
                    if (!custom_action) {
                        ev.services.action.custom_action = true;
                        //menuToggle.classList.add('__has_action');
                    }
                } else if (ev.services.action.custom_action) {
                    ev.services.action.restore();
                }
            }
        }
    }
}
registry.category("services").add("custom_menu", customMenu);