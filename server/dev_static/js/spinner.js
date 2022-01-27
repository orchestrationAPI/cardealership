"use strict";
//get spinner div which is visible by default

//while document is loading the DOMContentLoaded event get the callback function which
//after the document is loaded switch the
//spinner visibility to hiddden. Else: if document is loaded switch the spinner to hidden
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    spinner.style.visibility = "hidden";
  });
} else {
  spinner.style.visibility = "hidden";
}

//add ajax query to bootstrap table rows to switch the spinner on/off
let $table = $("#table");
$(function () {
  $table.on("click-row.bs.table", function (e, row, $element) {

    let hr = $element.children("td").children("a")[0];
    let spinner = document.getElementById("spinner");
	  if(spinner){
      if (spinner.style.visibility === "hidden") {
        spinner.style.visibility = "visible";
      }
    console.log($element);
    console.log($element.children("td").children("a")[0].href);
	    window.location = hr.href
		  
	  }else{
	    window.location = hr.href

	  }});
});

//add spinner and ajax to all anchor elements
$(() => {
  $("a").click((event) => {
    event.preventDefault();
    let spinner = document.getElementById("spinner");
    if (spinner) {
      if (spinner.style.visibility === "hidden") {
        spinner.style.visibility = "visible";
      }
      console.log(event.target);
      let h = event.target.href;
      console.log(h);
	    window.location = h;
    } else {
      console.error("Spinner is absent!");
    }
  });
});

