// New code start here remove below line
// console.log("login script loading")
// New code end here

// New code start here remove below line
// const loginForm = document.querySelector("#login_form");
// New code end here
const loginUser = document.querySelector("#adminLoginName");
const logiPassword = document.querySelector("#adminLoginPassword");

// New code Start here (removed addEventListener and add a function)
function LoginForm() {
// New code end here
    if(loginUser.value !== "" && logiPassword.value !== "") {
        // New code start here
        CheckEmail(loginUser)
        CheckPassword(logiPassword);
        rememberUser();
        encryptPass();
        document.querySelector("#login_form").submit();
        // console.log("form submitted")
        // New code end here
    } else {
        CheckEmail(loginUser)
        CheckPassword(logiPassword);
        console.log("form not submitted")
    }
}

// New code start here
function encryptPass() {
    var pass=document.getElementById('adminLoginPassword').value;
    var passhide=document.getElementById('adminloginpasshide').value;

    if(pass=="") {
        document.getElementById('err').innerHTML='Error:Password is missing';
        return false;
    } else {
        document.getElementById("passhide").value = document.getElementById("adminLoginPassword").value;
        var hashPass = CryptoJS.MD5(pass);
        document.getElementById('adminLoginPassword').value=passhide;
        return true;
    }
}
// New code end here

// Employee Email Call
$("#adminLoginName").keyup(function(evt){
    // New code start here (this below line no need)
    // console.log("key up event")
    // New code end here
	if(evt.which === 32) {
		evt.preventDefault();
		userShowError(this, "Space is not allowed");
	}
    // New code start here (make remove this CheckEmail(this))
    // CheckEmail(this);
    // New code start here
})

loginUser.addEventListener('keydown', function(evt) {
	if(evt.which === 32) {
		evt.preventDefault();
		userShowError(this, "Space is not allowed");
	}
	// New code start here (make remove this CheckEmail(this))
    // CheckEmail(this);
    // New code start here
})

const CheckEmail = (input) => {
	const reExp =
	  /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	if (reExp.test(input.value.trim())) {
	  userShowSuccess(input);
	} else if(input.value.length === 0) {
	  userShowError(input, `Email Should not Empty`);
	}else {
	  userShowError(input, `Email is not valid`);
	  // (Accepts Alphabets, Numbers, @ . _)
	}
};

