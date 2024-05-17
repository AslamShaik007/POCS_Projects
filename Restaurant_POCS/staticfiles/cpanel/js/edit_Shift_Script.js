function editShiftForm(evt) {
    evt.preventDefault();
    console.log("edit shift script calling");

    const edit_ShiftName = document.querySelector("#editShiftNameInput");
    const edit_shiftStartTime = document.querySelector("#editShiftStartTime");
    const edit_ShiftEndTime = document.querySelector("#editShiftEndTime");
    const edit_workMode = document.querySelector("#editWorkingFrom");
    const edit_TimeZone = document.querySelector("#editTimeZone");

    if(edit_ShiftName.value !== "" && edit_shiftStartTime.value !=="" && edit_ShiftEndTime.value !== "" && edit_workMode.value !== "" && edit_TimeZone.value !== "") {
        $("#editShiftModal").modal("hide");
        editShowSuccess(edit_ShiftName, "", "");
        editShowSuccess(edit_shiftStartTime, "", "");
        editShowSuccess(edit_ShiftEndTime, "", "");
        editShowSuccess(edit_workMode, "", "");
        editShowSuccess(edit_TimeZone, "", "");
        document.querySelector("#editShiftForm").submit();
    } else {
        editShowError(edit_ShiftName, "block", "Shift Name should not be Empty")
        editShowError(edit_shiftStartTime, "block", "Start Time should not be empty")
        editShowError(edit_ShiftEndTime, "block", "End Time should not be empty")
        editShowError(edit_workMode, "block", "Select Working From")
        editShowError(edit_TimeZone, "block", "Select Time Zone")
    }
    console.log("add shift form submitted");
}

//Show input error messages
const editShowError = (input, dState, message) => {
    const formFiled = input.parentElement;
    // console.log(formFiled);
    const small = formFiled.querySelector("small");
    small.style.display = dState;
    small.className = "cust_err text-danger";
    small.innerHTML = message;
};
  
//Show input success
const editShowSuccess = (input, dState, message) => {
    const formFiled = input.parentElement;
    // console.log(formFiled);
    const small = formFiled.querySelector("small");
    small.style.display = dState;
    small.className = "cust_err";
    small.innerHTML = message;
};

document.querySelector("#editBreakStartTime").addEventListener("change", function (evt) {
    const bst = document.querySelector("#editBreakStartTime").value;
    console.log("break start time is : " + bst);
})

// Break Start Time
document.querySelector("#editBreakStartTime").addEventListener("blur", function (evt) {
    if(document.querySelector("#editBreakStartTime").value == "") {
        editShowError(this, "block" ,"Select Break Start Time");
    } else {
        editShowSuccess(this, "none", "")
    }
})

// Break End Time
document.querySelector("#editBreakEndTime").addEventListener("blur", function (evt) {
    if(document.querySelector("#editBreakEndTime").value == "") {
        editShowError(this, "block" ,"Select Break End Time");
    } else {
        editShowSuccess(this, "none", "")
    }
})

// Shift Name
document.querySelector("#editShiftNameInput").addEventListener("keydown", function (evt) {
    var charCode = evt.keyCode || evt.which;
    if(charCode == 8 || charCode == 46 || charCode == 35 || charCode == 36 || charCode == 37 || charCode == 39) {
        return true;
    }

    if((evt.which >= 48 && evt.which <= 57) || (evt.which >= 96 && evt.which <= 105)) {
        evt.preventDefault();
        editShowError(this, "block" ,"Numbers are not allowed");
        return false;
    }  else if(!(/[a-zA-Z\t ]/i.test(String.fromCharCode(evt.keyCode)))) {
        evt.preventDefault();
        editShowError(this, "block" ,"Numbers are not allowed");
        return false;
    }

    if(evt.which === 32 && this.value.length === 0) {
        evt.preventDefault();
        editShowError(this, "block" ,"Space not allowed");
        return false;
    } else {
        this.value = this.value.replace(/\s+/g, ' ');
        document.querySelector("#editShift_shiftName").style.display = "none";
        document.querySelector("#editShift_shiftName").innerHTML = "";
    }
})

document.querySelector("#editShiftNameInput").addEventListener("blur", function (evt) {
    if(this.value.length !== 0) {
        this.value = this.value.trim();
    } else {
        editShowError(this, "block" ,"Shift Name should not be Empty");
    }
})

