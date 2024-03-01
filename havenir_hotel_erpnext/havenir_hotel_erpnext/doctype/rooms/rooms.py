# -*- coding: utf-8 -*-
# Copyright (c) 2020, Havenir and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Rooms(Document):
	def validate(self):
		if not frappe.db.exists("Item", f'Room - {self.room_number}'):
			item = frappe.new_doc("Item")
			item.item_code = f'Room - {self.room_number}'
			item.item_name = f'Room - {self.room_number}'
			item.is_stock_item = 0
			item.include_item_in_manufacturing = 0  
			item.item_group = "Rooms"
			is_purchased = 0
			item.insert()
			frappe.db.commit()

	def on_trash(self):
		item_name = f'Room - {self.room_number}'
		if frappe.db.exists("Item", item_name):
			frappe.delete_doc("Item", item_name)