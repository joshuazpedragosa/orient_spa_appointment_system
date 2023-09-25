function loadclientCards(){
    fetch('/controller/load_client_home_cards/')
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text();
    })
    .then((html) => {
        document.getElementById('clientCards').innerHTML = html;
    })
    .catch(error => {
        console.error('API Error: ', error)
        document.getElementById('clientCards').innerHTML = `<div class="alert alert-danger">
                                                            <i class="fas fa-triangle-exclamation"></i> 
                                                            Something went wrong.
                                                         </div>`;
    })
}

function loadclientTable(){
    fetch('/controller/load_client_home_table/')
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text();
    })
    .then((html) => {
        document.getElementById('clientHomeTable').innerHTML = html;
    })
    .catch(error => {
        console.error('API Error: ', error)
        document.getElementById('clientHomeTable').innerHTML = `<div class="alert alert-danger">
                                                            <i class="fas fa-triangle-exclamation"></i> 
                                                            Something went wrong.
                                                         </div>`;
    })
}

window.onload = () => {
    loadclientCards()
    loadclientTable()
}