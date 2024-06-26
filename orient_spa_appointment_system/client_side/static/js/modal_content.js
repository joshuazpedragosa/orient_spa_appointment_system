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


function showDeleteEmpModal(id){
    let modal_deleteEmp = `<div class="modal-dialog">
    <div class="modal-content">
    <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel"></h5>
        <button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
    </div>
    <div class="modal-body">
        <h4><i class="fas fa-warning ms-1 text-warning"></i> Delete Employee?</h4>
        <h6>Please input your password to confirm deletion.</h6>
        <p id="errmsg" class="text-danger"></p>
        <input type="password" id="adminPass" class="form-control rounded" placeholder="Password" />
    </div>
    <div class="modal-footer">
        <button type="button" id="closeModal" class="btn btn-secondary" data-mdb-dismiss="modal">Close</button>
        <button type="button" onclick="deleteEmp('${id}')" class="btn btn-danger">Delete</button>
    </div>
    </div>
    </div>`;

    document.getElementById('Modal').innerHTML = modal_deleteEmp;
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

                        <div class="input-group rounded mb-2 hidden">
                            <input type="text" class="form-control rounded" id="empPass" value="orientspa_new_employee" placeholder="Password" hidden aria-label="Search" aria-describedby="search-addon" required />
                        </div>

                        <div class="form-check hidden" hidden>
                            <input class="form-check-input" type="checkbox" onchange="hidePass()" value="" id="flexCheckChecked" hidden checked/>
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
        data['msg'] === 200 ? location.href ='/controller/logout_view/' : null
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

function ShowRatingModal(id){
    let modal_comment_rating = `<div class="modal-dialog">
    <div class="modal-content">
    <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Rate</h5>
        <button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
    </div>
    <div class="modal-body">
        <div class="form-outline">
            <textarea class="form-control" style="border: 1px solid gray;" id="comment" rows="4"></textarea>
            <label class="form-label" for="textAreaExample">Comment</label>
        </div>
        <div class="form-outline text-xl">
            Rate:
            <i class="fas fa-star text-warning" id="star1" onclick="starRating(1)"></i>
            <i class="fas fa-star text-warning" id="star2" onclick="starRating(2)"></i>
            <i class="fas fa-star text-warning" id="star3" onclick="starRating(3)"></i>
            <i class="fas fa-star text-warning" id="star4" onclick="starRating(4)"></i>
            <i class="fas fa-star text-warning" id="star5" onclick="starRating(5)"></i>
        </div>
    </div>
    <div class="modal-footer">
        <button type="button" id="closeModal" class="btn btn-secondary" data-mdb-dismiss="modal">Close</button>
        <button type="button" onclick="saveCommentRate(${id})" class="btn btn-primary">
            <i class="far fa-paper-plane"></i> Comment
        </button>
    </div>
    </div>
    </div>`;

    document.getElementById('Modal').innerHTML = modal_comment_rating;
}
let rate = 5

function starRating(num){
    let star_2 = document.getElementById('star2')
    let star_3 = document.getElementById('star3')
    let star_4 = document.getElementById('star4')
    let star_5 = document.getElementById('star5')

    switch (num) {
        case 1:
            star_2.classList.add('far')
            star_2.classList.remove('fas')
            star_3.classList.add('far')
            star_3.classList.remove('fas')
            star_4.classList.add('far')
            star_4.classList.remove('fas')
            star_5.classList.add('far')
            star_5.classList.remove('fas')
            rate = 1
            break;
        case 2:
            if(star_2.classList.contains('fas')){
                star_3.classList.add('far')
                star_3.classList.remove('fas')
                star_4.classList.add('far')
                star_4.classList.remove('fas')
                star_5.classList.add('far')
                star_5.classList.remove('fas')
                rate = 2
            }
            else{
                star_2.classList.add('fas')
                star_2.classList.remove('far')
            }
            break;
        case 3:
            if(star_3.classList.contains('fas')){
                star_4.classList.add('far')
                star_4.classList.remove('fas')
                star_5.classList.add('far')
                star_5.classList.remove('fas')
                rate = 3
            }
            else{
                star_2.classList.add('fas')
                star_2.classList.remove('far')
                star_3.classList.add('fas')
                star_3.classList.remove('far')
            }
            break;
        case 4:
            if(star_4.classList.contains('fas')){
                star_5.classList.add('far')
                star_5.classList.remove('fas')
                rate = 4
            }
            else{
                star_2.classList.add('fas')
                star_2.classList.remove('far')
                star_3.classList.add('fas')
                star_3.classList.remove('far')
                star_4.classList.add('fas')
                star_4.classList.remove('far')
            }
            break
        case 5:
            star_2.classList.add('fas')
            star_2.classList.remove('far')
            star_3.classList.add('fas')
            star_3.classList.remove('far')
            star_4.classList.add('fas')
            star_4.classList.remove('far')
            star_5.classList.add('fas')
            star_5.classList.remove('far')
            rate = 5
            break;
        default:
            break;
    }
}

function saveCommentRate(id){
    let comment = document.getElementById('comment')

    let rate_obj = {
        'app_id' : id,
        'comment' : comment.value,
        'rate' : rate
    }

    const my_rate = new appointment(rate_obj)
    my_rate.rating()
}