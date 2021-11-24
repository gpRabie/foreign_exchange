import frappe

def before_save(doc, method):
    doc.name = doc.customer_tracking_no