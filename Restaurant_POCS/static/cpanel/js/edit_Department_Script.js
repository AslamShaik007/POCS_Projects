console.log("edit department script is loading");

function editDepartmentForm(evt) {
    evt.preventDefault();

    // Get the value from form
    const editDeptName = document.querySelector("#editDeptNameInput").value;
    const editSubDeptName = document.querySelector("#editSubDeptNameInput").value;
    const editRole = document.querySelector(".editRoleName").value;

    if(editDeptName !== "" && editRole !== "") {
        $("#editDepartmentModal").modal("hide");
        $("#updatedDeptSuccessModalToggle").modal("show");
        setTimeout(function() {$('#updatedDeptSuccessModalToggle').modal('hide');}, 3000);
    } else if(editDeptName !== "" && editRole == "") {
        document.querySelector("#editDept_Role_Err").style.display = "block";
        document.querySelector("#editDept_Role_Err").innerHTML = "Role should not be empty";
        document.querySelector("#editDept_Role_Err").className = "cust_err text-danger";
    } else if(editDeptName == "" && editRole !== "") {
        document.querySelector("#editDept_Name_Err").style.display = 'block';
        document.querySelector("#editDept_Name_Err").innerHTML = "Department should not be empty";
        document.querySelector("#editDept_Name_Err").className = "cust_err text-danger";
    } else {
        document.querySelector("#editDept_Name_Err").style.display = 'block';
        document.querySelector("#editDept_Name_Err").innerHTML = "Department should not be empty";
        document.querySelector("#editDept_Name_Err").className = "cust_err text-danger";

        document.querySelector("#editDept_Role_Err").style.display = "block";
        document.querySelector("#editDept_Role_Err").innerHTML = "Role should not be empty";
        document.querySelector("#editDept_Role_Err").className = "cust_err text-danger";
    }
    console.log("submit is called")
}

// Department Name
document.querySelector("#editDeptNameInput").addEventListener("keydown", function (evt) {
    var charCode = evt.keyCode || evt.which;
    if(charCode == 37 || charCode == 39 || charCode == 46 || charCode == 8 || charCode == 16 || charCode == 36 || charCode == 35) {
        return true;
    }
    
    if((evt.which >= 48 && evt.which <= 57) || (evt.which >= 96 && evt.which <= 105)) {
        evt.preventDefault();
        document.querySelector("#editDept_Name_Err").style.display = 'block';
        document.querySelector("#editDept_Name_Err").innerHTML = "Numbers are not allowed";
        document.querySelector("#editDept_Name_Err").className = "cust_err text-danger";
        return false;
    } else if(!(/[a-zA-Z\t ]|[\b]/i.test(String.fromCharCode(evt.keyCode)))) {
        evt.preventDefault();
        document.querySelector("#editDept_Name_Err").style.display = 'block';
        document.querySelector("#editDept_Name_Err").innerHTML = "Numbers are not allowed";
        document.querySelector("#editDept_Name_Err").className = "cust_err text-danger";
        return false;
    }

    if(evt.which === 32 && this.value.length === 0) {
        evt.preventDefault();
        document.querySelector("#editDept_Name_Err").style.display = 'block';
        document.querySelector("#editDept_Name_Err").innerHTML = "Space not allowd";
        document.querySelector("#editDept_Name_Err").className = "cust_err text-danger";
        return false;
    } else {
        this.value = this.value.replace(/\s+/g, ' ');
        document.querySelector("#editDept_Name_Err").innerHTML = "";
        document.querySelector("#editDept_Name_Err").style.display = 'none';
    }
})

document.querySelector("#editDeptNameInput").addEventListener("blur", function (evt) {
    if(this.value.length !== 0) {
        this.value = this.value.trim();
    } else {
        document.querySelector("#editDept_Name_Err").style.display = 'block';
        document.querySelector("#editDept_Name_Err").innerHTML = "Department should not be empty";
        document.querySelector("#editDept_Name_Err").className = "cust_err text-danger";
    }
})

