console.log("Is this connected correctly")

// function for sending product to the cart
const updateBtn = document.getElementsByClassName('cart-update')

for(let i = 0; i <updateBtn.length; i++) {
    updateBtn[i].addEventListener('click', function () {
        const productId = this.dataset.productId
        const clicker = this.dataset.clicker
        console.log('productId:', productId, 'Clicker:', clicker)

        console.log('USER:' user)
        if (user == 'Stranger'){
            console.log('User has no authentification')
        }else{
            console.log('User is successfully authenticated')
        }
    })
}