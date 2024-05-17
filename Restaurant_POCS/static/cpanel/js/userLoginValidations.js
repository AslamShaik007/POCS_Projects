console.log("user login validations called");

const loginUser = document.querySelector("#userLoginName");
const logiPassword = document.querySelector("#userLoginPassword");


function loginForm() {
    if(loginUser.value !== "" && logiPassword.value !== "") {
        console.log("form submitted");
    } else {
        CheckEmail(loginUser)
        CheckPassword(logiPassword);
        console.log("form not submitted")
    }
}

// Employee Email Call
loginUser.addEventListener('keyup', function(evt) {
	if(evt.which === 32) {
		evt.preventDefault();
		userLoginShowError(this, "Space is not allowed");
	}
	CheckEmail(this);
})

loginUser.addEventListener('keydown', function(evt) {
	if(evt.which === 32) {
		evt.preventDefault();
		userLoginShowError(this, "Space is not allowed");
	}
	CheckEmail(this);
})

const CheckEmail = (input) => {
	const reExp =
	  /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	if (reExp.test(input.value.trim())) {
	  userLoginShowSuccess(input);
	} else if(input.value.length === 0) {
	  userLoginShowError(input, `Email Should not Empty`);
	}else {
	  userLoginShowError(input, `Email is not valid`);
	  // (Accepts Alphabets, Numbers, @ . _)
	}
};

// User Password Call
logiPassword.addEventListener('keyup', function(evt) {
	if(evt.which === 8 && evt.which === 46) {
		if(this.value.length < 8) {
            const formFiled = this.parentElement;
            formFiledParent.className = "Password Min contains 8 characters";
            formFiled.className = "input-group mb-3";
            formFiled.querySelector(":nth-child(1)").className = "form-control custom-login-form border border-danger";
            document.querySelector("#userLogin_err_password").innerHTML = "space is not allowed";
		} else {
			const formFiledParent = this.parentElement.parentElement;
            const formFiled = this.parentElement;
            formFiledParent.className = "col-md-12 form_field error";
            formFiled.className = "input-group mb-3";
            formFiled.querySelector(":nth-child(1)").className = "form-control custom-login-form border border-success";
            document.querySelector("#userLogin_err_password").innerHTML = "";
		}
	}
})

logiPassword.addEventListener("keydown", function(evt) {
	if(evt.which === 32) {
        console.log("space is not allowed")
		evt.preventDefault();
        const formFiledParent = this.parentElement.parentElement;
        const formFiled = this.parentElement;
        formFiledParent.className = "col-md-12 form_field error";
        formFiled.className = "input-group mb-3";
        formFiled.querySelector(":nth-child(1)").className = "form-control custom-login-form border border-danger";
        document.querySelector("#userLogin_err_password").innerHTML = "space is not allowed";
	} else {
		const passRegEx = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,15}$/;
		if(this.value.match(passRegEx)) {
            const formFiledParent = this.parentElement.parentElement;
            const formFiled = this.parentElement;
            formFiledParent.className = "col-md-12 form_field error";
            formFiled.className = "input-group mb-3";
            formFiled.querySelector(":nth-child(1)").className = "form-control custom-login-form border border-success";
            document.querySelector("#userLogin_err_password").innerHTML = "";
		} else {
            const formFiledParent = this.parentElement.parentElement;
            const formFiled = this.parentElement;
            formFiledParent.className = "col-md-12 form_field error";
            formFiled.className = "input-group mb-3";
            formFiled.querySelector(":nth-child(1)").className = "form-control custom-login-form border border-danger";
            document.querySelector("#userLogin_err_password").innerHTML = "Min 8 chars, at least 1 letter, 1 number and 1 special char";
		}
	}
})

