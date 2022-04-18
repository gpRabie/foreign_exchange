import frappe
import json
from frappe.utils.csvutils import read_csv_content, get_csv_content_from_google_sheets
from datetime import datetime
from frappe.utils import flt, add_to_date, today


@frappe.whitelist()
def get_data(url):
	content = get_csv_content_from_google_sheets(url)
	raw_data = read_csv_content(content)
	data = json.dumps(raw_data)
	new_data = json.loads(data)
	return new_data

@frappe.whitelist()
def create_new_journal_entry():
	data = get_data('https://docs.google.com/spreadsheets/d/1Id-1_SYEb8ZY_-rYQqown_9msjKD15RUrCszbVJzjc8/edit#gid=952708933')
	accounts = {
		'CC-COH': '10001-001-000-000 - Cash on Hand - FX-GPCAVITE - TGP', 
		'CC-CIV': '10203-001-000-000 - Cash in Vault - FX Reserve PHP-GPCAVITE - TGP',
        'CC-Short': '79303-001-000-000 - Cash Shortage/Overage - FX-GPCAVITE - TGP',
        'GTC-COH': '10001-002-000-000 - Cash on Hand - FX-GPGTC - TGP',
		'GTC-CIV': '10203-002-000-000 - Cash in Vault - FX Reserve PHP-GPGTC - TGP',
        'GTC-Short': '79303-002-000-000 - Cash Shortage/Overage - FX-GPGTC - TGP',
        'MOL-COH': '10001-003-000-000 - Cash on Hand - FX-GPMOL - TGP',
		'MOL-CIV': '10203-003-000-000 - Cash in Vault - FX Reserve PHP-GPMOL - TGP',
        'MOL-Short': '79303-003-000-000 - Cash Shortage/Overage - FX-GPMOL - TGP',
		'POB-COH': '10001-007-000-000 - Cash on Hand - FX-MPPOB - TGP',
		'POB-CIV': '10203-007-000-000 - Cash in Vault - FX Reserve PHP-MPPOB - TGP',
        'POB-Short': '79303-007-000-000 - Cash Shortage/Overage - FX-MPPOB - TGP',
		'TNZ-COH': '10001-008-000-000 - Cash on Hand - FX-MPTANZA - TGP',
		'TNZ-CIV': '10203-008-000-000 - Cash in Vault - FX Reserve PHP-MPTANZA - TGP',
        'TNZ-Short': '79303-008-000-000 - Cash Shortage/Overage - FX-MPTANZA - TGP',
        'MAIN': '10401-006-000-000 - Currencies Bought - FX-MPMAIN - TGP'
	}
	yesterday = add_to_date(datetime.now(), days=-1, as_string=True)
	for entry_no in range (2, len(data)):
		if data[entry_no][3] == today():
			if data[entry_no][4] == "CC":
				create_JE(data[entry_no][3], accounts.get("CC-COH"), accounts.get("CC-CIV"), accounts.get("CC-Short"), accounts.get("MAIN"), data[entry_no][6], data[entry_no][7], data[entry_no][9])
			elif data[entry_no][4] == "POB":
				create_JE(data[entry_no][3], accounts.get("POB-COH"), accounts.get("POB-CIV"), accounts.get("POB-Short"), accounts.get("MAIN"), data[entry_no][6], data[entry_no][7], data[entry_no][9])
			elif data[entry_no][4] == "GTC":
				create_JE(data[entry_no][3], accounts.get("GTC-COH"), accounts.get("GTC-CIV"), accounts.get("GTC-Short"), accounts.get("MAIN"), data[entry_no][6], data[entry_no][7], data[entry_no][9])
			elif data[entry_no][4] == "TNZ":
				create_JE(data[entry_no][3], accounts.get("TNZ-COH"), accounts.get("TNZ-CIV"), accounts.get("TNZ-Short"), accounts.get("MAIN"), data[entry_no][6], data[entry_no][7], data[entry_no][9])
			elif data[entry_no][4] == "MOL":
				create_JE(data[entry_no][3], accounts.get("MOL-COH"), accounts.get("MOL-CIV"), accounts.get("MOL-Short"), accounts.get("MAIN"), data[entry_no][6], data[entry_no][7], data[entry_no][9])
	
	return True
				
	

def create_JE(posting_date, coh_account, civ_account, shortage_account, currencies_bought_account, additional_funds, peso_out, shortage_overage):
    if flt(additional_funds) > 0:
        doc1 = frappe.new_doc('Journal Entry')
        doc1.voucher_type = 'Journal Entry'
        # doc1.company = 'Garcia\'s Pawnshop'
        doc1.company = 'TEST Garcia\'s Pawnshop'
        doc1.posting_date = posting_date

        row_values1 = doc1.append('accounts', {})
        row_values1.account = coh_account
        row_values1.credit_in_account_currency = flt(0)
        row_values1.debit_in_account_currency = flt(additional_funds)

        row_values2 = doc1.append('accounts', {})
        row_values2.account = civ_account
        row_values2.credit_in_account_currency = flt(additional_funds)
        row_values2.debit_in_account_currency = flt(0)

        doc1.save(ignore_permissions=True)
        doc1.submit()

    if flt(shortage_overage) > 0:
        doc2 = frappe.new_doc('Journal Entry')
        doc2.voucher_type = 'Journal Entry'
        # doc2.company = 'Garcia\'s Pawnshop'
        doc2.company = 'TEST Garcia\'s Pawnshop'
        doc2.posting_date = posting_date

        row_values1 = doc2.append('accounts', {})
        row_values1.account = shortage_account
        row_values1.credit_in_account_currency = flt(shortage_overage)
        row_values1.debit_in_account_currency = flt(0)

        row_values2 = doc2.append('accounts', {})
        row_values2.account = coh_account
        row_values2.credit_in_account_currency = flt(0)
        row_values2.debit_in_account_currency = flt(shortage_overage)

        doc2.save(ignore_permissions=True)
        doc2.submit()

    elif flt(shortage_overage) < 0:
        doc3 = frappe.new_doc('Journal Entry')
        doc3.voucher_type = 'Journal Entry'
        # doc3.company = 'Garcia\'s Pawnshop'
        doc3.company = 'TEST Garcia\'s Pawnshop'
        doc3.posting_date = posting_date

        row_values1 = doc3.append('accounts', {})
        row_values1.account = shortage_account
        row_values1.credit_in_account_currency = flt(0)
        row_values1.debit_in_account_currency = flt(shortage_overage)

        row_values2 = doc3.append('accounts', {})
        row_values2.account = coh_account
        row_values2.credit_in_account_currency = flt(shortage_overage)
        row_values2.debit_in_account_currency = flt(0)

        doc3.save(ignore_permissions=True)
        doc3.submit()

    if flt(peso_out) > 0:
        doc4 = frappe.new_doc('Journal Entry')
        doc4.voucher_type = 'Journal Entry'
        # doc4.company = 'Garcia\'s Pawnshop'
        doc4.company = 'TEST Garcia\'s Pawnshop'
        doc4.posting_date = posting_date
        
        row_values1 = doc4.append('accounts', {})
        row_values1.account = coh_account
        row_values1.credit_in_account_currency = flt(peso_out)
        row_values1.debit_in_account_currency = flt(0)

        row_values2 = doc4.append('accounts', {})
        row_values2.account = currencies_bought_account
        row_values2.credit_in_account_currency = flt(0)
        row_values2.debit_in_account_currency = flt(peso_out)
        
        doc4.save(ignore_permissions=True)
        doc4.submit()
	#doc.submit()