document.querySelector("#editSubDeptNameInput").addEventListener("keydown", function (evt) {
    var charCode = evt.keyCode || evt.which;
    if(charCode == 37 || charCode == 39 || charCode == 46 || charCode == 8 || charCode == 16 || charCode == 36 || charCode == 35) {
        return true;
    }

    if((evt.which >= 48 && evt.which <= 57) || (evt.which >= 96 && evt.which <= 105)) {
        evt.preventDefault();
        document.querySelector("#editDept_subDeptName_Err").style.display = "block";
        document.querySelector("#editDept_subDeptName_Err").innerHTML = "Numbers are not allowed";
        document.querySelector("#editDept_subDeptName_Err").className = "cust_err text-danger";
        return false;
    } else if(!(/[a-zA-Z\t ]|[\b]/i.test(String.fromCharCode(evt.keyCode)))) {
        evt.preventDefault();
        document.querySelector("#editDept_subDeptName_Err").style.display = "block";
        document.querySelector("#editDept_subDeptName_Err").innerHTML = "Numbers are not allowed";
        document.querySelector("#editDept_subDeptName_Err").className = "cust_err text-danger";
        return false;
    }

    if(evt.which === 32 && this.value.length === 0) {
        evt.preventDefault();
        document.querySelector("#editDept_subDeptName_Err").style.display = "block";
        document.querySelector("#editDept_subDeptName_Err").innerHTML = "Space not allowed";
        document.querySelector("#editDept_subDeptName_Err").className = "cust_err text-danger";
        return false;
    } else {
        this.value = this.value.replace(/\s+/g, ' ');
        document.querySelector("#editDept_subDeptName_Err").innerHTML = "";
        document.querySelector("#editDept_subDeptName_Err").style.display = "none";
    }
})

document.querySelector("#editSubDeptNameInput").addEventListener("keydown", function (evt) {
    if(this.value.length !== 0) {
        this.value = this.value.trim();
    }
})

document.querySelector(".editRoleName").addEventListener("keydown", function (evt) {
    var charCode = evt.keyCode || evt.which;
    if(charCode == 37 || charCode == 39 || charCode == 46 || charCode == 8 || charCode == 16 || charCode == 36 || charCode == 35) {
        return true;
    }

    if((evt.which >= 48 && evt.which <=57) || (evt.which >= 96 && evt.which <= 105)) {
        evt.preventDefault();
        document.querySelector("#editDept_Role_Err").style.display = "block";
        document.querySelector("#editDept_Role_Err").innerHTML = "Numbers are not allowed";
        document.querySelector("#editDept_Role_Err").className = "cust_err text-danger";
        return false;
    } else if(!(/[a-zA-Z\t ]|[\b]/i.test(String.fromCharCode(evt.keyCode)))) {
        evt.preventDefault();
        document.querySelector("#editDept_Role_Err").style.display = "block";
        document.querySelector("#editDept_Role_Err").innerHTML = "Numbers are not allowed";
        document.querySelector("#editDept_Role_Err").className = "cust_err text-danger";
        return false;
    }

    if(evt.which === 32 && this.value.length === 0) {
        evt.preventDefault();
        document.querySelector("#editDept_Role_Err").style.display = "block";
        document.querySelector("#editDept_Role_Err").innerHTML = "Space not allowed";
        document.querySelector("#editDept_Role_Err").className = "cust_err text-danger";
        return false;
    } else {
        this.value = this.value.replace(/\s+/g, ' ');
        document.querySelector("#editDept_Role_Err").style.display = "none";
        document.querySelector("#editDept_Role_Err").innerHTML = "";
    }
})

document.querySelector(".editRoleName").addEventListener("blur", function (evt) {
    if(this.value.length !== 0) {
        this.value = this.value.trim();
    } else {
        this.value = this.value.trim();
        document.querySelector("#editDept_Role_Err").style.display = "block";
        document.querySelector("#editDept_Role_Err").innerHTML = "Role should not be empty";
        document.querySelector("#editDept_Role_Err").className = "cust_err text-danger";
    }
})

document.querySelector(".editRoleName").addEventListener("keyup", function (evt) {
    if(evt.which === 32) {
        if(this.value.length === 0) {
            evt.preventDefault();
            document.querySelector("#editDept_Role_Err").style.display = "block";
            document.querySelector("#editDept_Role_Err").innerHTML = "Space not allowed";
            document.querySelector("#editDept_Role_Err").className = "cust_err text-danger";
        }
    }
})