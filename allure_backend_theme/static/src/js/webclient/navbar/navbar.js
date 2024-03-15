/** @odoo-module **/
import { browser } from "@web/core/browser/browser";
import { NavBar } from "@web/webclient/navbar/navbar";
import { patch } from 'web.utils';
import { useService } from "@web/core/utils/hooks";

patch(NavBar.prototype, 'web/static/src/webclient/navbar/navbar.js', {
    setup() {
        this._super();
        this.user = useService("user");
        const { origin } = browser.location;
        const { userId } = this.user;
        this.source = `${origin}/web/image?model=res.users&field=avatar_128&id=${userId}`;
        this.source;
        // this.props.apps.forEach((app) => {
        //     if (app.xmlid === 'allure_backend_theme.menu_global_search') {
        //         app.webIconData = __themesDB.default_web_theme.base_menu_icon === 'base_icon' && '/allure_backend_theme/static/src/img/global_search.png'
        //         || __themesDB.default_web_theme.base_menu_icon === '2d_icon' && '/allure_backend_theme/static/src/img/menu_2d/global_search.png'
        //         || __themesDB.default_web_theme.base_menu_icon === '3d_icon' && '/allure_backend_theme/static/src/img/menu/global_search.png';
        //     }
        // });
    },
    // /**
    //  * @private
    //  */
    // userData() {
    //     const { origin } = browser.location;
    //     const { userId } = this.user;
    //     this.source = `${origin}/web/image?model=res.users&field=avatar_128&id=${userId}`;
    //     console.log("???????????///", this.source)
    //     return this.source;
    // },

    CloseUserMenu() {
        $('.o_menu_systray').removeClass('show');
    }
});