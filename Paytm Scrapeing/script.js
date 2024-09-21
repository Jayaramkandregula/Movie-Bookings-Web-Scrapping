document.addEventListener("DOMContentLoaded", function () {
    const theatreContainer = document.getElementById("theatre-container");
    const createTheatreButton = document.getElementById("create-theatre");
    const theatreList = document.getElementById("theatre-list");

    loadTheatres();

    createTheatreButton.addEventListener("click", function () {
        const theatreName = document.getElementById("theatre-name").value.trim();
        const showTime = document.getElementById("show-time").value.trim();
        const ticketPrice = parseFloat(document.getElementById("ticket-price").value.trim());

        if (!theatreName || !showTime || isNaN(ticketPrice) || ticketPrice <= 0) {
            alert("Please fill all the fields with valid data");
            return;
        }

        const uniqueKey = ${theatreName}_${showTime};

        if (!localStorage.getItem(uniqueKey)) {
            localStorage.setItem(uniqueKey, JSON.stringify({
                totalAmount: 0,
                selectedSeats: {},
                ticketPrice: ticketPrice
            }));
        }

        loadTheatreSection(uniqueKey, theatreName, showTime);
    });

    function loadTheatreSection(uniqueKey, theatreName, showTime) {
        const theatreData = JSON.parse(localStorage.getItem(uniqueKey));
        const theatreDiv = document.createElement("div");
        theatreDiv.classList.add("theatre");

        theatreDiv.innerHTML = `
            <h2>${theatreName} - ${showTime}</h2>
            <label for="ticket-price-${uniqueKey}">Ticket Price:</label>
            <input type="number" id="ticket-price-${uniqueKey}" value="${theatreData.ticketPrice}" />
            <p>Total Amount: <span class="total-amount">${theatreData.totalAmount.toFixed(2)}</span></p>
            <div class="grid-container" data-key="${uniqueKey}">
            </div>
            <button class="finish-btn">Finish</button>
            <button class="delete-btn">Delete Theatre</button>
        `;

        theatreContainer.innerHTML = ''; // Clear previous theatre
        theatreContainer.appendChild(theatreDiv);

        generateGrid(theatreDiv.querySelector(".grid-container"));

        const finishBtn = theatreDiv.querySelector(".finish-btn");
        finishBtn.addEventListener("click", function () {
            const updatedTicketPrice = parseFloat(document.getElementById(ticket-price-${uniqueKey}).value);
            if (!isNaN(updatedTicketPrice) && updatedTicketPrice > 0) {
                saveTheatreData(uniqueKey, updatedTicketPrice);
                alert("Theatre layout and ticket price saved.");
            } else {
                alert("Please enter a valid ticket price.");
            }
        });

        const deleteBtn = theatreDiv.querySelector(".delete-btn");
        deleteBtn.addEventListener("click", function () {
            deleteTheatre(uniqueKey);
        });
    }

    function generateGrid(gridElement) {
        const uniqueKey = gridElement.dataset.key;
        const theatreData = JSON.parse(localStorage.getItem(uniqueKey));
        const selectedSeats = theatreData.selectedSeats;
        const totalAmountElement = gridElement.closest(".theatre").querySelector(".total-amount");
        const ticketPriceInput = gridElement.closest(".theatre").querySelector(#ticket-price-${uniqueKey});

        const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        for (let row = 1; row <= 15; row++) {  // 15 rows
            for (let seat = 1; seat <= 20; seat++) {  // 20 seats per row
                const rowLetter = alphabet[row - 1]; // Convert to alphabet
                const seatIndex = ${rowLetter}-${seat};
                const box = document.createElement("div");
                box.classList.add("grid-item");
                box.dataset.index = seatIndex;
                box.innerHTML = ${rowLetter}-${seat};  // Row and Seat Number

                if (selectedSeats[seatIndex]) {
                    box.classList.add("blocked");
                }

                box.addEventListener("click", function () {
                    handleSeatClick(box, uniqueKey, seatIndex, parseFloat(ticketPriceInput.value), totalAmountElement);
                });

                gridElement.appendChild(box);
            }
        }
    }

    function handleSeatClick(box, uniqueKey, seatIndex, ticketPrice, totalAmountElement) {
        const theatreData = JSON.parse(localStorage.getItem(uniqueKey));

        if (box.classList.contains("blocked")) {
            box.classList.remove("blocked");
            theatreData.totalAmount -= ticketPrice;
            delete theatreData.selectedSeats[seatIndex];
        } else {
            box.classList.add("blocked");
            theatreData.totalAmount += ticketPrice;
            theatreData.selectedSeats[seatIndex] = true;
        }

        totalAmountElement.textContent = theatreData.totalAmount.toFixed(2);
        localStorage.setItem(uniqueKey, JSON.stringify(theatreData));
    }

    function saveTheatreData(uniqueKey, ticketPrice) {
        const theatreData = JSON.parse(localStorage.getItem(uniqueKey));
        theatreData.ticketPrice = ticketPrice;
        localStorage.setItem(uniqueKey, JSON.stringify(theatreData));
    }

    function deleteTheatre(uniqueKey) {
        if (confirm("Are you sure you want to delete this theatre?")) {
            localStorage.removeItem(uniqueKey);
            theatreContainer.innerHTML = '';  // Clear current layout
            loadTheatres();  // Refresh the list of theatres
        }
    }

    function loadTheatres() {
        theatreList.innerHTML = '';
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key.includes("_")) {
                const [theatreName, showTime] = key.split("_");
                const listItem = document.createElement("li");
                listItem.textContent = ${theatreName} - ${showTime};
                listItem.addEventListener("click", function () {
                    loadTheatreSection(key, theatreName, showTime);
                });
                theatreList.appendChild(listItem);
            }
        }
    }
});