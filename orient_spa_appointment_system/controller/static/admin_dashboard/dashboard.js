function loadDashboardCards(){
    fetch('/controller/load_dashboard_main_cards/')
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text();
    })
    .then((html) => {
        document.getElementById('mainCards').innerHTML = html;
    })
    .catch(error => {
        console.error('API Error: ', error)
        document.getElementById('mainCards').innerHTML = `<div class="alert alert-danger">
                                                            <i class="fas fa-triangle-exclamation"></i> 
                                                            Something went wrong.
                                                         </div>`;
    })
}

function loadSalesRevenue(){
    fetch('/controller/load_sales_revenue/')
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text();
    })
    .then((html) => {
        document.getElementById('salesRevenue').innerHTML = html;
    })
    .catch(error => {
        console.error('API Error: ', error)
        document.getElementById('salesRevenue').innerHTML = `<div class="alert alert-danger">
                                                            <i class="fas fa-triangle-exclamation"></i> 
                                                            Something went wrong.
                                                         </div>`;
    })
}

function loadServicesSales(){
    fetch('/controller/load_services_sales/')
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text();
    })
    .then((html) => {
        document.getElementById('servicesSales').innerHTML = html;
    })
    .catch(error => {
        console.error('API Error: ', error)
        document.getElementById('servicesSales').innerHTML = `<div class="alert alert-danger">
                                                            <i class="fas fa-triangle-exclamation"></i> 
                                                            Something went wrong.
                                                         </div>`;
    })
}

window.onload = () => {
    loadDashboardCards()
    loadSalesRevenue()
    loadServicesSales()
}