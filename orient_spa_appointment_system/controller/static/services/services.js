window.onload =()=>{
    loadServices()
}

function loadServices(){
    fetch('/controller/service_content/')
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text();
    })
    .then((html) => {
         document.getElementById('allServices').innerHTML = html;
    })
    .catch(error => {
        console.error('API Error: ', error)
        alert('Something went wrong!')
    })
    document.getElementById('closeModal').click()
}

let def_rate = 5
let service_id = 0


class services{
    constructor(objects){
        this.objects = objects
    }

    replyComment(){
        fetch('/controller/save_reply/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.objects)
        })
        .then(response => response.json())
        .then(data => {
            data['msg'] == 200 ? sortComments(def_rate) : null
        })
        .catch(error => {
            console.log('api error: ', error)
            alert('Something went wrong.')
        })
        }

    update_availability(){
        fetch('/controller/update_availability/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.objects)
        })
        .then(response => response.json())
        .then(data => {
            data['msg'] == 200 ? loadServices() : null
        })
        .catch(error => {
            console.log('api error: ', error)
            alert('Something went wrong.')
        })
    }

    update_details(){
        fetch('/controller/udpate_service_details/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.objects)
        })
        .then(response => response.json())
        .then(data => {
            data['msg'] == 200 ? loadServices() : document.getElementById('errMsg').innerHTML = data['msg']
        })
        .catch(error => {
            console.log('api error: ', error)
            alert('Something went wrong.')
        })
    }

    deleteService(){
        fetch('/controller/deletService/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.objects)
        })
        .then(response => response.json())
        .then(data => {
            data['msg'] == 200 ? loadServices() : document.getElementById('confirmPassErr').innerHTML = data['msg']
        })
        .catch(error => {
            console.log('api error: ', error)
            alert('Something went wrong.')
        })
    }
}

function loadComments(id){
    service_id = id
    fetch('/controller/ratings/?a='+service_id)
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text();
    })
    .then((html) => {
        let load = document.getElementById('allServices').innerHTML = html;
        load ? sortComments(5) : null
    })
    .catch(error => {
        console.error('API Error: ', error)
        alert('Something went wrong!')
    })
}

function sortComments(rate){
    def_rate = rate
    fetch('/controller/comments/?a='+def_rate+'&&b='+service_id)
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text();
    })
    .then((html) => {
         document.getElementById('comments').innerHTML = html;
    })
    .catch(error => {
        console.error('API Error: ', error)
        alert('Something went wrong!')
    })
}

function saveReply(id){
    let reply = {
        'id' : id,
        'reply' : document.getElementById('reply_'+id).value
    }

    if(reply.reply != ''){
        const new_reply = new services(reply)
        new_reply.replyComment()
    }
}

function AvailabilityModal(id){
    let modal = `<div class="modal-dialog">
                    <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel"></h5>
                        <button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <h4><i class="fas fa-warning ms-1 text-warning"></i> Change service availability?</h4>
                    </div>
                    <div class="modal-footer">
                        <button type="button" id="closeModal" class="btn btn-secondary" data-mdb-dismiss="modal">Close</button>
                        <button type="button" onclick="AvailabilityFunction(${id})" class="btn btn-primary">Confirm</button>
                    </div>
                    </div>
                </div>`

                document.getElementById('Modal').innerHTML = modal
}

function AvailabilityFunction(id){
    let service_id = {
        's_id' : id
    }

    const service_update = new services(service_id)
    service_update.update_availability()
}

function openDetailsModal(id){
    fetch('/controller/modal_service_details/?id='+id)
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text();
    })
    .then((html) => {
         document.getElementById('Modal').innerHTML = html;
    })
    .catch(error => {
        console.error('API Error: ', error)
        alert('Something went wrong!')
    })
}

function updateServiceDetails(id){
    let service_name_update = document.getElementById('service_name')
    let service_price_update = document.getElementById('service_price')
    let service_description_update = document.getElementById('service_description')

    let service_update = {
        'service_id' : id,
        'name_update' : service_name_update.value,
        'price_update' : service_price_update.value,
        'description_update' : service_description_update.value
    }

    if(service_update.name_update !== '' && 
       service_update.price_update !== '' && 
       service_update.description_update !== '') 
       {
            const update_service = new services(service_update)
            update_service.update_details()
       }
    else{
        document.getElementById('errMsg').innerHTML = 'Please fill out the following' 
    }
}

function deletServiceModal(id){
    let modal = `<div class="modal-dialog">
                    <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel"></h5>
                        <button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <h4><i class="fas fa-warning ms-1 text-danger"></i> Delete service?</h4>
                        <p>Please confirm your password to delete the service.</p>
                        <span class="text-danger" id="confirmPassErr"></span>
                        <div class="input-group mb-3">
                            <input
                            type="password"
                            class="form-control rounded"
                            id="admin_password"
                            placeholder="Password"
                            />
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" id="closeModal" class="btn btn-secondary" data-mdb-dismiss="modal">Close</button>
                        <button type="button" onclick="deleteSericeFunction(${id})" class="btn btn-primary">Confirm</button>
                    </div>
                    </div>
                </div>`

                document.getElementById('Modal').innerHTML = modal
}

function deleteSericeFunction(id){
    let admin_password = document.getElementById('admin_password')

    let service_data = {
        'service_id' : id,
        'admin_pass' : admin_password.value
    }

    if (service_data.admin_pass !== ''){
        const data = new services(service_data)
        data.deleteService()
    }
    else{
        document.getElementById('confirmPassErr').innerHTML = 'Please Confirm your password.'
    }
}
