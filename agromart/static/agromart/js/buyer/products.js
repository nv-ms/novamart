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

const searchProducts = async() => {
    const keyword = document.getElementById('searchInput').value.toLowerCase();
    const data = await fetch('/getallproducts/');
    const productsData = await data.json();
    const products = productsData.products;

    const filteredProducts = products.filter(product => {
        for (const key in product) {
            if (typeof product[key] === 'string' && product[key].toLowerCase().includes(keyword)) {
                return true;
            }
        }
        return false;
    });

    displayProducts(filteredProducts);
}
searchProducts()
const displayProducts=async(products)=>{
    const productsContainer = document.getElementById('productContainer')
    productsContainer.innerHTML = ''
    products.forEach(product => {
        const productCard = document.createElement('div')
        const clickable = document.createElement('div')
        const thumbnail = document.createElement('img')
        const productDescription = document.createElement('div')
        const productName = document.createElement('h2')
        const price = document.createElement('p')
        const quantity = document.createElement('p')
        const buttonsContainer = document.createElement('div')
        const addCartButton = document.createElement('button')
        const buyBtn = document.createElement('button')

        productCard.classList.add('product-card')
        clickable.classList.add('clickable-cont-element')
        thumbnail.classList.add('img-thumbnail')
        productDescription.classList.add('prod-description')
        productName.classList.add('product-name')
        price.classList.add('product-price')
        quantity.classList.add('product-quantity')
        buttonsContainer.classList.add('buttons-container')
        addCartButton.classList.add('container-btn')
        buyBtn.classList.add('container-btn')
        
        thumbnail.src = product.images[0]
        productName.textContent = product.name
        price.textContent = `£ ${product.price}`
        quantity.textContent = product.quantity > 0 ? product.quantity + ' left' : 'Out of stock';
        addCartButton.textContent = 'Add To Cart'
        buyBtn.textContent = 'Buy Now'

        if(product.quantity == 0){
            addCartButton.disabled = true
            buyBtn.disabled = true
        }

        clickable.addEventListener('click',()=>{
            window.location.href = `/viewproduct/?productId=${product.productId}`
        })
        addCartButton.addEventListener('click',()=>{
            addItemsToCart(product.productId)
        })
        buyBtn.addEventListener('click',()=>{
            openModal(product)
        })

        productDescription.appendChild(productName)
        productDescription.appendChild(price)
        productDescription.appendChild(quantity)
        buttonsContainer.appendChild(addCartButton)
        buttonsContainer.appendChild(buyBtn)
        clickable.appendChild(thumbnail)
        clickable.appendChild(productDescription)
        productCard.appendChild(clickable)
        productCard.appendChild(buttonsContainer)
        productsContainer.appendChild(productCard)
    });
}
const logout =()=>{
    localStorage.clear()
    window.location.href='/'
}

const addItemsToCart=async(productId)=>{
    const userId = localStorage.getItem('user')
    const product = JSON.stringify({
        'productId':productId,
        'userId':userId,
        'quantity':1
    })
    const response = await fetch('/addtocart/',{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body:product
    })
    if(response.ok){
        alert("Added Sucessfully")
        return
    }
    const errorText = await response.json()
    console.log("Error", errorText.error)
}
const getUser = async()=>{
    const response = await fetch('/viewadmin/',{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  
        },
        body:JSON.stringify({'userId':localStorage.getItem('user')})
    })
    if(response.ok){
        const userItem = await response.json()
        const $user = userItem.user
        
        const bal = document.getElementById('rem_balance')
        bal.textContent = `£ ${$user.acc_balance}`
        return $user
    }            
    return errorText.error
}
const buyNow=async(productId,quantity,amount)=>{
    const country = document.getElementById('country').value
    const fname = document.getElementById('fname').value
    const lname = document.getElementById('lname').value
    const city = document.getElementById('city').value
    const province = document.getElementById('province').value
    const zipcode = document.getElementById('zipcode').value
    const phone = document.getElementById('phone').value

    const userQuantity = document.getElementById('shipping_quantity').value
    const paymentOptionElement = document.querySelector('input[name="payment-options"]:checked');
    const paymentoptions = paymentOptionElement ? paymentOptionElement.value : null;
    const creditcardno = document.getElementById('cardnumber').value;
    const expiry = document.getElementById('expiry').value;
    const cvc = document.getElementById('cvc').value;

    if(fname == ''||lname==''||city==''||province==''||zipcode==''||phone==''){
        alert('Please enter your shipping details correctly to continue')
        return
    }
    const phoneRegex = /^\+(?:[0-9] ?){6,14}[0-9]$/;
    if(!phoneRegex.test(phone)){
        alert("Pleas eneter a valid phone number")
    }
    const user = await getUser()
    if(userQuantity == 0 || userQuantity == null){
        alert(`Please enter the qantity to continue between(1 - ${quantity})`)
        return
    }
    if(userQuantity > quantity){
        alert(`Please choose a quantity lesser than ${quantity} to continue`)
        return
    }
    if(!paymentoptions){
        alert('Please Select a payment method')
        return
    }
    else if(paymentoptions == 'debitCard'){
        if(creditcardno == ''||expiry==''||cvc==''){
            alert('Please fill in your payment details correctly')
            return
        }
        const creditCardRegex = /^[0-9]{13,16}$/;
        if (!creditCardRegex.test(creditcardno)) {
            alert('Please enter a valid credit card number');
            return;
        }
        const expiryRegex = /^(0[1-9]|1[0-2])\/?([0-9]{2})$/;
        if (!expiryRegex.test(expiry)) {
            alert('Please enter a valid expiry date in MM/YY format');
            return;
        }
        const cvcRegex = /^[0-9]{3,4}$/;
        if (!cvcRegex.test(cvc)) {
            alert('Please enter a valid CVC (3 or 4 digits)');
            return;
        }
    }
   
    const totalAmount = amount * userQuantity
    if(user.acc_balance < totalAmount){
        alert('Your balance is too low for this transaction, please top up to continue')
        return
    }
    const obj = JSON.stringify({
        'userId':user.userId,
        'productId':productId,
        'quantity':userQuantity
    })
    const response = await fetch('/buyitem/',{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },body:obj
    })
    if(response.ok){
        alert("Sucessfull, we'll send your shipping details through your mail :)")
        window.location.reload()
        return
    }
    const errorData = await response.json()
    alert(errorData.error)
    console.log(errorData.error)
}
const openModal=(product)=>{
    const modalElement = document.getElementById("shipping_modal")
    modalElement.style.display = 'flex'
    const productImg = document.getElementById('shipping_thumbnail')
    const productName = document.getElementById('shipping_product_name')
    const items_left = document.getElementById('shipping_items_left')
    const checkoutBtn = document.getElementById('checkout_btn')

    productImg.src = product.images[0]
    productName.textContent = product.name
    items_left.textContent = product.quantity + 'left'

    checkoutBtn.addEventListener('click',()=>{
        buyNow(product.productId,product.quantity,product.amount)
    })
}
const closeModal = ()=>{
    const modalElement = document.getElementById("shipping_modal")
    modalElement.style.display = 'none'
}
getUser()