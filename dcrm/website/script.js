// Select the element with the btn-close class
const btnCloseElement = document.querySelectorAll('.btn-close');

// Function to fade out and remove the element
setTimeout(() => {
  btnCloseElement.classList.add('hidden'); // Fade out
  setTimeout(() => {
    btnCloseElement.style.display = 'none'; // Hide the element completely
  }, 1000); // Wait for the fade-out animation to complete
}, 3000); // Start fading out after 3 seconds
