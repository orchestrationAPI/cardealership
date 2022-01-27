"use strict";
//changing classname 'allert-error' to 'allert-warning' for sake of bootstrap
let erEl = document.getElementsByClassName("alert-error");
[...erEl].forEach((el) => {
  el.classList.add("alert-danger");
});
//init bootstrapTable
  $(function() {
    $('#table').bootstrapTable()
  })
