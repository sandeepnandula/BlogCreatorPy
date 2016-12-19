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
// $(".view").click(function() {
////     var title1 = $(this).attr('id');
////     var user = $(this).attr('value');
//     var id = $(this).attr('value');
//     console.log("view id is" + id)
//     $.post("blogcontent<id>", {
//         "id": id
//     }, function(result) {
//         console.log("result is " + result)
//     });
//
// });


 $(".delete").click(function() {

     var id = $(this).attr('value');
     console.log("on delete mode" + id)
     $(".delete_yes").one("click", function() {
         $.post("deleteblog", {
             "id": id
         }, function(result) {
             console.log("result is " + result)

         });
     });
 });

//  $(".edit").click(function() {
//     var id = $(this).attr('value');
//     console.log("edit id is"+ id)
////     var s = []
//     $.get("blogedit", {
//         "id": id
//         }, function(result) {
//         console.log("editing is on process" + result)
//
////
////         console.log(s)
////         $('[name=etitle]').val(s[0]);
////         $('[name=eheading]').val(s[1]);
////         $('[name=ediscription]').val(s[2]);
////
//     });
//// $.each(result, function(i, field) { //     for each function in the javascript to print the jason by each value and key
////             s.push(field); //        below code is used to add elements to the arry lists
////             console.log(field)
////
////         });
//
//     $("#updateblog").click(function() {
//         var etitle = $('[name=etitle]').val();
//         var eheading = $('[name=eheading]').val();
//         var ediscription = $('[name=ediscription]').val();
//         console.log("updating...")
//         $.post("blogedit", {
//             "title": title,
//             "etitle": etitle,
//             "eheading": eheading,
//             "ediscription": ediscription
//         }, function(result) {
//             console.log("updated")
//             history.go(0);
//         });
//
//     });
// });


});
