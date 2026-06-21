"""
SL Biz Tracker - Small Business Sales & Expense Tracker
PROG103 Final Project - GUI-Based Structured Programming Application

Real-world problem: Many small business owners in Sierra Leone keep no
organized record of daily sales and expenses, making it hard to know
whether they are actually making a profit.

SDG Alignment: SDG 8 - Decent Work and Economic Growth

File layout (as required): all LOGIC code first, all GUI code below it.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ============================================================
# CONSTANTS
# ============================================================
CURRENCY = "SLE"  # Sierra Leonean Leone
APP_TITLE = "SL Biz Tracker - Sales & Expense Manager"
TRANSACTION_TYPES = ["Sale", "Expense"]
CATEGORIES = ["Goods", "Services", "Transport", "Rent", "Utilities", "Supplies", "Other"]


# ============================================================
# LOGIC SECTION (business logic)
# ============================================================

class TransactionManager:
    """Handles all business logic: storing, calculating, and exporting data."""

    def __init__(self):
        # Each transaction is a dictionary stored in this list
        self.transactions = []

    def add_transaction(self, t_type, category, description, amount):
        """Create and store a new transaction record."""
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "type": t_type,
            "category": category,
            "description": description,
            "amount": amount
        }
        self.transactions.append(record)
        return record

    def delete_transaction(self, index):
        """Remove a transaction at the given position in the list."""
        if 0 <= index < len(self.transactions):
            del self.transactions[index]
            return True
        return False

    def calculate_summary(self):
        """Loop through every transaction and work out totals + business status."""
        total_sales = 0.0
        total_expenses = 0.0

        # Iteration (loop) through all records
        for record in self.transactions:
            if record["type"] == "Sale":
                total_sales += record["amount"]
            elif record["type"] == "Expense":
                total_expenses += record["amount"]

        net_profit = total_sales - total_expenses

        # Decision structure to interpret the result
        if net_profit > 0:
            status = "Profitable"
        elif net_profit == 0:
            status = "Break-even"
        else:
            status = "Operating at a Loss"

        return {
            "total_sales": total_sales,
            "total_expenses": total_expenses,
            "net_profit": net_profit,
            "status": status,
            "record_count": len(self.transactions)
        }

    def export_report(self, filepath):
        """Write a plain-text summary report to disk (data accessibility)."""
        summary = self.calculate_summary()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("SL BIZ TRACKER - BUSINESS REPORT\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            for r in self.transactions:
                f.write(f"{r['date']} | {r['type']:8} | {r['category']:10} | "
                        f"{r['description']:20} | {CURRENCY} {r['amount']:.2f}\n")
            f.write("\n" + "-" * 50 + "\n")
            f.write(f"Total Sales:    {CURRENCY} {summary['total_sales']:.2f}\n")
            f.write(f"Total Expenses: {CURRENCY} {summary['total_expenses']:.2f}\n")
            f.write(f"Net Profit:     {CURRENCY} {summary['net_profit']:.2f}\n")
            f.write(f"Status:         {summary['status']}\n")
        return filepath


def validate_amount(amount_str):
    """Validate that the input is a positive number. Returns float or None."""
    try:
        amount = float(amount_str)
        if amount <= 0:
            return None
        return amount
    except ValueError:
        return None


# ============================================================
# GUI SECTION (interface code)
# ============================================================

class BizTrackerApp:
    """Builds the tkinter interface and connects it to TransactionManager."""

    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("740x560")
        self.root.minsize(740, 560)
        self.root.resizable(True, True)

        self.manager = TransactionManager()  # backend logic instance

        # Widget attributes are created inside the build_* methods below,
        # but declared here first so static analysis (and other readers)
        # can see the full set of instance attributes at a glance.
        self.type_var = None
        self.category_var = None
        self.desc_entry = None
        self.amount_entry = None
        self.tree = None
        self.summary_label = None

        self.build_input_section()
        self.build_buttons_section()
        self.build_output_section()

    # ---------- GUI LAYOUT ----------

    def build_input_section(self):
        frame = tk.LabelFrame(self.root, text="New Transaction", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=10)

        tk.Label(frame, text="Type:").grid(row=0, column=0, sticky="w", pady=4)
        self.type_var = tk.StringVar(value=TRANSACTION_TYPES[0])
        ttk.Combobox(frame, textvariable=self.type_var, values=TRANSACTION_TYPES,
                     state="readonly", width=15).grid(row=0, column=1, pady=4)

        tk.Label(frame, text="Category:").grid(row=0, column=2, sticky="w", padx=(20, 0))
        self.category_var = tk.StringVar(value=CATEGORIES[0])
        ttk.Combobox(frame, textvariable=self.category_var, values=CATEGORIES,
                     state="readonly", width=15).grid(row=0, column=3, pady=4)

        tk.Label(frame, text="Description:").grid(row=1, column=0, sticky="w", pady=4)
        self.desc_entry = tk.Entry(frame, width=30)
        self.desc_entry.grid(row=1, column=1, columnspan=2, pady=4, sticky="w")

        tk.Label(frame, text=f"Amount ({CURRENCY}):").grid(row=1, column=2, sticky="w", padx=(20, 0))
        self.amount_entry = tk.Entry(frame, width=15)
        self.amount_entry.grid(row=1, column=3, pady=4)

    def build_buttons_section(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="x", padx=10, pady=5)

        tk.Button(frame, text="Add Transaction", width=16, bg="#2e7d32", fg="white",
                  command=self.add_transaction).pack(side="left", padx=5)
        tk.Button(frame, text="Delete Selected", width=14,
                  command=self.delete_transaction).pack(side="left", padx=5)
        tk.Button(frame, text="Calculate Summary", width=16, bg="#1565c0", fg="white",
                  command=self.calculate_summary).pack(side="left", padx=5)
        tk.Button(frame, text="Export Report", width=14,
                  command=self.export_report).pack(side="left", padx=5)
        tk.Button(frame, text="Clear", width=10,
                  command=self.clear_fields).pack(side="left", padx=5)
        tk.Button(frame, text="Exit", width=10, bg="#c62828", fg="white",
                  command=self.exit_app).pack(side="left", padx=5)

    def build_output_section(self):
        list_frame = tk.LabelFrame(self.root, text="Transaction Records", padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("date", "type", "category", "description", "amount")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        headings = {"date": "Date", "type": "Type", "category": "Category",
                    "description": "Description", "amount": f"Amount ({CURRENCY})"}
        widths = {"date": 130, "type": 70, "category": 90, "description": 190, "amount": 110}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col])
        self.tree.pack(fill="both", expand=True)

        summary_frame = tk.LabelFrame(self.root, text="Summary", padx=10, pady=10)
        summary_frame.pack(fill="x", padx=10, pady=5)
        self.summary_label = tk.Label(summary_frame, text="No data yet. Add a transaction to begin.",
                                       justify="left", anchor="w", wraplength=700)
        self.summary_label.pack(fill="x")

    # ---------- EVENT HANDLERS (call backend logic) ----------

    def add_transaction(self):
        """Validate input fields and add a new transaction record."""
        t_type = self.type_var.get()
        category = self.category_var.get()
        description = self.desc_entry.get().strip()
        amount = validate_amount(self.amount_entry.get())

        # Input validation (decision structure)
        if not description:
            messagebox.showerror("Input Error", "Please enter a description.")
            return
        if amount is None:
            messagebox.showerror("Input Error", "Please enter a valid positive amount.")
            return

        record = self.manager.add_transaction(t_type, category, description, amount)
        self.tree.insert("", "end", values=(record["date"], record["type"],
                                             record["category"], record["description"],
                                             f"{record['amount']:.2f}"))
        self.clear_fields()

    def delete_transaction(self):
        """Delete the selected transaction from both the table and the data list."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a record to delete.")
            return
        index = self.tree.index(selected[0])
        self.manager.delete_transaction(index)
        self.tree.delete(selected[0])

    def calculate_summary(self):
        """Calculate and display the business summary."""
        summary = self.manager.calculate_summary()

        if summary["record_count"] == 0:
            self.summary_label.config(text="No transactions recorded yet.")
            return

        text = (f"Records: {summary['record_count']}   |   "
                f"Total Sales: {CURRENCY} {summary['total_sales']:.2f}   |   "
                f"Total Expenses: {CURRENCY} {summary['total_expenses']:.2f}   |   "
                f"Net Profit: {CURRENCY} {summary['net_profit']:.2f}   |   "
                f"Status: {summary['status']}")
        self.summary_label.config(text=text)

    def export_report(self):
        """Export the current report to a text file."""
        if not self.manager.transactions:
            messagebox.showwarning("No Data", "Add transactions before exporting a report.")
            return
        filepath = self.manager.export_report("business_report.txt")
        messagebox.showinfo("Export Successful", f"Report saved to {filepath}")

    def clear_fields(self):
        """Reset all input fields to their default state."""
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.type_var.set(TRANSACTION_TYPES[0])
        self.category_var.set(CATEGORIES[0])

    def exit_app(self):
        """Confirm and close the application."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()


# -------------------- MAIN ENTRY POINT --------------------

def main():
    root = tk.Tk()
    BizTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()