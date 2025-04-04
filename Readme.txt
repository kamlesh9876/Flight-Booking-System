✈️ Flight Booking System — Documentation


📚 Overview
This is a GUI-based flight booking system implemented in Python using Tkinter. It allows users to:

Book flight tickets

Cancel tickets using Ticket ID

View all booked tickets

Generate and save an E-Ticket PDF with a QR code

View real-time seat availability per flight

🔧 Features
✅ Seat map with live availability

✅ QR code e-ticket generation (PDF)

✅ Payment simulation interface

✅ Database-backed with MySQL

✅ Modern GUI theme using ttkthemes

✅ Includes popular international/domestic flights

💻 Installation & Setup
📦 Required Python Libraries
Install the dependencies using pip:

bash
Copy
Edit
pip install tkcalendar
pip install ttkthemes
pip install mysql-connector-python
pip install reportlab
pip install qrcode[pil]
🗃️ MySQL Database Setup
Open MySQL terminal or MySQL Workbench.

USE flight_booking;
SELECT * FROM bookings;


python
Copy
Edit
user='root'
password='root@999'
Ensure these are correctly set or updated in the code if needed.

The system auto-creates the bookings table if it doesn't exist:

sql
Copy
Edit
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    flight VARCHAR(50),
    date DATE,
    seat VARCHAR(10),
    price DECIMAL(10,2)
);


🖼️ GUI Components & Functions
🧾 Booking Form:
Fields: Name, Flight (Dropdown), Date (Calendar), Seat

Seat Map: 24 Seats in 4 columns (A–D), live availability

Price Auto-Calculation: Based on seat row

E-Ticket Generation: After payment, with QR and PDF download

❌ Cancel Ticket:
Cancel booking using Ticket ID

📋 View Bookings:
Table of all bookings (ID, Name, Flight, Date, Seat, Price)

💡 Functional Highlights
Seat Pricing
python
Copy
Edit
SEAT_PRICES = {
    'A': 2000,
    'B': 1500,
    'C': 1500,
    'D': 2000
}
Payment Simulation
A simulated form that captures cardholder data

Confirmation pop-up on successful "payment"

E-Ticket PDF
Generated using reportlab

Includes:

Ticket info

QR code with booking summary

Branded heading and footer

Saved via a file dialog

Seat Availability Management
Updated dynamically based on selected flight & date

Red = Booked, Green = Available

🧩 Code Structure
Function	Description
connect_db()	Connects to MySQL database
create_table()	Creates the bookings table
book_ticket()	Handles booking flow
cancel_ticket()	Cancels a booking by ID
show_payment_window()	Simulates payment
finalize_booking()	Finalizes booking and saves to DB
generate_eticket()	Creates and saves a PDF ticket
is_seat_available()	Checks if a seat is taken
calculate_price()	Computes seat price
update_seat_map()	Refreshes seat buttons per flight/date
choose_seat(seat)	Selects seat and shows price
load_bookings()	Loads bookings in Treeview


📁 File Structure
bash
Copy
Edit
project/
│
├── main.py                # Main script with full GUI and logic
├── etickets/              # Folder for saving QR images & PDFs
│   ├── qr_1.png
│   └── eticket_1.pdf


🧪 Usage Instructions
Run the script:

bash
Copy
Edit
python main.py
GUI Opens:

Book tickets, select date/flight, pick seat.

Pay and download e-ticket.

Cancel or view tickets via sidebar.