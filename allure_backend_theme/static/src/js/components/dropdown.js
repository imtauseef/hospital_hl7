/** @odoo-module **/
import { Dropdown } from "@web/core/dropdown/dropdown";
const { patch } = require('web.utils');

import { useBus, useService } from "@web/core/utils/hooks";
import { usePosition } from "@web/core/position_hook";
import { useDropdownNavigationCustom } from "./dropdown_navigation_hook";
import { ParentClosingMode } from "@web/core/dropdown/dropdown_item";
import { localization } from "@web/core/l10n/localization";
import  { qweb as QWeb, _t } from 'web.core';
import { KanbanDropdownMenuWrapper } from "@web/views/kanban/kanban_dropdown_menu_wrapper"; 

const { Component, core, useState, useEffect, EventBus, onWillStart, 
useExternalListener, useRef, useSubEnv, useChildSubEnv } = owl;

const DIRECTION_CARET_CLASS = {
    bottom: "dropdown",
    top: "dropup",
    left: "dropleft",
    right: "dropright",
};
export const DROPDOWN = Symbol("Dropdown");
patch(KanbanDropdownMenuWrapper.prototype, 'KanbanDropdownMenuWrapper.Extends', {
    onClick(ev) {
        this.env[DROPDOWN].closeAllParents();
    }
});
patch(Dropdown.prototype, '@allure_backend_theme/js/components/dropdown.js', {
    /**
     * @override
     */
    setup() {
        /** @todo Add super */
        this.state = useState({
            open: this.props.startOpen,
            groupIsOpen: this.props.startOpen,
        });
        this.rootRef = useRef("root");
        owl.onMounted(() => {
            if (document.body.classList.contains('modal-open')) {
                this.state.groupIsOpen = false;
                this.state.open = false;
            }
        });
        // Set up beforeOpen ---------------------------------------------------
        onWillStart(() => {
            if (this.state.open && this.props.beforeOpen) {
                return this.props.beforeOpen();
            }
        });

        // Set up dynamic open/close behaviours --------------------------------
        if (!this.props.manualOnly) {
            // Close on outside click listener
            useExternalListener(window, "click", this.onWindowClicked, { capture: true });
            // // Listen to all dropdowns state changes
            // useBus(Dropdown.bus, "state-changed", ({ detail }) =>
            //     this.onDropdownStateChanged(detail)
            // );
            // Listen to all dropdowns state changes
            // useBus(Dropdown.bus, "state-changed", this.onDropdownStateChanged);
        }

        // Set up UI active element related behavior ---------------------------
        this.ui = useService("ui");
        useEffect(
            () => {
                Promise.resolve().then(() => {
                    this.myActiveEl = this.ui.activeElement;
                });
            },
            () => []
        );

        // Set up nested dropdowns ---------------------------------------------
        this.hasParentDropdown = this.env.inDropdown;
        useSubEnv({ inDropdown: true });
        // Set up nested dropdowns ---------------------------------------------
        this.parentDropdown = this.env[DROPDOWN];
        useChildSubEnv({
            [DROPDOWN]: {
                close: this.close.bind(this),
                closeAllParents: () => {
                    this.close();
                    if (this.parentDropdown) {
                        this.parentDropdown.closeAllParents();
                    }
                },
            },
        });

        // Set up key navigation -----------------------------------------------
        useDropdownNavigationCustom();
        // Set up toggler and positioning --------------------------------------
        /** @type {string} **/
        let position =
            this.props.position || (this.hasParentDropdown ? "right-start" : "bottom-start");
        let [direction, variant = "middle"] = position.split("-");
        if (localization.direction === "rtl") {
            if (["bottom", "top"].includes(direction)) {
                variant = variant === "start" ? "end" : "start";
            } else {
                direction = direction === "left" ? "right" : "left";
            }
            position = [direction, variant].join("-");
        }
        const positioningOptions = {
            popper: "menuRef",
            position,
            onPositioned: (el, { direction, variant }) => { 
                if (this.parentDropdown && ["right", "left"].includes(direction)) { 
                    // Correctly align sub dropdowns items with its parent's    
                    if (variant === "start") {  
                        el.style.marginTop = "calc(-.5rem - 1px)";  
                    } else if (variant === "end") { 
                        el.style.marginTop = "calc(.5rem - 2px)";   
                    }   
                }   
            },
        };
        this.directionCaretClass = DIRECTION_CARET_CLASS[direction];
        this.togglerRef = useRef("togglerRef");
        if (this.props.toggler === "parent") {
            // Add parent click listener to handle toggling
            useEffect(
                () => {
                    const onClick = (ev) => {
                        if (this.rootRef.el.contains(ev.target)) {
                            // ignore clicks inside the dropdown
                            return;
                        }
                        this.toggle();
                    };
                    if (this.rootRef.el) {
                        this.rootRef.el.parentElement.addEventListener("click", onClick);
                        return () => {
                            this.rootRef.el.parentElement.removeEventListener("click", onClick);
                        };
                    }
               },
                () => []
            );

            // Position menu relatively to parent element
            if (this.rootRef.el) {
                usePosition(() => this.rootRef.el.parentElement, positioningOptions);
            }
       } else {
            // Position menu relatively to inner toggler
            const togglerRef = useRef("togglerRef");
            usePosition(() => togglerRef.el, positioningOptions);
        }
    },
    /**
     * @override
     */
    onTogglerClick(ev) {
        var self = this;
        const dropdownEl = $(ev.target.parentElement) && $(ev.target.parentElement)[0] && $(ev.target.parentElement)[0].parentElement.querySelectorAll('.show');
        // const isSearch = $(ev.target.parentElement) && $(ev.target.parentElement)[0] &&  $($(ev.target.parentElement)[0].parentElement).hasClass('o_search_options');
        dropdownEl.forEach(function(item) {
            if (!document.body.classList.contains('modal-open') && item.querySelector('.dropdown-menu')) {
                var button = item.querySelector('button');
                button.click();
            }
        });
        this._super(...arguments);
    },
    /**
     * @override
     */
    onWindowClicked(ev) {
        if ($(ev.target).hasClass('scale_button_selection')) {
            console.log("?????????????//", $(ev.target).hasClass('scale_button_selection'))
            // $(ev.target).parents('.show').find('.d-block').remove()
            $(ev.target).parents('.show').removeClass('show')
            $('.o_cp_bottom_right').click();
            $('.o_cp_bottom_left').click();
        }
        if (document.body.classList.contains('modal-open')) {
            const dropdownEl = document.querySelector('.modal-body .o_dropdown_allure.show')
            var button = dropdownEl && dropdownEl.querySelector('button');
            // Close if we clicked outside the dropdown, or outside the parent
            if (button && !button.contains(ev.target) && !ev.target.classList.contains('o_input') &&
                !ev.target.classList.contains('custom-control-label') &&
                !ev.target.classList.contains('custom-control-input') && !ev.target.classList.contains('focus')) {
                button.click();
                $(dropdownEl).removeClass('show');
                $(dropdownEl.querySelector('.o-dropdown--menu')).removeClass('d-block');
            }
        } else {
            const isSearch = $(ev.target.parentElement) && $(ev.target.parentElement)[0] &&  $($(ev.target.parentElement)[0].parentElement).hasClass('o_search_options');
            if ($(ev.target).hasClass('dropdown-toggle') && $(ev.target).closest('.o_statusbar_buttons').length > 0) {
                $(ev.target).parents('.show').removeClass('show')
                $('.o_cp_bottom_right').click();
                $('.o_cp_bottom_left').click();
            }
            if (isSearch === false) {
                this._super(...arguments);
            }
        }
    }
});