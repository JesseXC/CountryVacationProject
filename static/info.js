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

  // Create a table to display the flight information
  const table = document.createElement("table");
  table.className = "flight-table";

  // Create table header
  const tableHeader = document.createElement("tr");
  const headerLabels = ["Flight Number", "Available Seats", "Duration", "Price"];
  for (const label of headerLabels) {
    const th = document.createElement("th");
    th.textContent = label;
    tableHeader.appendChild(th);
  }
  table.appendChild(tableHeader);

  // Iterate through each flight and create table rows for flight information
  for (const flightKey in ticketData) {
    const flight = ticketData[flightKey];
    const tableRow = document.createElement("tr");

    // Create table cells for flight details
    const flightNumberCell = document.createElement("td");
    flightNumberCell.textContent = flightKey;

    const seatsCell = document.createElement("td");
    seatsCell.textContent = flight.numberofBookableSeats;

    const durationCell = document.createElement("td");
    durationCell.textContent = flight.totalDuration;

    const priceCell = document.createElement("td");
    priceCell.textContent = `${flight.currency} ${flight.total_price}`;

    // Append cells to the table row
    tableRow.appendChild(flightNumberCell);
    tableRow.appendChild(seatsCell);
    tableRow.appendChild(durationCell);
    tableRow.appendChild(priceCell);

    // Append the table row to the table
    table.appendChild(tableRow);
  }

  // Append the table to the flight results container
  flightResultsContainer.appendChild(table);
}

console.log("JavaScript code executed!");