// Check Password
function CheckPassword (input) {
	const passRegEx = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
	if(input.value.match(passRegEx)) {
		const formFiledParent = input.parentElement.parentElement;
        const formFiled = input.parentElement;
        formFiledParent.className = "col-md-12 form_field error";
        formFiled.className = "input-group mb-3";
        formFiled.querySelector(":nth-child(1)").className = "form-control custom-login-form border border-success";
        document.querySelector("#userLogin_err_password").innerHTML = "";
	} else {
        const formFiledParent = input.parentElement.parentElement;
        const formFiled = input.parentElement;
        formFiledParent.className = "col-md-12 form_field error";
        formFiled.className = "input-group mb-3";
        formFiled.querySelector(":nth-child(1)").className = "form-control custom-login-form border border-danger";
        document.querySelector("#userLogin_err_password").innerHTML = "Min 8 chars, at least 1 letter, 1 number and 1 special char";
	}
}

// Show Password
function showPassword() {
    var inputType = document.querySelector("#userLoginPassword");
    if (inputType.type === "password") {
      inputType.type = "text";
      document.querySelector("#showPassIcon").className = "fa fa-eye";
    } else {
      inputType.type = "password";
      document.querySelector("#showPassIcon").className = "fa fa-eye-slash";
    }
}

//Show input error messages
const forgotPassError = (input, message) => {
    const formFiled = input.parentElement;
    formFiled.className = "col-12 form_field error";
    const small = formFiled.querySelector("small");
    small.innerHTML = message;
    formFiled.querySelector(":nth-child(2)").className = "form-control is-required border border-danger";
};
  
//Show input success
 const forgotPassSuccess = (input) => {
    const formFiled = input.parentElement;
    formFiled.className = "col-12 form_field success";
	const small = formFiled.querySelector("small");
    small.innerHTML = "Success";
    formFiled.querySelector(":nth-child(2)").className = "form-control is-required border border-success";
};

// Popup Employee Password Call
document.querySelector("#userForgotPassword").addEventListener('keyup', function(evt) {
	if(evt.which === 8 && evt.which === 46) {
		if(this.value.length > 8) {
			forgotPassSuccess(this);
		} else {
			forgotPassError(this,"Password Min contains 8 characters");
		}
	}
})

const forgotPass = $('#userForgotPassword').val();
const forgotConfPass = $('#userForgotConfPassword').val();

document.querySelector("#userForgotPassword").addEventListener("keydown", function(evt) {
const forgotPass = $('#userForgotPassword').val();
	if(evt.which === 32) {
		evt.preventDefault();
		forgotPassError(this, "space is not allowed");
	} else {
		const passRegEx = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,15}$/;
		if(this.value.match(passRegEx)) {
			forgotPassSuccess(this);
			if(this.value.length < 8) {
				forgotPassError(this, "Min 8 chars, at least 1 letter, 1 number and 1 special char")
			} else {
				forgotPassSuccess(this)
			}
		} else {
			forgotPassError(this,"Min 8 chars, at least 1 letter, 1 number and 1 special char");
		}
	}

	if(evt.which === 8 && evt.which === 46) {
		if(this.value.length > 8) {
			forgotPassSuccess(this);
		} else {
			forgotPassError(this,"Password Min contains 8 characters");
		}
	}
})

document.querySelector("#userForgotConfPassword").addEventListener("blur", function (evt) {
    CheckPasswordMatch(forgotPass, forgotConfPass);
})


$('#userForgotConfPassword').on('keyup', function () {
	if ($('#userForgotPassword').val() == $('#userForgotConfPassword').val()) {
	forgotPassSuccess(this)
	} else 
	forgotPassError(this, "Password do not match")
});

document.querySelector("#userForgotConfPassword").addEventListener("keydown", function(evt) {
	if(evt.which === 32) {
		evt.preventDefault();
		forgotPassError(this, "Space not allowed")
	} else {
		forgotPassSuccess(this)
	}
})

var matchResult = false;
// Check both Passwords are equal or not
const CheckPasswordMatch = (pass, confPass) => {
	if ($('#userForgotPassword').val() !== $('#userForgotConfPassword').val()) {
		// forgotPassError(confPass, "Password do not match")
        const formFiled = document.querySelector("#userForgotConfPassword").parentElement;
        formFiled.className = "col-12 form_field error";
        const small = formFiled.querySelector("small");
        small.innerHTML = "Password not matched";
        formFiled.querySelector(":nth-child(2)").className = "form-control is-required border border-danger";
        matchResult = false;
	} else {
		const formFiled = document.querySelector("#userForgotConfPassword").parentElement;
        formFiled.className = "col-12 form_field success";
        const small = formFiled.querySelector("small");
        small.innerHTML = "";
        formFiled.querySelector(":nth-child(2)").className = "form-control is-required border border-success";
        matchResult = true;
	}
};

