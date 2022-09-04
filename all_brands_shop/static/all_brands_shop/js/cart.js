var updateBtns = document.getElementsByClassName('update-cart')


for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var presentUrl = document.location.href

		var productId = this.dataset.product.split("-")[0]
		var action = this.dataset.action

		var sizeElement = document.querySelector('label.active > input')

		if (sizeElement == null && presentUrl.includes('shop')){
			window.location.replace(presentUrl.split("#")[0]+"#popup_not_choose_size")
		}
		else {

			if(presentUrl.includes('cart')){
				size = this.dataset.product.split("-")[1]
			}
			else{
				size = sizeElement.value.toString().toLowerCase()
			}

			if (user == 'AnonymousUser'){
				addCookieItem(productId, action, size)
			}
			else{
				updateUserOrder(productId, action, size)
			}

			// console.log('elem', sizeElement, 'pre', presentUrl)
			// console.log('productId:', productId, 'Action:', action, 'size:', size)
			// console.log('USER:', user)
		}

	})
}

function updateUserOrder(productId, action, size){
	// console.log('User is authenticated, sending data...')
	document.cookie ='cart=' + JSON.stringify({}) + ";domain=;path=/"

		var url = '/update_item/'



		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			},
			body:JSON.stringify({'productId':productId, 'action':action, 'size':size})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

function addCookieItem(productId, action, size){
	// console.log('User is not authenticated')

	productIdSize = productId+'-'+size

	if (action == 'add'){
		if (cart[productIdSize] == undefined){
			// console.log('UNDIFINED')
		cart[productIdSize] = {'quantity':1, 'size': size}

		}else{
			cart[productIdSize]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productIdSize]['quantity'] -= 1

		if (cart[productIdSize]['quantity'] <= 0){
			// console.log('Item should be deleted')
			delete cart[productId];
		}
	}

	if (action == 'delete'){
		delete cart[productIdSize];
	}
	// console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

	location.reload()
}


