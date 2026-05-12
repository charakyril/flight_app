<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Flight App Queries</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; }
    h1, h2 { color: #2a4d69; }
    form { margin-bottom: 28px; padding: 14px; border: 1px solid #ccc; }
    label { display: block; margin-top: 8px; }
    input[type="text"], input[type="date"], select { width: 280px; margin-top: 4px; padding: 6px; }
    button { margin-top: 12px; padding: 8px 14px; }
    .note { font-size: 0.95em; color: #555; }
  </style>
</head>
<body>
  <h1>Flight App Queries</h1>
  <p class="note">Run the server with <code>python app.py</code> and open <strong>http://localhost:8080</strong>.</p>

  <h2>1. Find Airline by Age</h2>
  <form action="/findAirlineByAge" method="post">
    <label>Maximum age (X): <input type="text" name="x" required /></label>
    <label>Minimum age (Y): <input type="text" name="y" required /></label>
    <button type="submit">Search</button>
  </form>

  <h2>2. Find Airport Visitors</h2>
  <form action="/findAirportVisitors" method="post">
    <label>Airline name: <input type="text" name="airline" required /></label>
    <label>Start date (YYYY-MM-DD): <input type="date" name="date_a" required /></label>
    <label>End date (YYYY-MM-DD): <input type="date" name="date_b" required /></label>
    <button type="submit">Search</button>
  </form>

  <h2>3. Find Alternative Flights</h2>
  <form action="/findAlternativeFlights" method="post">
    <label>Source city: <input type="text" name="source_city" required /></label>
    <label>Destination city: <input type="text" name="destination_city" required /></label>
    <label>Travel date (YYYY-MM-DD): <input type="date" name="travel_date" required /></label>
    <button type="submit">Search</button>
  </form>

  <h2>4. Find Largest Airlines</h2>
  <form action="/findLargestAirlines" method="post">
    <label>Number of airlines (N): <input type="text" name="top_n" required /></label>
    <button type="submit">Search</button>
  </form>

  <h2>5. Update Passenger Status</h2>
  <form action="/updatePassengerStatus" method="post">
    <label>Airline name: <input type="text" name="tier_airline" required /></label>
    <label>Tier category:
      <select name="tier_category" required>
        <option value="Basic">Basic</option>
        <option value="Silver">Silver</option>
        <option value="Gold">Gold</option>
        <option value="Platinum">Platinum</option>
      </select>
    </label>
    <button type="submit">Update and Show</button>
  </form>
</body>
</html>
