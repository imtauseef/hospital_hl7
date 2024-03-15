odoo.define("allure_backend_theme.DashboardGraph", function(require) {
    'use strict';
    var basic_fields = require('web.basic_fields');
    var JournalDashboardGraph = basic_fields.JournalDashboardGraph;
    const session = require('web.session');
    var __themesDB = require('allure_backend_theme.AllureWebThemes');
    const userTheme = __themesDB.get_theme_config_by_uid(session.uid);
    const _isValidHex = function(hexString) { return /^#[0-9A-F]{6}$/i.test(hexString); };
    const THEME_COLORS = _.uniq(_.filter(_.values(__themesDB.default_web_theme), function(value) { return _isValidHex(value); }));
    const invertColor = function(hexTripletColor) {
        var color = hexTripletColor;
        color = color.substring(1); // remove #
        color = parseInt(color, 16); // convert to integer
        color = 0xFFFFFF ^ color; // invert three bytes
        color = color.toString(16); // convert to hex
        color = ("000000" + color).slice(-6); // pad with leading zeros
        color = "#" + color; // prepend #
        return color;
    }

    for (let i = 0; i <= THEME_COLORS.length; i++) {
        if (THEME_COLORS[i]) {
            if (userTheme.mode === "night_mode_on") {
                THEME_COLORS[i] = invertColor(THEME_COLORS[i]);
            } else {
                THEME_COLORS[i] = THEME_COLORS[i];
            }
        }
    }

    JournalDashboardGraph.include({
        /**
         * @override
         */
        _getLineChartConfig: function() {
            var borderColor = this.data[0].is_sample_data ? THEME_COLORS[0] : THEME_COLORS[1];
            var backgroundColor = this.data[0].is_sample_data ? THEME_COLORS[0] : THEME_COLORS[1];
            var res = this._super.apply(this, arguments);
            res.data.datasets = [{
                data: this.data[0].values,
                fill: 'start',
                label: this.data[0].key,
                backgroundColor: backgroundColor,
                borderColor: borderColor,
                borderWidth: 2,
            }]
        },
        /**
         * @override
         */
        _getBarChartConfig: function() {
            var data = [];
            var labels = [];
            var backgroundColor = [];

            this.data[0].values.forEach(function(pt) {
                data.push(pt.value);
                labels.push(pt.label);
                var color = pt.type === 'past' ? THEME_COLORS[0] : (pt.type === 'future' ? THEME_COLORS[1] : THEME_COLORS[2]);
                backgroundColor.push(color);
            });
            var res = this._super.apply(this, arguments);
            res.data.datasets = [{
                data: data,
                fill: 'start',
                label: this.data[0].key,
                backgroundColor: backgroundColor,
            }]
            return res;
        },
    })
});