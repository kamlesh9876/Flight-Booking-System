import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from ttkthemes import ThemedTk
import mysql.connector
from datetime import date
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import qrcode
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

# Sample price data per seat (customizable)
SEAT_PRICES = {
    'A': 2000,
    'B': 1500,
    'C': 1500,
    'D': 2000
}

POPULAR_FLIGHTS = [
    "AI-202 Delhi to Mumbai",
    "6E-305 Bengaluru to Hyderabad",
    "SG-401 Kolkata to Chennai",
    "UK-202 Goa to Delhi",

    # 🌍 International Flights
    "BA-117 London to New York",
    "AA-100 New York to Los Angeles",
    "EK-501 Dubai to London",
    "SQ-322 Singapore to London",
    "LH-760 Frankfurt to Delhi",
    "AF-256 Paris to São Paulo",
    "QF-10 Melbourne to Singapore",
    "CX-890 Hong Kong to San Francisco",
    "JL-44 Tokyo to Paris",
    "TK-11 Istanbul to Chicago",
    "KE-85 Seoul to Vancouver",
    "EY-101 Abu Dhabi to New York",
    "QR-708 Doha to Washington",
    "AC-873 Toronto to Frankfurt",
    "NZ-1 Auckland to Los Angeles",
    "DL-200 Atlanta to Johannesburg",
    "UA-837 San Francisco to Tokyo",
    "VA-2 Sydney to Abu Dhabi",
    "AZ-610 Rome to Boston"
]

# DB Connection
def connect_db():
    try:
        return mysql.connector.connect(host='localhost', user='root', password='root@999', database='flight_booking')
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Connection Failed: {err}")
        return None

