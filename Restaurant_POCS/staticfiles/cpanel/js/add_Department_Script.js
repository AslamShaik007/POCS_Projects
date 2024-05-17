console.log("add department script is loading")

const addNewDeptForm = document.querySelector("#addNewDepartmentForm");

// Delete Table rows
$('#deptTable').on('click', 'td>a.deleteRowButton', function(e) {
    $(this).parents('tr').first().remove();
});

// Mouse Hand Pointer for Delete Button
$('.deleteRowButton').css({'cursor':'pointer'});

// Delete Role Text boxes
$(".delSubDeptName").on('click', function(e) {
    $(this).parent().parent().remove();
})

// Add and Remove New Role Textboxes 
$("#addNewRoleNameBtn").click(function () {
    $("#roleContainer").append(`<div class="roleFormField position-relative"><input type="text" class="form-control addNewRoleName" name="addNewRoleName" placeholder="Role" /><div class="actionPart position-absolute"><span class="text-danger delSubDeptName mx-1" onclick="$('.delSubDeptName').on('click', function(e) {$(this).parent().parent().remove();})">X</span></div></div>`);
});

function addNewDepartmentForm(evt) {
    evt.preventDefault();
    const newDeptName = document.querySelector("#newDeptNameInput").value;
    const newSubDeptName = document.querySelector("#addNewSubDeptNameInput").value;
    var elements = document.getElementsByClassName("addNewRoleName");

    let tableRow = $('#deptTable tr').length;
    
    // Department New Data
    for(let i = 0; i < elements.length; i++) {
        if(newDeptName !== "" && elements[i].value !== ""){
            $('#deptTable > tbody:last-child').append(`
                <tr>
                    <td>${tableRow + i}</td>
                    <td>${newDeptName}</td>
                    <td>${newSubDeptName}</td>
                    <td>${elements[i].value} </td>
                    <td> `+ `<a href="" data-bs-toggle="modal" data-bs-target="#editDepartmentModal"><img src="images/edit.png"></a><a class="ms-3 deleteRowButton" onclick="$('#deptTable').on('click', 'td>a.deleteRowButton', function(e) {$(this).parents('tr').first().remove();});"><img src="images/delete.png"></a>` + `</td>
                </tr>
            `);
            $("#addDepartmentModal").modal("hide");
            $("#addDeptSuccessModalToggle").modal("show");
            setTimeout(function() {$('#addDeptSuccessModalToggle').modal('hide');}, 3000);
        } else if(newDeptName !== "" && elements[i].value == ""){
            document.querySelector("#addDept_Role_Err").style.display = "block";
            document.querySelector("#addDept_Role_Err").className = "cust_err text-danger";
            document.querySelector("#addDept_Role_Err").innerHTML = "Role should not be empty";
        } else if(newDeptName == "" && elements[i].value !== ""){
            document.querySelector("#addDept_Name_Err").style.display = "block";
            document.querySelector("#addDept_Name_Err").className = "cust_err text-danger";
            document.querySelector("#addDept_Name_Err").innerHTML = "Department should not be empty";
        } else {
            document.querySelector("#addDept_Name_Err").style.display = "block";
            document.querySelector("#addDept_Name_Err").className = "cust_err text-danger";
            document.querySelector("#addDept_Name_Err").innerHTML = "Department should not be empty";

            document.querySelector("#addDept_Role_Err").style.display = "block";
            document.querySelector("#addDept_Role_Err").className = "cust_err text-danger";
            document.querySelector("#addDept_Role_Err").innerHTML = "Role should not be empty";
        }
    }
}

document.querySelector("#newDeptNameInput").addEventListener("keydown", function(evt) {
    var charCode = evt.keyCode || evt.which;
    if(charCode == 37 || charCode == 39 || charCode == 46 || charCode == 8 || charCode == 16 || charCode == 36 || charCode == 35) {
        return true;
    }
    
    if((evt.which >= 48 && evt.which <=57) || (evt.which >= 96 && evt.which <= 105)) {
        evt.preventDefault();
        document.querySelector("#addDept_Name_Err").style.display = "block";
        document.querySelector("#addDept_Name_Err").innerHTML = "Numbers or not allowed"
        document.querySelector("#addDept_Name_Err").className = "cust_err text-danger";
        return false;
    } else if(!(/[a-zA-Z\t ]|[\b]/i.test(String.fromCharCode(evt.keyCode)))){
        evt.preventDefault();
        document.querySelector("#addDept_Name_Err").style.display = "block";
        document.querySelector("#addDept_Name_Err").innerHTML = "Numbers or not allowed"
        document.querySelector("#addDept_Name_Err").className = "cust_err text-danger";
        return false;
    } 
    
    if(evt.which === 32 && this.value.length === 0) {
		evt.preventDefault();
        document.querySelector("#addDept_Name_Err").style.display = "block";
        document.querySelector("#addDept_Name_Err").innerHTML = "Space not Allowed"
        document.querySelector("#addDept_Name_Err").className = "cust_err text-danger";
		return false;
	} else {
		this.value = this.value.replace(/\s+/g, ' ');
		document.querySelector("#addDept_Name_Err").innerHTML = ""
        document.querySelector("#addDept_Name_Err").style.display = "none";
	}
})

