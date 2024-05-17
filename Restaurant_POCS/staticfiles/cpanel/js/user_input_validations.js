// console.log("Script is responding");
const inputData = [];
let isReqiredData = [];

const newEmpName = document.querySelector("#emp_Name");
const newEmpEmail = document.querySelector("#emp_Email");
const newEmpPassword = document.querySelector("#emp_Password");
const newEmpConfPassword = document.querySelector("#emp_ConfPassword");
const newEmpMobileNum = document.querySelector("#emp_Phone");
const newEmpDept = document.querySelector("#emp_Department")
const newEmpTag = document.querySelector("#emp_Tag");
const newEmpRole = document.querySelector("#emp_Role");
const newEmpShift = document.querySelector("#emp_Shift");
const newEmpConfig = document.querySelector("#emp_config");

// Form submition
function newUserEmpForm() {
	checkRequired([newEmpName, newEmpEmail, newEmpPassword, newEmpConfPassword, newEmpDept, newEmpRole])
	if(newEmpName.value !== "" && newEmpEmail !== "" && newEmpPassword.value !== "" && newEmpConfPassword.value !== "" && newEmpDept.value !== "" && newEmpRole.value !== "") {
		console.log("form submitted");
	} else {
		CheckEmployeeName(newEmpName);
		CheckEmail(newEmpEmail);
		CheckPassword(newEmpPassword);
		CheckPasswordMatch(newEmpPassword, newEmpConfPassword);
		CheckDepartment(newEmpDept);
		CheckRole(newEmpRole);
		console.log("form not submitted");
	}
	
	
	let valid = true;
	$('[required]').each(function() {
		if ($(this).is(':invalid') || !$(this).val()) valid = false;
	})
	if (!valid) console.log("error please fill all fields!");
	else {
		// Modal will open if all the required fields filled
		$('#addUserModalToggle').modal('show');
		$(".is-required").removeClass("border-success");
		$(".col-md-6 form_field").removeClass("success");
		// Modal will close automatically after 3 seconds
		setTimeout(function() {$('#addUserModalToggle').modal('hide');}, 3000);
		// clear the data form inputs and errors
		// $(".is-required").val('');
		// $(".cust_error").val("");
	};
}

newEmpName.addEventListener("keypress", function (e) {
    if(!(/[a-zA-Z ]/i.test(String.fromCharCode(e.keyCode)))){
        e.preventDefault();
		addShowError(this, "Numbers or not allowed");
        return false;
    }
	if(e.which === 32 && this.value.length === 0) {
		e.preventDefault();
		addShowError(this, "space not allowed")
		return false;
	} else {
		this.value = this.value.replace(/\s+/g, ' ');
		addShowSuccess(this)
	}
	// if(this.value.length >=3) {
	// 	addShowSuccess(this)
	// }

	// Backspace action
})

newEmpName.addEventListener("keyup", function (evt) {
	if(evt.which === 32 && this.value.length === 0) {
		evt.preventDefault();
		addShowError(this, "Space not allowed")
	}
	if(evt.which === 8 || evt.which === 46) {
		if(this.value.length < 3) {
			addShowError(this, "Employee Name should be minimum 3 characters")
		} else {
			addShowSuccess(this)
		}
	}
})

newEmpName.addEventListener("blur", function (e) {
	this.value = this.value.trim();
	if(this.value.length >= 3 ) {
		addShowSuccess(this)
	} else {
		addShowError(this, "Employee Name should be minimum 3 characters")
	}
})
newEmpEmail.addEventListener("keydown", function(evt) {
	if(evt.which === 32) {
		evt.preventDefault();
		addShowError(this, "Space not allowed");
	}
	CheckEmail(this);
})

