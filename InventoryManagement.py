import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

DATA_FILE = "inventory_data.json"
AUDIT_FILE = "audit_report.txt"
ADMIN_PASSWORD = "admin123"  # Basic security

# --------------------- Data Handling ---------------------

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --------------------- Inventory Operations ---------------------

def stock_in(product, quantity):
    data = load_data()
    quantity = int(quantity)
    if product in data:
        data[product]["stock"] += quantity
    else:
        data[product] = {"stock": quantity, "sales": 0, "removed": 0}
    save_data(data)

def sell_product(product, quantity):
    data = load_data()
    quantity = int(quantity)
    if product in data and data[product]["stock"] >= quantity:
        data[product]["stock"] -= quantity
        data[product]["sales"] += quantity
        save_data(data)
    else:
        messagebox.showerror("Error", "Not enough stock!")

def remove_product(product, quantity):
    data = load_data()
    quantity = int(quantity)
    if product in data and data[product]["stock"] >= quantity:
        data[product]["stock"] -= quantity
        data[product]["removed"] += quantity
        save_data(data)
    else:
        messagebox.showerror("Error", "Invalid removal quantity!")

# --------------------- Audit ---------------------

def generate_audit():
    data = load_data()
    with open(AUDIT_FILE, "w") as f:
        f.write("Inventory Audit Report\n")
        f.write(f"Date: {datetime.now()}\n\n")
        for product, details in data.items():
            f.write(f"{product}: Stock = {details['stock']}, Sold = {details['sales']}, Removed = {details['removed']}\n")
    messagebox.showinfo("Audit", f"Audit report saved to {AUDIT_FILE}")

# --------------------- Security ---------------------

def verify_admin():
    password = simpledialog.askstring("Admin Login", "Enter admin password:", show="*")
    return password == ADMIN_PASSWORD

# --------------------- GUI Setup ---------------------

def main():
    root = tk.Tk()
    root.title("Vendor Inventory Management System")
    root.geometry("400x400")

    def handle_stock_in():
        if not verify_admin(): return
        product = simpledialog.askstring("Stock In", "Enter product name:")
        quantity = simpledialog.askinteger("Stock In", "Enter quantity:")
        stock_in(product, quantity)
        messagebox.showinfo("Success", "Stock added!")

    def handle_sale():
        product = simpledialog.askstring("Sell", "Enter product name:")
        quantity = simpledialog.askinteger("Sell", "Enter quantity:")
        sell_product(product, quantity)
        messagebox.showinfo("Success", "Product sold!")

    def handle_remove():
        if not verify_admin(): return
        product = simpledialog.askstring("Remove", "Enter product name:")
        quantity = simpledialog.askinteger("Remove", "Enter quantity:")
        remove_product(product, quantity)
        messagebox.showinfo("Success", "Product removed!")

    tk.Button(root, text="Stock In", command=handle_stock_in, width=20).pack(pady=10)
    tk.Button(root, text="Sell Product", command=handle_sale, width=20).pack(pady=10)
    tk.Button(root, text="Manual Remove", command=handle_remove, width=20).pack(pady=10)
    tk.Button(root, text="Generate Audit", command=generate_audit, width=20).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
