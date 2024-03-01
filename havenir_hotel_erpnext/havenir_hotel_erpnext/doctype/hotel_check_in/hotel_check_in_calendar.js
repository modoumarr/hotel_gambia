frappe.views.calendar["Hotel Check In"] = {
	field_map: {
		"start": "check_in",
		"end": "check_out_date",
		"title": "guest_name",
		"eventColor": "color",
        "status":"status"
	},
	gantt: true,
	
	get_events_method: "havenir_hotel_erpnext.havenir_hotel_erpnext.doctype.hotel_check_in.hotel_check_in.get_events"
}

