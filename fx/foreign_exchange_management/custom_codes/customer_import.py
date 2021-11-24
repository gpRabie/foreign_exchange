import frappe
@frappe.whitelist()
def get_customer(tracking_number, first_name, last_name, risk_level, gender, place_of_birth, date_of_birth, id_type, id_expiry, id_docs_pic_name, phone_number, nationality, house_no_primary, street_or_brgy_primary, city_primary, state_primary, country_primary, house_no_present=None, street_or_brgy_present=None, city_present=None, state_present=None, country_present=None, corporate_account_name = None, nature_of_bussiness = None):
    if corporate_account_name == "" and nature_of_bussiness == "": # if transaction is personal
        create_customer_individual(tracking_number, first_name, last_name, risk_level, gender)
        customer = frappe.get_last_doc('Customer')
        create_contact_individual(first_name, last_name, gender, place_of_birth, date_of_birth, customer.name, id_type, id_expiry, id_docs_pic_name, phone_number, nationality)
        create_address_primary(house_no_primary, street_or_brgy_primary, city_primary, state_primary, country_primary, customer.name)
        if street_or_brgy_present != "":
            create_address_present(street_or_brgy_present, city_present, state_present, country_present, customer.name, house_no_present)
    else: # if transaction is corporate
        create_customer_company(tracking_number, corporate_account_name, risk_level, nature_of_bussiness)
        customer = frappe.get_last_doc('Customer')
        create_contact_company(first_name, last_name, gender, place_of_birth, date_of_birth, customer.name, id_type, id_expiry, id_docs_pic_name, phone_number, corporate_account_name, nationality)
        create_address_primary(house_no_primary, street_or_brgy_primary, city_primary, state_primary, country_primary, customer.name)

def create_customer_individual(tracking_number, first_name, last_name, risk_level, gender):
    customer = frappe.new_doc('Customer')
    customer.customer_tracking_no = tracking_number
    customer.customer_name = first_name + " " + last_name
    customer.customer_type = 'Individual'

    if gender == 'M':
        customer_gender = frappe.get_doc('Gender', 'Male')
        customer.gender = customer_gender.gender
    elif gender == 'F':
        customer_gender = frappe.get_doc('Gender', 'Female')
        customer.gender = customer_gender.gender

    customer.risk_level = risk_level
    customer.insert()
    customer.save()

def create_customer_company(tracking_number, corporate_account_name, risk_level, nature_of_bussiness):
    customer = frappe.new_doc('Customer')
    customer.customer_tracking_no = tracking_number
    customer.customer_name = corporate_account_name
    customer.customer_type = 'Company'
    if frappe.db.exists('Industry Type', nature_of_bussiness) == nature_of_bussiness.title():
        customer.industry = nature_of_bussiness.title()
    elif frappe.db.exists('Industry Type', nature_of_bussiness) is None:
        customer_bussiness = frappe.new_doc('Industry Type')
        customer_bussiness.industry = nature_of_bussiness
        customer_bussiness.insert()
        customer_bussiness.save()
        bussiness = frappe.get_last_doc('Industry Type')
        customer.industry = bussiness.industry

    customer.risk_level = risk_level
    customer.insert()
    customer.save()



