odoo.define('allure_layout.PdfViewer', function(require) {
"use strict";

var Dialog = require('web.Dialog');
var core = require('web.core');
var _t = core._t;
var qWeb = core.qweb;

var PdfViewer = Dialog.extend({

    init: function (parent, options, resState) {
        var self = this;
        var options = _.extend({
            title: resState.name,
            size: 'large',
            buttons: [],
            renderFooter: false,
        }, options || {});

        this._super(parent, options);

        this.cartQuickView = parent;
        this.dialogClass = 'oe_pdf_viewer';
        this.resState = resState;
    },

    _getPdfIframeContent() {
        if (this.resState.mimetype === 'image/svg+xml' || this.resState.mimetype === 'image/png' || this.resState.mimetype === 'image/jpg') {
            return $(qWeb.render('allure_layout.imageViewer'));
        }
        if (this.resState.mimetype === 'application/pdf') {
            return $(qWeb.render('allure_layout.PdfViewerIframe'));
        }
    },

    willStart: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function () {
            self.$modal.addClass('o_pdfviewer_modal');
            self.$content = self._getPdfIframeContent();
        });
    },

    start: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function(){
            self.$('.o_pdfviewer_iframe').attr('src', self._getURI());
        });
    },

    _getURI: function (fileURI) {
        var page = 1;
        if (!fileURI) {
            var queryString = $.param(this.resState);
            fileURI = '/web/content?' + queryString;
        }
        fileURI = '/web/content/ir.attachment/'+this.resState.id+'/datas';
        if (this.resState.mimetype === 'image/svg+xml' || this.resState.mimetype === 'image/png' || this.resState.mimetype === 'image/jpg') {
            return '/web/image/'+this.resState.id+'?unique=&model=ir.attachment';
        }
        if (this.resState.mimetype === 'application/pdf') {
            var viewerURL = '/web/static/lib/pdfjs/web/viewer.html?file=';
            return viewerURL + fileURI + '#page=' + page;
        }
    },

});

return PdfViewer;

});
