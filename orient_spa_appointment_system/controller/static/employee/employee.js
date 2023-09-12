class employee{
    constructor(object){
        this.object = object
    }

    saveEmployee(){
        fetch('/controller/signup/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.object)
        })
        .then(respose => respose.json())
        .then(data => {
            alert(data['msg']) 
        })
        .catch(error => {
            console.error('api error: ',error)
        })
    }
}

function submitEmployee(e){
    e.preventDefault()
    let empObject = {
        f_name : document.getElementById('f_name').value,
        l_name : document.getElementById('l_name').value,
        email : document.getElementById('email').value,
        password : document.getElementById('empPass').value,
        c_password : document.getElementById('empPass').value,
        priv : 3
    }

    const new_object = new employee(empObject)
    new_object.saveEmployee()
}