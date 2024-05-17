// console.log("editUserEmpForm");
const editUserName = document.querySelector("#editEmpName");
const editUserEmail = document.querySelector("#editEmpEmail");
const editUserPhone = document.querySelector("#editEmpPhone");
const editUserPassword = document.querySelector("#editEmpPassword");
const editUserDept = document.querySelector("#editEmpDept");
const editUserRole = document.querySelector("#editEmpRole");
const editUserShift = document.querySelector("#editEmpShift");
const editUserShiftStartTime = document.querySelector("#editEmpShiftEndTime");
const editUserShiftEndTime = document.querySelector("#editEmpShiftEndTime");
const editUserBreakStartTime = document.querySelector("#editEmpBreakStartTime");
const editUserBreakEndTime = document.querySelector("#editEmpBreakEndTime");
const editUserTimeZone = document.querySelector("#editEmpTimeZone");
const editUserTagName = document.querySelector("#editEmpTagName");
const editUserSynTime = document.querySelector("#editEmpSynTime");
const editUserScreenshotQuality = document.querySelector("#editEmpScreenshotQuality");
const editUserAlarm = document.querySelector("#editEmpAlarm");

// Change Password variables
const editChangePassword = document.querySelector("#editEmpChangePassword");
const editChangeConfPassword = document.querySelector("#editEmpChangeConfPassword");

// Form Submition
function editUserForm() {

    checkRequired([editUserName, editUserPassword, editUserDept, editUserRole ]);
	if(editUserName.value !== "" && editUserPassword !== "" && editUserDept.value !== "" && editUserRole.value !== "") {
		console.log("form submitted");
	} else {
		CheckEmployeeName(editUserName)
		// CheckEmail(editUserEmail);
		CheckDepartment(editUserDept);
		CheckRole(editUserRole);
		CheckPassword(editUserPassword);
		console.log("form not submitted");
	}
	// CheckEmail(editUserEmail);
	
	// CheckPasswordMatch(editChangePassword,editChangeConfPassword);
	let valid = true;
	$('#editEmpChangePasswordForm [required]').each(function() {
		if ($(this).is(':invalid') || !$(this).val()) valid = false;
	})
	if (!valid) alert("error please fill all fields!");
	else {
		// Modal will open if all the required fields filled
		$('#editUserModalToggle').modal('show');
		$(".is-required").removeClass("border-success");
		$(".col-md-4 form_field").removeClass("success");
		// Modal will close automatically after 3 seconds
		setTimeout(function() {$('#editUserModalToggle').modal('hide');}, 3000);
		// clear the data form inputs and errors
		// $(".is-required").val('');
		// $(".cust_error").val("");
	};
    // $('#editUserEmpForm').submit();
    console.log("form Submited")
    // alert("form data")
}

const getFieldName = (input) => {
    return input.id.charAt(0).toUpperCase() + input.id.slice(1);
};
  
//Show input error messages
const editShowError = (input, message) => {
	
    const formFiled = input.parentElement;
	console.log(formFiled)
    formFiled.className = "col-md-4 form_field error";
    const small = formFiled.querySelector("small");
    small.innerHTML = message;
    formFiled.querySelector(":nth-child(2)").className = "form-control is-required border border-danger";
};
  
//Show input success
 const editShowSuccess = (input) => {
    const formFiled = input.parentElement;
    formFiled.className = "col-md-4 form_field success";
    formFiled.querySelector(":nth-child(2)").className = "form-control is-required border border-success";
};

// for checking all required fileds have value or not
const checkRequired = (inputArr) => {
    inputArr.forEach(function (input) {
		if (input.value.trim() === "") {
			var title = input.previousElementSibling.innerHTML;
			console.log("title" , title)
			editShowError(input, `${title} is required`);
		} else {
			editShowSuccess(input);
			// isReqiredData.push(input.value);
		}
    });
};

editUserName.addEventListener("keypress", function (e) {
    if(!(/[a-z ]/i.test(String.fromCharCode(e.keyCode)))){
        e.preventDefault();
		editShowError(this, "Numbers or not allowed");
        return false;
    }
	if(e.which === 32 && this.value.length === 0) {
		e.preventDefault();
		editShowError(this, "space not allowed")
		return false;
	} else {
		this.value = this.value.replace(/\s+/g, ' ');
	}
	if(this.value.length >=3) {
		editShowSuccess(this)
	}
})

editUserName.addEventListener("keyup", function (evt) {
	// Backspace and Del Button Actions
	if(evt.which === 8 || evt.which === 46) {
		if(this.value.length < 3) {
			editShowError(this, "Employee Name should be minimum 3 characters")
		} else {
			editShowSuccess(this)
		}
	}
})

editUserName.addEventListener("blur", function (e) {
	this.value = this.value.trim();
	if(this.value.length >= 3 ) {
		editShowSuccess(this)
	} else {
		editShowError(this, "Employee Name should be minimum 3 characters")
	}
})

