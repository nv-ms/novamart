const loginUser = async()=>{
    try {
        const email = document.getElementById('email').value
        const password = document.getElementById('password').value
        const statusDiv = document.getElementById('statusDiv')

        if(email == ''){
            alert("please enter your email to continue")
            return
        }
        if(password == ''){
            alert("please enter a password to continue")
            return
        }

        const user = JSON.stringify({
            'email':email,
            'password':password
        })

        const getCookie=(name)=> {
            const cookieValue = document.cookie
            .split(';')
            .map(cookie => cookie.trim())
            .find(cookie => cookie.startsWith(`${name}=`))
            if (cookieValue) {
                return cookieValue.split('=')[1];
            }
            return null;
        }
        const response = await fetch('/loginlog/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':getCookie('csrftoken')
            },
            body:user
        })
        localStorage.clear()
        if(response.ok){
            const data = await response.json();
            localStorage.setItem('user',data.userId)
            window.location.href = data.url;
            return
        }
        const errorText = await response.text()
        statusDiv.textContent = errorText
    } catch (error) {
        console.log(error)
    }
}