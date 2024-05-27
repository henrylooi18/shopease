// method to make sure quantity added to existing item in basket does not exceed stock limit
document.getElementById('quantity').addEventListener('change', function() {
    let max = parseInt(document.getElementById('quantity').getAttribute('max'));
    if (this.value > max) {
        this.value = max;
    }
});


// method for purchase
function confirmPurchase() {
    if (confirm("Do you confirm to purchase the item(s) in your basket?")) {
        fetch('/purchase/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ confirmation: true })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Purchase was successful!");
                window.location.href = "/"; // redirect to home after purchase successful
            } else {
                alert("There was an error processing your purchase.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        alert("Purchase cancelled.");
    }
}


// method to favourite item
function like(productId) {
    fetch('/favourite/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const likeIcon = document.querySelector(`.like-icon[data-product="${productId}"]`);
            const likeCount = likeIcon.querySelector('.like-count');

            if (likeIcon.classList.contains('liked')) {
                likeIcon.classList.remove('liked');
                likeIcon.innerHTML = '<i class="far fa-heart"></i>';
                likeCount.textContent = parseInt(likeCount.textContent) - 1;
            } else {
                likeIcon.classList.add('liked');
                likeIcon.innerHTML = '<i class="fas fa-heart"></i>';
                likeCount.textContent = parseInt(likeCount.textContent) + 1;
            }
        } else {
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}