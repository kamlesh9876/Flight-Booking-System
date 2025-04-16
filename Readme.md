<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flight Booking System</title>
</head>
<body>

<h1>✈️ Flight Booking System</h1>

<h2>📚 Overview</h2>
<p>This is a GUI-based flight booking system implemented in Python using Tkinter. It allows users to:</p>
<ul>
    <li>Book flight tickets</li>
    <li>Cancel tickets using Ticket ID</li>
    <li>View all booked tickets</li>
    <li>Generate and save an E-Ticket PDF with a QR code</li>
    <li>View real-time seat availability per flight</li>
</ul>

<h2>🔧 Features</h2>
<ul>
    <li>✅ Seat map with live availability</li>
    <li>✅ QR code e-ticket generation (PDF)</li>
    <li>✅ Payment simulation interface</li>
    <li>✅ Database-backed with MySQL</li>
    <li>✅ Modern GUI theme using ttkthemes</li>
    <li>✅ Includes popular international/domestic flights</li>
</ul>

<h2>💻 Installation & Setup</h2>

<h3>📦 Required Python Libraries</h3>
<p>Install the dependencies using pip:</p>
<pre><code>
pip install tkcalendar
pip install ttkthemes
pip install mysql-connector-python
pip install reportlab
pip install qrcode[pil]
</code></pre>

<h3>🗃️ MySQL Database Setup</h3>
<ol>
    <li>Open MySQL terminal or MySQL Workbench.</li>
    <li>Select your database:</li>
    <pre><code>USE flight_booking;</code></pre>
    <li>Verify the <code>bookings</code> table:</li>
    <pre><code>SELECT * FROM bookings;</code></pre>
    <li>Ensure the following MySQL user credentials are set correctly in the code:</li>
    <pre><code>
user = 'root'
password = 'root@999'
</code></pre>
    <li>The system will auto-create the <code>bookings</code> table if it doesn't exist:</li>
    <pre><code>
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    flight VARCHAR(50),
    date DATE,
    seat VARCHAR(10),
    price DECIMAL(10,2)
);
</code></pre>
</ol>

<h2>🖼️ GUI Components & Functions</h2>

<h3>🧾 Booking Form:</h3>
<ul>
    <li><strong>Fields:</strong> Name, Flight (Dropdown), Date (Calendar), Seat</li>
    <li><strong>Seat Map:</strong> 24 Seats in 4 columns (A–D), live availability</li>
    <li><strong>Price Auto-Calculation:</strong> Based on seat row</li>
    <li><strong>E-Ticket Generation:</strong> After payment, with QR and PDF download</li>
</ul>

<h3>❌ Cancel Ticket:</h3>
<p>Cancel booking using Ticket ID</p>

<h3>📋 View Bookings:</h3>
<p>Table of all bookings (ID, Name, Flight, Date, Seat, Price)</p>

<h2>💡 Functional Highlights</h2>

<h3>Seat Pricing</h3>
<pre><code>
SEAT_PRICES = {
    'A': 2000,
    'B': 1500,
    'C': 1500,
    'D': 2000
}
</code></pre>

<h3>Payment Simulation</h3>
<ul>
    <li>A simulated form that captures cardholder data</li>
    <li>Confirmation pop-up on successful "payment"</li>
</ul>

<h3>E-Ticket PDF</h3>
<p>Generated using <strong>reportlab</strong></p>
<ul>
    <li>Includes:</li>
    <ul>
        <li>Ticket info</li>
        <li>QR code with booking summary</li>
        <li>Branded heading and footer</li>
    </ul>
    <li>Saved via a file dialog</li>
</ul>

<h3>Seat Availability Management</h3>
<ul>
    <li>Updated dynamically based on selected flight & date</li>
    <li><strong>Red</strong> = Booked, <strong>Green</strong> = Available</li>
</ul>

<h2>🧩 Code Structure</h2>

<table border="1">
    <thead>
        <tr>
            <th>Function</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>connect_db()</code></td>
            <td>Connects to MySQL database</td>
        </tr>
        <tr>
            <td><code>create_table()</code></td>
            <td>Creates the bookings table</td>
        </tr>
        <tr>
            <td><code>book_ticket()</code></td>
            <td>Handles booking flow</td>
        </tr>
        <tr>
            <td><code>cancel_ticket()</code></td>
            <td>Cancels a booking by ID</td>
        </tr>
        <tr>
            <td><code>show_payment_window()</code></td>
            <td>Simulates payment</td>
        </tr>
        <tr>
            <td><code>finalize_booking()</code></td>
            <td>Finalizes booking and saves to DB</td>
        </tr>
        <tr>
            <td><code>generate_eticket()</code></td>
            <td>Creates and saves a PDF ticket</td>
        </tr>
        <tr>
            <td><code>is_seat_available()</code></td>
            <td>Checks if a seat is taken</td>
        </tr>
        <tr>
            <td><code>calculate_price()</code></td>
            <td>Computes seat price</td>
        </tr>
        <tr>
            <td><code>update_seat_map()</code></td>
            <td>Refreshes seat buttons per flight/date</td>
        </tr>
        <tr>
            <td><code>choose_seat(seat)</code></td>
            <td>Selects seat and shows price</td>
        </tr>
        <tr>
            <td><code>load_bookings()</code></td>
            <td>Loads bookings in Treeview</td>
        </tr>
    </tbody>
</table>

<h2>📁 File Structure</h2>

<pre><code>
project/
│
├── main.py                # Main script with full GUI and logic
├── etickets/              # Folder for saving QR images & PDFs
│   ├── qr_1.png
│   └── eticket_1.pdf
</code></pre>

<h2>🧪 Usage Instructions</h2>
<ol>
    <li>Run the script:</li>
    <pre><code>python main.py</code></pre>
    <li>The GUI will open:</li>
    <ul>
        <li>Book tickets by selecting date/flight and picking a seat.</li>
        <li>Pay and download the e-ticket.</li>
        <li>Cancel or view tickets via the sidebar.</li>
    </ul>
</ol>

</body>
</html>
