document.addEventListener('DOMContentLoaded', () => {
    // Handle clicks for .submit-rating, .delete-game-btn, and .add-to-cart with event delegation

    document.body.addEventListener('click', function (event) {
        // Handle rating submission
        if (event.target.classList.contains('submit-rating')) {
            const ratingDiv = event.target.closest('.card-body').querySelector('.rating');
            const gameId = ratingDiv.getAttribute('data-game-id');
            const selectedStars = ratingDiv.querySelectorAll('.fa-star.selected').length;

            // Prevent action if no stars are selected
            if (selectedStars === 0) {
                alert('Please select a rating before submitting.');
                return;
            }

            // Send the rating to the server
            fetch(`/rate/${gameId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `stars=${selectedStars}` // Send stars only
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the displayed stars to reflect the new average
                    const stars = ratingDiv.querySelectorAll('.fa-star');
                    const newAverage = data.average_rating;

                    stars.forEach(star => {
                        const starValue = parseInt(star.getAttribute('data-star'), 10);
                        if (starValue <= newAverage) {
                            star.classList.add('selected');
                        } else {
                            star.classList.remove('selected');
                        }
                    });

                    // Update the average rating text if necessary
                    const averageRatingElement = event.target.closest('.card-body').querySelector('.average-rating');
                    if (averageRatingElement) {
                        averageRatingElement.textContent = `Average Rating: ${newAverage.toFixed(1)}`;
                    }
                } else {
                    alert('Failed to submit rating. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while submitting your rating.');
            });
        }

        // Handle delete game
        if (event.target && event.target.matches('.delete-game-btn')) {
            const button = event.target;
            const gameId = button.getAttribute('data-game-id');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
            // Prevent multiple clicks by disabling the button
            if (button.disabled) {
                return; // Prevent the request if the button is already disabled
            }
    
            // Disable the button to prevent multiple clicks
            button.disabled = true;
    
            // Confirm before deletion
            if (confirm('Are you sure you want to delete this game?')) {
                const url = `/delete/${gameId}/`;  // The URL where the delete request will be sent
    
                // Make the delete request to the server
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => {
                    if (response.ok) {
                        // Game deleted from the database (backend), no need to remove the game card here
                        alert('Game deleted successfully.');
                        location.reload(); // Reload the page to reflect the changes in the game list
                    } else {
                        alert('Failed to delete the game. Please try again.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                })
                .finally(() => {
                    // Re-enable the button after the request is completed
                    button.disabled = false;
                });
            } else {
                // If user cancels the deletion, re-enable the button
                button.disabled = false;
            }
        }

        // Handle add to cart
        if (event.target.classList.contains('add-to-cart')) {
            if (event.target.disabled) {
                return; // Prevent the request if the button is already disabled
            }
            const gameId = event.target.getAttribute('data-game-id');
            // Disable the button to prevent multiple clicks
            event.target.disabled = true;

            const url = `/cart/add/${gameId}/`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ game_id: gameId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateCartCount(data.total_items);
                    sessionStorage.setItem('cart_count', data.total_items); // Save to sessionStorage
                } else {
                    alert('Failed to add to cart. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred.');
            })
            .finally(() => {
                event.target.disabled = false; // Re-enable the button after the request
            });
        }
    });

    // Allow stars to be selected interactively
    document.querySelectorAll('.rating').forEach(ratingDiv => {
        const stars = ratingDiv.querySelectorAll('.fa-star');
        stars.forEach((star, index) => {
            star.addEventListener('click', function () {
                // Reset stars
                stars.forEach(s => s.classList.remove('selected'));
                // Mark stars up to the clicked star as selected
                for (let i = 0; i <= index; i++) {
                    stars[i].classList.add('selected');
                }
            });
        });
    });
});

function updateCartCount(count) {
    const cartCountElement = document.getElementById('cart-count');
    if (count > 0) {
        cartCountElement.textContent = count;
        cartCountElement.classList.remove('d-none');
    } else {
        cartCountElement.textContent = '';
        cartCountElement.classList.add('d-none');
    }
}