const urlParams = new URLSearchParams(window.location.search);
const productId = urlParams.get('productId');
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
let focusedProduct;
const getProduct=async()=>{
    const productId = urlParams.get('productId');
    const response = await fetch('/getproduct/',{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body:JSON.stringify({'productId':productId})
    })
    if(response.ok){
        const productData = await response.json()
        const product = productData.product
        const productContainer = document.getElementById('productContainer')
        const imageDiv = document.getElementById('imgDiv')
        const itemImg = document.getElementById('itemImage')
        focusedProduct=product
        const name = document.getElementById('name')
        const price = document.getElementById('price')
        const quantity = document.getElementById('quantity')
        const description = document.getElementById('description')
        const addCartButton = document.getElementById('addToCart')
        const buyBtn = document.getElementById('buyNow')
        itemImg.src = product.images[0]
        name.textContent = product.name
        price.textContent ='£ ' + product.price
        quantity.textContent = product.quantity > 0 ? product.quantity + ' left' : 'Out of stock';
        description.textContent = product.description
        if(product.quantity == 0){
            addCartButton.disabled = true
            buyBtn.disabled = true
        }
        
        return
    }
    const errorText = await response.json()
    return errorText.error
}
const addItemsToCart=async()=>{
    const productId = urlParams.get('productId');
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
    console.log(errorText.error)
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
const getAllProducts=async()=>{
    const data = await fetch('/getallproducts/');
    const productsData = await data.json();
    const products = productsData.products;
    const productsContainer = document.getElementById('productsContainer')
    products.forEach(product => {
        const productCard = document.createElement('div')
        const image =document.createElement('img')
        const extradesc = document.createElement('div')
        const clickable = document.createElement('div')
        const buttonsContainer = document.createElement('div')
        const addCartButton = document.createElement('button')
        const buyBtn = document.createElement('button')
        const name = document.createElement('h3')
        const price = document.createElement('h4')

        buttonsContainer.classList.add('buttons-container')
        addCartButton.classList.add('cbutton')
        buyBtn.classList.add('cbutton')
        image.classList.add('extraimg')
        productCard.classList.add('extra-card')

        image.src = product.images[0]
        name.textContent = product.name
        price.textContent = "£ "+product.price
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
        
        extradesc.appendChild(name)
        extradesc.appendChild(price)
        clickable.appendChild(image)
        clickable.appendChild(extradesc)
        buttonsContainer.appendChild(addCartButton)
        buttonsContainer.appendChild(buyBtn)
        productCard.appendChild(clickable)
        productCard.appendChild(buttonsContainer)
        productsContainer.appendChild(productCard)          
    });
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
getProduct()
getAllProducts()