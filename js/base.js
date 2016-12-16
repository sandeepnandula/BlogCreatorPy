$(document).ready( function(){
 $.get("/", function(result) {
    console.log("Blog content working")

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
            if(result == ""){
            history.go(0);
            }
        });
    });

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


 $(".view").click(function() {
     var title1 = $(this).attr('id');
     var user = $(this).attr('value');
     console.log(title1 + user)
     $.post("blogcontent",{
            "title":title1,
            "user":user
     },function(result){
     console.log("result is " + result)
     $("#mainpage").hide()
     $("#blogcontent").html(result).show()
     });

 });


});