document.querySelector("#newDeptNameInput").addEventListener("blur", function(evt) {
    if(this.value.length !== 0) {
        this.value = this.value.trim();
    } else {
        document.querySelector("#addDept_Name_Err").innerHTML = "Department should not be empty"
        document.querySelector("#addDept_Name_Err").style.display = "block";
        document.querySelector("#addDept_Name_Err").className = "cust_err text-danger";
    }
    
})

document.querySelector("#addNewSubDeptNameInput").addEventListener("keydown", function (evt) {
    var charCode = evt.keyCode || evt.which;
    if(charCode == 37 || charCode == 39 || charCode == 46 || charCode == 8 || charCode == 16 || charCode == 36 || charCode == 35) {
        return true;
    }

    if((evt.which >= 48 && evt.which <=57) || (evt.which >= 96 && evt.which <= 105)) {
        evt.preventDefault();
        document.querySelector("#addDept_subDeptName_Err").style.display = "block";
        document.querySelector("#addDept_subDeptName_Err").innerHTML = "Numbers are not allowed"
        document.querySelector("#addDept_subDeptName_Err").className = "cust_err text-danger";
        return false;
    } else if(!(/[a-zA-Z\t ]|[\b]/i.test(String.fromCharCode(evt.keyCode)))){
        evt.preventDefault();
        document.querySelector("#addDept_subDeptName_Err").style.display = "block";
        document.querySelector("#addDept_subDeptName_Err").innerHTML = "Numbers are not allowed"
        document.querySelector("#addDept_subDeptName_Err").className = "cust_err text-danger";
        return false;
    } else {
        document.querySelector("#addDept_subDeptName_Err").style.display = "none";
        document.querySelector("#addDept_subDeptName_Err").innerHTML = ""
        document.querySelector("#addDept_subDeptName_Err").className = "cust_err";
    }

    if(evt.which === 32 && this.value.length === 0) {
        evt.preventDefault();
        document.querySelector("#addDept_subDeptName_Err").style.display = "block";
        document.querySelector("#addDept_subDeptName_Err").innerHTML = "Space not Allowed"
        document.querySelector("#addDept_subDeptName_Err").className = "cust_err text-danger";
        return false;
    } else {
        this.value = this.value.replace(/\s+/g, ' ');
		document.querySelector("#addDept_subDeptName_Err").innerHTML = ""
        document.querySelector("#addDept_subDeptName_Err").style.display = "none";
        document.querySelector("#addDept_subDeptName_Err").className = "cust_err";
    }
})

document.querySelector("#addNewSubDeptNameInput").addEventListener("blur", function(evt) {
    if(this.value.length !== 0)
    this.value = this.value.trim();
})

var allRoleNames = document.getElementsByClassName("addNewRoleName");

Array.from(allRoleNames).forEach(function(element) {
    element.addEventListener('keydown', myAllRoleCheck);
});

Array.from(allRoleNames).forEach(function(element) {
    element.addEventListener('blur', removeWhiteSpace);
});

function removeWhiteSpace(evt) {
    if(this.value.length !== 0) {
        this.value = this.value.trim();    
    } else {
        document.querySelector("#addDept_Role_Err").style.display = "block";
        document.querySelector("#addDept_Role_Err").innerHTML = "Role should not be empty"
        document.querySelector("#addDept_Role_Err").className = "cust_err text-danger";
    }
    
}

// var allRoleCheck = function(evt) {
function myAllRoleCheck(evt) {
    var charCode = evt.keyCode || evt.which;
    if(charCode == 37 || charCode == 39 || charCode == 46 || charCode == 8 || charCode == 16 || charCode == 36 || charCode == 35) {
        return true;
    }

    if((evt.which >= 48 && evt.which <=57) || (evt.which >= 96 && evt.which <= 105)) {
        evt.preventDefault()
        document.querySelector("#addDept_Role_Err").style.display = "block";
        document.querySelector("#addDept_Role_Err").innerHTML = "Numbers are not allowed"
        document.querySelector("#addDept_Role_Err").className = "cust_err text-danger";
        return false;
    } else if(!(/[a-zA-Z\t ]|[\b]/i.test(String.fromCharCode(evt.keyCode)))){
        evt.preventDefault()
        document.querySelector("#addDept_Role_Err").style.display = "block";
        document.querySelector("#addDept_Role_Err").innerHTML = "Numbers are not allowed"
        document.querySelector("#addDept_Role_Err").className = "cust_err text-danger";
        return false;
    }
    if(evt.which === 32 && this.value.length === 0) {
        evt.preventDefault()
        document.querySelector("#addDept_Role_Err").style.display = "block";
        document.querySelector("#addDept_Role_Err").innerHTML = "Space not Allowed"
        document.querySelector("#addDept_Role_Err").className = "cust_err text-danger";
    } else {
        this.value = this.value.replace(/\s+/g, ' ');
		document.querySelector("#addDept_Role_Err").innerHTML = ""
        document.querySelector("#addDept_Role_Err").style.display = "none";
        document.querySelector("#addDept_Role_Err").className = "cust_err";
    }
}

$(document).ready(function() {});