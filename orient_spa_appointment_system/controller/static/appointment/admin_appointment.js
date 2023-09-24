const currentDate = new Date();

const year = currentDate.getFullYear();
const month = currentDate.getMonth() + 1; 

let new_year = year
let new_month = month

window.onload =()=>{
    displayAdminPending()
}

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

function displayAdminDone(){
    fetch('/controller/display_admin_done/?a='+new_month+'&&b='+new_year)
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text()
    })
    .then((html) => {
        document.getElementById('ex-with-icons-tabs-3').innerHTML = html;
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

    displayAdminDone()
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

    done(){
        fetch('/controller/mark_as_done/', {
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

    admin_cancel(){
        Spinner()
        fetch('/controller/cancel_appointment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.object)
        })
        .then(response => response.json())
        .then(data => {
            if(data['msg'] === 200)
                {displayAdminConfirmed()}
                 else{
                    alert(data['msg'])
                 }
        })
        .catch(error => {
            console.error('api error: ', error);
            alert('Network error. Please try again')
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
        'id' : id,
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


function MarkasDone(id){
    const html = `<div class="modal-dialog">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel"></h5>
                            <button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <h5>Mark Appointment as done?</h5>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" id="closeModal" data-mdb-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary" onclick="doneAppointment('${id}')">Done</button>
                        </div>
                        </div>
                    </div>`
    document.getElementById('Modal').innerHTML = html;
}

function doneAppointment(id){
    let object = {
        'id' : id
    }

    const done = new manageAppointment(object)
    done.done()
}

function canceModal(id){
    let modal = `<div class="modal-dialog">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel"></h5>
                            <button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <h4>Please Specify your reason for cancelation</h4>
                            <form id="colorForm">
                                <div class="form-outline">
                                    <textarea class="form-control" style="border: 1px solid gray;" id="textAreaExample" rows="4"></textarea>
                                    <label class="form-label" for="textAreaExample">Reason for Cancelation</label>
                                    <span class="text-danger" id="reasonerr"></span>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" id="closeModal" class="btn btn-secondary" data-mdb-dismiss="modal">Close</button>
                            <button type="button" onclick="adminCancel(${id})" class="btn btn-danger">Submit</button>
                        </div>
                        </div>
                    </div>`;

    document.getElementById('Modal').innerHTML = modal;
}

function adminCancel(id){
    let reason = document.getElementById('textAreaExample').value;

    if (reason === ''){
        document.getElementById('reasonerr').innerHTML = 'Please state your reason.'
    }
    else{
        let obj = {
            'id' : id,
            'reason' : reason,
            'canceled_by' : 'admin'
        }

        const cancel = new manageAppointment(obj)
        cancel.admin_cancel()
    }
}

function printReciept() {
    let receipt = document.getElementById('receipt')
    
    var printWindow = window.open('', '', 'width=600,height=600');
    
    printWindow.document.open();
    printWindow.document.write('');
    printWindow.document.write(`
                                <html><head>
                                <title>Orient SPA Receipt</title>
                                <!-- Font Awesome -->
                                <link
                                href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
                                rel="stylesheet"
                                />
                                <!-- Google Fonts -->
                                <link
                                href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"
                                rel="stylesheet"
                                />
                                <!-- MDB -->
                                <link
                                href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/6.4.1/mdb.min.css"
                                rel="stylesheet"
                                />
                                <script
                                type="text/javascript"
                                src="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/6.4.1/mdb.min.js"
                                ></script>
                                </head><body>
                                <div>
                                   ${receipt.innerHTML}
                                </div>
                                <div style="margin-top: 10%; margin-left: 80%;">Signed by: ___________________</div>
                                </body></html>
                                `);
    printWindow.document.write('');
    printWindow.document.close();
    
    printWindow.print();
    printWindow.close();
}