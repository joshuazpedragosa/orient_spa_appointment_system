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


function addEmployeeModal(){
    let modal_emp = `<div class="modal-dialog">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h5>Add Employee</h5>
                            <h5 class="modal-title" id="exampleModalLabel"></h5>
                            <button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            
                        <div class="input-group rounded mb-2">
                            <input type="text" class="form-control rounded" id="f_name" placeholder="First Name" aria-label="Search" aria-describedby="search-addon" required />
                        </div>
                            
                        <div class="input-group rounded mb-2">
                            <input type="text" class="form-control rounded" id="l_name" placeholder="Last Name" aria-label="Search" aria-describedby="search-addon" required />
                        </div>

                        <div class="input-group rounded mb-2">
                            <input type="email" class="form-control rounded" id="email" placeholder="Email" aria-label="Search" aria-describedby="search-addon" required />
                        </div>

                        <div class="input-group rounded mb-2">
                            <input type="text" class="form-control rounded" id="empPass" value="orientspa_new_employee" placeholder="Password" aria-label="Search" aria-describedby="search-addon" required />
                        </div>

                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" onchange="hidePass()" value="" id="flexCheckChecked" checked/>
                            <label class="form-check-label" for="flexCheckChecked">Show Password</label>
                        </div>

                        </div>
                        <div class="modal-footer">
                            <button type="button" id="closeModal" class="btn btn-secondary" data-mdb-dismiss="modal">Close</button>
                            <button type="button" onclick="submitEmployee()" class="btn btn-primary">Add</button>
                        </div>
                        </div>
                    </div>`;

    document.getElementById('Modal').innerHTML = modal_emp;
}

function hidePass(){
    let input = document.getElementById('empPass');

    if (input.type === 'text'){
        input. type = 'password'
    }
    else{
    input.type = 'text'
    }
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
    fetch('/controller/modal_service/')
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


function viewImg(){
    const [file] = imgInp.files
    if (file) {
       img.src = URL.createObjectURL(file)
    }
}