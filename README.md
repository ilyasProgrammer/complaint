# Complaint
Website Complaint Odoo module for Odoo 16.0 CE or EE

## Description
Module provides feature for tenants to file complaints from the website form without authentication.
In the backend complaint records are created, using which customer care team can handle complaints, take appropriate actions, log progress and send emails to tenants.

## Installation
* You need to have Odoo 16.0 community or enterprise installed in order to use this module.
* No 3rd party modules or specific python libs are required. 
* Clone or download repository.
* Add complete path to the root folder where module itself located into your Odoo config file. 
* Enable debug mode (/web?debug=1). In Odoo Apps click Update Apps List.
* Search for module bp_complaint and activate it.

## How to use
* Video demo: https://recordit.co/O3kbhBu2C1
* Login into Odoo as an admin user.
* In the Odoo backend go to general settings. 
* Look for Complaint Responsible setting in the Users section and set responsible user. Save changes.
* From the main menu go to Complaints -> Complaint Types. Here you can edit or create new complaint types.

### To try main workflow:
* Logout from Odoo.
* Click Complaint.
* Fill up all fields as a tenant, provide problem description and press Submit button. 
* You will see confirmation page, telling that complaint has been received.
* Login into Odoo and go to Complaints -> Complaints.
* Here you will see created complaint. Click it. In the chatter you can see confirmation email has been sent to the tenant.
* For each tenant contact record (res.partner) is created based on tenant email.
* Here you can click status bar to change complaint status.
* You can enter Workorder Todo instructions and then click Print -> Workorder to print workorder form.
* There is Send Email button in the complaint form. You can use it to send emails to the tenant.
* All send emails are reflected in the chatter.
* You can add support team members as followers and use internal communication or create activities related to a complaint.
* You can create complaints directly from the backend. **Consider that email to tenant will be send right after complaint is created.**

## Technical information
* Module creates 2 new models: bp.complaint and bp.complaint.type.
* Regular users (all internal users) can read, create, edit records.
* Delete records access available only to admin users (group_system). 
* To run unit tests run odoo with argument: -u bp_complaint --test-enable
* To run UI test (JS tour) you need to use ?debug=tests. Open debug console. Enter: odoo.startTour("complaint_tour");

## Roadmap
Some code updates can be done based on business logic requirements.
* Update customer info when new complaint created for existing tenant. Maybe create new child contact for each new address for the same tenant (email).
* Setting to not send notification email to tenants, if complaint created from the backend.
* Use portal instead.
* Check ToDos in the code.
