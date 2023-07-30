from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class HotelGuests(Document):
    def validate(self):
        if not frappe.db.exists("Customer", self.email):
            customer = frappe.new_doc("Customer")
            customer.email = self.email
            customer.customer_name = self.guest_name
            customer.customer_group = "Individual"
            customer.customer_type = "Individual"
            
            
            customer.insert()
            frappe.db.commit()

    def on_trash(self):
        customer = self.email
        if frappe.db.exists("Customer", customer):
              frappe.delete_doc("Customer", customer)