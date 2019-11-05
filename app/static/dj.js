$(document).ready(function() {
  $('input').on('click',function(ev){
    alert("ciao");
    ev.preventDefault();
    var risp;

    $.ajax({
      processData: false,
      contentType: false,
      dataType: "JSON",
      url:"/_popsong",
      type: 'post',
      data: '',
      success: function() {
        alert('succes');
      } ,
      error :  function() {
          alert('FAIL');
     },
     complete : function(jXHR,status) {
        var data = $.parseJSON(jXHR.responseText);
        alert(data.result);
        if (data.result == "null"){
            $('#current').text("No Song to play");
            $('ol').children().remove();
           return;
         }
        var strs= data.result.split(" ")[1].split(",")
        $('#current').text(strs[0]+","+strs[1]);
        $('#'+strs[0]).remove();
     }
      });
  });
  });



  setInterval(function() {
        var risp;
    $.ajax({
      processData: false,
      contentType: false,
      dataType: "JSON",
      url:"/_update",
      type: 'get',
      data: '',
      success: function() {

      } ,
      error :  function() {

     },
     complete : function(jXHR,status) {
        var data = $.parseJSON(jXHR.responseText);
        if (data.result == "null"){
           return;
         }
        var strs= data.result;
        var c=$("ol").children()
        c.remove();
        console.log("data.result= "+strs)
        for (var i=0; i<strs.length;i++){
             var song= strs[i].split(" ")[1].split(",");
             $("ol").append("<li id=\'"+song[0]+"\'>"+song[0]+","+song[1]+"</li>");
        }
     }
      });
  }, 5000);

  