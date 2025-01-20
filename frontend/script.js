const API_URL = "http://127.0.0.1:5000";

// Store logged-in user ID
let userId = null;

// Register a user
document.getElementById("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const goal = document.getElementById("goal").value;

    const response = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password, goal }),
    });

    const result = await response.json();
    alert(result.message || "Registration successful!");
});

// Login a user
document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });

    const result = await response.json();
    if (result.user_id) {
        alert("Login successful!");
        userId = result.user_id;  // Store user_id globally
        sessionStorage.setItem("user_id", userId);  // Optional: Store in sessionStorage
        document.getElementById("plansSection").style.display = "block";
    } else {
        alert(result.error || "Login failed!");
    }
});

// Generate plans (FIXED: Sends `user_id`)
document.getElementById("generatePlansButton").addEventListener("click", async () => {
    if (!userId) {
        alert("You need to log in first!");
        return;
    }

    const goal = document.getElementById("goal").value; // Fetch user goal

    const response = await fetch(`${API_URL}/plans/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, goal }),
    });

    const result = await response.json();
    if (result.message) {
        alert(result.message);
    } else {
        alert(result.error || "Failed to generate plans!");
    }
});

// View plans (FIXED: Sends `user_id` as query parameter)
document.getElementById("viewPlansButton").addEventListener("click", async () => {
    if (!userId) {
        alert("You need to log in first!");
        return;
    }

    const response = await fetch(`${API_URL}/plans/retrieve?user_id=${userId}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
    });

    const result = await response.json();

    if (result.workout_plans && result.diet_plans) {
        const plansContainer = document.getElementById("plansContainer");
        plansContainer.innerHTML = ""; // Clear previous content

        // Display workout plans
        const workoutTitle = document.createElement("h3");
        workoutTitle.textContent = "Workout Plans";
        plansContainer.appendChild(workoutTitle);

        result.workout_plans.forEach((plan) => {
            const planItem = document.createElement("div");
            planItem.textContent = `${plan.day_of_week}: ${plan.workout_routine}`;
            plansContainer.appendChild(planItem);
        });

        // Display diet plans
        const dietTitle = document.createElement("h3");
        dietTitle.textContent = "Diet Plans";
        plansContainer.appendChild(dietTitle);

        result.diet_plans.forEach((plan) => {
            const planItem = document.createElement("div");
            planItem.textContent = `${plan.day_of_week}: ${plan.diet_routine}`;
            plansContainer.appendChild(planItem);
        });
    } else {
        alert(result.error || "No plans available!");
    }
});

// Fetch a random motivational quote
document.getElementById("getQuote").addEventListener("click", async () => {
    const response = await fetch(`${API_URL}/quotes/random`);
    const result = await response.json();

    if (result.quote) {
        document.getElementById("quote").textContent = result.quote;
    } else {
        alert(result.error || "Failed to fetch quote!");
    }
});

// Store user_id after login (FIXED)
async function login(email, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    if (response.ok) {
        const data = await response.json();
        console.log("Logged in as User ID:", data.user_id);
        userId = data.user_id; // Store user_id globally
        sessionStorage.setItem("user_id", userId); // Store user_id in session storage
    } else {
        console.error("Login failed");
    }
}