def create_contact_individual(first_name, last_name, gender, place_of_birth, date_of_birth, link_name, id_type, id_expiry, id_docs_pic_name, phone_number, nationality):
    contact = frappe.new_doc('Contact')
    contact.first_name = first_name
    contact.last_name = last_name

    if frappe.db.exists('Nationality', nationality) == nationality:
        contact.nationality = nationality
    elif frappe.db.exists('Nationality', nationality) is None:
        new_nationality = frappe.new_doc('Nationality')
        new_nationality.nationality = nationality
        new_nationality.insert()
        new_nationality.save()
        customer = frappe.get_last_doc('Nationality')
        contact.nationality = customer.nationality

    if gender == 'M':
        contact.gender = 'Male'
    elif gender == 'F':
        contact.gender = 'Female'
    contact.place_of_birth = place_of_birth
    contact.date_of_birth = date_of_birth

    ids = contact.append('id_type', {})
    if frappe.db.exists('ID Type', id_type) == id_type: 
        ids.id_type = id_type
        ids.id_docs_pic_name = id_docs_pic_name
        if id_expiry is not "0000-00-00":
            ids.expiry_date = id_expiry
    elif frappe.db.exists('ID Type', id_type) is None:
        new_id = frappe.new_doc('ID Type')      #Creates new ID Type if ID not in document
        new_id.type = id_type
        new_id.insert()
        new_id.save()
        get_new_id = frappe.get_last_doc('ID Type')
        ids.id_type = get_new_id.name
        ids.id_docs_pic_name = id_docs_pic_name
        if id_expiry is not "0000-00-00":
            ids.expiry_date = id_expiry

    contact_numbers = contact.append('phone_nos', {})
    contact_numbers.phone = phone_number

    link = contact.append('links', {})
    link.link_doctype = 'Customer'
    link.link_name = link_name

    contact.insert()
    contact.save()

def create_contact_company(first_name, last_name, gender, place_of_birth, date_of_birth, link_name, id_type, id_expiry, id_docs_pic_name, phone_number, company_name, nationality):
    contact = frappe.new_doc('Contact')
    contact.first_name = first_name
    contact.last_name = last_name
    if frappe.db.exists('Nationality', nationality) == nationality:
        contact.nationality = nationality
    elif frappe.db.exists('Nationality', nationality) is None:
        new_nationality = frappe.new_doc('Nationality')
        new_nationality.nationality = nationality
        new_nationality.insert()
        new_nationality.save()
        customer = frappe.get_last_doc('Nationality')
        contact.nationality = customer.nationality

    if gender == 'M':
        contact.gender = 'Male'
    elif gender == 'F':
        contact.gender = 'Female'
    contact.place_of_birth = place_of_birth
    contact.date_of_birth = date_of_birth
    contact.company_name = company_name

    ids = contact.append('id_type', {})
    if frappe.db.exists('ID Type', id_type) == id_type: 
        ids.id_type = id_type
        ids.id_docs_pic_name = id_docs_pic_name
        if id_expiry is not "0000-00-00":
            ids.expiry_date = id_expiry
    elif frappe.db.exists('ID Type', id_type) is None:
        new_id = frappe.new_doc('ID Type')      #Creates new ID Type if ID not in document
        new_id.type = id_type
        new_id.insert()
        new_id.save()
        get_new_id = frappe.get_last_doc('ID Type')
        ids.id_type = get_new_id.name
        ids.id_docs_pic_name = id_docs_pic_name
        if id_expiry is not "0000-00-00":
            ids.expiry_date = id_expiry

    contact_numbers = contact.append('phone_nos', {})
    contact_numbers.phone = phone_number

    link = contact.append('links', {})
    link.link_doctype = 'Customer'
    link.link_name = link_name

    contact.insert()
    contact.save()



def create_address_primary(house_no, street_or_brgy, city, state, country, link_name):
    address = frappe.new_doc('Address')
    address.address_type = 'Permanent'
    address.house_no = house_no
    address.street_or_brgy = street_or_brgy
    address.city = city
    address.state = state
    address.country = country
    address.address_line1 = house_no + ", " + street_or_brgy
    

    link = address.append('links', {})
    link.link_doctype = 'Customer'
    link.link_name = link_name

    address.insert()
    address.save()

def create_address_present(street_or_brgy, city, state, country, link_name, house_no=None):
    address = frappe.new_doc('Address')
    address.address_type = 'Present'
    address.house_no = house_no
    address.street_or_brgy = street_or_brgy
    address.city = city
    address.state = state
    address.country = country
    if house_no is None:
        address.address_line1 = street_or_brgy
    else:
        address.address_line1 = house_no + ", " + street_or_brgy 

    link = address.append('links', {})
    link.link_doctype = 'Customer'
    link.link_name = link_name

    address.insert()
    address.save()