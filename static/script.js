// script.js

const form = document.getElementById('countryForm');
const countryInput = document.getElementById('countryInput');
const validCountries = ['United States', 'Country2', 'Country3']; 

form.addEventListener('submit', function(event) {
  event.preventDefault();

  const enteredCountry = countryInput.value.trim();

  if (enteredCountry === '') {
    alert('Please enter a country name.');
    return;
  }

  if (!isValidCountry(enteredCountry)) {
    alert('Invalid country. Please enter a valid country.');
    return;
  }
  
  // Redirect to countryInformation route in Flask
  window.location.href = `/countryInformation?country=${encodeURIComponent(enteredCountry)}`;
});

function isValidCountry(country) {
  return validCountries.includes(country);
}

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