// Change Password Show Passwords
function userForgotPassShowCall() {
	var password = document.querySelector("#userForgotPassword");
	var confirmPassword = document.querySelector("#userForgotConfPassword");
	if (password.type === "password" && confirmPassword.type === "password") {
	  password.type = "text";
	  confirmPassword.type = "text";
	} else {
	  password.type = "password";
	  confirmPassword.type = "password";
	}
}

$("#userForgotClose").click(function() {
	$('#userForgotPasswordModalToggle').modal('hide')
})

// Update Password Button Enable Disable
$('#userForgotPassword, #userForgotConfPassword').bind('keyup, change', function() {
	if(allFilled()) {
        $('#userForgotPasswordSubmitBtn').removeAttr('disabled')
    } else {
        $('#userForgotPasswordSubmitBtn').attr('enabled')
    }
});
  
function allFilled() {
	var filled = true;
	$('.isRequired').each(function() {
		if($(this).val() == '') filled = false;
	});
	return filled;
}

function userForgotPasswordForm(evt) {
    evt.preventDefault();
    const passw = document.querySelector("#userForgotPassword").value;
    const confPassw = document.querySelector("#userForgotConfPassword").value;
    CheckPasswordMatch(passw, confPassw);
    if(matchResult === true) {
        $('#userForgotSuccessModalToggle').modal('show');
        $(".isRequired").removeClass("border-success");
        $(".col-12 form_field").removeClass("success");
        // Modal will close automatically after 3 seconds
		setTimeout(function() {$('#userForgotSuccessModalToggle').modal('hide');}, 3000);
        $('#userForgotPasswordModalToggle').modal('hide')
        // clear the data form inputs and errors
        document.querySelectorAll(".isRequired").value = "";
        document.querySelectorAll(".forgotErrMsg").value = "";
        document.querySelector("#userForgotPasswordForm").submit();
    } else {
        console.log("password not match")
    }
}

// Forgot Password Call
document.querySelector("#forgotPasswordBtn").addEventListener("click", function (evt) {
    // clear the data form inputs and errors
    document.querySelectorAll(".isRequired").value = "";
    document.querySelectorAll(".forgotErrMsg").value = "";
})

//Show input error messages
const userLoginShowError = (input, message) => {
    const formFiled = input.parentElement;
    formFiled.className = "col-md-12 form_field error";
    const small = formFiled.querySelector("small");
    small.innerHTML = message;
    formFiled.querySelector(":nth-child(1)").className = "form-control is-required border border-danger";
};
  
//Show input success
 const userLoginShowSuccess = (input) => {
    const formFiled = input.parentElement;
    formFiled.className = "col-md-12 form_field success";
    formFiled.querySelector(":nth-child(1)").className = "form-control is-required border border-success";
};

// Remember Me
const rmCheck = document.querySelector("#remember_Me");

rmCheck.addEventListener("change", function(evt) {
    if(rmCheck.checked == true) {
        remember_Me();
    }
})

// console.log(localStorage.getItem("loginUser"))

function remember_Me() {
    localStorage.setItem("loginUser", loginUser.value);
    localStorage.setItem("loginPass", logiPassword.value);                
    
}

window.onload = checkUser;

function checkUser(){
    if(localStorage.getItem("loginUser") !== "") {
      document.querySelector("#userLoginName").value = localStorage.getItem("loginUser");
      document.querySelector("#userLoginPassword").value = localStorage.getItem("loginPass");
    } 
    else {
        document.querySelector("#userLoginName").value = "";
        document.querySelector("#userLoginPassword").value = "";
        document.querySelector("#userLoginName").focus();
    }
};


document.querySelector("#userLogin_err_password").style.fontSize = "0.75rem";
document.querySelector("#userLogin_err_username").style.fontSize = "0.75rem";