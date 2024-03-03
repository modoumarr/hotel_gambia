# Copyright (c) 2024, Havenir and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import datetime, add_to_date, nowdate, getdate

class Reservation(Document):
	def validate(self):
		self.validate_room()
		#check if arrival date is not in the past
		if getdate(self.arrival_date) < getdate(nowdate()):
			frappe.throw('Arrival date must not be in the past')
		#check if departure date is not in the past
		if getdate(self.departure) < getdate(nowdate()):
			frappe.throw('Departure date must not be in the past')
		#check if departure date is not less than arrival date
		if getdate(self.departure) < getdate(self.arrival_date):
			frappe.throw('Departure date must not be less than arrival date')
		
	#check in the room if check in button is selected
	
	def on_submit(self):
		self.reserve_room()
		self.status = 'To Check In'
		doc = frappe.get_doc('Reservation', self.name)
		doc.db_set('status', 'To Check In')
		# send_payment_sms(self)

	#set check the reserved field to true
	def reserve_room(self):
		for room in self.rooms:
			room = frappe.get_doc('Rooms', room.room_no)
			room.append('reservations', {
				'reservation_id': self.name,
				'arrival_date': self.arrival_date,
				'departure': self.departure,
				'guest_name': self.guest_name,
			})
			room.save()

	#checkif room is not reserved and not checked in
	def validate_room(self):
		for room in self.rooms:
			room = frappe.get_doc('Rooms', room.room_no)
			reservations = room.get('reservations')
			#validate check in date
			if room.room_status == 'Checked In':
				check_in_date = frappe.db.get_value('Hotel Check In', room.check_in_id, 'check_in')
				check_out_date = frappe.db.get_value('Hotel Check In', room.check_in_id, 'check_out')
				
				if getdate(check_in_date) <= getdate(self.arrival_date) and getdate(self.arrival_date) <= getdate(check_out_date):
					frappe.throw(f'Room {room.name} is already checked in for the selected date')
			if reservations:
					for reservation in reservations:
						if getdate(reservation.arrival_date) <= getdate(self.arrival_date) and getdate(self.arrival_date) <= getdate(reservation.departure):
							frappe.throw(f'Room {room.name} is already reserved for the selected date')
	
	
	#check if invoice is created against this reservation
	def check_invoice(self):
		invoice = frappe.get_list('Sales Invoice', filters={
			'custom_reservation_id': self.name
		})
		if invoice:
			return True
		else:
			return False
	
	#create invoice

