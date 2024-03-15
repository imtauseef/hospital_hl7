# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Allure Backend Theme (For Community Edition)',
    'category': "Themes/Backend",
    'version': '1.0',
    'license': 'OPL-1',
    'summary': 'Flexible, Powerful and Fully Responsive Customized Backend Theme with many features(Favorite Bar, Vertical Horizontal Menu Bar, Night Mode, Tree view of Menu and Sub menu, Fuzzy search for apps, Display density) in Community Edition.',
    'description': """ Flexible, Powerful and Fully Responsive Customized Backend Theme with many features(Favorite Bar,
    Vertical Horizontal Menu Bar, Night Mode, Tree view of Menu and Sub menu, Fuzzy search for apps, Display density).

    allure backend theme
Backend
backend theme
responsive backend theme
responsive frontend theme
responsive web theme
responsive website theme
responsive ecommerce theme

global search
fully responsive
User Interface
Odoo ERP
submenu
main menu[

toggle
ui ux
ui & ux
bootstrap
Customized Layouts
Menu bar
Submenu bar
Control Panel
List view
Search option layout
Form view action buttons
Dashboard
Kanban View
List View Form View
Graph View Pivot View
General View
Calendar View
Planner view Chat Panel
variations
color palette
default color panel
color scheme
colour palette
default colour panel
colour scheme
Dynamic Graph view
desktop layout
tablet layout
mobile layout
desktop view
tablet view
mobile view
favourite bar
full width
horizontal tab
vertical tab
normal view
light view
night view
customized icons
2d icon
3d icon
isometric icon
base icon
dynamic color palette
dynamic colour palette
display density
horizontal menu
vertical menu
full screen
default form view
comfortable
compact
allure
flexible
fuzzy search
theme color
theme colour
app icon
without global search


    """,
    'author': 'Synconics Technologies Pvt. Ltd.',
    'depends': ['web', 'web_editor', 'mail'],
    'website': 'www.synconics.com',
    'data': [
        'data/theme_data.xml',
        'security/security.xml',
        'security/global_search_security.xml',
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
        'views/web_layout_custom.xml',
        'views/ir_module_views.xml',
        'views/search_config_view.xml',
        'wizard/global_search_batch_wizard_view.xml',
        'views/search_config_batch_view.xml',
        'views/webclient_templates.xml',
        'views/res_config_settings_view.xml',
    ],
    'images': [
        'static/description/main_screen.png',
        'static/description/allure_screenshot.png',
    ],
     'assets': {
        'web.assets_common':[
            '/allure_backend_theme/static/src/js/freamwork/config.js',
        ],
        'web._assets_primary_variables' :    [
            # <!-- link scss variables-->
            "allure_backend_theme/static/src/scss/variables.scss",
            "allure_backend_theme/static/src/scss/other_variable.scss",
            "allure_backend_theme/static/src/scss/night_mode/ni_variables.scss",
        ],
        'web.assets_backend': [
            # <!-- Layout File - Start-->
            "/allure_backend_theme/static/src/lib/minicolors/jquery.minicolors.css",
            "/allure_backend_theme/static/src/scss/animation.scss",
            "/allure_backend_theme/static/src/scss/fonts.scss",
            "/allure_backend_theme/static/src/scss/light_mode/light_mode.scss",
            
            #Global Search
            'allure_backend_theme/static/src/js/global_search/global_search.js',
            'allure_backend_theme/static/src/js/global_search/global_auto_complete.js',
            'allure_backend_theme/static/src/scss/input_search.scss',
            'allure_backend_theme/static/src/xml/global_search.xml',

            # Home Menu
            "/allure_backend_theme/static/src/scss/layout/home_menu/home_menu.scss",
            # Left panel
            "/allure_backend_theme/static/src/scss/layout/left_panel/left_menu_horizontal.scss",
            "/allure_backend_theme/static/src/scss/layout/left_panel/left_menu_vertical.scss",
            "/allure_backend_theme/static/src/scss/layout/left_panel/left_menu.scss",
            "/allure_backend_theme/static/src/scss/layout/left_panel/theme_customize_model.scss",
            #control panel
            "/allure_backend_theme/static/src/scss/layout/burger_menu.scss",
            "/allure_backend_theme/static/src/scss/layout/control_panel/control_panel_search.scss",
            "/allure_backend_theme/static/src/scss/layout/control_panel/control_search_options.scss",
            "/allure_backend_theme/static/src/scss/layout/control_panel/control_action_view.scss",
            "/allure_backend_theme/static/src/scss/layout/control_panel/control_panel_top.scss",
            "/allure_backend_theme/static/src/scss/layout/control_panel/control_panel_bottom.scss",
            "/allure_backend_theme/static/src/scss/layout/control_panel/control_panel_model.scss",
            "/allure_backend_theme/static/src/scss/layout/control_panel/control_panel.scss",
            "/allure_backend_theme/static/src/scss/layout/control_panel/search_panel.scss",
            # kanban view
            "/allure_backend_theme/static/src/scss/layout/kanban/group_kanban.scss",
            "/allure_backend_theme/static/src/scss/layout/kanban/ungroup_kanban.scss",
            "/allure_backend_theme/static/src/scss/layout/kanban/kanban_model.scss",
            "/allure_backend_theme/static/src/scss/layout/kanban/kanban_view.scss",
            #List View
            "/allure_backend_theme/static/src/scss/layout/list/list_view.scss",
            #calendar view
            "/allure_backend_theme/static/src/scss/layout/calendar/calendar_view.scss",
            "/allure_backend_theme/static/src/scss/layout/calendar/web_calender.scss",
            # activity view
            "/allure_backend_theme/static/src/scss/layout/activity/activity_view.scss",
            # pivot view
            "/allure_backend_theme/static/src/scss/layout/pivot/pivot_view.scss",
            #discuss
            "/allure_backend_theme/static/src/scss/layout/discuss/composer_view.scss",
            "/allure_backend_theme/static/src/scss/layout/discuss/message_view.scss",
            "/allure_backend_theme/static/src/scss/layout/discuss/video_view.scss",
            "/allure_backend_theme/static/src/scss/layout/discuss/mailbox_mail.scss",
            "/allure_backend_theme/static/src/scss/layout/discuss/chat_view.scss",
            # Form view
            "/allure_backend_theme/static/src/scss/layout/form/form_statusbar.scss",
            "/allure_backend_theme/static/src/scss/layout/form/button_box.scss",
            "/allure_backend_theme/static/src/scss/layout/form/notbook_view.scss",
            "/allure_backend_theme/static/src/scss/layout/form/form_view_mixin.scss",
            "/allure_backend_theme/static/src/scss/layout/form/form_view.scss",
            "/allure_backend_theme/static/src/scss/layout/form/form_model.scss",
            "/allure_backend_theme/static/src/scss/layout/form/setting_view.scss",
            # Graph view
            "/allure_backend_theme/static/src/scss/layout/graph/graph_view.scss",
            # Import view
            "/allure_backend_theme/static/src/scss/layout/import/import_view.scss",
            "/allure_backend_theme/static/src/scss/layout/import/select_drop.scss",
            #App
            "/allure_backend_theme/static/src/scss/layout/app/expense_view.scss",
            "/allure_backend_theme/static/src/scss/layout/app/hr_view.scss",
            "/allure_backend_theme/static/src/scss/layout/app/lunch_view.scss",
            "/allure_backend_theme/static/src/scss/layout/app/purchase_view.scss",
            #core
            "/allure_backend_theme/static/src/scss/layout/core/loading.scss",
            "/allure_backend_theme/static/src/scss/layout/core/error_message_view.scss",
            "/allure_backend_theme/static/src/scss/layout/core/nocontent_view.scss",
            "/allure_backend_theme/static/src/scss/layout/core/signout_layout.scss",
            "/allure_backend_theme/static/src/scss/layout/core/effects.scss",
            "/allure_backend_theme/static/src/scss/layout/web_client.scss",
            "/allure_backend_theme/static/src/scss/layout/layout.scss",
            # <!-- Responsive -->
            #left_panel
            "/allure_backend_theme/static/src/scss/responsive/left_panel/left_menu.scss",
            #app
            "/allure_backend_theme/static/src/scss/responsive/app/r_hr_view.scss",
            "/allure_backend_theme/static/src/scss/responsive/home_menu.scss",
            "/allure_backend_theme/static/src/scss/responsive/chat_view.scss",
            "/allure_backend_theme/static/src/scss/responsive/control_panel_view.scss",
            "/allure_backend_theme/static/src/scss/responsive/kanban_view.scss",
            "/allure_backend_theme/static/src/scss/responsive/list_view.scss",
            "/allure_backend_theme/static/src/scss/responsive/responsive_form_view.scss",
            "/allure_backend_theme/static/src/scss/responsive/configration.scss",
            "/allure_backend_theme/static/src/scss/responsive/mail_view.scss",
            "/allure_backend_theme/static/src/scss/responsive/pivot_view.scss",
            "/allure_backend_theme/static/src/scss/responsive/base_settings.scss",
            "/allure_backend_theme/static/src/scss/responsive/responsive_xs.scss",
            # <!-- Rtl -->
            "/allure_backend_theme/static/src/scss/rtl/rtl.scss",
            # <!-- Lib -->
            "/allure_backend_theme/static/src/lib/custom_radiobutton.scss",
            "/allure_backend_theme/static/src/lib/custom_checkbox.scss",
            # <!-- NI mode -->
            "/allure_backend_theme/static/src/scss/night_mode/freamwork/ni_control_panel.scss",
            "/allure_backend_theme/static/src/scss/night_mode/freamwork/ni_header_layout.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_home_menu.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_kanban_view.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_list_view.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_graph_layout.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_activity_view.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_barcode_view.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_pivot_view.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/dashboard.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_calander_view.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_mail_view.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_gernal_setting_view.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_dashboards_view.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_form_view.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_model_view.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_import_view.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_window_chnage_view.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_attendance_view.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_lunch_view.scss",
            "/allure_backend_theme/static/src/scss/night_mode/views/ni_purchase_view.scss",
            "/allure_backend_theme/static/src/scss/night_mode/ni_common_layout.scss",
            "/allure_backend_theme/static/src/scss/night_mode/ni_layout.scss",

            # <!-- JS Path - start -->
            "/allure_backend_theme/static/src/js/allure_web_themes.js",
            "/allure_backend_theme/static/src/lib/minicolors/jquery.minicolors.min.js",
            "/allure_backend_theme/static/src/js/main_view.js",
            # "/allure_backend_theme/static/src/js/views/res_config_settings.js",
            "/allure_backend_theme/static/src/js/views/menu.js",
            "/allure_backend_theme/static/src/js/chrome/error_handlers.js",
            "/allure_backend_theme/static/src/js/components/chat_window/chat_window.js",
            "/allure_backend_theme/static/src/js/components/action_menus.js",
            "/allure_backend_theme/static/src/js/components/dropdown_navigation_hook.js",
            "/allure_backend_theme/static/src/js/components/dropdown_menu.js",
            "/allure_backend_theme/static/src/js/components/dropdown.js",
            "/allure_backend_theme/static/src/js/views/control_panel/filter_menu.js",
            "/allure_backend_theme/static/src/js/views/control_panel/control_panel.js",
            "/allure_backend_theme/static/src/js/views/control_panel/control_panel_ext.js",
            "/allure_backend_theme/static/src/js/views/control_panel/search_bar.js",
            "/allure_backend_theme/static/src/js/search/search_panel.js",
            "/allure_backend_theme/static/src/js/search/search_bar/search_bar.js",
            "/allure_backend_theme/static/src/js/webclient/navbar/navbar.js",
            # "/allure_backend_theme/static/src/js/webclient/navbar/systray_activity_menu.js",
            "/allure_backend_theme/static/src/js/webclient/menubar.js",
            "/allure_backend_theme/static/src/js/webclient/favorite_menu_view.js",
            # "/allure_backend_theme/static/src/js/webclient/action_service.js",
            "/allure_backend_theme/static/src/js/webclient/webclient.js",
            "/allure_backend_theme/static/src/js/webclient/custom_menu/custom_menu.js",
            "/allure_backend_theme/static/src/js/webclient/custom_menu/menus/menu_helpers.js",
            # "/allure_backend_theme/static/src/js/services/systray_hepler.js",
            # "/allure_backend_theme/static/src/js/views/search_panel_mobile.js",
            "/allure_backend_theme/static/src/js/views/form/form_renderer.js",
            "/allure_backend_theme/static/src/js/views/form/notebook.js",
            # "/allure_backend_theme/static/src/js/views/list/list_model.js",
            "/allure_backend_theme/static/src/js/views/list/list_controller.js",
            "/allure_backend_theme/static/src/js/views/list/list_renderer.js",
            "/allure_backend_theme/static/src/js/views/list/viewer.js",
            "/allure_backend_theme/static/src/js/views/list/list_view.js",
            # "/allure_backend_theme/static/src/js/views/kanban/kanban_column_quick_create_mobile.js",
            # "/allure_backend_theme/static/src/js/views/kanban/kanban_controller.js",
            # "/allure_backend_theme/static/src/js/views/kanban/kanban_renderer_mobile.js",
            # "/allure_backend_theme/static/src/js/views/kanban/kanban_view.js",
            "/allure_backend_theme/static/src/js/views/graph/color.js",
            "/allure_backend_theme/static/src/js/views/graph/graph_renderer.js",
            "/allure_backend_theme/static/src/js/freamwork/dashboard.js",
            # "/allure_backend_theme/static/src/js/views/import_action.js",
            "/allure_backend_theme/static/src/js/core/dialog.js",
            "/allure_backend_theme/static/src/js/core/block_ui.js",
            # "/allure_backend_theme/static/src/js/fields/relational_fields.js",
            # "/allure_backend_theme/static/src/js/fields/basic_fields.js",
            # "/allure_backend_theme/static/src/js/responsive/breadcrumb.js",
            # '/allure_backend_theme/static/src/js/main.js',

            'allure_backend_theme/static/src/xml/*.xml',
            'allure_backend_theme/static/src/xml/**/*.xml',

            #webclient
            '/allure_backend_theme/static/src/js/services/*.js',
            '/allure_backend_theme/static/src/xml/base.xml',
            '/allure_backend_theme/static/src/xml/dashboard.xml',
            '/allure_backend_theme/static/src/xml/notebook.xml',
            # '/allure_backend_theme/static/src/xml/mobile.xml',
            '/allure_backend_theme/static/src/xml/navbar.xml',
            '/allure_backend_theme/static/src/xml/quick_menu.xml',
        ],
        'web.assets_frontend': [
            'allure_backend_theme/static/src/scss/login_scss/variable_login_screen.scss',
            'allure_backend_theme/static/src/scss/login_scss/login_view.scss',
            'allure_backend_theme/static/src/scss/login_scss/responsive_login_screen.scss',
            'allure_backend_theme/static/src/scss/login_scss/login_fonts.scss',
        ],
        'web.assets_backend_prod_only': [
            # '/allure_backend_theme/static/src/js/main.js',
            ('replace', 'web/static/src/main.js', '/allure_backend_theme/static/src/js/main.js'),
        ],
        # 'web.assets_qweb': [
            # 'allure_backend_theme/static/src/xml/*.xml',
            # 'allure_backend_theme/static/src/xml/**/*.xml',
        # ],
    },
    'post_init_hook': 'post_init_check',
    'uninstall_hook': 'uninstall_hook',
    'price': 250.0,
    'currency': 'USD',
    'installable': True,
    'auto_install': False,
    'bootstrap': True,
}
