import frappe
from frappe.model.document import Document

@frappe.whitelist()
def get_sales_invoice(guest):
    invoices = frappe.db.sql(f"""  SELECT name FROM 'tabSales Inovice' WHERE customer={guest} """, as_dict=True)
    frappe.msgprint(invoices)
    # return invoices