newEmpEmail.addEventListener("change", function(evt) {
	CheckEmail(this);
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

// Email Checking
function CheckEmail(input) {
	const reExp =
	  /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	if (reExp.test(input.value.trim())) {
	  addShowSuccess(input);
	} else if(input.value.length === 0) {
	  addShowError(input, `Email Should not Empty`);
	}else {
	  addShowError(input, `Email is not valid`);
	  // (Accepts Alphabets, Numbers, @ . _)
	}
}

// Check Phone Number 
const CheckMobileNum = (input) => {
	const reExp = /^\d{10}$/;
	if (reExp.test(input.value)) {
		addShowSuccess(input);
	} else {
		addShowError(input, `Valied Phone number required`);
	}
}
// Employee Phone Call
newEmpMobileNum.addEventListener('keydown', function (evt) {
	if((evt.which >= 48 && evt.which <=57) || (evt.which >= 96 && evt.which <= 105) || evt.which === 8 || evt.which === 46 || evt.which === 9) {
		if(evt.which === 9 && this.value.length < 10) {
			addShowError(this, "Phone Number should be 10 digits")

		} else {
			addShowSuccess(this)
		}
	}else {
		if(evt.which === 32) {
			evt.preventDefault();
			addShowError(this, "Space not allowed")
		} else {
			addShowError(this, "Only Numbers are allowed here")
			evt.preventDefault();
		}
	}
	// CheckMobileNum(this)
})

newEmpMobileNum.addEventListener("keyup", function (evt) {
	// Backspace is calling
	if(evt.which === 8) {
		console.log("Phone Backspace calling")
		if(this.value.length < 10) {
			addShowError(this, "Phone Number should be 10 Numbers");
		} else {
			addShowSuccess(this);
		}
	}
})

newEmpMobileNum.addEventListener("change", function (evt) {
	if(this.value.length < 10) {
		addShowError(this, "Phone Number should be 10 Numbers");
	} else {
		addShowSuccess(this);
	}
})

// Employee Password Call
newEmpPassword.addEventListener('keyup', function(evt) {
	if(evt.which === 8 && evt.which === 46) {
		if(this.value.length < 8) {
			const formField = this.parentElement;
			formField.className = "col-md-6 form_field error";
			document.querySelector("#empPasswordErr").style.display = "block";
			document.querySelector("#emp_Password").className = "form-control is-required border border-danger";
			document.querySelector("#empPasswordErr").innerHTML = "Password minimum contains 8 characters";
		} else {
			const formField = this.parentElement;
			formField.className = "col-md-6 form_field success";
			document.querySelector("#empPasswordErr").style.display = "none";
			document.querySelector("#emp_Password").className = "form-control is-required border border-success";
			document.querySelector("#empPasswordErr").innerHTML = "";
		}
	}
})

newEmpPassword.addEventListener("keydown", function(evt) {
	// console.log("keypress count " + this.value.length)
	if(evt.which === 32) {
		evt.preventDefault();
		const formField = this.parentElement;
		formField.className = "col-md-6 form_field error";
		document.querySelector("#empPasswordErr").style.display = "block";
		document.querySelector("#emp_Password").className = "form-control is-required border border-danger";
		document.querySelector("#empPasswordErr").innerHTML = "space is not allowed";
	} else {
		const passRegEx = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,15}$/;
		if(this.value.match(passRegEx)) {
			const formField = this.parentElement;
			formField.className = "col-md-6 form_field success";
			document.querySelector("#empPasswordErr").style.display = "none";
			document.querySelector("#emp_Password").className = "form-control is-required border border-success";
			document.querySelector("#empPasswordErr").innerHTML = "";
			if(this.value.length <= 8) {
				const formField = this.parentElement;
				formField.className = "col-md-6 form_field error";
				document.querySelector("#empPasswordErr").style.display = "block";
				document.querySelector("#emp_Password").className = "form-control is-required border border-danger";
				document.querySelector("#empPasswordErr").innerHTML = "Minimum 8 characters, at least one letter, one number and one special character";
				// console.log("Minimum 8 characters, at least one letter, one number and one special character keydown")
			} else {
				const formField = this.parentElement;
				formField.className = "col-md-6 form_field success";
				document.querySelector("#empPasswordErr").style.display = "none";
				document.querySelector("#emp_Password").className = "form-control is-required border border-success";
				document.querySelector("#empPasswordErr").innerHTML = "";
			}
		} else {
			const formField = this.parentElement;
			formField.className = "col-md-6 form_field error";
			document.querySelector("#empPasswordErr").style.display = "block";
			document.querySelector("#emp_Password").className = "form-control is-required border border-danger";
			document.querySelector("#empPasswordErr").innerHTML = "Minimum 8 characters, at least one letter, one number and one special character";
		}
	}
})

newEmpPassword.addEventListener("blur", function(evt) {
	if(this.value.length < 8) {
		const formField = this.parentElement;
		formField.className = "col-md-6 form_field error";
		document.querySelector("#empPasswordErr").style.display = "block";
		document.querySelector("#emp_Password").className = "form-control is-required border border-danger";
		document.querySelector("#empPasswordErr").innerHTML = "Minimum 8 characters, at least one letter, one number and one special character mat";
	} else {
		const formField = this.parentElement;
		formField.className = "col-md-6 form_field success";
		document.querySelector("#empPasswordErr").style.display = "none";
		document.querySelector("#emp_Password").className = "form-control is-required border border-success";
		document.querySelector("#empPasswordErr").innerHTML = "Success";
	}
})

// Check Password
function CheckPassword (input) {
	const passRegEx = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,15}$/;
	if(input.value.match(passRegEx)) {
		if(input.value.length < 8) {
			const formField = input.parentElement;
			formField.className = "col-md-6 form_field error";
			document.querySelector("#empPasswordErr").style.display = "block";
			document.querySelector("#emp_Password").className = "form-control is-required border border-danger";
			document.querySelector("#empPasswordErr").innerHTML = "Minimum 8 characters, at least one letter, one number and one special character sta";
		} else {
			const formField = input.parentElement;
			formField.className = "col-md-6 form_field success";
			document.querySelector("#empPasswordErr").style.display = "none";
			document.querySelector("#emp_Password").className = "form-control is-required border border-success";
			document.querySelector("#empPasswordErr").innerHTML = "";
		}
	} 
}

