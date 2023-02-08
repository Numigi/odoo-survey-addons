# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Partner(models.Model):

    _inherit = 'res.partner'

    survey_answers_count = fields.Integer(
        compute='_compute_survey_answers_count')

    def _compute_survey_answers_count(self):
        for partner in self:
            partner.survey_answers_count = self.env['survey.user_input'].search([
                ('partner_id', 'child_of', partner.id),
            ], count=True)
