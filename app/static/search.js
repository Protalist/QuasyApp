$(document).ready(function() {
  $("form#songs").submit(function(ev){
    alert("CIAO");
    ev.preventDefault();
    var songname = new FormData(this);
    var risp;
    $.ajax({
      processData: false,
      contentType: false,
      dataType: "JSON",
      url:"/_retrievesong",
      type: 'post',
      data: songname,
      success: function() {

      } ,
      error :  function() {
          alert('FAIL');
     },
     complete : function(jXHR,status) {
       var data = $.parseJSON(jXHR.responseText);
       console.log("INSIDE");
         if (data.result == "null"){

           return;
         }
         else {
         console.log("HI");
          var lis_possibilities = data.result;
          var res = document.getElementById("Res");
          var n = document.createElement("p");

          for each (var i in lis_possibilities){
               n.appendChild(document.createTextNode(i));
               res.appendChild(n);
               n = document.createElement("p");
          }
           return "Fatto";
         }
       }
     });
   });
  });
