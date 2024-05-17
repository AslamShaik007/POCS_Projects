console.log("add_New_Shift_Script loading")

const shiftName = document.querySelector("#addShiftNameInput");
const shiftStartTime = document.querySelector("#addShiftStartTime");
const shiftEndTime = document.querySelector("#addShiftEndTime");
const shiftBreakStartTime = document.querySelector("#addBreakStartTime");
const shiftBreakEndTime = document.querySelector("#addBreakEndTime");
const workingFrom = document.querySelector("#addWorkingFrom");
const timeZone = document.querySelector("#addTimeZone");

function newShiftForm() {

    let valid = true;
	$('[required]').each(function() {
		if ($(this).is(':invalid') || !$(this).val()) valid = false;
	})
    if (!valid) console.log("error please fill all fields!");

    // if(shiftName.value !== "" && shiftStartTime.value !== "" && shiftEndTime.value !== "" && workingFrom.value !=="" && timeZone.value !== "") {
    if(shiftName.value !== "" && shiftStartTime.value !== "" && timeZone.value !== "") {
        console.log("submitted")
        document.querySelector("#newShiftForm").submit();
    } else {
        console.log("not submitted")
    }
}

// Show Error 
const addShiftShowError = (input, dState, message) => {
    const regFormField = input.parentElement;
    const small = regFormField.querySelector("small");
    small.style.visibility = dState;
    small.className = "cust_error text-danger";
    small.innerHTML = message;
}

// Show Success
const addShiftShowSuccess = (input, dState, message) => {
    const regFormField = input.parentElement;
    const small = regFormField.querySelector("small");
    small.style.visibility = dState;
    small.className = "cust_error";
    small.innerHTML = message;
}

document.querySelector("#addShiftNameInput").addEventListener("keydown", function (evt) {
    var charCode = evt.keyCode || evt.which;
    if(charCode == 8 || charCode == 9 || charCode == 46 || charCode == 35 || charCode == 36 || charCode == 37 || charCode == 39 ) {
        return true;
    }

    if((evt.which >= 48 && evt.which <= 57) || (evt.which >= 96 && evt.which <= 105)) {
        evt.preventDefault();
        addShiftShowError(this, "visible", "Numbers not allowed")
        return false;
    } else if(!(/[a-zA-Z\t ]/i.test(String.fromCharCode(evt.keyCode)))) {
        evt.preventDefault();
        addShiftShowError(this, "visible" ,"Numbers not allowed");
        return false;
    }

    if(evt.which === 32 && this.value.length === 0) {
        evt.preventDefault();
        addShiftShowError(this, "visible" ,"Space not allowed");
        return false;
    } else {
        this.value = this.value.replace(/\s+/g, ' ');
        addShiftShowSuccess(this, "hidden", "");
    }
    CheckShiftName(this)
})

document.querySelector("#addShiftNameInput").addEventListener("blur", function (evt) {
    if(shiftName.value.length === 0) {
        addShiftShowError(this, "visible" ,"Shift name should not be empty");
    }
})

document.querySelector("#addWorkingFrom").addEventListener("change", function (evt) {
    if(workingFrom.value == "") {
        addShiftShowError(this, "visible", "Need to select Work Mode")
    } else {
        
        addShiftShowSuccess(this, "hidden", "");
    }
})

document.querySelector("#addWorkingFrom").addEventListener("blur", function (evt) {
    if(workingFrom.value === "") {
        addShiftShowError(this, "visible", "Need to select Work Mode")
    } else {
        addShiftShowSuccess(this, "hidden", "");
    }
})

document.querySelector("#addTimeZone").addEventListener("change", function (evt) {
    if(workingFrom.value == "") {
        addShiftShowError(this, "visible", "Need to select Time Zone")
    } else {
        
        addShiftShowSuccess(this, "hidden", "");
    }
})

document.querySelector("#addTimeZone").addEventListener("blur", function (evt) {
    if(workingFrom.value === "") {
        addShiftShowError(this, "visible", "Need to select Time Zone")
    } else {
        addShiftShowSuccess(this, "hidden", "");
    }
})




// Shift Name
function CheckShiftName(input) {
    if(input.value.length < 3) {
        addShiftShowError(input, "visible", "Shift Name contains at least 3 chars")
    }
}