// Employee Name Checking
function CheckEmployeeName(input){
	// console.log(`input value is:${input.value}`)
	const reExp = /^[a-zA-Z\s]+$/;
	if(reExp.test(input)) {
		if(input.value.length > 3) {
			addShowSuccess(input);
		}else {
			addShowError(input, "Employee Name between 3 to 50 characters");
		}
	} 
	// console.log("checking employee name");
}

// Employee Email Call
editUserEmail.addEventListener('keyup', function(evt) {
	if(evt.which === 32) {
		evt.preventDefault();
		editShowError(this, "Space is not allowed");
	}
	CheckEmail(this);
})

editUserEmail.addEventListener('keydown', function(evt) {
	if(evt.which === 32) {
		evt.preventDefault();
		editShowError(this, "Space is not allowed");
	}
	CheckEmail(this);
})

const CheckEmail = (input) => {
	const reExp =
	  /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	if (reExp.test(input.value.trim())) {
	  editShowSuccess(input);
	} else if(input.value.length === 0) {
	  editShowError(input, `Email Should not Empty`);
	}else {
	  editShowError(input, `Email is not valid`);
	  // (Accepts Alphabets, Numbers, @ . _)
	}
};

// Check Phone Number 
const CheckMobileNum = (input) => {
	const reExp = /^\d{10}$/;
	if (reExp.test(input.value)) {
		editShowSuccess(input);
	} else {
		editShowError(input, `Valied Phone number required`);
	}
}


// Employee Phone Call
editUserPhone.addEventListener('keydown', function (evt) {
	if((evt.which >= 48 && evt.which <=57) || (evt.which >= 96 && evt.which <= 105) || evt.which === 8 || evt.which === 46 || evt.which === 9) {
		if(evt.which === 9 && this.value.length < 10) {
			editShowError(this, "Phone Number should be 10 digits")

		} else {
			editShowSuccess(this)
		}
		
	}else {
		if(evt.which === 32) {
			evt.preventDefault();
			editShowError(this, "Space not allowed")
		} else {
			editShowError(this, "Only Numbers are allowed here")
			evt.preventDefault();
		}
	}
	// CheckMobileNum(this)
})

editUserPhone.addEventListener("keyup", function (evt) {
	// Backspace is calling
	if(evt.which === 8) {
		console.log("Phone Backspace calling")
		if(this.value.length < 10) {
			editShowError(this, "Phone Number should be 10 Numbers");
		} else {
			editShowSuccess(this);
		}
	}
})
editUserPhone.addEventListener("change", function (evt) {
	if(this.value.length < 10) {
		editShowError(this, "Phone Number should be 10 Numbers");
	} else {
		editShowSuccess(this);
	}
})

// Employee Password Call
editUserPassword.addEventListener('keyup', function(evt) {
	if(evt.which === 8 && evt.which === 46) {
		if(this.value.length < 8) {
			editShowError(this, "Password minimum contains 8 characters")
		} else {
			editShowSuccess(this);
		}
	}
})

editUserPassword.addEventListener("keydown", function(evt) {
	if(evt.which === 32) {
		evt.preventDefault();
		editShowError(this, "space is not allowed")
	} else {
		// editShowSuccess(this)
		const passRegEx = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,15}$/;
		if(this.value.match(passRegEx)) {
			editShowSuccess(this)
		} else {
			editShowError(this, "Minimum 8 characters, at least one letter, one number and one special character");
		}
	}
})





// Check Password
function CheckPassword (input) {
	const passRegEx = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
	if(input.value.match(passRegEx)) {
		editShowSuccess(this)
	} else {
		editShowError(this, "Minimum 8 characters, at least one letter, one number and one special character check");
	}
}

// Employee Department Call
editUserDept.addEventListener('change', function(evt) {
    // console.log("Department called")
	CheckDepartment(this)
})

function CheckDepartment(input) {
	if(input.value.length > 0) {
		editShowSuccess(input)
		// console.log(input.value);
	} else {
		editShowError(input, "Select Department")
		// console.log('select dept')
	}
}

// Employee Role Call
editUserRole.addEventListener('change', function(evt) {
    // console.log("Role called")
	CheckRole(this);
})

function CheckRole(input) {
	if(input.value.length > 0) {
		editShowSuccess(input)
		// console.log(input.value);
	} else {
		editShowError(input, "Select Role")
		// console.log('select dept')
	}
}

$(".edituserPassChangeClose").click(function() {
	$('#editUserPasswordChangeModalToggle').modal('hide')
})

// Button Enable Disable
$('#editEmpChangePassword, #editEmpChangeConfPassword').bind('keyup, change', function() {
	if(allFilled()) $('#editChangePasswordSubmitBtn').removeAttr('disabled');
});
  
function allFilled() {
	var filled = true;
	$('.isRequired').each(function() {
		if($(this).val() == '') filled = false;
	});
	return filled;
}

// Change Password Show Passwords
function changePassShowCall() {
	var password = document.querySelector("#editEmpChangePassword");
	var confirmPassword = document.querySelector("#editEmpChangeConfPassword");
	if (password.type === "password" && confirmPassword.type === "password") {
	  password.type = "text";
	  confirmPassword.type = "text";
	} else {
	  password.type = "password";
	  confirmPassword.type = "password";
	}
}

