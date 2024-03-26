from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    complaint_responsible_id = fields.Many2one(
        'res.users',
        string='Complaint Responsible',
        default=lambda self: self.env.ref('base.user_admin')
    )
