const signin = document.getElementById('signup')
const code1 = document.getElementById('code1')
const code2 = document.getElementById('code2')
const code3 = document.getElementById('code3')
const code4 = document.getElementById('code4')
const numericRegex = /^[0-9]+$/;


function showAlert(key){
    document.getElementById('alert').innerHTML = `<div class="alert alert-danger">${key}</div>`
}

function showAlertSuccess(key){
    document.getElementById('alert').innerHTML = `<div class="alert alert-success">${key}<a href="#" onclick="location.href='/auth'">Login your account</a></div>`
}

class authentication{
    constructor(objectData){
        this.objectData = objectData
    }

    validate(){
        let not_valid = true;

        for (const key in this.objectData) {
            if (this.objectData.hasOwnProperty(key)) {
              const value = this.objectData[key].trim();
              if (value === '') {
                  showAlert('Please Fillout all fields!')
                  not_valid = false;
              }
            }
          }
          
          not_valid ? this.signup() : null
    }
                
                verifyCode(){
                    fetch('/controller/verify_account/',{
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(this.objectData)
                    })
                    .then(respose => respose.json())
                    .then(data => {
                        data['msg'] === 200 ?  showAlertSuccess('Account Verified!') : showAlert(data['msg'])
                    })
                    .catch(error => {
                        console.error('api error: ',error)
                    })
                }

                 signup(){
                    document.getElementById('signup').style.display='none'
                    document.getElementById('btnSpinner').style.display='block'
                    fetch('/controller/signup/',{
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(this.objectData)
                    })
                    .then(respose => respose.json())
                    .then(data => {
                        data['msg'] === 200 ? location.href='/verification/?email='+data['email'] : showAlert(data['msg'])
                    })
                    .catch(error => {
                        console.error('api error: ',error)
                    })
                 }

                 signin(){
                    document.getElementById('loginBtn').style.display='none'
                    document.getElementById('btnSpinnerLogin').style.display='block'
                    fetch('/controller/signin/',{
                        method: 'POST',
                        headers : {
                            'Content-Type': 'application/json'
                        }, 
                        body: JSON.stringify(this.objectData)
                    })
                    .then(response => response.json())
                    .then(data => {
                        setTimeout(function(){
                            if(data['msg'] === 200){
                                location.href = '/client_view/'
                            }
                            else if(data['msg'] === 400){
                                location.href='/verification/?email='+data['email']
                            }
                            document.getElementById('alertLogin').innerHTML = `<div class="alert alert-danger">${data['msg']}</div>`
                            document.getElementById('loginBtn').style.display='block'
                            document.getElementById('btnSpinnerLogin').style.display='none'
                        }, 2000)
                    })
                    .catch(error => {
                        document.getElementById('alertLogin').innerHTML = `<div class="alert alert-danger">Something went wrong. Please check your internet connection</div>`
                        console.error('api error: ', error)
                    })
                 }
}

signin.addEventListener('click', function(event){
    event.preventDefault()

    let object = {
        'f_name' : document.getElementById('f_name').value,
        'l_name' : document.getElementById('l_name').value,
        'email' : document.getElementById('email').value,
        'password' : document.getElementById('pass').value,
        'c_password' : document.getElementById('c_pass').value,
        'priv' : '2'
    }

    let auth = new authentication(object)
    auth.validate();
})

function navSignup(){
    document.getElementById('tab-register').click()
}

function navLogin(){
    document.getElementById('tab-login').click()
}

function loginAcc(){
    let credentials = {
        email : document.getElementById('emailLogin').value,
        password: document.getElementById('Loginpassword').value
    }

    if(credentials.email === ''){
        document.getElementById('alertLogin').innerHTML = `<div class="alert alert-danger">Email is required!</div>`
        return false
    }
    else if(credentials.password === ''){
        document.getElementById('alertLogin').innerHTML = `<div class="alert alert-danger">Password is required!</div>`
        return false
    }

    let login_auth = new authentication(credentials)
    login_auth.signin()
}

function Code1(val){
    if(!numericRegex.test(val)){
       code1.value = val.replace(/[^0-9]/g, '')
    }
    else if(numericRegex.test(val) && code1.value !== ''){
        code2.focus()
    }
}

function Code2(val){
    if(!numericRegex.test(val)){
       code2.value = val.replace(/[^0-9]/g, '')
    }
    else if(numericRegex.test(val) && code2.value !== ''){
        code3.focus()
    }
}

function Code3(val){
    if(!numericRegex.test(val)){
       code3.value = val.replace(/[^0-9]/g, '')
    }
    else if(numericRegex.test(val) && code3.value !== ''){
        code4.focus()
    }
}

function Code4(val){
    if(!numericRegex.test(val)){
       code4.value = val.replace(/[^0-9]/g, '')
    }
}

function submitCode(email){
     let code = {
        v_code : code1.value+code2.value+code3.value+code4.value,
        email : email
     }

     const submit = new authentication(code)
     submit.verifyCode()
}