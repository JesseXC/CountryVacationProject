// script.js

// Form Validation
const form = document.querySelector('form');

form.addEventListener('submit', function(event) {
  event.preventDefault();
  
  // Perform form validation logic here
  
  // Example: Check if the country name is entered
  const countryInput = form.elements.countryName;
  if (countryInput.value.trim() === '') {
    // Display an error message
    alert('Please enter a country name.');
    return;
  }
  
  // Proceed with submitting the form
  form.submit();
});

// Image Slider
const slides = document.querySelectorAll('.slider .slide');
let currentSlide = 0;

function showSlide(slideIndex) {
  // Hide all slides
  slides.forEach(slide => {
    slide.style.display = 'none';
  });

  // Display the current slide
  slides[slideIndex].style.display = 'block';
}

function nextSlide() {
  currentSlide = (currentSlide + 1) % slides.length;
  showSlide(currentSlide);
}

function previousSlide() {
  currentSlide = (currentSlide - 1 + slides.length) % slides.length;
  showSlide(currentSlide);
}

// Show the initial slide
showSlide(currentSlide);

// Smooth Scrolling
const anchorLinks = document.querySelectorAll('a[href^="#"]');

anchorLinks.forEach(link => {
  link.addEventListener('click', function(event) {
    event.preventDefault();
    
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      window.scrollTo({
        top: target.offsetTop,
        behavior: 'smooth'
      });
    }
  });
});
