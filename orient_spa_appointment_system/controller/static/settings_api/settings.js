function Spinner(){
    let spinner = `
                     <div style="display: flex; justify-content: center; margin-top: 20rem; overflow: hidden;">
                        <div class="text-center">
                            <div class="spinner-border text-light" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <h5 class="text-light" id="spinner_note">Updating Account.....</h5>
                        </div>
                        <button type="button" id="closeModal" class="btn btn-secondary" hidden data-mdb-dismiss="modal">Close</button>
                    </div>
                    ` 
    document.getElementById('Modal').innerHTML = spinner;
}

function renderAccountSettings(request){
    fetch('/controller/settings_view/?req='+request)
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text()
    })
    .then((html) => {
        document.getElementById('settings_content').innerHTML = html;
    })
    .catch(error => {
        console.error('api error: ', error)
        alert('Unstable internet connection.')
    })
}

function navSettings(param){
    renderAccountSettings(param.id)
}

function returnBtn(){
    location.href = '/client_view/settings/'
}

class settings{
    constructor(data_obj){
        this.data_obj = data_obj
    }

    update_user(){
        document.getElementById('spinnerTrigger').click()
        fetch('/controller/updateAccount/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.data_obj)
        })
        .then(respnse => respnse.json())
        .then(data => {
            if(data['msg'] === 200){
                delSession()
            }else{
                alert(data['msg'])
                setTimeout(function(){
                    document.getElementById('closeModal').click()
                },1000)
            }
        })
        .catch(error => {
            console.error('api error: ', error)
            alert('Something went wrong! Please try again.')
        })
    }

    delete_account(){
        document.getElementById('spinnerTrigger').click()

        fetch('/controller/delete_account/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.data_obj)
        })
        .then(respnse => respnse.json())
        .then(data => {
            if(data['msg'] === 200){
                delSession()
            }else{
                alert(data['msg'])
                setTimeout(function(){
                    document.getElementById('closeModal').click()
                },1000)
            }
        })
        .catch(error => {
            console.error('api error: ', error)
            alert('Something went wrong! Please try again.')
        })
    }

    forgot_pass_email(){
        document.getElementById('spinnerTrigger').click()

        fetch('/controller/send_change_pass_link/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.data_obj)
        })
        .then(respnse => respnse.json())
        .then(data => {
            if(data['msg'] === 200){
                ShowCodeModal()
            }else{
                alert(data['msg'])
                setTimeout(function(){
                    document.getElementById('closeModal').click()
                },1000)
            }
        })
        .catch(error => {
            console.error('api error: ', error)
            alert('Something went wrong! Please try again.')
        })
    }

    change_password_function(){
        document.getElementById('spinnerTrigger').click()

        fetch('/controller/update_user_password/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.data_obj)
        })
        .then(respnse => respnse.json())
        .then(data => {
            if(data['msg'] === 200){
                setTimeout(function(){
                    document.getElementById('errmsg').classList.add('text-success')
                    document.getElementById('errmsg').classList.remove('text-danger')
                    document.getElementById('errmsg').innerHTML = 'Password updated!'
                    document.getElementById('closeModal').click()
                },1000)
            }else{
                setTimeout(function(){
                    document.getElementById('errmsg').innerHTML = data['msg']
                    document.getElementById('closeModal').click()
                },1000)
            }
        })
        .catch(error => {
            console.error('api error: ', error)
            alert('Something went wrong! Please try again.')
        })
    }
}

function updateAccount(){
    let f_name = document.getElementById('f_name')
    let l_name = document.getElementById('l_name')
    let email = document.getElementById('email')
    let pass = document.getElementById('pass')
    let cpass = document.getElementById('cpass')

    let obj = {
        'f_name' : f_name.value,
        'l_name' : l_name.value,
        'email' : email.value,
        'new_pass' : pass.value,
        'c_pass' : cpass.value
    }

    if (f_name.value === '' && l_name.value === '' && email.value === ''){
        alert('Please complete all fields')
    }
    else if(pass.value != '' && pass.value.length < 8){
        alert('Password requires 8 characters.')
    }
    else{
        const user_update = new settings(obj)
        user_update.update_user()
        Spinner()
    }
}

function showPass(){
    let checkbox = document.getElementById('flexCheckDefault')
    let pass = document.getElementById('pass')
    let cpass = document.getElementById('cpass')

    if(checkbox.checked){
        pass.type = 'text'
        cpass.type = 'text'
    }
    else{
        pass.type = 'password'
        cpass.type = 'password'
    }
}

function deleteAccountValidation(){
    let admin_pass = document.getElementById('admin_password').value

    if (admin_pass === ''){
        alert('Please input your password')
    }
    else{
        let data = {
            'admin_pass' : admin_pass
        }
        const _delete = new settings(data)
        _delete.delete_account()
        Spinner()
    }
}

function verifyEmail(){
    let email = document.getElementById('verification_email').value

    if (email == ''){
        alert('Please input your email.')
    }
    else{
        let obj = {
            'email' : email
        }
        const send_email = new settings(obj)
        send_email.forgot_pass_email()
        Spinner()
        document.getElementById('spinner_note').innerHTML = 'Verifying email....'
    }
}

function updatePassword(email){
    let pass = document.getElementById('pass').value
    let cpass = document.getElementById('cpass').value

    if (pass === '' && cpass === ''){
        document.getElementById('errmsg').innerHTML = 'Please complete all fields'
    }
    else if (pass !== cpass){
        document.getElementById('errmsg').innerHTML = 'Passwords dont Match'
    }
    else if (pass.length < 8){
        document.getElementById('errmsg').innerHTML = 'Password require 8 characters'
    }
    else{
        let obj = {
            'email': email,
            'new_pass' : pass
        }
        const update_pass = new settings(obj)
        update_pass.change_password_function()
        Spinner()
        document.getElementById('spinner_note').innerHTML = 'Updating Password....'
    }
}

function ShowCodeModal(){
    let modal = `<div class="modal-dialog">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel"></h5>
                            <button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                                <h5 class="modal-title">
                                <i class="fas fa-check-double text-success"></i>
                                Change password link was sent to your email.
                                </h5>
                        </div>
                        <div class="modal-footer">
                            <button type="button" id="closeModal" class="btn btn-secondary" data-mdb-dismiss="modal">Close</button>
                        </div>
                        </div>
                    </div>`;

    document.getElementById('Modal').innerHTML = modal;
}