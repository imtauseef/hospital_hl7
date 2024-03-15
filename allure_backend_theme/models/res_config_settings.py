# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import os
from odoo.http import request
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    video_url = fields.Char(string='URL')
    login_image = fields.Binary('Login Image')
    background_color = fields.Char(string='Background Color', size=7, help="Add HTML Color Code.")
    background_video_layout = fields.Selection([
        ('youtube', 'Youtube/Vimeo/Dailymotion URL'),
        ('other', 'Other Video'),
    ], default='other',
        help="The 'Youtube Video' is used for youtube URL and 'Other Video' is used for other URL")

    @api.constrains('background_color')
    def _check_background_color(self):
        if self.background_color and self.background_color[0] != '#':
            raise ValidationError(_('Kindly add proper color code.'))

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        video_url = params.get_param('base_setup.video_url', default=False)
        login_image = params.get_param('base_setup.login_image', default=False)
        background_color = params.get_param('base_setup.background_color', default=False)
        background_video_layout = params.get_param('base_setup.background_video_layout', default=False)
        res.update(
            video_url=video_url,
            login_image=login_image,
            background_color=background_color,
            background_video_layout=background_video_layout,
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        em_url = self._embed_url(self.video_url)
        self.env['ir.config_parameter'].sudo().set_param("base_setup.video_url", em_url)
        self.env['ir.config_parameter'].sudo().set_param("base_setup.login_image", self.login_image)
        self.env['ir.config_parameter'].sudo().set_param("base_setup.background_color",
                                                         self.background_color)
        self.env['ir.config_parameter'].sudo().set_param("base_setup.background_video_layout",
                                                         self.background_video_layout)
        self._set_bg_color(self.background_color)

    def _set_bg_color(self, bg_color):
        theme_color = request.env['ir.config_parameter'].sudo().get_param('base_setup.background_color')
        if not theme_color:
            theme_color = '#2d7bb8'
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = path + "/static/src/scss/variable_login_screen.scss"

        f = open(path, "w")
        f.write("$brand-primary-login:" + theme_color + ';')
        f.close()

    def _embed_url(self, video_url):
        if video_url:
            if 'youtube' in video_url:
                video_url = video_url.replace("watch?v=", "embed/")
            if 'dailymotion' in video_url:
                video_url = video_url.replace("/video", "/embed/video")
            if 'vimeo' in video_url:
                video_url = "//player.vimeo.com/video/" + video_url.split('/')[-1]     
        return video_url or False
