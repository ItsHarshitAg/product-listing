/**
 * Main JavaScript file for the Product Listing application
 */

// Handle error responses from fetch
function handleFetchError(response) {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response;
}

// Update cart count badge in the navbar
async function updateCartCount() {
    try {
        const response = await fetch('/api/cart/');
        handleFetchError(response);
        
        const cart = await response.json();
        document.getElementById('cart-count').textContent = cart.count;
    } catch (error) {
        console.error('Error updating cart count:', error);
    }
}

// Initialize the page when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Update cart count when page loads
    updateCartCount();
    
    // Add scroll-to-top button functionality if it exists
    const scrollTopBtn = document.getElementById('scroll-top-btn');
    if (scrollTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                scrollTopBtn.classList.remove('d-none');
            } else {
                scrollTopBtn.classList.add('d-none');
            }
        });
        
        scrollTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});
