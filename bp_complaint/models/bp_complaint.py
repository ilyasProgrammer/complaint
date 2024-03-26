from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BPComplaint(models.Model):
    _name = 'bp.complaint'
    _description = 'Complaint'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    name = fields.Char(
        'Name', copy=False, readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('bp.complaint'))
    tenant_name = fields.Char(required=True)
    partner_id = fields.Many2one('res.partner', "Customer")
    city = fields.Char(required=True)
    street = fields.Char(required=True)
    zip = fields.Char()
    email_from = fields.Char('Email', required=True)
    subject = fields.Char(required=True)
    description = fields.Text(required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('in_review', 'In Review'),
        ('in_progress', 'In Progress'),
        ('solved', 'Solved'),
        ('dropped', 'Dropped'),
    ], default='new', tracking=True)
    complaint_type = fields.Many2one('bp.complaint.type', required=True)
    user_id = fields.Many2one(
        'res.users', 
        'Responsible', 
        default=lambda self: self.env.company.complaint_responsible_id,
        required=True,
        tracking=True
    )
    workorder_todo = fields.Text(tracking=True)
    l10n_din5008_template_data = fields.Binary(compute='_compute_l10n_din5008_template_data')
    l10n_din5008_document_title = fields.Char(compute='_compute_l10n_din5008_document_title')

    def _compute_l10n_din5008_template_data(self):
        for record in self:
            current_datetime = fields.Datetime.context_timestamp(record, fields.Datetime.now()).date()
            record.l10n_din5008_template_data = data = []
            data.append((_("for Complaint No."), record.name))
            data.append((_("Complaint Type"), record.complaint_type.name))
            data.append((_("Subject"), record.subject))
            data.append((_("Responsible"), record.user_id.name))
            data.append((_("Complaint Date"), record.create_date.date()))
            data.append((_("Workorder Date"), current_datetime))

    def _compute_l10n_din5008_document_title(self):
        for record in self:
            record.l10n_din5008_document_title = _("Workorder ") + record.name

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('email_from'):
                # Find or create partner for the tenant
                # TODO update partner details if already exist? Create new contact for new address ?
                partner = self.env['res.partner'].search([('email', '=', vals['email_from'])])
                if not partner:
                    partner = self.env['res.partner'].create(
                        {
                            'email': vals['email_from'],
                            'name': vals['tenant_name'],
                            'city': vals['city'],
                            'zip': vals.get('zip'),
                            'street': vals['street'],
                         }
                    )
                vals['partner_id'] = partner.id
        records = super(BPComplaint, self).create(vals_list)
        # Send notification email
        mail_template = self.env.ref('bp_complaint.mail_template_complaint_received')
        for rec in records:
            # TODO Do not send email if created from backend ?
            email_values = {
                'email_cc': False,
                'auto_delete': False,
                'recipient_ids': [],
                'partner_ids': [],
                'scheduled_date': False,
            }
            mail_template.send_mail(
                rec.id, force_send=True, raise_exception=False, email_values=email_values
            )
        return records

    def action_send_email(self):
        # Open email composer
        self.ensure_one()
        if not self.partner_id:
            raise ValidationError(_("Select or create customer first."))
        composer = self.env['mail.compose.message'].with_context({
            'default_model': self._name,
            'active_ids': [self.id],
            'active_model': self._name,
            'active_id': self.id
        }).create({'partner_ids': [(6, 0, self.partner_id.ids)]})
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': _('Complaint email'),
            'view_mode': 'form',
            'res_model': composer._name,
            'res_id': composer.id,
        }


class BPComplaintType(models.Model):
    _name = 'bp.complaint.type'
    _description = "Complaint Type"

    name = fields.Char()


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Might be useful in future to see all complaints of a tenant
    complaint_ids = fields.One2many('bp.complaint', 'partner_id')
