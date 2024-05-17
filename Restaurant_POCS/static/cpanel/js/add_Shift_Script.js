console.log("add Shift script is loading")

function addShiftForm(evt) {
    evt.preventDefault();
    const add_ShiftName = document.querySelector("#addShiftNameInput");
    const add_shiftStartTime = document.querySelector("#addShiftStartTime");
    const addS_hiftEndTime = document.querySelector("#addShiftEndTime");
    const add_workMode = document.querySelector("#addWorkingFrom");
    const add_TimeZone = document.querySelector("#addTimeZone");
    
    if(add_ShiftName.value !== "" && add_shiftStartTime.value !=="" && addS_hiftEndTime.value !== "" && add_workMode.value !== "" && add_TimeZone.value !== "") {
        $("#addShiftModal").modal("hide");
        showSuccess(add_ShiftName, "", "");
        showSuccess(add_shiftStartTime, "", "");
        showSuccess(addS_hiftEndTime, "", "");
        showSuccess(add_workMode, "", "");
        showSuccess(add_TimeZone, "", "");
        document.querySelector("#addShiftForm").submit();
    } else {
        showError(add_ShiftName, "block", "Shift Name should not be Empty")
        showError(add_shiftStartTime, "block", "Start Time should not be empty")
        showError(addS_hiftEndTime, "block", "End Time should not be empty")
        showError(add_workMode, "block", "Select Working From")
        showError(add_TimeZone, "block", "Select Time Zone")
    }
    console.log("add shift form submitted");
}

//Show input error messages
const showError = (input, dState, message) => {
    const formFiled = input.parentElement;
    // console.log(formFiled);
    // 1st Way
    // formFiled.className = "addShiftFormField error";
    // formFiled.querySelector(":nth-child(3)").style.display = dState;
    // formFiled.querySelector(":nth-child(3)").className = "cust_err text-danger";
    // formFiled.querySelector(":nth-child(3)").innerHTML = message;
    // 2nd Way
    const small = formFiled.querySelector("small");
    small.style.display = dState;
    small.className = "cust_err text-danger";
    small.innerHTML = message;
};
  
//Show input success
const showSuccess = (input, dState, message) => {
    const formFiled = input.parentElement;
    // console.log(formFiled);
    // 1st Way
    // formFiled.querySelector(":nth-child(3)").style.display = dState;
    // formFiled.querySelector(":nth-child(3)").className = "cust_err";
    // formFiled.querySelector(":nth-child(3)").innerHTML = message;
    // 2nd Way
    const small = formFiled.querySelector("small");
    small.style.display = dState;
    small.className = "cust_err";
    small.innerHTML = message;
};

document.querySelector("#addBreakStartTime").addEventListener("change", function (evt) {
    const bst = document.querySelector("#addBreakStartTime").value;
    // console.log("break start time is : " + bst);
})

// Break Start Time
document.querySelector("#addBreakStartTime").addEventListener("blur", function (evt) {
    if(document.querySelector("#addBreakStartTime").value == "") {
        showError(this, "block" ,"Select Break Start Time");
    } else {
        showSuccess(this, "none", "")
    }
})

// Break End Time
document.querySelector("#addBreakEndTime").addEventListener("blur", function (evt) {
    if(document.querySelector("#addBreakEndTime").value == "") {
        showError(this, "block" ,"Select Break End Time");
    } else {
        showSuccess(this, "none", "")
    }
})

// Shift Name
document.querySelector("#addShiftNameInput").addEventListener("keydown", function (evt) {
    var charCode = evt.keyCode || evt.which;
    if(charCode == 8 || charCode == 46 || charCode == 35 || charCode == 36 || charCode == 37 || charCode == 39) {
        return true;
    }

    if((evt.which >= 48 && evt.which <= 57) || (evt.which >= 96 && evt.which <= 105)) {
        evt.preventDefault();
        showError(this, "block" ,"Numbers are not allowed");
        return false;
    }  else if(!(/[a-zA-Z\t ]/i.test(String.fromCharCode(evt.keyCode)))) {
        evt.preventDefault();
        showError(this, "block" ,"Numbers are not allowed");
        return false;
    }

    if(evt.which === 32 && this.value.length === 0) {
        evt.preventDefault();
        showError(this, "block" ,"Space not allowed");
        return false;
    } else {
        this.value = this.value.replace(/\s+/g, ' ');
        document.querySelector("#addShtErr_shiftName").style.display = "none";
        document.querySelector("#addShtErr_shiftName").innerHTML = "";
    }
})

document.querySelector("#addShiftNameInput").addEventListener("blur", function (evt) {
    if(this.value.length !== 0) {
        this.value = this.value.trim();
    } else {
        showError(this, "block" ,"Shift Name should not be Empty");
    }
})

