let tabs = document.querySelector(".tabs");
let tabHeader = tabs.querySelector(".tab-header");
let tabHeaderNodes = tabs.querySelectorAll(".tab-header > div");
let tabContent = tabs.querySelector(".tab-content");
let tabContentNodes = tabs.querySelectorAll(".tab-content > div");

for (let i = 0; i < tabHeaderNodes.length; i++) {
  tabHeaderNodes[i].addEventListener("click", function() {
    tabHeader.querySelector(".active").classList.remove("active");
    tabHeaderNodes[i].classList.add("active");
    tabContent.querySelector(".active").classList.remove("active");
    tabContentNodes[i].classList.add("active");
  });
}

const flightForm = document.getElementById("flight-form");
const flightResultsContainer = document.getElementById("flight-results");

flightForm.addEventListener("submit", function(event) {
  event.preventDefault();
  const departure = flightForm.elements["departure"].value;
  const arrival = flightForm.elements["arrival"].value;
  const travelDate = flightForm.elements["travel-date"].value;
  const passengers = flightForm.elements["passengers"].value;

  // Make an API request to the Python backend using fetch
  fetch('/get_ticket_info', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      departure,
      arrival,
      travelDate,
      passengers,
    }),
  })
    .then(response => response.json())
    .then(data => {
      // Handle the ticket information received from the backend
      displayTicketInformation(data);
    })
    .catch(error => {
      console.error("Error fetching ticket information:", error);
    });
});

function displayTicketInformation(ticketData) {
  const flightResultsContainer = document.getElementById("flight-results");

  // Clear previous search results
  flightResultsContainer.innerHTML = "";

  // Check if any flights were found
  if (Object.keys(ticketData).length === 0) {
    flightResultsContainer.innerHTML = "<p>No flights found for the given criteria.</p>";
    return;
  }

  // Iterate through each flight and create elements to display the flight information
  for (const flightKey in ticketData) {
    const flight = ticketData[flightKey];
    const flightElement = document.createElement("div");
    flightElement.className = "flight-info";

    // Create elements to display flight details (you can customize this part as needed)
    const flightNumberElement = document.createElement("p");
    flightNumberElement.textContent = `Flight Number: ${flightKey}`;

    const seatsElement = document.createElement("p");
    seatsElement.textContent = `Available Seats: ${flight.numberofBookableSeats}`;

    const durationElement = document.createElement("p");
    durationElement.textContent = `Duration: ${flight.totalDuration}`;

    const priceElement = document.createElement("p");
    priceElement.textContent = `Price: ${flight.currency} ${flight.total_price}`;

    flightElement.appendChild(flightNumberElement);
    flightElement.appendChild(seatsElement);
    flightElement.appendChild(durationElement);
    flightElement.appendChild(priceElement);

    // Append the flight information element to the flight results container
    flightResultsContainer.appendChild(flightElement);
  }
}
console.log("JavaScript code executed!");
