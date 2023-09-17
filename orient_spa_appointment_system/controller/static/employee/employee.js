const currentDate = new Date();

const year = currentDate.getFullYear();
const month = currentDate.getMonth() + 1; 
const day = currentDate.getDate();
const formattedDate = `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;


function Spinner(){
    let spinner = `
                     <div style="display: flex; justify-content: center; margin-top: 20rem; overflow: hidden;">
                        <div class="spinner-border text-light" role="status">
                             <span class="visually-hidden">Loading...</span>
                        </div>
                        <button type="button" id="closeModal" class="btn btn-secondary" hidden data-mdb-dismiss="modal">Close</button>
                    </div>
                    ` 
    document.getElementById('Modal').innerHTML = spinner;
}

class employee{
    constructor(object){
        this.object = object
    }

    saveEmployee(){
        Spinner()
        fetch('/controller/signup/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.object)
        })
        .then(respose => respose.json())
        .then(data => {
            data['msg'] === 200 ? DisplayEmployee(formattedDate) : alert(data['msg'])
            document.getElementById('closeModal').click()
        })
        .catch(error => {
            console.error('api error: ',error)
        })
    }

    new_dtr(){
        fetch('/controller/insert_dtr/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.object)
        })
        .then(respose => respose.json())
        .then(data => {
            data['msg'] === 200 ? DisplayEmployee(formattedDate) : alert(data['msg'])
        })
        .catch(error => {
            console.error('api error: ',error)
            alert('Something went wrong! Please try again')
        })
    }

    delete(){
        fetch('/controller/delete_employee/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.object)
        })
        .then(respose => respose.json())
        .then(data => {
            data['msg'] === 200 ? DisplayEmployee(formattedDate) : document.getElementById('errmsg').innerHTML = data['msg']
            if (data['msg'] === 200) {
                document.getElementById('closeModal').click()
            }
        })
        .catch(error => {
            console.error('api error: ',error)
            alert('Something went wrong! Please try again')
        })
    }
}

function submitEmployee(){
    let empObject = {
        f_name : document.getElementById('f_name').value,
        l_name : document.getElementById('l_name').value,
        email : document.getElementById('email').value,
        password : document.getElementById('empPass').value,
        c_password : document.getElementById('empPass').value,
        priv : 3
    }

    if(empObject.f_name === '' || empObject.l_name === '' || empObject.email === '' || empObject.password === ''){
        alert('Please fillout all fields!')
    }
    else{
        const new_object = new employee(empObject)
        new_object.saveEmployee()
        return false;
    }
}

window.onload =()=>{
    DisplayEmployee(formattedDate)
}

function Return(){
    DisplayEmployee(formattedDate)
}

function DisplayEmployee(date){
    fetch('/controller/employee_details/?a='+date)
    .then((response) => {
        if(!response.ok){
            throw new Error('Network response unstable.')
        }
        return response.text();
    })
    .then((html) => {
        document.getElementById('employee_cards').innerHTML = html;
        document.getElementById('date').innerHTML = date
    })
    .catch(error => {
        console.error('API Error: ', error)
        alert('Something went wrong!')
    })
}

let get_month = month
let get_year = year
let user_vid = ""

function selectMonth(){
    get_month = document.getElementById('monthSelect').value;
    get_year = document.getElementById('dateInput').value;

    DisplayDTR(user_vid)
}

function DisplayDTR(id){
    user_vid = id
    if(user_vid !== '' && get_month !== ''){
        fetch('/controller/employee_dtr/?a='+user_vid+'&&b='+get_month+'&&c='+get_year)
        .then((response) => {
            if(!response.ok){
                throw new Error('Network response unstable.')
            }
            return response.text();
        })
        .then((html) => {
            document.getElementById('employee_cards').innerHTML = html;
        })
        .catch(error => {
            console.error('API Error: ', error)
            alert('Something went wrong!')
        })
    }
    else{
        alert('Something went wrong!')
    }
}

function setDtr(data){
    var date = new Date()
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12; 
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    let dtr_type = ''
    let new_time = ''

    if (hours <= 9){
        new_time = "0"+strTime
    }
    else{
        new_time = strTime
    }

    if (date.getHours() >= 12){
        dtr_type = 'afternoon'
    }
    else{
        dtr_type ='morning'
    }

    if(dtr_type != ''){
        let dtrObject = {
            emp_vid : data,
            time : new_time,
            date : formattedDate,
            dtr_type : dtr_type,
            hour : hours,
            minutes : minutes
        }
        const newDtr = new employee(dtrObject)
        newDtr.new_dtr()
        // alert(JSON.stringify(dtrObject))
    }
    else{
        alert('Something went wrong! Please try again.test')
    }
}

function chooseDate(){
    let datechosen =  document.getElementById('choosedate').value;

    if(new Date() < new Date(datechosen)){
        alert('No record for this date!')
    }
    else{
        DisplayEmployee(datechosen)
        document.getElementById('date').innerHTML = datechosen
    }
}

function searchTable(){
    const tbl_row = document.getElementsByTagName('tr')
    const searchBox = document.getElementById('searchBox')

    const searchtxt = searchBox.value.toLowerCase();

    for(let i = 1; i < tbl_row.length; i++){
        const row = tbl_row[i];
        const rowData = row.getElementsByTagName('td');
        let matchFound = false;

        for (let x = 0; x < rowData.length; x++){
            const cellData = rowData[x].textContent.toLowerCase();

            if(cellData.includes(searchtxt)){
                matchFound = true;
                break;
            }
        }

        if (matchFound) {
            row.style.display = '';
            document.getElementById('trDtr').style.display = '';
            document.getElementById('trDtr1').style.display = '';
        } else {
            row.style.display = 'none';
            document.getElementById('trDtr').style.display = '';
            document.getElementById('trDtr1').style.display = '';
        }
    }
}

function deleteEmp(id){
    let adminpass = document.getElementById('adminPass')
    let errmsg = document.getElementById('errmsg')
    let data = {
        u_id : id,
        adminpass : adminpass.value
    }

    if (data.adminpass == ''){
        errmsg.innerHTML = 'Please confirm your password.'
    }
    else{
        const newdelete = new employee(data)
        newdelete.delete()
    }
}

function printTbl() {
    let tbl = document.getElementById('dtrTbl')
    
    var printWindow = window.open('', '', 'width=600,height=600');
    
    printWindow.document.open();
    printWindow.document.write('<html><head><title>DTR(Daily Time Record)</title></head><body>');
    printWindow.document.write(`<div style="display: flex; justify-content: center; align-items: center;">
                                   <table style="border: 1px solid black; width: 100%; border-collapse: collapse;">
                                        ${tbl.innerHTML}
                                   </table> 
                                </div>
                                <div style="margin-top: 10%; margin-left: 80%;">Signed by: ___________________</div>
                                `);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    
    printWindow.print();
    printWindow.close();
}
