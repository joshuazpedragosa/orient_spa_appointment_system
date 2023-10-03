function loadNotice(){
    setTimeout(function(){
        ModalAdminNotice()
    }, 1000)
}

function ModalAdminNotice(){
    let modal = `<div class="modal-dialog">
    <div class="modal-content">
    <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel"></h5>
        <button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
    </div>
    <div class="modal-body">
        <div class="text-center">
            <h4 class="text-warning">
                <i class="fas fa-circle-exclamation"></i>
                Update Account Notice
            </h4>
            <h6 class="card-text">
                Your account was set as default by the system. Please change your Admin Account email
                and Admin Account password for security purpose.
            </h6>
        </div>
    </div>
    <div class="modal-footer">
    <button type="button" id="modalNotice" hidden data-mdb-toggle="modal" data-mdb-target="#Modal" class="btn btn-secondary"></button>
        <button type="button" onclick="location.href = '/client_view/settings/'" class="btn btn-secondary">Update Account</button>
    </div>
    </div>
</div>`;

document.getElementById('Modal').innerHTML = modal;
document.getElementById('modalNotice').click()
}

fetch('/controller/validate_admin_account/')
.then(response => response.json())
.then(data => {
    data['msg'] === 'default' ? loadNotice() : null
})
.catch(error => {
    console.error('api error', error)
    alert('There was a problem on validating admin account.')
})