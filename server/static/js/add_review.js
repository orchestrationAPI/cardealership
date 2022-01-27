const check = function(form, spinner){
	if (form.checkValidity()){
        spinner.style.visibility = "visible";
		form.submit
	}else{
		return false;
	}
}

const form = document.getElementById('form');

form.addEventListener('submit',(ev)=>{
    let spinner = document.getElementById("spinner");
	console.log(ev.target)
check(ev.target,spinner )
	})


//get checkbox value for switching enabled and disabled attributes of input fields and make those required or non required


let chBox = document.getElementById("id_purchase");
//function for disabling elems in queryset
const disableElem = function (querySet) {
  querySet.forEach((field) => {
    field.setAttribute("disabled", "disabled");
    field.removeAttribute("required");
  });
};
//function for enabling elems in queryset
const enableElem = function (querySet) {
  querySet.forEach((field) => {
    field.removeAttribute("disabled");
    field.setAttribute("required", "required");
  });
};
//get disabled elems
q = document.querySelectorAll(":disabled");
//add eventListener to the checkbox and pass the disabled objects to eventListener
chBox.addEventListener("change", function () {
  if (this.checked) {
    console.log("checked");
    enableElem(q);
  } else {
    disableElem(q);
  }
});

//datetimepicker to purchase date
$("#id_purchase_date").datetimepicker({
  timepicker: false,
  format: "Y-m-d",
});
//add spinner to submit button
