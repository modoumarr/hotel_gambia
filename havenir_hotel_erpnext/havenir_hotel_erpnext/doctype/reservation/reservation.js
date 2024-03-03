// Copyright (c) 2024, Havenir and contributors
// For license information, please see license.txt

frappe.ui.form.on('Reservation', {
	refresh: function(frm) {
		//add a button to check in the reservation
				frm.add_custom_button(__('Check In'), function() {
					frm.call({
						method: "havenir_hotel_erpnext.api.check_in",
						args: {
							"doc": frm.doc.name
						},
						callback: function(r) {
							if(r.message) {
								frappe.msgprint(__("Checked In"));
							}
						}
					});

				}, __("Create"))
				//add a create invoice button if the invoice is not created
				if (frm.doc.status == "To Check In" && !frm.doc.invoice_created) {
					frm.add_custom_button(__('Create Invoice'), function() {
						frappe.call({
							method: "havenir_hotel_erpnext.api.create_invoice",
							args: {
								"doc": frm.doc.name
							},
							callback: function(r) {
								if(r.message) {
									frappe.msgprint(__("Invoice Created"));
								}
							}
						});

					}, __("Create"));
				}
			

					
				}
	

			});
