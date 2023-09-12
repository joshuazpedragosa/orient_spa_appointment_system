class services{
    constructor(objects){
        this.objects = objects
    }

    Services(){
       
        }
}


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
}