import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root  # Main window
        self.root.title("Expense Tracker")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.entries = []  # Stores all saved expense entries
        self.build_ui()

    def build_ui(self):
        main = ttk.Frame(self.root, padding=12)  # Main layout container
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Expense Tracker", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 10)
        )

        self.fields = {}  # Holds the input variables
        labels = [
            ("Date:", "(YYYY-MM-DD)", "date"),
            ("Description:", "(what did you buy?)", "desc"),
            ("Amount:", "(e.g. 15.50)", "amount"),
            ("Category:", "(Food, Travel, Bills)", "category"),
        ]

        for i, (label_text, hint, key) in enumerate(labels, start=1):
            ttk.Label(main, text=label_text).grid(row=i, column=0, sticky="w")
            var = tk.StringVar()
            if key == "date":
                var.set(date.today().strftime("%Y-%m-%d"))
            elif key == "category":
                var.set("General")
            self.fields[key] = var
            ttk.Entry(main, textvariable=var, width=30).grid(row=i, column=1, sticky="ew", pady=3)
            ttk.Label(main, text=hint, foreground="gray").grid(row=i, column=2, sticky="w", padx=(6, 0))

        button_row = ttk.Frame(main)  # Buttons section
        button_row.grid(row=5, column=0, columnspan=3, sticky="w", pady=10)
        ttk.Button(button_row, text="Save Entry", command=self.save_entry).pack(side="left", padx=(0, 8))
        ttk.Button(button_row, text="Clear Form", command=self.clear_form).pack(side="left")

        ttk.Label(main, text="Diary Entries").grid(row=6, column=0, columnspan=3, sticky="w", pady=(10, 5))

        self.diary_text = tk.Text(main, height=16, width=80, wrap="word")  # Diary display area
        self.diary_text.grid(row=7, column=0, columnspan=3, sticky="nsew")
        self.diary_text.insert("1.0", "No entries yet.\n")

        ttk.Label(main, text="Total Spent:").grid(row=8, column=0, sticky="w", pady=(8, 0))
        self.total_var = tk.StringVar(value="$0.00")
        ttk.Label(main, textvariable=self.total_var, font=("Segoe UI", 11, "bold")).grid(row=8, column=1, sticky="w", pady=(8, 0))

        main.columnconfigure(1, weight=1)
        main.rowconfigure(7, weight=1)

    def save_entry(self):
        date_value = self.fields["date"].get().strip()
        desc = self.fields["desc"].get().strip()
        amount_text = self.fields["amount"].get().strip()
        category = self.fields["category"].get().strip() or "General"

        if not date_value or not desc or not amount_text:
            messagebox.showwarning("Missing Fields", "Please fill in the date, description, and amount.")
            return

        try:
            amount = float(amount_text)  # Convert amount to a number
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid number for the amount.")
            return

        self.entries.append({"date": date_value, "description": desc, "amount": amount, "category": category})
        self.display_entries()
        self.clear_form()

    def display_entries(self):
        self.diary_text.delete("1.0", tk.END)
        total = sum(item["amount"] for item in self.entries)
        self.total_var.set(f"${total:,.2f}")

        if not self.entries:
            self.diary_text.insert("1.0", "No entries yet.\n")
            return

        for item in self.entries:
            self.diary_text.insert(tk.END, f"Date: {item['date']}\n")
            self.diary_text.insert(tk.END, f"Category: {item['category']}\n")
            self.diary_text.insert(tk.END, f"Description: {item['description']}\n")
            self.diary_text.insert(tk.END, f"Amount: ${item['amount']:.2f}\n")
            self.diary_text.insert(tk.END, "-" * 40 + "\n")

    def clear_form(self):
        self.fields["date"].set(date.today().strftime("%Y-%m-%d"))
        self.fields["desc"].set("")
        self.fields["amount"].set("")
        self.fields["category"].set("General")


if __name__ == "__main__":
    root = tk.Tk()
    ExpenseTrackerApp(root)
    root.mainloop()

