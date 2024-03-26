from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    complaint_responsible_id = fields.Many2one(
        related='company_id.complaint_responsible_id', readonly=False
    )
