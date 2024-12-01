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
const getProducts = async() => {
    const data = await fetch('/viewcartitems/',{
        method:'POST',
        headers:{
            'content-Type':'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  
        },
        body:JSON.stringify({'userId':localStorage.getItem('user')})
    });
    const productsData = await data.json();
    const products = productsData.products;
    displayProducts(products);
}
getProducts()
const displayProducts=async(products)=>{
    const productsContainer = document.getElementById('productContainer')
    const checkoutBtn = document.getElementById('checkOut')
    if(products == '' || products == undefined){
        const emptyTagline = document.createElement('h1')
        const clearBtn = document.getElementById('clearBtn')
        const checkoutBtn = document.getElementById('checkout')
        clearBtn.disabled = true
        checkoutBtn.disabled = true
        emptyTagline.classList.add('emptyTagLine')
        emptyTagline.textContent = 'Seems a little empty here, why don\'t you add some items to the cart :)'
        productsContainer.appendChild(emptyTagline)
        return
    }
    productsContainer.innerHTML = ''
    products.forEach(product => {
        if(product.itemsLeft == 0){
            const emptyTagline = document.createElement('h1')
            const clearBtn = document.getElementById('clearBtn')
            const checkoutBtn = document.getElementById('checkout')
            clearBtn.disabled = true
            checkoutBtn.disabled = true
            emptyTagline.classList.add('emptyTagLine')
            emptyTagline.textContent = 'Seems a little empty here, why don\'t you add some items to the cart :)'
            productsContainer.appendChild(emptyTagline)
            return
        }
        let boughtItemQuantity = 1
        const productCard = document.createElement('div')
        const clickable = document.createElement('div')
        const thumbnail = document.createElement('img')
        const productDescription = document.createElement('div')
        const productName = document.createElement('h2')
        const price = document.createElement('p')
        const itemsLeft = document.createElement('p')
        const buttonsContainer = document.createElement('div')
        const deleteBtn = document.createElement('button')
        const quantityContainer = document.createElement('div')
        const addQuant = document.createElement('button')
        const Quant =document.createElement('button')
        const redQuant = document.createElement('button')

        productCard.classList.add('product-card')
        clickable.classList.add('clickable-cont-element')
        thumbnail.classList.add('img-thumbnail')
        productDescription.classList.add('prod-description')
        productName.classList.add('product-name')
        price.classList.add('product-price')
        itemsLeft.classList.add('product-quantity')
        buttonsContainer.classList.add('buttons-container')
        deleteBtn.classList.add('container-btn')
        quantityContainer.classList.add('quantity-container')
        addQuant.classList.add('quantity-button')
        Quant.classList.add('quantity-text')
        redQuant.classList.add('quantity-button')
        
        thumbnail.src = product.images[0]
        productName.textContent = product.name
        price.textContent = 'Total price = £' + product.price * boughtItemQuantity
        itemsLeft.textContent = parseInt(product.itemsLeft) + ' left'
        deleteBtn.textContent = 'Remove'
        addQuant.textContent = '+'
        Quant.textContent = product.quantity.toString();
        redQuant.textContent = '-'
        productCard.dataset.productId = product.productId;

        clickable.addEventListener('click',()=>{
            window.location.href = `/viewproduct/?productId=${product.productId}`
        })
        deleteBtn.addEventListener('click',()=>{
            removefromCart(product.productId)
        })

        addQuant.addEventListener('click', () => {
            if (product.quantity < product.itemsLeft) {
                Quant.textContent = product.quantity + 1
            }
        });
        redQuant.addEventListener('click', () => {
            let currentQuantity = parseInt(Quant.textContent);
            if (currentQuantity > 1) {
                Quant.textContent = (currentQuantity - 1).toString();
            }
        });

        productDescription.appendChild(productName)
        productDescription.appendChild(price)
        productDescription.appendChild(itemsLeft)
        quantityContainer.appendChild(redQuant)
        quantityContainer.appendChild(Quant)
        quantityContainer.appendChild(addQuant)
        buttonsContainer.appendChild(deleteBtn)
        buttonsContainer.appendChild(quantityContainer)
        clickable.appendChild(thumbnail)
        clickable.appendChild(productDescription)
        productCard.appendChild(clickable)
        productCard.appendChild(buttonsContainer)
        productsContainer.appendChild(productCard)

    });
}
const removefromCart=async(productId)=>{
    const response = await fetch('/removefromcart/',{
        method:'POST',
        headers:{
            'Content-Type':'application.json',
            'X-CSRFToken':getCookie('csrftoken')
        },
        body:JSON.stringify({'productId':productId})
    })
    if(response.ok){
        window.location.reload()
        alert('removed')
        return
    }
    const errorData = await response.json()
    console.log(errorData.error)
}
const clearCart = async()=>{
    const response = await fetch('/clearcart/',{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body:JSON.stringify({'userId':localStorage.getItem('user')})
    })
    if(response.ok){
        window.location.reload()
        alert('Cleared')
        return
    }
    const errorData = await response.json()
    alert(errorData.error)
    console.log(errorData.error)
}
const logout =()=>{
    localStorage.clear()
    window.location.href='/'
}
const getAllProducts=async()=>{
    const data = await fetch('/getallproducts/');
    const productsData = await data.json();
    const products = productsData.products;
    const productsContainer = document.getElementById('productsContainer')
    products.forEach(product => {
        if(product.quantity == 0){
            return
        }
        const productCard = document.createElement('div')
        const image =document.createElement('img')
        const extradesc = document.createElement('div')
        const clickable = document.createElement('div')
        const buttonsContainer = document.createElement('div')
        const addCartButton = document.createElement('button')
        const name = document.createElement('h3')
        const price = document.createElement('h4')

        buttonsContainer.classList.add('buttons-container')
        addCartButton.classList.add('cbutton')
        image.classList.add('extraimg')
        productCard.classList.add('extra-card')

        image.src = product.images[0]
        name.textContent = product.name
        price.textContent = "£ "+product.price
        addCartButton.textContent = 'Add To Cart'

        clickable.addEventListener('click',()=>{
            window.location.href = `/viewproduct/?productId=${product.productId}`
        })
        addCartButton.addEventListener('click',()=>{
            addItemsToCart(product.productId)
        })               
        
        extradesc.appendChild(name)
        extradesc.appendChild(price)
        clickable.appendChild(image)
        clickable.appendChild(extradesc)
        buttonsContainer.appendChild(addCartButton)
        productCard.appendChild(clickable)
        productCard.appendChild(buttonsContainer)
        productsContainer.appendChild(productCard)          
    });
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
const checkOut = async () => {
    const user = await getUser();
    if (!user) {
        alert('User not found!');
        return;
    }
    let totalAmount = 0;
    const cartProducts = [];
    document.querySelectorAll('.product-card').forEach(productCard => {
        const productId = productCard.dataset.productId;
        const quantity = parseInt(productCard.querySelector('.quantity-text').textContent);
        const price = parseFloat(productCard.querySelector('.product-price').textContent.replace('Total price = £', ''));
        cartProducts.push({ productId, quantity });
        totalAmount += price * quantity;
    });
    const country = document.getElementById('country').value
        const fname = document.getElementById('fname').value
        const lname= document.getElementById('lname').value
        const city= document.getElementById('city').value
        const province= document.getElementById('province').value
        const zipcode= document.getElementById('zipcode').value
        const phone= document.getElementById('phone').value
        if(country== '' || fname== '' || lname== '' || city== '' || province== '' || zipcode== ''||phone == ''){
            alert("Please fill in your shipping details correctly to proceed")
            return
        }
    if(cartProducts.quantity == 0  || totalAmount == 0){
        return
    }
    if (totalAmount > user.acc_balance) {
        alert('Your balance is too low for this transaction');
        return;
    }
    for (const product of cartProducts) {
        await buyItem(product.productId, product.quantity);
    }
    alert('Operation sucessful')
    closeModal()
    window.location.reload()
}

const buyItem = async (productId, quantity) => {
    const obj = JSON.stringify({
        'userId': localStorage.getItem('user'),
        'productId': productId,
        'quantity': quantity
    })
    try {
        const response = await fetch('/buyitem/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: obj
        });
        if (response.ok) {
            console.log(`Item ${productId} bought successfully.`);
        } else {
            console.error(`Failed to buy item ${productId}. Status: ${response.status}`);
        }
    } catch (error) {
        console.error(`Error buying item ${productId}:`, error);
    }
}
const openModal=async()=>{
    const modalElement = document.getElementById("shipping_modal")
    modalElement.style.display = 'flex'
    const productsContainer =  document.getElementById('checkout_section')
    productsContainer.innerHTML = ''
    const cartProducts = [];
    document.querySelectorAll('.product-card').forEach(productCard => {
        const productname = productCard.querySelector('.product-name').textContent
        cartProducts.push({ productname });
    });
    cartProducts.forEach(product=>{
        const productName = document.createElement('p')
        productName.classList.add('checkout-product-name')
        productName.textContent = product.productname
        productsContainer.appendChild(productName)
    })
}
const closeModal = ()=>{
    const modalElement = document.getElementById("shipping_modal")
    modalElement.style.display = 'none'
}
getUser()
getAllProducts()