var shiftStartTime = shiftEndTime = allocatedShiftTime = 0;
// Shift Start Time
document.querySelector("#addShiftStartTime").addEventListener("keydown", function (evt) {
    const startTime = document.querySelector("#addShiftStartTime").value;
    var sHours = startTime.substring(0,2);
    var sMinutes = startTime.substring(3,5);
    // console.log("start Hours :" + sHours);
    // console.log("start Minutes :" + sMinutes);
    if(sHours == "" && sMinutes == "") {
        shiftStartTime = 0;
    } else if(sHours == "" && sMinutes !== "") {
        shiftStartTime = sHours + 0;
    } else if(sHours !== "" && sMinutes == "") {
        shiftStartTime = 0 + sMinutes;
    } else {
        shiftStartTime = startTime;
    }
    // console.log("shift Start time :" + startTime + " = " + shiftStartTime);
})

document.querySelector("#addShiftStartTime").addEventListener("change", function (evt) {
    const startTime = document.querySelector("#addShiftStartTime").value;
    var sHours = startTime.substring(0,2);
    var sMinutes = startTime.substring(3,5);
    // console.log("start Hours :" + sHours);
    // console.log("start Minutes :" + sMinutes);
    if(sHours == "" && sMinutes == "") {
        shiftStartTime = 0;
    } else if(sHours == "" && sMinutes !== "") {
        shiftStartTime = sHours + 0;
    } else if(sHours !== "" && sMinutes == "") {
        shiftStartTime = 0 + sMinutes;
    } else {
        shiftStartTime = startTime;
    }
    // console.log("shift Start time :" + startTime + " = " + shiftStartTime);
})

document.querySelector("#addShiftStartTime").addEventListener("blur", function (evt) {
    if(document.querySelector("#addShiftStartTime").value == "") {
        showError(this, "block" ,"Start Time should not be empty");
    } else {
        showSuccess(this, "none", "")
    }
})

// Shift End Time
document.querySelector("#addShiftEndTime").addEventListener("keydown", function (evt) {
    const endTime = document.querySelector("#addShiftEndTime").value;
    var eHours = endTime.substring(0,2);
    var eMinutes = endTime.substring(3,5);
    // console.log("end Hours :" + eHours);
    // console.log("end Minutes :" + eMinutes);
    if(eHours == "" && eMinutes == "") {
        shiftEndTime = 0;
    } else if(eHours == "" && eMinutes !== "") {
        shiftEndTime = eHours + 0;
    } else if(eHours !== "" && eMinutes == "") {
        shiftEndTime = 0 + eMinutes;
    } else {
        shiftEndTime = endTime;
    }
    // console.log("shift End time :" + endTime + " = " + shiftEndTime);
})

document.querySelector("#addShiftEndTime").addEventListener("change", function (evt) {
    const endTime = document.querySelector("#addShiftEndTime").value;
    var eHours = endTime.substring(0,2);
    var eMinutes = endTime.substring(3,5);
    // console.log("end Hours :" + eHours);
    // console.log("end Minutes :" + eMinutes);
    if(eHours == "" && eMinutes == "") {
        shiftEndTime = 0;
    } else if(eHours == "" && eMinutes !== "") {
        shiftEndTime = eHours + 0;
    } else if(eHours !== "" && eMinutes == "") {
        shiftEndTime = 0 + eMinutes;
    } else {
        shiftEndTime = endTime;
    }
    // console.log("shift End time :" + endTime + " = " + shiftEndTime);
})

document.querySelector("#addShiftEndTime").addEventListener("blur", function (evt) {
    if(document.querySelector("#addShiftEndTime").value == "") {
        showError(this, "block" ,"End Time should not be empty");
    } else {
        showSuccess(this, "none", "")
    }
    
    // console.log("start time :" + typeof shiftStartTime )
    // console.log("end time :" + typeof shiftEndTime )
    var sHours = sMinutes = eHours = eMinutes = 0;
    
    // sHours = parseInt(shiftStartTime.substring(0,2))
    // sMinutes = parseInt(shiftStartTime.substring(3,5))
    // eHours = parseInt(shiftEndTime.substring(0,2))
    // eMinutes = parseInt(shiftEndTime.substring(3,5))
    // console.log(typeof sHours + sHours)
    // console.log(typeof sMinutes + sMinutes)
    // console.log(typeof eHours + eHours)
    // console.log(typeof eMinutes + eMinutes)
    var dHours = eHours - sHours;
    var dMinutes = eMinutes - sMinutes;

    allocatedShiftTime = dHours +" hours "+ dMinutes + " minutes allocated";
    // console.log("allocated Shift time is :" + allocatedShiftTime)
    // document.querySelector("#allocatedTimeMsg").innerHTML = allocatedShiftTime;
})

