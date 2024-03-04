// Copyright (c) 2020, Havenir and contributors
// For license information, please see license.txt

frappe.ui.form.on("Hotel Check In", {
  setup: function(frm) {
    // setting query for rooms to be visible in list
    frm.set_query('room_no','rooms', function (doc){
      return{
        filters: [
          ['room_status', 'in', ['Available', 'Expected']]
      ]
      }
    });
  },
    
   
    
  
  guest_id: function(frm){
    var image_html = '<img src="' + frm.doc.guest_photo_attachment + '">';
    $(frm.fields_dict['guest_photo'].wrapper).html(image_html);
    frm.refresh_field('guest_photo');
  },
  
  refresh: function(frm){  
   

     //create a button to prompt tp extend the stay
     if (!frm.is_new()){

     frm.add_custom_button(__('Extend Stay'), function(){
      
      
      frappe.prompt([
        {'fieldname': 'extend_date', 'fieldtype': 'Datetime', 'label': 'Extend Date', 'reqd': 1}
      ],
      function(values){
        frm.call({
          method: 'extend_stay',
          args: {
            'doc': frm.doc.name,
            'check_out': values.extend_date
          },
          callback: function(r){
            console.log(r);
            if (!r.exc){
              frm.reload_doc();
            }
          }
        });
      },
      __('Extend Stay'));
    
  }, __('Make'));
}


  
  
    

  },

  total_amount: function(frm){
    var temp_total_amount = 0;
    for (var i in frm.doc.rooms){
      if (frm.doc.rooms[i].price){
        temp_total_amount += frm.doc.rooms[i].price;
      }
    }
    frm.doc.total_amount = temp_total_amount;
    frm.refresh_field('total_amount');
  },  // validate: function(frm){
    //   for (var i in frm.doc.rooms){
    //     if (frm.doc.rooms[i].male == 0 && frm.doc.rooms[i].female == 0){
    //       frappe.throw('Please Enter Guests Details for Room ' + frm.doc.rooms[i].room_no);
    //     }
    //   }
    // },
  
  check_out: function(frm){
    frm.set_value('duration', frappe.datetime.get_diff(frm.doc.check_out, frm.doc.check_in));
  },
  check_in: function(frm){
    frm.set_value('duration', frappe.datetime.get_diff(frm.doc.check_out, frm.doc.check_in));
  },
  check_out_time: function(frm){
    frm.set_value('duration', frappe.datetime.get_hour_diff(frm.doc.check_out_time, frm.doc.check_in_time));

  },
  check_in_time: function(frm){
    frm.set_value('duration', frappe.datetime.get_hour_diff(frm.doc.check_out_time, frm.doc.check_in_time));
  }
});

frappe.ui.form.on('Hotel Check In Room', {
  room_no: function(frm, cdt, cdn) {
    let count = 0;
    let row = frappe.get_doc(cdt, cdn)
    if (row.room_no){
      for(var i in frm.doc.rooms){
        if (frm.doc.rooms[i].room_no == row.room_no){
          count += 1;
        }
      }
      if (count>1){
        let alert = 'Room ' + row.room_no + ' already selected';
        row.room_no = undefined;
        row.room_type = undefined;
        row.price = undefined;
        frm.refresh_field('rooms')
        frappe.throw(alert)
      }
      
    }
    frm.trigger('total_amount');
  },
  
  rooms_remove: function(frm) {
    frm.trigger('total_amount');
  }
})
