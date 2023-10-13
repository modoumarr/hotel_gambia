import frappe
from frappe.model.document import Document

class GuestCheckOut(Document):

    @frappe.whitelist()
    def get_sales_invoice(self):
       customer = self.guest_id
       invoices = frappe.db.get_list("Sales Invoice", filters={"customer": customer}, fields=["name"], as_list=True)
       return invoices
