class services{
    constructor(objects){
        this.objects = objects
    }

    saveService(){
        fetch('/controller/save_service/',{
            method : 'POST',
            headers : {
                'Content-Type': 'application/json'
            },
            body : JSON.stringify(this.objects)
        })
        .then(response => response.json())
        .then(data => {
            alert(data['msg'])
        })
        .catch(error => {
            console.log('api error: ', error)
        })
        //  alert(JSON.stringify(this.objects))
    }
}

function validateService(){
    const err = document.getElementById('errmsg')
    let object = {
        img : document.getElementById('imgInp').files[0].name,
        service_name : document.getElementById('service_name').value,
        price : document.getElementById('price').value,
        description : document.getElementById('description').value,
    }

    err.innerHTML = '';

    if(!object.img) {
        err.innerHTML = 'Image is required'
    }
    else if(object.service_name === ''){
        err.innerHTML = 'Service name is required'
    }
    else if(object.price === ''){
        err.innerHTML = 'Price is required'
    }
    else if(object.description === ''){
        err.innerHTML = 'Description is required'
    }
    else{
        const new_service = new services(object)
        new_service.saveService()   
    }
}


function loadForm(){
    document.getElementById('addService').addEventListener('submit', function(e){
        e.preventDefault();

        const err = document.getElementById('errmsg')
        let object = {
            img : document.getElementById('imgInp').files[0].name,
            service_name : document.getElementById('service_name').value,
            price : document.getElementById('price').value,
            description : document.getElementById('description').value,
        }
    
        err.innerHTML = '';
    
        if(!object.img) {
            err.innerHTML = 'Image is required'
        }
        else if(object.service_name === ''){
            err.innerHTML = 'Service name is required'
        }
        else if(object.price === ''){
            err.innerHTML = 'Price is required'
        }
        else if(object.description === ''){
            err.innerHTML = 'Description is required'
        }
        else{
            const new_service = new services(object)
            new_service.saveService()   
        }
    })
}