// Employee Password Call
logiPassword.addEventListener('keyup', function(evt) {
	if(evt.which === 8 && evt.which === 46) {
		if(this.value.length < 8) {
            const formFiled = this.parentElement;
            formFiledParent.className = "Password Min contains 8 characters";
            formFiled.className = "input-group mb-3";
            formFiled.querySelector(":nth-child(1)").className = "form-control custom-login-form border border-danger";
            document.querySelector("#login_err_password").innerHTML = "space is not allowed";
		} else {
			const formFiledParent = this.parentElement.parentElement;
            const formFiled = this.parentElement;
            formFiledParent.className = "col-md-12 form_field error";
            formFiled.className = "input-group mb-3";
            formFiled.querySelector(":nth-child(1)").className = "form-control custom-login-form border border-success";
            document.querySelector("#login_err_password").innerHTML = "";
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
        document.querySelector("#login_err_password").innerHTML = "space is not allowed";
	} else {
		const passRegEx = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,15}$/;
		if(this.value.match(passRegEx)) {
            const formFiledParent = this.parentElement.parentElement;
            const formFiled = this.parentElement;
            formFiledParent.className = "col-md-12 form_field error";
            formFiled.className = "input-group mb-3";
            formFiled.querySelector(":nth-child(1)").className = "form-control custom-login-form border border-success";
            document.querySelector("#login_err_password").innerHTML = "";
		} else {
            const formFiledParent = this.parentElement.parentElement;
            const formFiled = this.parentElement;
            formFiledParent.className = "col-md-12 form_field error";
            formFiled.className = "input-group mb-3";
            formFiled.querySelector(":nth-child(1)").className = "form-control custom-login-form border border-danger";
            // New code start here (please remove the "data insize quotes")
            document.querySelector("#login_err_password").innerHTML = "";
            // New code end here
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
        document.querySelector("#login_err_password").innerHTML = "";
	} else {
        const formFiledParent = input.parentElement.parentElement;
        const formFiled = input.parentElement;
        formFiledParent.className = "col-md-12 form_field error";
        formFiled.className = "input-group mb-3";
        formFiled.querySelector(":nth-child(1)").className = "form-control custom-login-form border border-danger";
        document.querySelector("#login_err_password").innerHTML = "Min 8 chars, at least 1 letter, 1 number and 1 special char";
	}
}

// Show Password
function showPassword() {
    console.log("show password call")
    var inputType = document.querySelector("#adminLoginPassword");
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
document.querySelector("#forgotUserPassword").addEventListener('keyup', function(evt) {
	if(evt.which === 8 && evt.which === 46) {
		if(this.value.length > 8) {
			forgotPassSuccess(this);
		} else {
			forgotPassError(this,"Password Min contains 8 chars");
		}
	}
})

const forgotPass = $('#forgotUserPassword').val();
const forgotConfPass = $('#forgotUserConfPassword').val();

document.querySelector("#forgotUserPassword").addEventListener("keydown", function(evt) {
const forgotPass = $('#forgotUserPassword').val();
	if(evt.which === 32) {
		evt.preventDefault();
		forgotPassError(this, "space is not allowed");
	} else {
		const passRegEx = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,15}$/;
		if(this.value.match(passRegEx)) {
			forgotPassSuccess(this);
			if(this.value.length < 8) {
                // New code start here (remove the "data inside the quotes")
				forgotPassError(this, "")
                // New code end here
			} else {
				forgotPassSuccess(this)
			}
		} else {
            // New code start here (remove the "data inside the quotes")
			forgotPassError(this,"");
            // New code end here
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

document.querySelector("#forgotUserConfPassword").addEventListener("blur", function (evt) {
    CheckPasswordMatch(forgotPass, forgotConfPass);
})


$('#forgotUserConfPassword').on('keyup', function () {
	if ($('#forgotUserPassword').val() == $('#forgotUserConfPassword').val()) {
	forgotPassSuccess(this)
	} else 
	forgotPassError(this, "Password do not match")
});

document.querySelector("#forgotUserConfPassword").addEventListener("keydown", function(evt) {
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
	if ($('#forgotUserPassword').val() !== $('#forgotUserConfPassword').val()) {
		// forgotPassError(confPass, "Password do not match")
        const formFiled = document.querySelector("#forgotUserConfPassword").parentElement;
        formFiled.className = "col-12 form_field error";
        const small = formFiled.querySelector("small");
        small.innerHTML = "Password not matched";
        formFiled.querySelector(":nth-child(2)").className = "form-control is-required border border-danger";
        matchResult = false;
	} else {
		const formFiled = document.querySelector("#forgotUserConfPassword").parentElement;
        formFiled.className = "col-12 form_field success";
        const small = formFiled.querySelector("small");
        small.innerHTML = "";
        formFiled.querySelector(":nth-child(2)").className = "form-control is-required border border-success";
        matchResult = true;
	}
};

// Change Password Show Passwords
function forgotPassShowCall() {
	var password = document.querySelector("#forgotUserPassword");
	var confirmPassword = document.querySelector("#forgotUserConfPassword");
	if (password.type === "password" && confirmPassword.type === "password") {
	  password.type = "text";
	  confirmPassword.type = "text";
	} else {
	  password.type = "password";
	  confirmPassword.type = "password";
	}
}

$(".forgotUserClose").click(function() {
	$('#forgotUserPasswordModalToggle').modal('hide')
})

// Update Password Button Enable Disable
$('#forgotUserPassword, #forgotUserConfPassword').bind('keyup, change', function() {
	if(allFilled()) {
        $('#forgotUserPasswordSubmitBtn').removeAttr('disabled')
    } else {
        $('#forgotUserPasswordSubmitBtn').attr('enabled')
    }
});
  
function allFilled() {
	var filled = true;
	$('.isRequired').each(function() {
		if($(this).val() == '') filled = false;
	});
	return filled;
}

// New code start here (I removed addEventListener and added function name what i given for button)
function userForgotPasswordForm(evt) {
    // (remove the evt.preventDefault())
    // evt.preventDefault();
    // New code end here
    const passw = document.querySelector("#forgotUserPassword").value;
    const confPassw = document.querySelector("#forgotUserConfPassword").value;
    CheckPasswordMatch(passw, confPassw);
    if(matchResult === true) {
        $('#forgotUserSuccessModalToggle').modal('show');
        $(".isRequired").removeClass("border-success");
        $(".col-12 form_field").removeClass("success");
        // Modal will close automatically after 3 seconds
		setTimeout(function() {$('#forgotUserSuccessModalToggle').modal('hide');}, 3000);
        $('#forgotUserPasswordModalToggle').modal('hide')
        // clear the data form inputs and errors
        document.querySelectorAll(".isRequired").value = "";
        document.querySelectorAll(".forgotErrMsg").value = "";
         // New code start here 
         encrypt();
         document.querySelector("#forgotUserPasswordForm").submit();
         // New code end here
    } else {
        console.log("password not match")
    }
}


// New code start here
function encrypt() {
    var pass=document.getElementById('forgotUserPassword').value;
    var confPass=document.getElementById('forgotUserConfPassword').value;
    var passhide=document.getElementById('passhide').value;
    var confPasshide=document.getElementById('confPasshide').value;

    if(pass=="") {
        document.getElementById('err').innerHTML='Error:Password is missing';
        return false;
    } else {
        document.getElementById("passhide").value = document.getElementById("forgotUserPassword").value;
        var hashPass = CryptoJS.MD5(pass);
        document.getElementById('forgotUserPassword').value=passhide;

        document.getElementById("confPasshide").value = document.getElementById("forgotUserConfPassword").value;
        var hashPass = CryptoJS.MD5(confPass);
        document.getElementById('forgotUserConfPassword').value=confPasshide;
        return true;
    }
}
// New code end here

// Forgot Password Call
document.querySelector("#forgotPasswordBtn").addEventListener("click", function (evt) {
    // clear the data form inputs and errors
    document.querySelectorAll(".isRequired").value = "";
    document.querySelectorAll(".forgotErrMsg").value = "";
})

//Show input error messages
const userShowError = (input, message) => {
    const formFiled = input.parentElement;
    formFiled.className = "col-md-12 form_field error";
    const small = formFiled.querySelector("small");
    small.innerHTML = message;
    formFiled.querySelector(":nth-child(1)").className = "form-control is-required border border-danger";
};
  
//Show input success
 const userShowSuccess = (input) => {
    const formFiled = input.parentElement;
    formFiled.className = "col-md-12 form_field success";
    formFiled.querySelector(":nth-child(1)").className = "form-control is-required border border-success";
};

// Remember Me
const rmCheck = document.querySelector("#rememberMe");

rmCheck.addEventListener("change", function(evt) {
    if(rmCheck.checked == true) {
        rememberMe();
    }
})

// console.log(localStorage.getItem("loginUser"))

function rememberMe() {
    localStorage.setItem("addLoginUser", loginUser.value);
    localStorage.setItem("addLoginPass", logiPassword.value);                    
    
}

window.onload = checkUser;

function checkUser(){
    if(localStorage.getItem("loginUser") !== "") {
      document.querySelector("#adminLoginName").value = localStorage.getItem("addLoginUser");
      document.querySelector("#adminLoginPassword").value = localStorage.getItem("addLoginPass");
    } 
    else {
        document.querySelector("#adminLoginName").value = "";
        document.querySelector("#adminLoginPassword").value = "";
        document.querySelector("#adminLoginName").focus();
    }
};


// New code start here
function rememberUser() {
    localStorage.setItem("addLoginUser", loginUser.value);
}
// New code end here