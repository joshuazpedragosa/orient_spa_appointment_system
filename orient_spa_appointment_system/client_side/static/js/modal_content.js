document.getElementById('NewAppointment').addEventListener('click', function(e){
    e.preventDefault()

    let modal_content = `<div class="modal-dialog">
                            <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="exampleModalLabel">Add New Appointment</h5>
                                <button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">

                            <div class="form-outline">
                                <input type="number" id="typeNumber" class="form-control border-dark" />
                                <label class="form-label" for="typeNumber">Number input</label>
                            </div>

                            <div class="form-outline">
                                <input type="Date" class="form-control" />
                                <input type="Time" class="form-control" />
                            </div>

                            <div class="form-outline">
                                <select id="services" class="form-control">
                                    <option value=""></option>
                                    <option value="1">One</option>
                                    <option value="2">Two</option>
                                    <option value="3">Three</option>
                                </select>
                                <label class="form-label" for="services">Choose Service</label>
                            </div>

                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-mdb-dismiss="modal">Close</button>
                                <button type="button" class="btn btn-primary">Save</button>
                            </div>
                            </div>
                        </div>`;

  document.getElementById('Modal').innerHTML = modal_content;
})

function logout(){
    let modal_logout = `<div class="modal-dialog">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel"></h5>
                            <button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <h4><i class="fas fa-warning ms-1 text-warning"></i> Logout your account?</h4>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-mdb-dismiss="modal">Close</button>
                            <button type="button" onclick="delSession()" class="btn btn-danger">Logout</button>
                        </div>
                        </div>
                    </div>`;

    document.getElementById('Modal').innerHTML = modal_logout;
}

function delSession(){
    fetch('/controller/logout/',{
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        data['msg'] === 200 ? location.href ='/' : null
    })
    .catch(error => {
        alert('Something went wrong! Please check your internet connection.')
        console.error('api error: ' , error)
    })
}