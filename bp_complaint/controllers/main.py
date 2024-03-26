from odoo import http
from odoo.http import request


class WebsiteComplaintController(http.Controller):

    @http.route(['/complaint'], type='http', auth="public", website=True)
    def complaints(self, **kwargs):
        values = {
            'complaint_types': request.env['bp.complaint.type'].sudo().search([]),
        }
        return request.render("bp_complaint.complaint_page_template", values)
