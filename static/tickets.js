// tickets.js
const form = document.getElementById("flight-form");
const flightResultsDiv = document.getElementById("flight-results");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const departure = document.getElementById("departure").value;
  const arrival = document.getElementById("arrival").value;
  const travelDate = document.getElementById("travel-date").value;
  const passengers = document.getElementById("passengers").value;

  const accessToken = "fZS0EEgq1a3IfK5tispBWwUixqjQMGWS"; 
  const headers = {
    Authorization: `Bearer ${accessToken}`,
  };

  try {
    const flightDestinations = await getFlightDestinations(departure, headers);
    displayFlightDestinations(flightDestinations.data);

    const cheapestDate = await getCheapestDate(departure, arrival, headers);
    console.log("Cheapest Date:", cheapestDate.data);

    const flightOffers = await getFlightOffers(departure, arrival, travelDate, passengers, headers);
    console.log("Flight Offers:", flightOffers.data);


  } catch (error) {
    console.error("Error:", error);
  }
});

async function getFlightDestinations(origin, headers) {
  const response = await fetch(`https://test.api.amadeus.com/v1/shopping/flight_destinations?origin=${origin}`, { headers });
  return response.json();
}

async function getCheapestDate(origin, destination, headers) {
  const response = await fetch(`https://test.api.amadeus.com/v1/shopping/flight_dates?origin=${origin}&destination=${destination}`, { headers });
  return response.json();
}

async function getFlightOffers(origin, destination, departureDate, passengers, headers) {
  const apiUrl = `https://test.api.amadeus.com/v1/shopping/flight_offers_search?originLocationCode=${origin}&destinationLocationCode=${destination}&departureDate=${departureDate}&adults=${passengers}`;
  const response = await fetch(apiUrl, { headers });
  return response.json();
}


function displayFlightDestinations(destinations) {
  
  flightResultsDiv.innerHTML = "";

 
  destinations.forEach((destination) => {
    const destinationDiv = document.createElement("div");
    destinationDiv.classList.add("flight-destination");

    const origin = destination.origin;
    const destinationName = destination.destination;
    const departureDate = destination.departureDate;
    const price = destination.price.total;

    destinationDiv.innerHTML = `
      <p><strong>Origin:</strong> ${origin}</p>
      <p><strong>Destination:</strong> ${destinationName}</p>
      <p><strong>Departure Date:</strong> ${departureDate}</p>
      <p><strong>Price:</strong> ${price} EUR</p>
      <hr>
    `;

    flightResultsDiv.appendChild(destinationDiv);
  });
}
