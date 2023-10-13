frappe.ui.form.on('Guest Check Out', {
	setup: function(frm) {
		// setting query for rooms to be visible in list
		frm.set_query("room", function(doc) {
			return {
				filters: {
					room_status: "Checked In"
				}
			};
		});
	},

	// room: function(frm) {
    //     let guest = frm.doc.guest_id;
    //     if (frm.doc.room) {
    //         frm.call('get_sales_invoice').done((r) => {
	// 			frm.doc.invoices = []
	// 			$.each(r.message, function(_i, e){
	// 				let entry = frm.doc.add_child("invoices");
	// 				entry.invoice = e.name
	// 			})
	
	// 		});
    //     }
    // }

	room: function(frm) {
        if (frm.doc.room) {
            frappe.call({
                method: "get_sales_invoice",
                doc: frm.doc,
                callback: function(r) {

					console.log(r)
				// frm.doc.invoices = []
				// $.each(r.message, function(_i, e){
				// 	let entry = frm.doc.add_child("invoices");
				// 	entry.invoice = e.name


				// })
			}
            });
        }
    }
});