var eShtStartTime = eShtEndTime = eAllocatedShiftTime = 0;
// Shift Start Time
document.querySelector("#editShiftStartTime").addEventListener("keydown", function (evt) {
    const startTime = document.querySelector("#editShiftStartTime").value;
    var sHours = startTime.substring(0,2);
    var sMinutes = startTime.substring(3,5);
    // console.log("start Hours :" + sHours);
    // console.log("start Minutes :" + sMinutes);
    if(sHours == "" && sMinutes == "") {
        eShtStartTime = 0;
    } else if(sHours == "" && sMinutes !== "") {
        eShtStartTime = sHours + 0;
    } else if(sHours !== "" && sMinutes == "") {
        eShtStartTime = 0 + sMinutes;
    } else {
        eShtStartTime = startTime;
    }
    // console.log("shift Start time :" + startTime + " = " + eShtStartTime);
})

document.querySelector("#editShiftStartTime").addEventListener("change", function (evt) {
    const startTime = document.querySelector("#editShiftStartTime").value;
    var sHours = startTime.substring(0,2);
    var sMinutes = startTime.substring(3,5);
    // console.log("start Hours :" + sHours);
    // console.log("start Minutes :" + sMinutes);
    if(sHours == "" && sMinutes == "") {
        eShtStartTime = 0;
    } else if(sHours == "" && sMinutes !== "") {
        eShtStartTime = sHours + 0;
    } else if(sHours !== "" && sMinutes == "") {
        eShtStartTime = 0 + sMinutes;
    } else {
        eShtStartTime = startTime;
    }
    // console.log("shift Start time :" + startTime + " = " + eShtStartTime);
})

document.querySelector("#editShiftStartTime").addEventListener("blur", function (evt) {
    if(document.querySelector("#editShiftStartTime").value == "") {
        editShowError(this, "block" ,"Start Time should not be empty");
    } else {
        editShowSuccess(this, "none", "")
    }
})

// Shift End Time
document.querySelector("#editShiftEndTime").addEventListener("keydown", function (evt) {
    const endTime = document.querySelector("#editShiftEndTime").value;
    var eHours = endTime.substring(0,2);
    var eMinutes = endTime.substring(3,5);
    // console.log("end Hours :" + eHours);
    // console.log("end Minutes :" + eMinutes);
    if(eHours == "" && eMinutes == "") {
        eShtEndTime = 0;
    } else if(eHours == "" && eMinutes !== "") {
        eShtEndTime = eHours + 0;
    } else if(eHours !== "" && eMinutes == "") {
        eShtEndTime = 0 + eMinutes;
    } else {
        eShtEndTime = endTime;
    }
    // console.log("shift End time :" + endTime + " = " + eShtEndTime);
})

document.querySelector("#editShiftEndTime").addEventListener("change", function (evt) {
    const endTime = document.querySelector("#editShiftEndTime").value;
    var eHours = endTime.substring(0,2);
    var eMinutes = endTime.substring(3,5);
    // console.log("end Hours :" + eHours);
    // console.log("end Minutes :" + eMinutes);
    if(eHours == "" && eMinutes == "") {
        eShtEndTime = 0;
    } else if(eHours == "" && eMinutes !== "") {
        eShtEndTime = eHours + 0;
    } else if(eHours !== "" && eMinutes == "") {
        eShtEndTime = 0 + eMinutes;
    } else {
        eShtEndTime = endTime;
    }
    // console.log("shift End time :" + endTime + " = " + eShtEndTime);
})

document.querySelector("#editShiftEndTime").addEventListener("blur", function (evt) {
    if(document.querySelector("#editShiftEndTime").value == "") {
        editShowError(this, "block" ,"End Time should not be empty");
    } else {
        editShowSuccess(this, "none", "")
    }
    
    // console.log("start time :" + typeof eShtStartTime )
    // console.log("end time :" + typeof eShtEndTime )
    var sHours = sMinutes = eHours = eMinutes = 0;
    
    // sHours = parseInt(eShtStartTime.substring(0,2))
    // sMinutes = parseInt(eShtStartTime.substring(3,5))
    // eHours = parseInt(eShtEndTime.substring(0,2))
    // eMinutes = parseInt(eShtEndTime.substring(3,5))
    // console.log(typeof sHours + sHours)
    // console.log(typeof sMinutes + sMinutes)
    // console.log(typeof eHours + eHours)
    // console.log(typeof eMinutes + eMinutes)
    var dHours = eHours - sHours;
    var dMinutes = eMinutes - sMinutes;

    eAllocatedShiftTime = dHours +" hours "+ dMinutes + " minutes allocated";
    // console.log("allocated Shift time is :" + eAllocatedShiftTime)
    // document.querySelector("#editAllocatedTimeMsg").innerHTML = eAllocatedShiftTime;
})

