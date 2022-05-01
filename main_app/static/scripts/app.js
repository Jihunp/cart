console.log("this is a tester for my button")
// function for sending product to the cart

// need to fix my buttons

function clicker() {
    for(let i = 0; i < updateBtn.length; i++) {
        const updateBtn = document.getElementById('cart-updated')
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
}
function UserOrderUpdate(productId, action){
    console.log('User is successfully authenticated')

    let url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action' :action})
    })
    .then((response)=> {
        return response.json()
    })

    .then((data)=> {
        console.log('data:', data)
    })
}