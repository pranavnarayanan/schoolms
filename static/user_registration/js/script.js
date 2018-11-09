// JavaScript Document

$(document).ready(function(){
	
	
//For select dropdown
    $('select').formSelect();
//For select dropdown

//For bottom line on controls
	if($(".form_box .form-control").val()==0)
		{$(this).parent().removeClass("focus_line");}
	else
		{$(this).parent().addClass("focus_line");}

	$(".form_box .form-control").focusin(function(e) {
		$(this).parent().addClass("focus_line");
    });
	$(".form_box .form-control").focusout(function(e) {
		if($(this).val()==0)
		{$(this).parent().removeClass("focus_line");}
	});
	$(".select-dropdown").focusin(function(e) {
		$(this).parent().parent().addClass("focus_line");
	});
	$(".select-dropdown").focusout(function(e) {
		if($(this).val()==0)
		{$(this).parent().parent().removeClass("focus_line");}
	});
//For bottom line on controls

//For datepicker	
    $('.datepicker').bootstrapMaterialDatePicker({
        format: 'DD/MM/YYYY',
        clearButton: false,
        weekStart: 1,
        time: false
    }).on('change', function(e)
		{
			$(this).parent().addClass("focus_line");
		});
//For datepicker

//For Number mask 
   $(".txt_mobile").mask("999 999 9999");
//For Number mask 

//For Pincode mask 
   $(".txt_pin").mask("999 999");
//For Pincode mask 

//For landline check(page2)
	$(".registration.page2 .check_landline").change(function(e) {
		
        if($(this).prop("checked") == true)
		{
            $(".registration.page2 .form-group.landline_control").removeClass("disable");
        }
		else
		{
			$(".registration.page2 .form-group.landline_control").addClass("disable");
		}
    });
//For landline check(page2)

//For Mobile View Button Alignment
if($(window).width() <= 350)
{
	$(".registration .btn_back, .registration .btn_next, .registration .btn_finish").removeClass("float-left float-right");
}
//For Mobile View Button Alignment

});