// Flexible Break
document.querySelector("#flexRadioForFlexibleBreak").addEventListener("click", function(evt) {
    if(document.querySelector("#flexRadioForFlexibleBreak").checked == true) {
        showSuccess(document.querySelector("#addShtErr_breakType"), "none", "");
        document.querySelector("#takeBreakTypeFlexible").style.display = 'block';
        document.querySelector("#takeBreakTypeFixed").style.display = 'none';
    } 
    var breakType = document.querySelector("#flexRadioForFlexibleBreak").value;
    // console.log("Break Type :" + breakType)
})

// Fixed Break
document.querySelector("#flexRadioForFixedBreak").addEventListener("click", function(evt) {
    if(document.querySelector("#flexRadioForFixedBreak").checked == true) {
        showSuccess(document.querySelector("#addShtErr_breakType"), "none", "");
        document.querySelector("#takeBreakTypeFlexible").style.display = 'none';
        document.querySelector("#takeBreakTypeFixed").style.display = 'block';
    } 
    var breakType = document.querySelector("#flexRadioForFixedBreak").value;
    // console.log("Break Type :" + breakType)
})

// Break Type Error
document.querySelector("#flexRadioForFlexibleBreak").addEventListener("blur", function (evt) {
    if(document.querySelector("#flexRadioForFlexibleBreak").checked == false && document.querySelector("#flexRadioForFixedBreak").checked == false) {
        showError(document.querySelector("#addShtErr_breakType"), 'block', "Select Break Mode")
    } else if(document.querySelector("#flexRadioForFlexibleBreak").checked == false && document.querySelector("#flexRadioForFixedBreak").checked == true) {
        showSuccess(document.querySelector("#addShtErr_breakType"), 'none', "")
    } else if(document.querySelector("#flexRadioForFlexibleBreak").checked == true && document.querySelector("#flexRadioForFixedBreak").checked == false) {
        showSuccess(document.querySelector("#addShtErr_breakType"), 'none', "")
    } else {
        showSuccess(document.querySelector("#addShtErr_breakType"), 'none', "")
    }
    // console.log(document.querySelector("#flexRadioForFixedBreak").checked)
})

document.querySelector("#flexRadioForFixedBreak").addEventListener("blur", function (evt) {
    if(document.querySelector("#flexRadioForFlexibleBreak").checked == false && document.querySelector("#flexRadioForFixedBreak").checked == false) {
        showError(document.querySelector("#addShtErr_breakType"), 'block', "Select Break Mode")
    } else if(document.querySelector("#flexRadioForFlexibleBreak").checked == false && document.querySelector("#flexRadioForFixedBreak").checked == true) {
        showSuccess(document.querySelector("#addShtErr_breakType"), 'none', "")
    } else if(document.querySelector("#flexRadioForFlexibleBreak").checked == true && document.querySelector("#flexRadioForFixedBreak").checked == false) {
        showSuccess(document.querySelector("#addShtErr_breakType"), 'none', "")
    } else {
        showSuccess(document.querySelector("#addShtErr_breakType"), 'none', "")
    }
    // console.log(document.querySelector("#flexRadioForFlexibleBreak").checked)
    // console.log(document.querySelector("#flexRadioForFixedBreak").checked)
})

// Flexible Break Time
// document.querySelector("#addFlexibleBreak").addEventListener("change", function (evt) {
//     if(document.querySelector("#addFlexibleBreak").value == "") {
//         document.querySelector("#breakButtonAct").setAttribute("enable", true)
//     } else {
//         document.querySelector("#breakButtonAct").removeAttribute('disabled');
//     }
// })

document.querySelector("#addFlexibleBreak").addEventListener("blur", function (evt) {
    if(document.querySelector("#addFlexibleBreak").value == "") {
        showError(this, "block", "Select Break Time")
    } else {
        showSuccess(this, "none", "")
    }
})

// Break Start Time

// Break End Time

// Working From
document.querySelector("#addWorkingFrom").addEventListener("change", function (evt) {
    const workMode = document.querySelector("#addWorkingFrom").value;
    if(workMode === "") {
        console.log("empty")
    }
    // console.log("working from :" + workMode);
})

document.querySelector("#addWorkingFrom").addEventListener("blur", function (evt) {
    if(document.querySelector("#addWorkingFrom").value == "") {
        showError(this, "block" ,"Select Working Mode");
    } else {
        showSuccess(this, "none", "")
    }
})

// Time Zone
document.querySelector("#addTimeZone").addEventListener("change", function (evt) {
    var timeZone = document.querySelector("#addTimeZone").value;
    // console.log("time zone is :" + timeZone);
})

document.querySelector("#addTimeZone").addEventListener("blur", function (evt) {
    if(document.querySelector("#addTimeZone").value == "") {
        showError(this, "block" ,"Select Time Zone");
    } else {
        showSuccess(this, "none", "")
    }
})