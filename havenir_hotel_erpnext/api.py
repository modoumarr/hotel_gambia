import frappe
from frappe.model.document import Document
from erpnext.accounts.utils import get_balance_on

@frappe.whitelist()
def get_sales_invoice(guest):
    invoices = frappe.db.sql(f"""  SELECT name FROM 'tabSales Inovice' WHERE customer={guest} """, as_dict=True)
    frappe.msgprint(invoices)
    # return invoices

@frappe.whitelist()
def get_unpaid():
    #get all guests
    guests = frappe.db.get_list('Hotel Guests', fields=['name', 'balance'])
    for guest in guests:
        balance = get_balance_on(
            party_type='Customer',
            party=guest.name
        )
        guest.balance = balance
        guest.save()
        

    # return invoices
@frappe.whitelist()
def create_invoice(doc, method=None):
    doc = frappe.get_doc("Reservation", doc)
    if doc.invoice_created:
        frappe.msgprint("Invoice already created for this reservation")
    else:
        sales_invoice_doc = frappe.new_doc("Sales Invoice")
        company = frappe.get_doc("Company", doc.company)
        sales_invoice_doc.discount_amount = 0
        sales_invoice_doc.customer = doc.guest_id
        sales_invoice_doc.custom_reservation_id = doc.name
        sales_invoice_doc.due_date = doc.departure
        sales_invoice_doc.debit_to = company.default_receivable_account

        total_amount = 0
        for room in doc.rooms:
            room_price = room.price
            total_amount += float(room_price)
            sales_invoice_doc.append(
                "items",
                {
                    "item_code": f'Room - {room.room_no}',
                    "qty": float(doc.duration),
                    "rate": float(room_price),
                    "amount": float(room_price)*float(doc.duration),
                },
            )
        sales_invoice_doc.insert(ignore_permissions=True)
        sales_invoice_doc.submit()
        frappe.db.set_value('Reservation', doc.name, 'invoice_created', 1)

    @frappe.whitelist()
    def check_in_reservation(source_name, target_doc=None):
        reservation = frappe.get_doc('Reservation', source_name)
        for room in reservation.rooms:
            room_doc = frappe.get_doc('Rooms', room.room_no)
            room_doc.append('reservations', {
                'reservation_id': reservation.name,
                'arrival_date': reservation.arrival_date,
                'departure': reservation.departure,
                'guest_name': reservation.guest_name,
            })
            room_doc.save()
        reservation.status = 'To Check In'
        reservation.save()
        
        