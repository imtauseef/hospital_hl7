/** @odoo-module **/

import { NavBar } from "@web/webclient/navbar/navbar";
import { useService } from "@web/core/utils/hooks";
const { Component, hooks } = owl;
import { SearchDropdownItem } from "@web/search/search_dropdown_item/search_dropdown_item";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { Dropdown } from "@web/core/dropdown/dropdown";

export class FavoriteMenu extends Component {
    setup() {
        super.setup();

        this.CustomMenu = useService("custom_menu");
    }
}
FavoriteMenu.template = "web.NavBar.favroitMenu";