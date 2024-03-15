/** @odoo-module **/

import { startWebClient } from "@web/start";
import { WebClientCustomize } from "./webclient/webclient";

var __themesDB = require('allure_backend_theme.AllureWebThemes');
var session = require('web.session');
// Added Global
window['AllureTheme'] = __themesDB.get_theme_config_by_uid(session.uid);
startWebClient(WebClientCustomize);