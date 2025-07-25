# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SurveyWithType(models.Model):

    _inherit = "survey.survey"

    type_id = fields.Many2one("survey.type", "Type", ondelete="restrict")
