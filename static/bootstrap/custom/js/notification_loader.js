
/*
setInterval(function() {
  getNotifications();
},3000); //on every 3 seconds
*/

function getNotifications(){
  $.ajax({
      url:"../Notification/LiveNotify",
      type:"POST",
      success:function (data) {
        $(".content").html(data);
          //alert("Success : \n"+data);
      },
      error:function(data){
        $(".content").html(data.responseText);
       }
   });
}