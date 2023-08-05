var updateBtns = document.getElementsByClassName('update-favorites')


for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action

			if (user == 'AnonymousUser'){
				// alert('Пожалуйста зарегестрируйтесь или войдите в профиль')
			}
			else{
				updateUserFavorites(productId, action)
			}

			console.log('elem', sizeElement, 'pre', presentUrl)
			console.log('productId:', productId, 'Action:', action, 'size:', size)
			console.log('USER:', user)


	})
}

function updateUserFavorites(productId, action) {
    console.log('User is authenticated, sending data...')

    var url = '/update_favorites/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            location.reload()
        });
}