// Show Passwords
function showPassword() {
	var password = document.querySelector("#emp_Password");
	var confirmPassword = document.querySelector("#emp_ConfPassword");
	if (password.type === "password" && confirmPassword.type === "password") {
	  password.type = "text";
	  confirmPassword.type = "text";
	} else {
	  password.type = "password";
	  confirmPassword.type = "password";
	}
}

// Confirm Password Checking
$('#emp_ConfPassword').on('keyup', function () {
	if ($('#emp_Password').val() == $('#emp_ConfPassword').val()) {
		const formField = this.parentElement;
		formField.className = "col-md-6 form_field success";
		document.querySelector("#empConfirmPasswordErr").style.display = "none";
		document.querySelector("#emp_ConfPassword").className = "form-control is-required border border-success";
		document.querySelector("#empConfirmPasswordErr").innerHTML = "";
	} else {
		const formField = this.parentElement;
		formField.className = "col-md-6 form_field error";
		document.querySelector("#empConfirmPasswordErr").style.display = "block";
		document.querySelector("#emp_ConfPassword").className = "form-control is-required border border-danger";
		document.querySelector("#empConfirmPasswordErr").innerHTML = "Password do not match";
	}
});

// Department Calling
newEmpDept.addEventListener("change", function (evt) {
	CheckDepartment(this)
})

// Department Checking 
function CheckDepartment(input) {
	// console.log("Department Checking");
	if(input.value.length > 0) {
		addShowSuccess(input)
		// console.log(input.value);
	} else {
		addShowError(input, "Select Department")
		// console.log('select dept')
	}
}

// Designation Calling
newEmpRole.addEventListener("change", function (evt) {
	CheckRole(this);
})

// Role Checking 
function CheckRole(input) {
	if(input.value.length > 0) {
		addShowSuccess(input)
		// console.log(input.value);
	} else {
		addShowError(input, "Select Role")
		// console.log('select role')
	}
}

// Get the Field Name
const getFieldName = (input) => {
	return input.id.charAt(0).toUpperCase() + input.id.slice(1);
};

//Show input error messages
const addShowError = (input, message) => {
	const formField = input.parentElement;
	formField.className = "col-md-6 form_field error";
	const small = formField.querySelector("small");
	small.innerHTML = message;
	formField.querySelector(":nth-child(2)").className = "form-control is-required border border-danger";
};
  
//Show input success
const addShowSuccess = (input) => {
	const formField = input.parentElement;
	formField.className = "col-md-6 form_field success";
	formField.querySelector(":nth-child(2)").className = "form-control is-required border border-success";
};

// for checking all required fileds have value or not
const checkRequired = (inputArr) => {
	inputArr.forEach(function (input) {
		if (input.value.trim() === "") {
			addShowError(input, `${getFieldName(input)} is required`);
		} else {
			addShowSuccess(input);
			isReqiredData.push(input.value);
		}
	});
};

newEmpConfPassword.addEventListener('keydown', function(evt) {
	if(evt.which === 32) {
		evt.preventDefault();
		addShowError(this, "Space not allowed");
	}
})

newEmpConfPassword.addEventListener('keyup', function(evt) {
	if(evt.which === 32) {
		evt.preventDefault();
		addShowError(this, "Space not allowed");
	}
})

// Confirm Password Match
function CheckPasswordMatch(pass, confPass) {
	// if ($('#newEmpPassword').val() !== $('#newEmpConfPassword').val()) {
	if (pass.value !== confPass.value) {
		const formField = confPass.parentElement;
		formField.className = "col-md-6 form_field error";
		document.querySelector("#empConfirmPasswordErr").style.display = "block";
		document.querySelector("#emp_ConfPassword").className = "form-control is-required border border-danger";
		document.querySelector("#empConfirmPasswordErr").innerHTML = "Password do not match";
	} else {
		const formField = confPass.parentElement;
		// console.log("formField is ", formField)
		formField.className = "col-md-6 form_field success";
		document.querySelector("#empConfirmPasswordErr").style.display = "none";
		document.querySelector("#emp_ConfPassword").className = "form-control is-required border border-success";
		document.querySelector("#empConfirmPasswordErr").innerHTML = "";
	}
};

// Button Enable Disable
$('#emp_Name, #emp_Email, #emp_Password, #emp_ConfPassword, #emp_Department, #emp_Role').bind('keyup, change', function() {
	if(allFilled()) $('#empSubmit').removeAttr('disabled');
	if(allFilled()) $("#empAddMore").removeAttr('disabled');
});
  
function allFilled() {
	var filled = true;
	$('.is-required').each(function() {
		if($(this).val() == '') filled = false;
	});
	return filled;
}

