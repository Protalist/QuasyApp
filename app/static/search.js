$(document).ready(function() {

  $("form#songs").submit(function(ev){

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
       $("#Res").html("");
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
          var b = document.createElement("input")


          for (var i=0; i<lis_possibilities.length;i++){
               n.appendChild(document.createTextNode(lis_possibilities[i]));
               var s = lis_possibilities[i].substring(5,lis_possibilities[i].length-1);
               console.log(s);
               b.setAttribute("type","button");
               b.setAttribute("id",s);

               b.setAttribute("value","aggiungi");

               n.appendChild(b);
               res.appendChild(n);
               n = document.createElement("p");
               b = document.createElement("input")
          }
          preparebutton();

         }
       }
     });
   });


  });




