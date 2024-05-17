console.log("edit_New_Shift_Script.js")

const shiftName = document.querySelector("#editShiftNameInput");
const shiftStartTime = document.querySelector("#editShiftStartTime");
const shiftEndTime = document.querySelector("#editShiftEndTime");
const shiftBreakStartTime = document.querySelector("#editBreakStartTime");
const shiftBreakEndTime = document.querySelector("#editBreakEndTime");
const workingFrom = document.querySelector("#editWorkingFrom");
const timeZone = document.querySelector("#editTimeZone");

function editShiftForm() {

    let valid = true;
	$('[required]').each(function() {
		if ($(this).is(':invalid') || !$(this).val()) valid = false;
	})
    if (!valid) console.log("error please fill all fields!");

    // if(shiftName.value !== "" && shiftStartTime.value !== "" && shiftEndTime.value !== "" && workingFrom.value !=="" && timeZone.value !== "") {
    if(shiftName.value !== "" && shiftStartTime.value !== "" && timeZone.value !== "") {
        console.log("submitted")
        document.querySelector("#editShiftForm").submit();
    } else {
        console.log("not submitted")
    }
}

// Show Error 
const editShiftShowError = (input, dState, message) => {
    const regFormField = input.parentElement;
    const small = regFormField.querySelector("small");
    small.style.visibility = dState;
    small.className = "cust_error text-danger";
    small.innerHTML = message;
}

// Show Success
const editShiftShowSuccess = (input, dState, message) => {
    const regFormField = input.parentElement;
    const small = regFormField.querySelector("small");
    small.style.visibility = dState;
    small.className = "cust_error";
    small.innerHTML = message;
}

document.querySelector("#editShiftNameInput").addEventListener("keydown", function (evt) {
    var charCode = evt.keyCode || evt.which;
    if(charCode == 8 || charCode == 9 || charCode == 46 || charCode == 35 || charCode == 36 || charCode == 37 || charCode == 39 ) {
        return true;
    }

    if((evt.which >= 48 && evt.which <= 57) || (evt.which >= 96 && evt.which <= 105)) {
        evt.preventDefault();
        editShiftShowError(this, "visible", "Numbers not allowed")
        return false;
    } else if(!(/[a-zA-Z\t ]/i.test(String.fromCharCode(evt.keyCode)))) {
        evt.preventDefault();
        editShiftShowError(this, "visible" ,"Numbers not allowed");
        return false;
    }

    if(evt.which === 32 && this.value.length === 0) {
        evt.preventDefault();
        editShiftShowError(this, "visible" ,"Space not allowed");
        return false;
    } else {
        this.value = this.value.replace(/\s+/g, ' ');
        editShiftShowSuccess(this, "hidden", "");
    }
    CheckShiftName(this)
})

document.querySelector("#editShiftNameInput").addEventListener("blur", function (evt) {
    if(shiftName.value.length === 0) {
        editShiftShowError(this, "visible" ,"Shift name should not be empty");
    }
})

document.querySelector("#editWorkingFrom").addEventListener("change", function (evt) {
    if(workingFrom.value == "") {
        editShiftShowError(this, "visible", "Need to select Work Mode")
    } else {
        
        editShiftShowSuccess(this, "hidden", "");
    }
})

document.querySelector("#editWorkingFrom").addEventListener("blur", function (evt) {
    if(workingFrom.value === "") {
        editShiftShowError(this, "visible", "Need to select Work Mode")
    } else {
        editShiftShowSuccess(this, "hidden", "");
    }
})


document.querySelector("#editTimeZone").addEventListener("change", function (evt) {
    if(workingFrom.value == "") {
        editShiftShowError(this, "visible", "Need to select Time Zone")
    } else {
        
        editShiftShowSuccess(this, "hidden", "");
    }
})

document.querySelector("#editTimeZone").addEventListener("blur", function (evt) {
    if(workingFrom.value === "") {
        editShiftShowError(this, "visible", "Need to select Time Zone")
    } else {
        editShiftShowSuccess(this, "hidden", "");
    }
})

// Shift Name
function CheckShiftName(input) {
    if(input.value.length < 3) {
        editShiftShowError(input, "visible", "Shift Name contains at least 3 chars")
    }
}