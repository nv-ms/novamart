const initializeData=async()=>{
    const response = await fetch('/viewusers/')
    const userData = response.json()
    const users = userData.users
    const role = document.getElementById('role')
    if(users == ''){
        const admin = document.createElement('option')
        admin.value = 'admin'
        admin.textContent='Admin'
        role.appendChild(admin)
        console.log('No users')
        return
    }
}
initializeData()
const registerUser=async()=>{
    try {
        const fname = document.getElementById('fname').value
        const lname= document.getElementById('lname').value
        const phone= document.getElementById('phone').value
        const email= document.getElementById('email').value
        const username= document.getElementById('username').value
        const role = "buyer"
        const password= document.getElementById('password').value
        const confirmPass= document.getElementById('cpassword').value
        if(fname==''||lname==''||phone==''||username==''||password==''||confirmPass==''){
            alert('Please enter all details correctly')
            return
        }
        const phoneRegex = /^\+(?:[0-9] ?){6,14}[0-9]$/;
        if(!phoneRegex.test(phone)){
            alert("Pleas eneter a valid phone number")
        }
        if(role == "null"){
            alert("Please Choose a role to continue")
            return
        }
        if (password !== confirmPass) {
            alert("Passwords Do not Match")
            console.error('Passwords do not match');
            return;
        }
        const getCookie=(name)=> {
            const cookieValue = document.cookie
            .split(';')
            .map(cookie => cookie.trim())
            .find(cookie => cookie.startsWith(`${name}=`));
            if (cookieValue) {
                return cookieValue.split('=')[1];
            }
            return null;
        }

        const user ={
            "first_name":fname,
            "last_name":lname,
            "phone":phone,
            "email":email,
            "username":username,
            "role":role,
            "password":password
        }
        const response = await fetch('/createuser/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':getCookie('csrftoken')
            },
            body:JSON.stringify(user)
        })
        if(response.ok){
            window.location.href = '/login/'
        }else{
            const errorText = await response.text()
            statusDiv.textContent = errorText
            console.log(errorText)
        }
    } catch (error) {
        console.log(error)
    }
}