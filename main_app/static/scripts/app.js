console.log("this is a tester for my button")
// function for sending product to the cart
const updateBtn = document.getElementById('cart-updated')

function clicker() {
    console.log("this is clicking")
}

for(let i = 0; i < updateBtn.length; i++) {
    updateBtn[i].addEventListener('click', function(){
        let productId = this.dataset.productId
        let action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        console.log('USER:', user)
        if (user === 'Stranger'){
            console.log('User has no authentification')
        }else{
            console.log('User is successfully authenticated')
        }
    })
}