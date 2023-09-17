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
        alert('Unstable internet connection. Test')
    })
    document.getElementById('closeModal').click()
}

class manageAppointment{
    constructor(object){
        this.object = object
    }
    confirm(){
        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.object)
        })
        .then(response => response.json())
        .then(data => {
            alert(data['msg'])
        })
        .catch(error => {
            console.error('api error: ', error)
            alert('Something went wrong! Please try again.')
        })
    }
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

    alert(JSON.stringify(object))
}