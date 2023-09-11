function NewAppointment(){
    fetch('/controller/modal_content/')
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

    return false;
}


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

function addService(){
    let service_form = `<div class="modal-dialog">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel">Add Service</h5>
                            <button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <form method="submit" id="addService" enctype="multipart/form-data">
                        <div class="modal-body">
                        <span style="color: red;" id="errmsg"></span>
                            <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 5px;">
                                <img
                                src="#"
                                alt="Service"
                                class="img-fluid rounded"
                                style="width: 20%;"
                                id="img"
                                />
                            </div>
                            <div class="form-outline">
                            <input type="file" onchange="viewImg()" id="imgInp" style="border: 1px solid gray;" accept="image/png, image/gif, image/jpeg" class="form-control" />
                            </div><br>

                            <div class="form-outline">
                            <input type="text" id="service_name" style="border: 1px solid gray;" class="form-control" />
                            <label class="form-label" for="service_namet">Service Name</label>
                            </div><br>

                            <div class="form-outline">
                            <input type="number" id="price" style="border: 1px solid gray;" class="form-control" />
                            <label class="form-label" for="price">Price</label>
                            </div><br>

                            <div class="form-outline">
                            <textarea class="form-control" id="description" style="border: 1px solid gray;" rows="4"></textarea>
                            <label class="form-label" for="description">Description</label>
                            </div>
                            
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-mdb-dismiss="modal">Close</button>
                            <button type="submit" class="btn btn-primary">Save</button>
                        </div>
                        </form>
                        </div>
                    </div>`;

    document.getElementById('Modal').innerHTML = service_form;
    loadForm()
}


function viewImg(){
    const [file] = imgInp.files
    if (file) {
       img.src = URL.createObjectURL(file)
    }
}