# Create bookings table if not exists
def create_table():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                flight VARCHAR(50),
                date DATE,
                seat VARCHAR(10),
                price DECIMAL(10,2)
            )
        """)
        conn.commit()
        conn.close()

def is_seat_available(flight, date, seat):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM bookings WHERE flight = %s AND date = %s AND seat = %s", (flight, date, seat))
        result = cursor.fetchone()
        conn.close()
        return result[0] == 0
    return False

def load_bookings():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings")
        records = cursor.fetchall()
        tree.delete(*tree.get_children())
        for record in records:
            tree.insert("", "end", values=record)
        conn.close()

def calculate_price(seat):
    if seat:
        seat_row = seat[0]
        return SEAT_PRICES.get(seat_row.upper(), 100)
    return 0

def generate_eticket(ticket_id, name, flight, date_val, seat, price):
    if not os.path.exists("etickets"):
        os.makedirs("etickets")

    save_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        initialfile=f"eticket_{ticket_id}.pdf",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not save_path:
        return

    # Generate QR Code
    qr_data = f"Ticket ID: {ticket_id}\nName: {name}\nFlight: {flight}\nDate: {date_val}\nSeat: {seat}\nPrice: ₹{price:.2f}"
    qr = qrcode.make(qr_data)
    qr_path = f"etickets/qr_{ticket_id}.png"
    qr.save(qr_path)

    c = canvas.Canvas(save_path, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(colors.darkblue)
    c.drawString(50, height - 70, "✈️  E-Ticket Confirmation")

    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(1.5)
    c.line(50, height - 80, width - 50, height - 80)

    # Ticket Box
    c.setFillColor(colors.whitesmoke)
    c.roundRect(40, height - 330, width - 80, 230, 10, fill=1)

    # Ticket Info
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)
    details = [
        ("Ticket ID", ticket_id),
        ("Passenger Name", name),
        ("Flight", flight),
        ("Date", date_val),
        ("Seat Number", seat),
        ("Price Paid", f"₹{price:.2f}")
    ]

    y_pos = height - 110
    for label, value in details:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, y_pos, f"{label}:")
        c.setFont("Helvetica", 12)
        c.drawString(180, y_pos, str(value))
        y_pos -= 30

    # Divider Line
    c.setStrokeColor(colors.grey)
    c.setLineWidth(0.5)
    c.line(50, y_pos + 10, width - 50, y_pos + 10)

    # Add QR Code Image
    try:
        qr_img = ImageReader(qr_path)
        c.drawImage(qr_img, width - 140, height - 300, width=80, height=80)
    except Exception as e:
        print("Failed to load QR code:", e)

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.grey)
    c.drawString(50, 50, "Thank you for choosing our service. Have a pleasant journey! ✈")

    c.save()

    # Clean up QR image
    os.remove(qr_path)

    messagebox.showinfo("E-Ticket Saved", "Your e-ticket has been downloaded successfully!")
# Payment simulation window
def show_payment_window(name, flight, date_val, seat, price):
    payment_win = tk.Toplevel(root)
    payment_win.title("Payment")
    payment_win.geometry("400x300")
    payment_win.resizable(False, False)

    tk.Label(payment_win, text="Enter Payment Details", font=("Arial", 14, "bold")).pack(pady=10)

    form_frame = tk.Frame(payment_win)
    form_frame.pack(pady=10)

    labels = ["Cardholder Name:", "Card Number:", "Expiry (MM/YY):", "CVV:"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(form_frame, text=label, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(form_frame, width=30, show="*" if label == "CVV:" else None)
        entry.grid(row=i, column=1, pady=5)
        entries.append(entry)

    def process_payment():
        if all(e.get().strip() for e in entries):
            messagebox.showinfo("Payment Successful", "Payment completed successfully!")
            payment_win.destroy()
            finalize_booking(name, flight, date_val, seat, price)
        else:
            messagebox.showerror("Error", "Please fill in all payment fields.")

    tk.Button(payment_win, text="Pay ₹{:.2f}".format(price), command=process_payment, bg="green", fg="white", font=("Arial", 12)).pack(pady=20)

def finalize_booking(name, flight, date_val, seat, price):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bookings (name, flight, date, seat, price) VALUES (%s, %s, %s, %s, %s)",
                       (name, flight, date_val, seat, price))
        conn.commit()
        ticket_id = cursor.lastrowid
        conn.close()
        messagebox.showinfo("Success", f"Ticket Booked Successfully!\nAmount Paid: ₹{price:.2f}")
        update_seat_map()
        generate_eticket(ticket_id, name, flight, date_val, seat, price)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def book_ticket():
    name, flight, date_val, seat = entry_name.get(), combo_flight.get(), entry_date.get(), entry_seat.get()
    if not all([name, flight, date_val, seat]):
        messagebox.showerror("Error", "All fields are required!")
        return
    if not is_seat_available(flight, date_val, seat):
        messagebox.showerror("Error", "Seat unavailable! Please choose another seat.")
        return

    price = calculate_price(seat)
    show_payment_window(name, flight, date_val, seat, price)

def cancel_ticket():
    ticket_id = entry_cancel.get()
    if not ticket_id:
        messagebox.showerror("Error", "Please enter a Ticket ID to cancel!")
        return
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookings WHERE id = %s", (ticket_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Ticket ID {ticket_id} Cancelled Successfully!")
        update_seat_map()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def update_seat_map():
    flight = combo_flight.get()
    date_val = entry_date.get()
    if not flight or not date_val:
        seat_label.config(text="Available Seats: -/24")
        for btn in seat_buttons.values():
            btn.configure(bg="green", state="normal")
        return

    for btn in seat_buttons.values():
        btn.configure(bg="green", state="normal")

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT seat FROM bookings WHERE flight = %s AND date = %s", (flight, date_val))
        booked = cursor.fetchall()
        for (seat,) in booked:
            if seat in seat_buttons:
                seat_buttons[seat].configure(bg="red", state="disabled")
        seat_label.config(text=f"Available Seats: {24 - len(booked)}/24")
        conn.close()

def choose_seat(seat):
    entry_seat.delete(0, tk.END)
    entry_seat.insert(0, seat)
    seat_price = calculate_price(seat)
    seat_price_label.config(text=f"Price: ₹{seat_price:.2f}")

def update_price_from_entry():
    seat = entry_seat.get()
    seat_price = calculate_price(seat)
    seat_price_label.config(text=f"Price: ₹{seat_price:.2f}")

# UI Setup
root = ThemedTk(theme="arc")
root.title("Flight Booking System")
root.geometry("1000x600")

main_frame = tk.Frame(root, bg="#f5f5f5")
main_frame.pack(fill="both", expand=True)

sidebar = tk.Frame(main_frame, bg="#004466", width=220)
sidebar.pack(side="left", fill="y")

ttk.Label(sidebar, text="✈ Flight Menu", font=("Arial", 16, "bold"), background="#004466", foreground="white").pack(pady=20)

buttons = [
    ("📅 Book Ticket", lambda: show_frame(booking_frame)),
    ("❌ Cancel Ticket", lambda: show_frame(cancel_frame)),
    ("📋 View Bookings", lambda: [show_frame(view_frame), load_bookings()]),
    ("🚪 Exit", root.quit)
]
for text, cmd in buttons:
    ttk.Button(sidebar, text=text, command=cmd, width=20).pack(pady=10)

content = tk.Frame(main_frame, bg="#f5f5f5")
content.pack(side="right", expand=True, fill="both")

def show_frame(f):
    f.tkraise()

booking_frame = tk.Frame(content, bg="#f5f5f5")
labels = ["Name:", "Flight:", "Date:", "Seat Number:"]

entry_name = ttk.Entry(booking_frame, width=40)
combo_flight = ttk.Combobox(booking_frame, values=POPULAR_FLIGHTS, width=38, state="readonly")
combo_flight.set(POPULAR_FLIGHTS[0])
entry_date = DateEntry(booking_frame, width=37, background='darkblue', foreground='white', borderwidth=2, mindate=date.today())
entry_seat = ttk.Entry(booking_frame, width=40)
entry_seat.bind("<KeyRelease>", lambda e: update_price_from_entry())

entries = [entry_name, combo_flight, entry_date, entry_seat]
for i, text in enumerate(labels):
    ttk.Label(booking_frame, text=text, font=("Arial", 12), background="#f5f5f5").grid(row=i, column=0, padx=15, pady=7, sticky="w")
    entries[i].grid(row=i, column=1, pady=7)

seat_price_label = ttk.Label(booking_frame, text="Price: ₹0.00", font=("Arial", 12), background="#f5f5f5")
seat_price_label.grid(row=4, column=1, pady=5, sticky="w")

seat_frame = tk.Frame(booking_frame, bg="#f5f5f5")
seat_frame.grid(row=0, column=2, rowspan=6, padx=20)

seat_label = tk.Label(seat_frame, text="Available Seats: 24/24", font=("Arial", 12), bg="#f5f5f5")
seat_label.grid(row=0, column=0, columnspan=5, pady=(0, 10))

seat_buttons = {}
rows = range(1, 7)
left_cols = ['A', 'B']
right_cols = ['C', 'D']

for r in rows:
    for idx, col in enumerate(left_cols):
        seat = f"{col}{r}"
        btn = tk.Button(seat_frame, text=seat, width=4, height=2, bg="green", fg="white", command=lambda s=seat: choose_seat(s))
        btn.grid(row=r, column=idx, padx=2, pady=2)
        seat_buttons[seat] = btn

    tk.Label(seat_frame, text=" ", bg="#f5f5f5", width=2).grid(row=r, column=2)

    for idx, col in enumerate(right_cols):
        seat = f"{col}{r}"
        btn = tk.Button(seat_frame, text=seat, width=4, height=2, bg="green", fg="white", command=lambda s=seat: choose_seat(s))
        btn.grid(row=r, column=3 + idx, padx=2, pady=2)
        seat_buttons[seat] = btn

ttk.Button(booking_frame, text="🛫 Book Ticket", command=book_ticket).grid(row=6, column=0, columnspan=2, pady=15)

cancel_frame = tk.Frame(content, bg="#f5f5f5")
ttk.Label(cancel_frame, text="Enter Ticket ID to Cancel:", font=("Arial", 12), background="#f5f5f5").grid(row=0, column=0, padx=15, pady=7, sticky="w")
entry_cancel = ttk.Entry(cancel_frame, width=25)
entry_cancel.grid(row=0, column=1, pady=7)
ttk.Button(cancel_frame, text="❌ Cancel Ticket", command=cancel_ticket).grid(row=1, column=0, columnspan=2, pady=15)

view_frame = tk.Frame(content, bg="#f5f5f5")
ttk.Label(view_frame, text="Booked Tickets:", font=("Arial", 14, "bold"), background="#f5f5f5").pack(pady=10)

tree = ttk.Treeview(view_frame, columns=("ID", "Name", "Flight", "Date", "Seat", "Price"), show="headings")
for col in ("ID", "Name", "Flight", "Date", "Seat", "Price"):
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(expand=True, fill="both", padx=20, pady=10)

combo_flight.bind("<<ComboboxSelected>>", lambda e: update_seat_map())
entry_date.bind("<<DateEntrySelected>>", lambda e: update_seat_map())

for frame in (booking_frame, cancel_frame, view_frame):
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

create_table()
show_frame(booking_frame)
update_seat_map()
root.mainloop()
