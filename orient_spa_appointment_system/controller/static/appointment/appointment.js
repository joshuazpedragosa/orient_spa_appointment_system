const currentDate = new Date();

const year = currentDate.getFullYear();
const month = currentDate.getMonth() + 1; 

let new_year = year
let new_month = month

document.getElementById('dateInput').value = year

function Spinner(){
    let spinner = `
                     <div style="display: flex; justify-content: center; margin-top: 20rem; overflow: hidden;">
                        <div class="spinner-border text-light" role="status">
                             <span class="visually-hidden">Loading...</span>
                        </div>
                        <button type="button" id="closeModal" class="btn btn-secondary" hidden data-mdb-dismiss="modal">Close</button>
                    </div>
                    ` 
    document.getElementById('Modal').innerHTML = spinner;
}

class appointment{
    constructor(objects){
        this.objects = objects
    }

    save(){
        fetch('/controller/save_appointment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.objects)
        })
        .then(response => response.json())
        .then(data => {
             data['msg'] === 200 ? displayPending() : alert(data['msg'])
        })
        .catch(error => {
            console.error('api error: ', error);
        })
        // alert(JSON.stringify(this.objects))
    }

    cancel(){
        fetch('/controller/cancel_appointment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.objects)
        })
        .then(response => response.json())
        .then(data => {
             data['msg'] === 200 ? displayPending() : null
        })
        .catch(error => {
            console.error('api error: ', error);
        })
    }

    rating(){
        fetch('/controller/save_rating/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.objects)
        })
        .then(response => response.json())
        .then(data => {
             data['msg'] === 200 ? displayDone() : null
        })
        .catch(error => {
            console.error('api error: ', error);
            alert('Something went wrong.')
        })
    }
}

function saveAppointment(){
    let phone_num = document.getElementById('client_phone_number').value
    let splitted_num = phone_num.split('')

    if (phone_num.length !== 11){
        alert('Phone number is not valid.')
        return false;
    }

    for(let x = 0; x < phone_num.length; x++){
        if (isNaN(splitted_num[x])){
            console.log('Phone number dont require letters or any special characters.')
            break;
        }
    }

    let _str_num = phone_num.toString()
    let phone_number ='+63' + _str_num.substring(1)

    let appointment_data = {
        'phone_number' : phone_number,
        'date' : document.getElementById('appointmentDate').value,
        'time' : document.getElementById('time').value,
        'service' : document.getElementById('services').value
    }

    if(appointment_data.phone_number === '' || appointment_data.date === '' || appointment_data.time === '' || appointment_data.service === ''){
        alert('Please fillout the details')
    }
    else if(new Date() >  new Date(appointment_data.date)){
        alert('Date is not available')
    }
    else{
        const new_appointment = new appointment(appointment_data)
        new_appointment.save()
        // alert(JSON.stringify(appointment_data))
    }
}

function warningModal(id){
    let modal_warning = `<div class="modal-dialog">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel"></h5>
                            <button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <h4>Please Specify your reason for cancelation</h4>
                            <form id="colorForm">
                                <label for="red">
                                    <input type="radio" name="reason" value="I change my mind"> I change my mind
                                </label><br>
                                <label for="blue">
                                    <input type="radio" name="reason" value="I want to change the date and time"> I want to change the date and time
                                </label><br>
                                <label for="green">
                                    <input type="radio"  name="reason" value="I want to change my phone number"> I want to change my phone number
                                </label><br>
                                <label for="yellow">
                                    <input type="radio"  name="reason" value="I want to change the service"> I want to change the service
                                </label><br>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" id="closeModal" class="btn btn-secondary" data-mdb-dismiss="modal">Close</button>
                            <button type="button" onclick="cancelAppointment(${id})" class="btn btn-danger">Submit</button>
                        </div>
                        </div>
                    </div>`;

    document.getElementById('Modal').innerHTML = modal_warning;
}

function cancelAppointment(id){
    var selected = document.querySelector('input[name="reason"]:checked');

    let object = {
        id : id,
        reason : selected.value
    }

    if (selected) {
        let cancel = new appointment(object)
        cancel.cancel()
        Spinner()
    } else {
        alert("Please state your reason");
    }
}

window.onload = () =>{
    displayPending()
    displayCanceled()
}

function displayPending(){
    fetch('/controller/pending_appointments/')
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text()
    })
    .then((html) => {
        document.getElementById('pending').innerHTML = html;
    })
    .catch(error => {
        console.error('api error: ', error)
        alert('Unstable internet connection.')
    })
    document.getElementById('closeModal').click()
}

function displayCanceled(){
    fetch('/controller/canceled_appointments/?a='+new_month+'&&b='+new_year)
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text()
    })
    .then((html) => {
        document.getElementById('canceled').innerHTML = html;
    })
    .catch(error => {
        console.error('api error: ', error)
        alert('Unstable internet connection.')
    })
}

function displayConfirmed(){
    fetch('/controller/display_confirmed_appointment/')
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text()
    })
    .then((html) => {
        document.getElementById('ex1-tabs-2').innerHTML = html;
    })
    .catch(error => {
        console.error('api error: ', error)
        alert('Unstable internet connection.')
    })
}

function displayDone(){
    fetch('/controller/display_done_appointment/?a='+new_month+'&&b='+new_year)
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text()
    })
    .then((html) => {
        document.getElementById('ex1-tabs-4').innerHTML = html;
    })
    .catch(error => {
        console.error('api error: ', error)
        alert('Unstable internet connection.')
    })
    document.getElementById('closeModal').click()
}

function selectDate(){
    new_year = document.getElementById('dateInput').value;
    new_month = document.getElementById('monthSelect').value;

    displayCanceled()
    displayDone()
}