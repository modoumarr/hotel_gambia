# Copyright (c) 2023, Havenir and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class khan(Document):
	def on_submit(self):
		if self.age < 5:
			frappe.msgprint("Please enter a valid Age")