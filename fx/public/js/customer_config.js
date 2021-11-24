frappe.ui.form.on("Customer", {
    refresh:function(frm){
        customer_type_toggle();
    },

    customer_type:function(frm) {
        customer_type_toggle();
        frm.refresh_fields();
    }
})

function customer_type_toggle(frm) {
    if (cur_frm.doc.customer_type == "Individual") {
        cur_frm.set_df_property('customer_name', 'label', 'Full Name');
    } else {
        cur_frm.set_df_property('customer_name', 'label', 'Corporate Account Name');
    }
    cur_frm.refresh_fields();
}