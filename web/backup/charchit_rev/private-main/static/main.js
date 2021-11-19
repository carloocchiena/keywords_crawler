
$(function(){
  var socket = io.connect(window.location.href);
  socket.on('message', function(msg) {
    $("#stamp1").hide()
    for (const value in msg){
      $("#result").append(`<p class = "text-primary col-md-10"> ${value} </p>`)
      for (let item of msg[value]){
        $("#result").append(`<p class = "col-md-10">  ${item[0]} ${item[1]} </p>`)
      }
    }
  });
  $("#my_btn").click(function (){
    console.log("test")
    socket.send($('#my_inp').val());
    $("#stamp1").text("please wait while we fetch data.....")
// function sleep(ms) {
//     return new Promise(resolve => setTimeout(resolve, ms));
//   }
  
//   async function stamp() {
    
//     document.getElementById("stamp1").innerHTML = "Process started...";
//     await sleep(10000);
//     document.getElementById("stamp2").innerHTML = "...we're going, please hold. 45 sec. passed.";
//     await sleep(10000);
//     document.getElementById("stamp3").innerHTML = "...script running. 1.30 min passed.";
//     await sleep(10000);
//     document.getElementById("stamp4").innerHTML = "...script running. 2.15 min passed.";

      
//   }

  })

})