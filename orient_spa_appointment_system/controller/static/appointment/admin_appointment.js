window.onload =()=>{
    displayAdminPending()
}

function displayAdminPending(){
    fetch('/controller/display_admin_pending/')
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text()
    })
    .then((html) => {
        document.getElementById('AdminPending').innerHTML = html;
    })
    .catch(error => {
        console.error('api error: ', error)
        alert('Unstable internet connection.')
    })
    document.getElementById('closeModal').click()
    displayAdminConfirmed()
}

function displayAdminConfirmed(){
    fetch('/controller/display_admin_scheduled/')
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text()
    })
    .then((html) => {
        document.getElementById('ex-with-icons-tabs-2').innerHTML = html;
    })
    .catch(error => {
        console.error('api error: ', error)
        alert('Unstable internet connection.')
    })
    document.getElementById('closeModal').click()
}

function paymentModal(id){
    fetch('/controller/payment_modal/?id='+id)
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text()
    })
    .then((html) => {
        document.getElementById('Modal').innerHTML = html;
    })
    .catch(error => {
        console.error('api error: ', error)
        alert('Unstable internet connection.')
    })
}

class manageAppointment{
    constructor(object){
        this.object = object
    }
    confirm(){
        fetch('/controller/confirm_appointment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.object)
        })
        .then(response => response.json())
        .then(data => {
           if (data['msg'] == 200) { 
            displayAdminPending()
            this.notif()
            } else { alert(data['msg'])}
        })
        .catch(error => {
            console.error('api error: ', error)
            alert('Something went wrong! Please try again.')
        })
    }

    confirm_payment(){
        fetch('/controller/confirm_payment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.object)
        })
        .then(response => response.json())
        .then(data => {
           if (data['msg'] == 200) { 
            displayAdminConfirmed()
            } else { alert(data['msg'])}
        })
        .catch(error => {
            console.error('api error: ', error)
            alert('Something went wrong! Please try again.')
        })
    }

    notif(){
        fetch('/controller/notif/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.object)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
        })
        .catch(error => {
            console.error(error)
        })
    }

}

function confirmPayment(id){
    let id_obj = {
        'id' : id
    }
    const pay = new manageAppointment(id_obj)
    pay.confirm_payment()
}

function showModalAvailable(id){
    fetch('/controller/display_available_employee/?id='+id)
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text()
    })
    .then((html) => {
        document.getElementById('Modal').innerHTML = html;
    })
    .catch(error => {
        console.error('api error: ', error)
        alert('Unstable internet connection.')
    })
}

function ConfirmAppointment(id){
    let selected = document.querySelector('input[id="employee"]:checked')
    let object = {
        'app_id' : id,
        'employee' : selected.value
    }

    const confirm_app = new manageAppointment(object)
    confirm_app.confirm()
}