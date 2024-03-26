from odoo.tests import TransactionCase, tagged
from odoo.exceptions import ValidationError


class TestComplaint(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_bp_complaint(self):
        # Create a complaint
        compaint_type = self.env['bp.complaint.type'].create({'name': 'Test Type'})
        compaint = self.env['bp.complaint'].create(
            {
                'city': 'Stuttgart',
                'street': 'Königstraße 123',
                'zip': '70173',
                'subject': 'Test Subject',
                'tenant_name': 'Test Tenant',
                'complaint_type': compaint_type.id,
                'email_from': 'test_tenant@testemail.bp',
                'description': 'It is too cold here',
            }
        )
        # Basic checks
        self.assertIn('BC/', compaint.name, msg="Wrong sequence")
        self.assertTrue(compaint.partner_id, msg="Missing partner")
        self.assertEqual(
            compaint.user_id,
            self.env.company.complaint_responsible_id,
            msg="Wrong responsible"
        )
        # Search for "Your complaint has been received" email
        email = self.env['mail.mail'].search(
            [
                ('res_id', '=', compaint.id),
                ('model', '=', compaint._name),
            ]
        )
        self.assertTrue(email, msg="Notification email missing")
        self.assertIn(compaint.name, email.subject, msg="Wrong email subject")

        # Partner is mandatory check
        partner = compaint.partner_id
        compaint.partner_id = False
        with self.assertRaises(ValidationError):
            compaint.action_send_email()
        compaint.partner_id = partner
        action = compaint.action_send_email()

        # Test mail composer
        self.assertEqual(action['type'], 'ir.actions.act_window')
        composer = self.env['mail.compose.message'].browse(action['res_id'])
        # Send email to the tenant
        composer.action_send_mail()
        emails = self.env['mail.mail'].search(
            [
                ('res_id', '=', compaint.id),
                ('model', '=', compaint._name),
            ]
        )
        self.assertEqual(len(emails), 2, msg="Wrong quantity of emails")

        # Test workorder report
        compaint.workorder_todo = "Fix heating"
        wo_report = self.env.ref('bp_complaint.report_report_workorder', raise_if_not_found=True)
        rendered = wo_report._render('bp_complaint.report_report_workorder', compaint.id)
        html = rendered[0].decode()
        self.assertIn(
            compaint.name,
            html,
            msg="Missing complaint name in workorder report"
        )
        self.assertIn(
            compaint.workorder_todo,
            html,
            msg="Missing workorder_todo in workorder report"
        )

    def test_01_ui_complaint(self):
        # UI can be tested with HttpCase
        # self.start_tour("/", 'complaint_tour', step_delay=100)
        pass
