document.addEventListener("DOMContentLoaded", function () {
    // Get references to various DOM elements
    const registrationForm = document.getElementById("registrationForm");
    const playlistItems = document.querySelectorAll(".playlist-item");
    const songImages = document.querySelectorAll(".playlist-item img");

    // Right-click event on playlist images
    songImages.forEach((image) => {
        image.addEventListener("contextmenu", function (event) {
            event.preventDefault();
            alert("Right-click is disabled on playlist images.");
        });
    });

    // Hover event on playlist items
    playlistItems.forEach((item) => {
        item.addEventListener("mouseover", function () {
            this.style.boxShadow = "0px 0px 20px rgba(235, 40, 40, 0.548)"; // Adds a soft shadow  
            this.style.borderRadius = "10px"; // Adds rounded corners  
            this.style.transform = "scale(1.05)"; // Slightly increases size on hover  
            this.style.opacity = "0.8"; // Reduces opacity for a faded effect  
        });
        item.addEventListener("mouseout", function () {
            this.style.boxShadow = ""; // Adds a soft shadow  
            this.style.borderRadius = ""; // Adds rounded corners  
            this.style.transform = ""; // Slightly increases size on hover  
            this.style.opacity = ""; // Reduces opacity for a faded effect  
        });
    });


    const uploadForm = document.getElementById("uploadForm");


    // Create tables for users and songs dynamically
    const tableContainer = document.getElementById("tableContainer");
    tableContainer.innerHTML = `
    <h2>Stored Users</h2>
    <table id="userTable" border="1">
        <thead>
            <tr><th>Name</th><th>Email</th><th>Gender</th><th>Date of Birth</th></tr>
        </thead>
        <tbody></tbody>
    </table>

    <h2>Uploaded Songs</h2>
    <table id="songTable" border="1">
        <thead>
            <tr><th>Song Title</th><th>Artist</th><th>Genre</th><th>File Name</th><th>Description</th></tr>
        </thead>
        <tbody></tbody>
    </table>

    <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px;">
        <button id="clearUserStorage" style="background-color: crimson; color: white; padding: 10px 20px; border: none; border-radius: 5px;">
            Clear User Storage
        </button>

        <button id="clearSongStorage" style="background-color: crimson; color: white; padding: 10px 20px; border: none; border-radius: 5px;">
            Clear Song Storage
        </button>
    </div>
`;
    //document.body.appendChild(tableContainer);


    // Function to update the user and song tables
    function updateTables() {
        const userTableBody = document.querySelector("#userTable tbody");
        const songTableBody = document.querySelector("#songTable tbody");

        userTableBody.innerHTML = "";
        songTableBody.innerHTML = "";

        // Retrieve stored users and songs from localStorage
        const users = JSON.parse(localStorage.getItem("users")) || [];
        const songs = JSON.parse(localStorage.getItem("songs")) || [];

        // Display users in the table
        if (users.length === 0) {
            userTableBody.innerHTML = `<tr><td colspan="4" style="text-align:center; color: gray;">No users stored.</td></tr>`;
        } else {
            users.forEach(user => {
                const row = document.createElement("tr");
                row.innerHTML = `<td>${user.name}</td><td>${user.email}</td><td>${user.gender}</td><td>${user.dob}</td>`;
                userTableBody.appendChild(row);
            });
        }
    
        // Display songs in the table
        if (songs.length === 0) {
            songTableBody.innerHTML = `<tr><td colspan="5" style="text-align:center; color: gray;">No songs uploaded.</td></tr>`;
        } else {
            songs.forEach(song => {
                const row = document.createElement("tr");
                row.innerHTML = `<td>${song.title}</td><td>${song.artist}</td><td>${song.genre}</td><td>${song.fileName}</td><td>${song.description}</td>`;
                songTableBody.appendChild(row);
            });
        }
     
    }

    // Menu Toggle functionality
    const menuToggle = document.getElementById("menu-toggle");
    const sideMenu = document.getElementById("side-menu");
    const closeMenu = document.getElementById("close-menu");

    menuToggle.addEventListener("click", function () {
        sideMenu.style.left = "0";
        menuToggle.style.display = "none";
    });

    closeMenu.addEventListener("click", function () {
        sideMenu.style.left = "-250px";
        menuToggle.style.display = "block";
    });

    // Close menu when clicking outside
    document.addEventListener("click", function (event) {
        if (!sideMenu.contains(event.target) && !menuToggle.contains(event.target)) {
            sideMenu.style.left = "-250px";
            menuToggle.style.display = "block";
        }
    });

    // Registration Form Validation & Storage
    registrationForm.addEventListener("submit", function (event) {
        if (!confirm("Are you sure you want to submit the form?")) {
        event.preventDefault();
        }else{

        
        let valid = true;

        // Get form values
        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const gender = document.getElementById("gender").value;
        const dob = document.getElementById("dob").value;
        const password = document.getElementById("password").value;

        // Name Validation
        if (name.length < 3) {
            document.getElementById("nameError").textContent = "Name must be at least 3 characters long.";
            valid = false;
        } else {
            document.getElementById("nameError").textContent = "";
        }

        // Email Validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            document.getElementById("emailError").textContent = "Invalid email format.";
            valid = false;
        } else {
            document.getElementById("emailError").textContent = "";
        }

        // Password Validation
        const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{6,}$/;
        if (!passwordPattern.test(password)) {
            document.getElementById("passwordError").textContent = "Password must have 6+ chars, uppercase, lowercase, number, and special char.";
            valid = false;
        } else {
            document.getElementById("passwordError").textContent = "";
        }
        
        if (valid) {
            const users = JSON.parse(localStorage.getItem("users")) || [];
            users.push({ name, email, gender, dob });
            localStorage.setItem("users", JSON.stringify(users));
            updateTables();
            alert("Registered successfully!");
            registrationForm.reset();
        }
                
    }



    });

    // Upload Form Validation & Storage
    uploadForm.addEventListener("submit", function (event) {
        if (!confirm("Are you sure you want to submit the form?")) {
            event.preventDefault(); // Prevent form submission
        }else{
            const title = document.getElementById("title").value.trim();
            const artist = document.getElementById("artist").value.trim();
            const genre = document.getElementById("genre").value;
            const file = document.getElementById("musicFile").files[0];
            const description = document.getElementById("description").value.trim();

            if (!title || !artist || !genre) {
                alert("Please fill out all required fields.");
                return;
            }

            if (file && file.size > 5 * 1024 * 1024) { // Limit file size to 5MB
                alert("File size should not exceed 5MB.");
                return;
            }

            const fileName = file ? file.name : "No file uploaded";
            const songs = JSON.parse(localStorage.getItem("songs")) || [];
            songs.push({ title, artist, genre, fileName, description });
            localStorage.setItem("songs", JSON.stringify(songs));
            updateTables();
            alert("Music uploaded successfully!");
            uploadForm.reset();
        }
    });

    // Add event listener to clear User Storage
    document.getElementById("clearUserStorage").addEventListener("click", function () {
        if (confirm("Are you sure you want to clear all user registrations?")) {
            localStorage.removeItem("users");
            updateTables();
            alert("User storage cleared successfully.");
        }
    });

    // Add event listener to clear Song Storage
    document.getElementById("clearSongStorage").addEventListener("click", function () {
        if (confirm("Are you sure you want to clear all uploaded songs?")) {
            localStorage.removeItem("songs");
            updateTables();
            alert("Song storage cleared successfully.");
        }
    });

    // Initial table update when page loads
    updateTables();
});


