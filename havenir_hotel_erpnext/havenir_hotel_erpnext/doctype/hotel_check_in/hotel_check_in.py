# -*- coding: utf-8 -*-
# Copyright (c) 2020, Havenir and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from datetime import datetime
from frappe.utils import add_to_date, nowdate, getdate



class HotelCheckIn(Document):
    def validate(self):
        for room in self.rooms:
            room_doc = frappe.get_doc('Rooms', room.room_no)
            if room_doc.room_status == 'Checked In' :
                frappe.throw('Room {} is not Available'.format(room.room_no))
        self.validate_room()

            # if room_doc.expectation_id:
            #     expectation_date = room_doc.expectation_date
            #     expectation_doc = frappe.get_doc('Hotel Expectation', room_doc.expectation_id)
            #     duration = add_to_date(expectation_date, days=expectation_doc.duration, as_string=True, as_datetime=True)
            #     check_in_date = datetime(self.check_in)
            #     if datetime(expectation_date) <= check_in_date <= datetime(duration):
            #         frappe.throw('Check-In date must not fall within the Expectation date range for room {}'.format(room.room_no))


    def validate_room(self):
            for room in self.rooms:
                room = frappe.get_doc('Rooms', room.room_no)
                reservations = room.get('reservations')
                if reservations:
                        for reservation in reservations:
                            if getdate(reservation.arrival_date) <= getdate(self.check_in) and getdate(self.check_in) <= getdate(reservation.departure):
                                frappe.throw(f'Room {room.name} is already reserved for the selected date')

    def on_submit(self):
        self.create_sales_invoice()
        self.add_guest_to_in_house_guest()
        self.status = 'To Check Out'
        doc = frappe.get_doc('Hotel Check In', self.name)
        doc.db_set('status', 'To Check Out')
        for room in self.rooms:
            room_doc = frappe.get_doc('Rooms', room.room_no)
            room_doc.db_set('check_in_id', self.name)
            room_doc.db_set('room_status', 'Checked In')
            if room_doc.expectation_id:
                room_doc.db_set('expectation_id', None)
                room_doc.db_set('expectation_date', None)
        # send_payment_sms(self)

    def on_cancel(self):
        self.status = "Cancelled"
        doc = frappe.get_doc('Hotel Check In', self.name)
        doc.db_set('status', 'Cancelled')
        for room in self.rooms:
            room_doc = frappe.get_doc('Rooms', room.room_no)
            room_doc.db_set('check_in_id', None)
            room_doc.db_set('room_status', 'Available')
    # @frappe.whitelist()
    # def get_room_price(self, room):
    #     room_price = frappe.get_value('Rooms', {
    #         'room_number': room
    #     }, [
    #         'price'
    #     ])
    #     return room_price
    
    
           
    

    def create_sales_invoice(self):
        sales_invoice_doc = frappe.new_doc("Sales Invoice")
        company = frappe.get_doc("Company", self.company)
        sales_invoice_doc.discount_amount = 0
        sales_invoice_doc.customer = self.guest_id
        sales_invoice_doc.check_in_id = self.name
        sales_invoice_doc.check_in_date = self.check_in
        sales_invoice_doc.due_date = add_to_date(getdate(self.check_in), days=self.duration, as_string=True)
        sales_invoice_doc.debit_to = company.default_receivable_account

        total_amount = 0
        for room in self.rooms:
            room_price = room.price
            total_amount += float(room_price)  # Convert to float before addition
            sales_invoice_doc.append(
                "items",
                {
                    "item_code": f'Room - {room.room_no}',
                    "qty": float(self.duration),  # Convert to float before assignment
                    "rate": room.rate,  # Convert to float before assignment
                    "amount": float(room.rate) * float(self.duration),  # Convert to float before multiplication
                },
            )
        sales_invoice_doc.insert(ignore_permissions=True)
        sales_invoice_doc.submit()

#add guest to in hosue guest
    def add_guest_to_in_house_guest(self):
        #check if user is already in
    
        if not frappe.db.exists("Guest In House", {'email': self.guest_id}):
            rooms = 'Room '
            for room in self.rooms:
                rooms = f'{rooms}, {room.room_no}'
            doc = frappe.get_doc({
                "doctype": "Guest In House",
                "guest_name": self.guest_name,
                "email": self.guest_id,
                "room": rooms,
                "check_in_date": self.check_in,
                "departure": self.check_out,
                "check_in_id": self.name
            })
            doc.insert()
            doc.save()
        else:
            doc = frappe.get_doc("Guest In House", {'email': self.guest_id})
            rooms = f'{doc.room} '
            for room in self.rooms:
                rooms = f'{rooms}, {room.room_no}'
            doc.db_set('room', rooms)


    #calculate the check out date based on the check in date and duration and the unit of measurement
    def calculate_check_out_date(self):
        if self.check_in and self.duration:
            if self.unit_of_measurement == 'Days':
                return add_to_date(self.check_in, days=self.duration)
            return add_to_date(self.check_in, self.duration, self.unit_of_measurement)
    
    #validate room availability
def send_payment_sms(self):
    sms_settings = frappe.get_doc('SMS Settings')
    if sms_settings.sms_gateway_url:
        msg = 'Dear '
        msg += self.guest_name
        msg += ''',\nWe are delighted that you have selected our hotel. The entire team at the Hotel PakHeritage welcomes you and trust your stay with us will be both enjoyable and comfortable.\nRegards,\nHotel Management'''
        send_sms([self.contact_no], msg = msg)

  