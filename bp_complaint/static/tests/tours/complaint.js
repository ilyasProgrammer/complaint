odoo.define('bp_complaint.tour', function (require) {
'use strict';

    var tour = require("web_tour.tour");
    //odoo.startTour("complaint_tour");

    tour.register('complaint_tour', {
            url: '/complaint',
            test: true,
        },
        [
            {
                trigger: 'input[name="tenant_name"]',
                run: "text David Beckham",
            },
            {
                trigger: 'input[id="contact2"]',
                run: "text Berlin",
            },
            {
                trigger: 'input[name="street"]',
                run: "text Stresemannstraße 123",
            },
            {
                trigger: 'input[name="zip"]',
                run: "text 110000",
            },
            {
                trigger: 'input[name="email_from"]',
                run: "text david_b@bestfootbal.gg",
            },
            {
                trigger: 'input[name="subject"]',
                run: "text I need help",
            },
            {
                trigger: 'textarea[name="description"]',
                run: "text Need to replace the bulb in the kitchen",
            },
            {
                trigger: 'a[id="submit_button"]',
                run: "click",
            },
        ]
    );

});
