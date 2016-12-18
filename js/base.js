$(document).ready( function(){
 $.get("/", function(result) {
    console.log("Blog content working")
    });

$("#loginmodal").click(function() {
    $("#loginform").modal();

});

$("#login").click(function() {
    var userName = $('[name=userName]').val()
    var password = $('[name=password]').val()
    $.post("login", {
        "userName": userName,
        "password": password
    }, function(result) {
        console.log(result)
        console.log("getting response from the login handler")
        $("#error").text(result)
        if (result == "") {
            history.go(0);

        }
    });
});

 $("#createblog").click(function() {
     var title = $('[name=title]').val();
     var heading = $('[name=heading]').val();
     var discription = $('[name=discription]').val();
     console.log(title)
     $.get("blogcreation", {
         "title": title,
         "heading": heading,
         "discription": discription
     }, function(result) {
         console.log(result)
         $(".formerror").text(result)
            if(result == ""){
             history.go(0);
            }
        });
    });







 $(".view").click(function() {
     var title1 = $(this).attr('id');
     var user = $(this).attr('value');
     var id = $(this).attr('name');
     console.log(title1 + id)
     $.post("blogcontent",{
            "title":title1,
            "user":user,
            "id":id
     },function(result){
     console.log("result is " + result)
     $("#mainpage").hide()
     $("#blogcontent").html(result).show()
     });

 });


     $(".delete").click(function(){
      var id = $(this).attr('name');
      var title = $(this).attr('value');
      console.log("on delete mode")
      $(".delete_yes").one("click",function(){
             $.post("deleteblog",{
                    "id":id,
                    "title":title
              },function(result){
              console.log("result is " + result)
              history.go(0);
                  });
      });
});

  $(".edit").click(function() {
      var id = $(this).attr('name');
     console.log(id)
     $.getJSON("blogedit", function(result){
        console.log(result)
        $('[name=title]').val("hi")
        $('[name=heading]').val("hi")
        $('[name=discription]').val("hi")

//     for each function in the javascript to print the jason by each value and key
//        $.each(result, function(i, field){
//            console.log(i + ":" + field )
//        });

    });
//     $.post("blogedit",{
//
//     },function(result){
//     var test= result
//     console.log("result is " + test[0])
//
//     });

 });
//${"#deleteblog"}.click(function(){
//console.log("delete button is clicking")
//
//});

});
