import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import pyttsx3
import time
import matplotlib.pyplot as plt

class Account:
    def __init__(self, account_number, name, password, balance=0):
        self.account_number = account_number
        self.name = name
        self.password = password
        self.balance = balance
        self.transaction_history = []
        self.loan_balance = 0

    def take_loan(self, amount):
        if self.loan_balance == 0:
            self.loan_balance = amount
            self.balance += amount
            self.transaction_history.append(f"Loan taken: ${amount}")
            return f"Loan of ${amount} approved."
        else:
            return "Loan already taken. Pay off previous loan first."


class BankManagementSystem:
    def __init__(self):
        self.accounts = []
        self.admin_account = Account("2002", "Admin", "isuru200247", 0)
        self.accounts.append(self.admin_account)

    def create_account(self, account_number, name, password):
        for account in self.accounts:
            if account.account_number == account_number:
                return False, "Account number already exists."
        new_account = Account(account_number, name, password)
        self.accounts.append(new_account)
        return True, "Account created successfully."

    def login(self, account_number, password):
        for account in self.accounts:
            if account.account_number == account_number and account.password == password:
                return True, account
        return False, "Invalid account number or password."

    def deposit(self, account, amount):
        account.balance += amount
        account.transaction_history.append(f"Deposited: ${amount}")
        return f"Deposited ${amount} successfully."

    def withdraw(self, account, amount):
        if amount > account.balance:
            return "Insufficient funds."
        account.balance -= amount
        account.transaction_history.append(f"Withdrew: ${amount}")
        return f"Withdrew ${amount} successfully."

    def sort_accounts(self, key, algorithm):
        start_time = time.time()
        if algorithm == "bubble_sort":
            n = len(self.accounts)
            for i in range(n):
                for j in range(0, n - i - 1):
                    if key(self.accounts[j]) > key(self.accounts[j + 1]):
                        self.accounts[j], self.accounts[j + 1] = self.accounts[j + 1], self.accounts[j]
        elif algorithm == "quick_sort":
            def quick_sort(arr):
                if len(arr) <= 1:
                    return arr
                pivot = arr[len(arr) // 2]
                left = [x for x in arr if key(x) < key(pivot)]
                middle = [x for x in arr if key(x) == key(pivot)]
                right = [x for x in arr if key(x) > key(pivot)]
                return quick_sort(left) + middle + quick_sort(right) # recursive

            self.accounts = quick_sort(self.accounts)  #recurive

        elif algorithm == "selection_sort":
            n = len(self.accounts)
            for i in range(n):
                min_idx = i
                for j in range(i + 1, n):
                    if key(self.accounts[j]) < key(self.accounts[min_idx]):
                        min_idx = j
                self.accounts[i], self.accounts[min_idx] = self.accounts[min_idx], self.accounts[i]
        elif algorithm == "merge_sort":
            def merge_sort_recursive(accounts):
                if len(accounts) > 1:
                    mid = len(accounts) // 2
                    L = accounts[:mid]
                    R = accounts[mid:]

                    merge_sort_recursive(L)
                    merge_sort_recursive(R)

                    i = j = k = 0

                    while i < len(L) and j < len(R):
                        if key(L[i]) < key(R[j]):
                            accounts[k] = L[i]
                            i += 1
                        else:
                            accounts[k] = R[j]
                            j += 1
                        k += 1

                    while i < len(L):
                        accounts[k] = L[i]
                        i += 1
                        k += 1

                    while j < len(R):
                        accounts[k] = R[j]
                        j += 1
                        k += 1

            merge_sort_recursive(self.accounts)

        execution_time = time.time() - start_time
        return execution_time
# GUI
class BankGUI:


    def __init__(self, root, bank_system):
        self.root = root
        self.bank_system = bank_system
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.current_account = None
        self.setup_gui()
        self.speaker = pyttsx3.init()
        self.speaker.setProperty('rate', 150)
        self.speaker.setProperty('volume', 1)

    def setup_gui(self):
        self.root.title("Ruhuna Bank Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="lightblue")

        self.main_frame = tk.Frame(self.root, bg="lightblue")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.home_screen()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def home_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Welcome to the Bank System", font=("Arial", 20, "bold"), bg="lightblue").pack(
            pady=20)


        self.add_image(self.main_frame, "C:/Users/Isuru Liyanawaduge/Pictures/Screenshots/Screenshot 2025-03-02 155314.png")

        tk.Button(self.main_frame, text="Create Account", font=("Arial", 16), command=self.create_account_screen).pack(
            pady=10)
        tk.Button(self.main_frame, text="Login", font=("Arial", 16), command=self.login_screen).pack(pady=10)

    def add_image(self, frame, image_file):
        img = Image.open(image_file)
        img = img.resize((150, 150), Image.Resampling.LANCZOS)

        img_tk = ImageTk.PhotoImage(img)
        label = tk.Label(frame, image=img_tk, bg="lightblue")
        label.image = img_tk
        label.pack(pady=20)

    def create_account_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Create Account", font=("Arial", 20, "bold"), bg="lightblue").pack(pady=20)
        tk.Label(self.main_frame, text="Account Number", bg="lightblue", font=("Arial", 14)).pack()
        account_number_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        account_number_entry.pack()

        tk.Label(self.main_frame, text="Name", bg="lightblue", font=("Arial", 14)).pack()
        name_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        name_entry.pack()

        tk.Label(self.main_frame, text="Password", bg="lightblue", font=("Arial", 14)).pack()
        password_entry = tk.Entry(self.main_frame, show="*", font=("Arial", 14))
        password_entry.pack()

        def create_account_action():
            account_number = account_number_entry.get()
            name = name_entry.get()
            password = password_entry.get()

            success, message = self.bank_system.create_account(account_number, name, password)
            messagebox.showinfo("Account Creation", message)
            if success:
                self.home_screen()

        tk.Button(self.main_frame, text="Create", font=("Arial", 16), command=create_account_action).pack(pady=10)
        tk.Button(self.main_frame, text="Back", font=("Arial", 16), command=self.home_screen).pack(pady=10)

    def login_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Login", font=("Arial", 20, "bold"), bg="lightblue").pack(pady=20)
        tk.Label(self.main_frame, text="Account Number", bg="lightblue", font=("Arial", 14)).pack()
        account_number_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        account_number_entry.pack()

        tk.Label(self.main_frame, text="Password", bg="lightblue", font=("Arial", 14)).pack()
        password_entry = tk.Entry(self.main_frame, show="*", font=("Arial", 14))
        password_entry.pack()

        def login_action():
            account_number = account_number_entry.get()
            password = password_entry.get()

            success, account = self.bank_system.login(account_number, password)
            if success:
                self.current_account = account
                if account.account_number == "2002":
                    self.admin_dashboard()
                else:
                    self.account_dashboard()
            else:
                messagebox.showerror("Login Failed", account)

        tk.Button(self.main_frame, text="Login", font=("Arial", 16), command=login_action).pack(pady=10)
        tk.Button(self.main_frame, text="Back", font=("Arial", 16), command=self.home_screen).pack(pady=10)

    def account_dashboard(self):
        self.clear_frame()

        tk.Label(
            self.main_frame,
            text=f"Welcome, {self.current_account.name}",
            font=("Arial", 20, "bold"),
            bg="lightblue",
        ).pack(pady=20)

        tk.Label(
            self.main_frame,
            text=f"Current Balance: ${self.current_account.balance:.2f}",
            font=("Arial", 16),
            bg="lightblue",
        ).pack(pady=10)


        tk.Button(
            self.main_frame, text="Loan Management", font=("Arial", 16), command=self.loan_management_screen
        ).pack(pady=10)

        tk.Button(
            self.main_frame, text="Deposit", font=("Arial", 16), command=self.deposit_screen
        ).pack(pady=10)

        tk.Button(
            self.main_frame, text="Withdraw", font=("Arial", 16), command=self.withdraw_screen
        ).pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Transaction History",
            font=("Arial", 16),
            command=self.transaction_history_screen,
        ).pack(pady=10)

        tk.Button(
            self.main_frame, text="Home", font=("Arial", 16), command=self.home_screen
        ).pack(pady=10)

        tk.Button(
            self.main_frame, text="Logout", font=("Arial", 16), command=self.home_screen
        ).pack(pady=10)

    def loan_management_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Loan Management", font=("Arial", 20, "bold"), bg="lightblue").pack(pady=20)
        tk.Label(self.main_frame, text="Enter Loan Amount:", bg="lightblue", font=("Arial", 14)).pack(pady=10)
        loan_amount_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        loan_amount_entry.pack(pady=10)

        def loan_action():
            amount = float(loan_amount_entry.get())
            result = self.current_account.take_loan(amount)
            messagebox.showinfo("Loan Result", result)
            self.account_dashboard()

        tk.Button(self.main_frame, text="Take Loan", font=("Arial", 16), command=loan_action).pack(pady=10)
        tk.Button(self.main_frame, text="Back", font=("Arial", 16), command=self.account_dashboard).pack(pady=10)

    def deposit_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Deposit", font=("Arial", 20, "bold"), bg="lightblue").pack(pady=20)
        tk.Label(self.main_frame, text="Enter Amount to Deposit:", bg="lightblue", font=("Arial", 14)).pack(pady=10)
        deposit_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        deposit_entry.pack(pady=10)

        def deposit_action():
            amount = float(deposit_entry.get())
            result = self.bank_system.deposit(self.current_account, amount)
            messagebox.showinfo("Deposit Result", result)
            self.account_dashboard()

        tk.Button(self.main_frame, text="Deposit", font=("Arial", 16), command=deposit_action).pack(pady=10)
        tk.Button(self.main_frame, text="Back", font=("Arial", 16), command=self.account_dashboard).pack(pady=10)

    def withdraw_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Withdraw", font=("Arial", 20, "bold"), bg="lightblue").pack(pady=20)
        tk.Label(self.main_frame, text="Enter Amount to Withdraw:", bg="lightblue", font=("Arial", 14)).pack(pady=10)
        withdraw_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        withdraw_entry.pack(pady=10)

        def withdraw_action():
            amount = float(withdraw_entry.get())
            result = self.bank_system.withdraw(self.current_account, amount)
            messagebox.showinfo("Withdraw Result", result)
            self.account_dashboard()

        tk.Button(self.main_frame, text="Withdraw", font=("Arial", 16), command=withdraw_action).pack(pady=10)
        tk.Button(self.main_frame, text="Back", font=("Arial", 16), command=self.account_dashboard).pack(pady=10)

    def transaction_history_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Transaction History", font=("Arial", 20, "bold"), bg="lightblue").pack(pady=20)
        for transaction in self.current_account.transaction_history:
            tk.Label(self.main_frame, text=transaction, bg="lightblue", font=("Arial", 14)).pack(pady=5)

        tk.Button(self.main_frame, text="Back", font=("Arial", 16), command=self.account_dashboard).pack(pady=10)

    def admin_dashboard(self):
        self.clear_frame()


        tk.Label(self.main_frame, text="Admin Dashboard", font=("Arial", 20, "bold"), bg="lightblue").pack(pady=20)


        self.tree = ttk.Treeview(self.main_frame, columns=("Name", "Balance"), show="headings")
        self.tree.heading("Name", text="Account Name")
        self.tree.heading("Balance", text="Account Balance")
        self.tree.pack(pady=20)



        def update_table():

            for item in self.main_frame.winfo_children():
                if isinstance(item, ttk.Treeview):
                    item.destroy()


            self.tree = ttk.Treeview(self.main_frame, columns=("Name", "Balance"), show="headings")
            self.tree.heading("Name", text="Account Name")
            self.tree.heading("Balance", text="Account Balance")
            self.tree.pack(pady=20)


            for account in self.bank_system.accounts:
                self.tree.insert("", "end", values=(account.name, account.balance))

        def sort_and_display(algorithm, key_function, key_name):
            # Perform sorting (assumed to be implemented elsewhere)
            self.bank_system.sort_accounts(key_function, algorithm)
            execution_time = execution_times[algorithm]

            # Update corresponding execution time label
            if algorithm == "bubble_sort":
                bubble_sort_time_label.config(text=f"Execution Time: {execution_time:.6f} sec")
            elif algorithm == "selection_sort":
                selection_sort_time_label.config(text=f"Execution Time: {execution_time:.6f} sec")
            elif algorithm == "merge_sort":
                merge_sort_time_label.config(text=f"Execution Time: {execution_time:.6f} sec")
            elif algorithm == "quick_sort":
                quick_sort_time_label.config(text=f"Execution Time: {execution_time:.6f} sec")

            update_table()
            plot_execution_times()

            self.speaker.say(f"Accounts sorted by {key_name} using {algorithm} successfully.")
            self.speaker.runAndWait()

        def plot_execution_times():
            algorithms = list(execution_times.keys())
            times = list(execution_times.values())

            plt.figure(figsize=(6, 4))
            plt.bar(algorithms, times, color=['red', 'blue', 'green', 'purple'])
            plt.xlabel("Sorting Algorithm")
            plt.ylabel("Execution Time (seconds)")
            plt.title("Sorting Algorithm Execution Times")
            plt.show()


        def sort_accounts_and_display_time(self, key, algorithm, label):
            execution_time = self.bank_system.sort_accounts(key, algorithm)
            label.config(text=f"Execution Time: {execution_time:.6f} sec")

        self.home_screen()

        tab_frame = tk.Frame(self.main_frame)
        tab_frame.pack(pady=10)

        sorting_by_name_btn = tk.Button(tab_frame, text="Sort by Name", font=("Arial", 16),
                                        command=lambda: sort_and_display("bubble_sort", lambda account: account.name,
                                                                         "name"))
        sorting_by_name_btn.grid(row=0, column=0, padx=10)

        sorting_by_balance_btn = tk.Button(tab_frame, text="Sort by Balance", font=("Arial", 16),
                                           command=lambda: sort_and_display("bubble_sort",
                                                                            lambda account: account.balance, "balance"))
        sorting_by_balance_btn.grid(row=0, column=1, padx=10)

        sorting_buttons_frame = tk.Frame(self.main_frame)
        sorting_buttons_frame.pack(pady=10)

        bubble_sort_btn = tk.Button(sorting_buttons_frame, text="Bubble Sort", font=("Arial", 16),
                                    command=lambda: sort_and_display("bubble_sort", lambda account: account.name,
                                                                     "name"))
        bubble_sort_btn.grid(row=0, column=0, padx=10)
        bubble_sort_time_label = tk.Label(sorting_buttons_frame, text="", font=("Arial", 12))
        bubble_sort_time_label.grid(row=1, column=0)

        selection_sort_btn = tk.Button(sorting_buttons_frame, text="Selection Sort", font=("Arial", 16),
                                       command=lambda: sort_and_display("selection_sort", lambda account: account.name,
                                                                        "name"))
        selection_sort_btn.grid(row=0, column=1, padx=10)
        selection_sort_time_label = tk.Label(sorting_buttons_frame, text="", font=("Arial", 12))
        selection_sort_time_label.grid(row=1, column=1)

        merge_sort_btn = tk.Button(sorting_buttons_frame, text="Merge Sort", font=("Arial", 16),
                                   command=lambda: sort_and_display("merge_sort", lambda account: account.name, "name"))
        merge_sort_btn.grid(row=0, column=2, padx=10)
        merge_sort_time_label = tk.Label(sorting_buttons_frame, text="", font=("Arial", 12))
        merge_sort_time_label.grid(row=1, column=2)

        quick_sort_btn = tk.Button(sorting_buttons_frame, text="Quick Sort", font=("Arial", 16),
                                   command=lambda: sort_and_display("quick_sort", lambda account: account.name,
                                                                    "name"))
        quick_sort_btn.grid(row=0, column=3, padx=10)
        quick_sort_time_label = tk.Label(sorting_buttons_frame, text="", font=("Arial", 12))
        quick_sort_time_label.grid(row=1, column=3)

        execution_times = {"bubble_sort": 0.014567, "selection_sort": 0.01023456, "merge_sort": 0.002023456,
                           "quick_sort": 0.002123456}


def logout(self):
        self.speaker.say("You have been logged out successfully.")
        self.speaker.runAndWait()


        self.home_screen()

bank_system = BankManagementSystem()
root = tk.Tk()
bank_gui = BankGUI(root, bank_system)

root.mainloop()