// // Show Error 
// const editChangePassShowError = (input, dState, message) => {
//     const regFormField = input.parentElement;
//     const small = regFormField.querySelector("small");
//     small.style.visibility = dState;
//     small.className = "cust_err text-danger";
//     small.innerHTML = message;
// }

// // Show Success
// const editChangePassShowSuccess = (input, dState, message) => {
//     const regFormField = input.parentElement;
//     const small = regFormField.querySelector("small");
//     small.style.visibility = dState;
//     small.className = "cust_err";
//     small.innerHTML = message;
// }


//Show input error messages
const editChangePassShowError = (input, message) => {
    const formFiled = input.parentElement;
	// console.log(formFiled)
    formFiled.className = "col-12 form_field error";
    const small = formFiled.querySelector("small");
    small.innerHTML = message;
    formFiled.querySelector(":nth-child(2)").className = "form-control is-required border border-danger";
};

//Show input success
const editChangePassShowSuccess = (input) => {
    const formFiled = input.parentElement;
	// console.log(formFiled)
    formFiled.className = "col-12 form_field success";	
	const small = formFiled.querySelector("small");
    small.innerHTML = "Success";
    formFiled.querySelector(":nth-child(2)").className = "form-control is-required border border-success";
};

const CheckChangePassword = (input) => {
	const passRegEx = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
	if(input.value.match(passRegEx)) {
		editChangePassShowSuccess(this)
	} else {
		editChangePassShowError(this, "Minimum 8 characters, at least one letter, one number and one special character check");
	}
}

const CheckChangeConfPassword = (input) => {
	if ($('#editEmpChangePassword').val() !== $('#editEmpChangeConfPassword').val()) {
		editChangePassShowError(confPass, "Password do not match")
	} else {
		editChangePassShowSuccess(confPass)
	}
	console.log("confirm call")
}

function editChangePasswordSubmit() {
	if(($('#editEmpChangePassword').val() !== "" && $('#editEmpChangeConfPassword').val() !== "")&& ($('#editEmpChangePassword').val() === $('#editEmpChangeConfPassword').val())) {
		console.log("Password changed")
		document.querySelector("#editEmpChangePasswordForm").submit();
		$('#editUserPasswordChangeModalToggle').modal('hide');
	} else {
		console.log("failed Password changed")
	}
}

document.querySelector("#editEmpChangePassword").addEventListener("keydown", function(evt) {
	if(evt.which === 32) {
		evt.preventDefault();
		editChangePassShowError(this, "space is not allowed");
	} else {
		const passRegEx = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,15}$/;
		if(this.value.match(passRegEx)) {
			editChangePassShowSuccess(this);
			if(this.value.length < 8) {
				editChangePassShowError(this, "Minimum 8 characters, at least one letter, one number and one special character keydown")
				// console.log("keydown if password " + this.value)
				// console.log("keydown if password length " + this.value.length)
			} else {
				editChangePassShowSuccess(this)
			}
		} else {
			editChangePassShowError(this,"Minimum 8 characters, at least one letter, one number and one special character");
			// console.log("keydown else password " + this.value)
			// console.log("keydown else password length " + this.value.length)
		}
	}

	if(evt.which === 8 && evt.which === 46) {
		if(this.value.length > 8) {
			editChangePassShowSuccess(this);
		} else {
			editChangePassShowError(this,"Password minimum contains 8 characters");
		}
	}
})

// Popup Employee Password Call
document.querySelector("#editEmpChangePassword").addEventListener('keyup', function(evt) {
	if(evt.which === 8 && evt.which === 46) {
		if(this.value.length > 8) {
			editChangePassShowSuccess(this);
		} else {
			editChangePassShowError(this,"Password minimum contains 8 characters");
		}
	}
})

$('#editEmpChangeConfPassword').on('keyup', function () {
	if ($('#editEmpChangePassword').val() == $('#editEmpChangeConfPassword').val()) {
	//   $('#message').html('Matching').css('color', 'green');
	editChangePassShowSuccess(this)
	} else 
	//   $('#message').html('Not Matching').css('color', 'red');
	editChangePassShowError(this, "Password do not match")
});

document.querySelector("#editEmpChangeConfPassword").addEventListener("keydown", function(evt) {
	if(evt.which === 32) {
		evt.preventDefault();
		editChangePassShowError(this, "Space not allowed")
	} else {
		editChangePassShowSuccess(this)
	}
	// chandu
})

$('#editEmpChangePassword').on('blur', function () {
	if($("#CheckChangePassword").val() < 8) {
		editChangePassShowError(this, "Password min 8 chars")
	}
})

$('#editEmpChangeConfPassword').on('blur', function () {
	if ($('#editEmpChangePassword').val() == $('#editEmpChangeConfPassword').val()) {
		//   $('#message').html('Matching').css('color', 'green');
		editChangePassShowSuccess(this)
		} else 
		//   $('#message').html('Not Matching').css('color', 'red');
		editChangePassShowError(this, "Password do not match")
})