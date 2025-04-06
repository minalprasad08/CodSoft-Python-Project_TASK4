import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from ttkthemes import ThemedTk

def init_db():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        email TEXT,
                        address TEXT)''')
    conn.commit()
    conn.close()

def add_contact():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    address = entry_address.get()
    
    if not name or not phone:
        messagebox.showerror("Error", "Name and Phone are required!")
        return
    
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)", (name, phone, email, address))
    conn.commit()
    conn.close()
    
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    
    messagebox.showinfo("Success", "Contact added successfully!")
    view_contacts()

def view_contacts():
    for row in tree.get_children():
        tree.delete(row)
    
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone FROM contacts")
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        tree.insert("", tk.END, values=row)

def search_contact():
    query = entry_search.get()
    for row in tree.get_children():
        tree.delete(row)
    
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone FROM contacts WHERE name LIKE ? OR phone LIKE ?", (f"%{query}%", f"%{query}%"))
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        tree.insert("", tk.END, values=row)

def delete_contact():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a contact to delete.")
        return
    
    contact_id = tree.item(selected_item)['values'][0]
    
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Contact deleted successfully!")
    view_contacts()

# GUI Setup
root = ThemedTk(theme="breeze")
root.title("Contact Book")
root.geometry("600x500")
root.configure(bg="#d1c4e9")  # Light purple background

style = ttk.Style()
style.configure("TButton", font=("Arial", 12, "bold"), background="#1E88E5", foreground="black", padding=5)
style.map("TButton", background=[("active", "#0D47A1")])  # Dark blue on hover
style.configure("TLabel", font=("Arial", 11, "bold"), background="#d1c4e9", foreground="black")
style.configure("TEntry", font=("Arial", 11), padding=5)
style.configure("Treeview", font=("Arial", 11), rowheight=25, background="#E3F2FD", foreground="black")  # Light blue background
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#3949AB", foreground="black")  # Dark blue heading

frame = ttk.Frame(root, padding=10, style="TFrame")
frame.pack(pady=10)

lbl_name = ttk.Label(frame, text="Name:")
lbl_name.grid(row=0, column=0)
entry_name = ttk.Entry(frame, width=30)
entry_name.grid(row=0, column=1)

lbl_phone = ttk.Label(frame, text="Phone:")
lbl_phone.grid(row=1, column=0)
entry_phone = ttk.Entry(frame, width=30)
entry_phone.grid(row=1, column=1)

lbl_email = ttk.Label(frame, text="Email:")
lbl_email.grid(row=2, column=0)
entry_email = ttk.Entry(frame, width=30)
entry_email.grid(row=2, column=1)

lbl_address = ttk.Label(frame, text="Address:")
lbl_address.grid(row=3, column=0)
entry_address = ttk.Entry(frame, width=30)
entry_address.grid(row=3, column=1)

btn_add = ttk.Button(root, text="Add Contact", command=add_contact)
btn_add.pack(pady=5)

entry_search = ttk.Entry(root, width=30)
entry_search.pack()
btn_search = ttk.Button(root, text="Search", command=search_contact)
btn_search.pack(pady=5)

btn_delete = ttk.Button(root, text="Delete Contact", command=delete_contact)
btn_delete.pack(pady=5)

tree = ttk.Treeview(root, columns=("ID", "Name", "Phone"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

init_db()
view_contacts()
root.mainloop()

