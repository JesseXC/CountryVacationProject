// script.js

const form = document.getElementById('countryForm');
const countryInput = document.getElementById('countryInput');

destinationForm.addEventListener('submit', function(event) {
  event.preventDefault();

  const enteredCountry = countryInput.value.trim();
  const enteredCity = cityInput.value.trim();

  if (enteredCountry === '') {
    alert('Please enter a country name.');
    return;
  }

  if (enteredCity === '') {
    alert('Please enter a city name.');
    return;
  }

  verifyCountryAndCity(enteredCountry, enteredCity);
});

function isValidCountry(country) {
  return validCountries.includes(country);
}

function verifyCountryAndCity(country, city) {
  const countryUrl = `https://restcountries.com/v3/name/${country}`;

  // Verify the country first
  fetch(countryUrl)
    .then(response => {
      if (!response.ok) {
        throw new Error('Invalid country. Please enter a valid country.');
      }
      return response.json();
    })
    .then(data => {
      if (!data || data.length === 0 || !data[0].hasOwnProperty('cca2')) {
        throw new Error('Invalid country data or missing alpha2Code.');
      }
      const alpha2Code = data[0].cca2;
      // If the country is valid, verify the city
      const cityUrl = `http://api.geonames.org/searchJSON?q=${city}&country=${alpha2Code}&username=jessemeci`;

      return fetch(cityUrl)
        .then(response => response.json())
        .then(data => {
          if (!data || !data.geonames || data.geonames.length === 0) {
            throw new Error('Invalid city or city does not exist in the specified country.');
          }
          // If both country and city are valid, redirect to the destinationInformation route in Flask
          const url = `/countryInformation?country=${encodeURIComponent(country)}&city=${encodeURIComponent(city)}`;
          window.location.href = url;
        });
    })
    .catch(error => {
      alert(error.message);
    });
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