// Flexible Break
document.querySelector("#editflexRadioForFlexibleBreak").addEventListener("click", function(evt) {
    if(document.querySelector("#editflexRadioForFlexibleBreak").checked == true) {
        editShowSuccess(document.querySelector("#editShift_breakType"), "none", "");
        document.querySelector("#editTakeBreakTypeFlexible").style.display = 'block';
        document.querySelector("#editTakeBreakTypeFixed").style.display = 'none';
    } 
    var breakType = document.querySelector("#editflexRadioForFlexibleBreak").value;
    // console.log("Break Type :" + breakType)
})

// Fixed Break
document.querySelector("#editflexRadioForFixedBreak").addEventListener("click", function(evt) {
    if(document.querySelector("#editflexRadioForFixedBreak").checked == true) {
        editShowSuccess(document.querySelector("#editShift_breakType"), "none", "");
        document.querySelector("#editTakeBreakTypeFlexible").style.display = 'none';
        document.querySelector("#editTakeBreakTypeFixed").style.display = 'block';
    } 
    var breakType = document.querySelector("#editflexRadioForFixedBreak").value;
    // console.log("Break Type :" + breakType)
})

// Break Type Error
document.querySelector("#editflexRadioForFlexibleBreak").addEventListener("blur", function (evt) {
    if(document.querySelector("#editflexRadioForFlexibleBreak").checked == false && document.querySelector("#editflexRadioForFlexibleBreak").checked == false) {
        editShowError(document.querySelector("#editShift_breakType"), 'block', "Select Break Mode")
    } else if(document.querySelector("#editflexRadioForFlexibleBreak").checked == false && document.querySelector("#editflexRadioForFlexibleBreak").checked == true) {
        editShowSuccess(document.querySelector("#editShift_breakType"), 'none', "")
    } else if(document.querySelector("#editflexRadioForFlexibleBreak").checked == true && document.querySelector("#editflexRadioForFlexibleBreak").checked == false) {
        editShowSuccess(document.querySelector("#editShift_breakType"), 'none', "")
    } else {
        editShowSuccess(document.querySelector("#editShift_breakType"), 'none', "")
    }
})

document.querySelector("#editflexRadioForFixedBreak").addEventListener("blur", function (evt) {
    if(document.querySelector("#editflexRadioForFlexibleBreak").checked == false && document.querySelector("#editflexRadioForFlexibleBreak").checked == false) {
        editShowError(document.querySelector("#editShift_breakType"), 'block', "Select Break Mode")
    } else if(document.querySelector("#editflexRadioForFixedBreak").checked == false && document.querySelector("#editflexRadioForFlexibleBreak").checked == true) {
        editShowSuccess(document.querySelector("#editShift_breakType"), 'none', "")
    } else if(document.querySelector("#editflexRadioForFixedBreak").checked == true && document.querySelector("#editflexRadioForFlexibleBreak").checked == false) {
        editShowSuccess(document.querySelector("#editShift_breakType"), 'none', "")
    } else {
        editShowSuccess(document.querySelector("#editShift_breakType"), 'none', "")
    }
})


document.querySelector("#editFlexibleBreak").addEventListener("blur", function (evt) {
    if(document.querySelector("#editFlexibleBreak").value == "") {
        editShowError(this, "block", "Select Break Time")
    } else {
        editShowSuccess(this, "none", "")
    }
})

// Break Start Time

// Break End Time

// Working From
document.querySelector("#editWorkingFrom").addEventListener("change", function (evt) {
    const workMode = document.querySelector("#editWorkingFrom").value;
    if(workMode === "") {
        console.log("empty")
    }
    // console.log("working from :" + workMode);
})

document.querySelector("#editWorkingFrom").addEventListener("blur", function (evt) {
    if(document.querySelector("#editWorkingFrom").value == "") {
        editShowError(this, "block" ,"Select Working Mode");
    } else {
        editShowSuccess(this, "none", "")
    }
})

// Time Zone
document.querySelector("#editTimeZone").addEventListener("change", function (evt) {
    var timeZone = document.querySelector("#editTimeZone").value;
    // console.log("time zone is :" + timeZone);
})

document.querySelector("#editTimeZone").addEventListener("blur", function (evt) {
    if(document.querySelector("#editTimeZone").value == "") {
        editShowError(this, "block" ,"Select Time Zone");
    } else {
        editShowSuccess(this, "none", "")
    }
})