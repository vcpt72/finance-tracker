from tkinter import * 
import tkinter.font
from tkinter import ttk
from tkinter import messagebox
import os

class myApp:

    def display_author(self):
        messagebox.showinfo(
        "Author",
        "Patrik Vachník - VAC0289\n"
        "\n"
        "This project was created for the URO course\n"
        "at VSB-TUO using tkinter"
    )
    
    def open_balance_window(self):
       
        self.balance_window = Toplevel()
        self.balance_window.title("Add Balance")
        self.balance_window.geometry("300x150")
        self.balance_window.resizable(False, False)
    
        Label(self.balance_window, text="Enter Amount:", font=("Bahnschrift", 12)).pack(pady=10)

        self.amount_entry_popup = Entry(self.balance_window, font=("Bahnschrift", 12))
        self.amount_entry_popup.pack(pady=5)
        
        Button(self.balance_window, text="Confirm", command=self.add_balance).pack(pady=10)

    def add_balance(self):
        try:
            amount = float(self.amount_entry_popup.get().strip()) 
            if amount <= 0:
                messagebox.showerror("Error", "Balance must be positive")
                return
            self.balance += amount  
            self.balance_label.config(text=f"Balance: {self.balance:.2f} CZK")  
            self.balance_window.destroy() 
            self.update_balance_bar() 

        except ValueError:
            messagebox.showerror("Error", "Enter a valid numeric value")
    def add_expense_popup(self):
        
        self.expense_window = Toplevel()
        self.expense_window.title("Add Expense")
        self.expense_window.geometry("400x300")
        self.expense_window.resizable(False, False)

        Label(self.expense_window, text="Enter Name:", font=("Bahnschrift", 12)).pack(pady=10)
        self.name_entry = Entry(self.expense_window, font=("Bahnschrift", 12))
        self.name_entry.pack(pady=5)

        Label(self.expense_window, text="Enter Amount:", font=("Bahnschrift", 12)).pack(pady=10)
        self.amount_entry = Entry(self.expense_window, font=("Bahnschrift", 12))
        self.amount_entry.pack(pady=5)

        Label(self.expense_window, text="Enter Price:", font=("Bahnschrift", 12)).pack(pady=10)
        self.price_entry = Entry(self.expense_window, font=("Bahnschrift", 12))
        self.price_entry.pack(pady=5)

        Button(self.expense_window, text="Confirm", command=self.add_expense_to_treeview).pack(pady=10)

    def add_expense_to_treeview(self):
        name = self.name_entry.get().strip()
        try:
            amount = int(self.amount_entry.get().strip())
            price = float(self.price_entry.get().strip())
            if price > self.balance:
                messagebox.showerror("Error", "Insufficient balance to add this expense.")
                return
            if name and amount > 0 and price > 0:
                self.balance -= price
                self.expenses += price  
                self.balance_label.config(text=f"Balance: {self.balance:.2f} CZK")
                self.recent_expenses_tree.insert("", "end", values=(name, amount, f"{price:.2f}"))
                self.expense_window.destroy()
                self.update_balance_bar()  
            else:
                messagebox.showerror("Error", "Please enter valid values for all fields")
            
        except ValueError:
            messagebox.showerror("Error", "Amount must be an integer and Price must be a valid number")
    def remove_expense(self):
        selected_item = self.recent_expenses_tree.selection()  
        if selected_item:
            # Get the values of the selected expense
            item_values = self.recent_expenses_tree.item(selected_item)['values']
            # Extract the price of the expense (assuming it's the third value in the tuple)
            expense_price = float(item_values[2])  # Ensure to convert to float

            # Add the expense price back to the balance
            self.balance += expense_price
            self.expenses -= expense_price  # Assuming `self.expenses` keeps track of total expenses

            # Update the balance display
            self.balance_label.config(text=f"Balance: {self.balance:.2f} CZK")

            # Remove the selected item from the treeview
            self.recent_expenses_tree.delete(selected_item)

            # Optionally, update the balance bar or any other display elements
            self.update_balance_bar()  
        else:
            messagebox.showerror("Error", "Please select an expense to remove")
    def remove_wishlist_item(self):
        selected_item = self.wishlist_treeview.selection()
        if selected_item:
            self.wishlist_treeview.delete(selected_item)
        else:
            messagebox.showerror("Error", "Please select an item to remove")
    def add_to_wishlist_popup(self):
        self.wishlist_window = Toplevel()
        self.wishlist_window.title("Add Item to Wishlist")
        self.wishlist_window.geometry("300x150")
        self.wishlist_window.resizable(False, False)
        Label(self.wishlist_window, text="Enter Item Name:", font=("Bahnschrift", 12)).pack(pady=10)
        self.item_name_entry = Entry(self.wishlist_window, font=("Bahnschrift", 12))
        self.item_name_entry.pack(pady=5)  
        Button(self.wishlist_window, text="Confirm", command=self.add_item_to_wishlist).pack(pady=10)

    def update_balance_bar(self):
        max_width = 700  
        
        if self.balance > 0:
       
            current_balance_width = (self.balance / self.balance) * max_width
        else:
            current_balance_width = 0  
    
        if self.balance > 0:
            current_expense_width = (self.expenses / self.balance) * max_width
        else:
            current_expense_width = 0  
    
    
        self.canvas.delete("all")
    
        if current_balance_width > 0:
            self.canvas.create_rectangle(10, 10, 10 + current_balance_width, 30, fill="green")
        if current_expense_width > 0:
            self.canvas.create_rectangle(10, 40, 10 + current_expense_width, 60, fill="red")
    
    def add_item_to_wishlist(self):
        item_name = self.item_name_entry.get().strip()  
        if item_name:  
            self.wishlist_treeview.insert("", "end", values=(item_name,))
            self.wishlist_window.destroy()  
        else:
            messagebox.showerror("Error", "Please enter a valid item name")
    def __init__(self, root):

        #SETTINGS
        root.title('Finance Tracker')
        root.resizable(False, False)
        root.geometry("1050x600")
        root.grid_rowconfigure(0, weight=1) # MAIN GRID
        root.grid_columnconfigure(1, weight=1)
        
        # INITIAL BALANCE
        self.balance = 0
        self.expenses = 0   


        # STYLES
        style = ttk.Style()
        style.theme_use("clam")  
        style.configure("TButton",
                        font=("Bahnschrift", 12),
                        padding=10,
                        background="#7303fc",  # #030bfc
                        foreground="white",  
                        borderwidth=0,
                        relief="flat")
        style.configure("QuickButton.TButton",
                        font=("Bahnschrift", 12),
                        padding=10,
                        background="gray10",  
                        foreground="white",  
                        borderwidth=0,
                        relief="flat")
        style.configure("Custom.Treeview", 
                background="gray18",   
                foreground="white",    
                fieldbackground="gray18",    
                rowheight=20,
                borderwidth=0,
                highlightthickness=0,
                relief="flat",
                bd=0,
                show="tree"
                )
        style.configure("Custom.Treeview.Heading", 
                background="gray18",
                foreground="gray34",
                borderwidth=0,
                relief="flat",
                font=("Bahnschrift", 7)
                )   
        style.layout("Custom.Treeview", [
        ('Custom.Treeview.treearea', {'sticky': 'nswe', 'border': '0'}) # KEEP THE TREEVIEW BORDERLESS
        ])
        style.map("Custom.Treeview.Heading",
        background=[('active', 'gray18')],  # Keep the same color when active/hovered
        foreground=[('active', 'gray34')]    # Keep the same text color when active/hovered
        )

        style.configure("LeftAligned.TButton", 
                font=("Bahnschrift", 12),
                padding=10,
                background="#7303fc", # #030bfc
                foreground="white",
                borderwidth=0,
                relief="flat",
                anchor="w")
          
        # FRAMES
        menu_frame = Frame(root, width=150, bg="gray18")
        content_frame = Frame(root, bg="gray10")
        left_column_frame = Frame(content_frame, bg="gray10")
        left_column_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)

        wishlist_frame = Frame(left_column_frame, bg="gray18") # wishlist
        recent_frame = Frame(content_frame, bg="gray18")   # recent expenses
        quick_frame = Frame(content_frame, bg="gray18")    # Quick Actions
        report_frame = Frame(content_frame, bg="gray18")   # monthly report
        
        #PACK
        menu_frame.grid(row=0, column=0, sticky="nsw")
        menu_frame.grid_propagate(False)
        
        content_frame.grid(row=0, column=1, sticky="nsew")
        wishlist_frame.grid(row=1, column= 0, sticky ="nsew", padx=50, pady=5)
        wishlist_frame.grid_propagate(False)  # Prevent automatic resizing
        wishlist_frame.config(width=300, height=135)

        recent_frame.grid(row=1, column= 1, pady=5, sticky="nsew", padx=50)
        recent_frame.config(width=320, height=135)
        recent_frame.grid_propagate(False)
        quick_frame.grid(row= 2, column=0, sticky = "nsew", padx=50, pady=50, columnspan=2)
        
        report_frame.grid(row=3, column= 0, sticky ="nsew", padx=50, pady=20, columnspan=2)
        report_frame.grid_propagate(False)  
        report_frame.config(height=120)
        
        self.canvas = Canvas(report_frame, width=700, height=60, bg="gray18", highlightthickness=0, bd=0)
        self.canvas.grid(row=1, column=0, pady=20)
        self.update_balance_bar()
    
        # MENU 
        profile_path = os.path.join(base_dir, "profilepic.png")
        self.photo = PhotoImage(file=profile_path)
        self.ca = Canvas(menu_frame, width=50, height=50, bg="gray18", highlightthickness=0)
        self.ca.grid(row=0, column=0, pady=10)  
        self.ca.create_image(25, 25, image=self.photo) 
        Label(menu_frame, text="User", bg="gray18", font=("Bahnschrift", 10), fg="white").grid(row=1, column=0)
        Label(menu_frame, bg="gray18").grid(row=2, column=0, pady=5)

        menu_frame.grid_columnconfigure(0, weight=1)
        ttk.Button(menu_frame, text="Add Balance",style="LeftAligned.TButton", command=self.open_balance_window      ).grid(row=3,column=0, sticky='ew', pady=5)
        #ttk.Button(menu_frame, text="Expenses", style="LeftAligned.TButton" ).grid(row=4,column=0, sticky='ew', pady=5)
        #ttk.Button(menu_frame, text="Settings", style="LeftAligned.TButton" ).grid(row=5,column=0, sticky='ew', pady=5)
        #ttk.Button(menu_frame, text="Reports",  style="LeftAligned.TButton" ).grid(row=6,column=0, sticky='ew', pady=5)
        ttk.Button(menu_frame, text="Author",  style="LeftAligned.TButton" , command=self.display_author).grid(row=7,column=0, sticky='ew', pady=5)
        
        # CONTENT
        Label(content_frame, text ="Dashboard", font=("Bahnschrift", 12), bg="gray10", fg="white").grid(row=0, column=0, pady = 20, padx=50, sticky = "w")
        self.balance_label = Label(content_frame, text =f"Balance: {self.balance}", font=("Bahnschrift", 12), bg="gray10", fg="white")
        self.balance_label.grid(row=0, column=1, sticky = "w", padx=50)
       
        #WISHLIST
        Label(wishlist_frame, text="Wishlist", font=("Bahnschrift", 10, "underline"), bg="gray18", fg="white").grid(row=0, column=0, sticky="w", padx=5)
        self.wishlist_treeview = ttk.Treeview(wishlist_frame, columns=("Name"), show="headings", height=4, style="Custom.Treeview")
        self.wishlist_treeview.column("Name", width=320, anchor="w")
        self.wishlist_treeview.heading("Name", text="Wish", anchor="w")
        tree_scroll = Scrollbar(wishlist_frame, orient="vertical", relief="flat", borderwidth=0)    
        tree_scroll.grid(row=1, column=2, sticky="ns")
        tree_scroll.config(command=self.wishlist_treeview.yview, bd=0, highlightthickness=0)
        tree_scroll.grid_forget()  
        self.wishlist_treeview.grid(row=1, column=0, columnspan=2, padx=3, pady=5)

        #RECENT EXPENSES
        Label(recent_frame, text="Recent Expenses", font=("Bahnschrift", 10, "underline"), bg="gray18", fg="white").grid(row=0, column=0, sticky = "w", padx=5)

        #RECENT EXPENSES TREEVIEW
        self.recent_expenses_tree = ttk.Treeview( recent_frame, columns=("Name", "Amount", "Price"), show="headings", height=4, style="Custom.Treeview")
        self.recent_expenses_tree.column("Name", width=140, anchor="w")   
        self.recent_expenses_tree.column("Amount", width=50, anchor="e")
        self.recent_expenses_tree.column("Price", width=120, anchor="e")
        self.recent_expenses_tree.heading("Name", text="Name", anchor="w")
        self.recent_expenses_tree.heading("Amount", text="Amount",anchor="e" )
        self.recent_expenses_tree.heading("Price", text="Price", anchor="e")
        tree_scroll = Scrollbar(recent_frame, orient="vertical",relief="flat", borderwidth=0)    
        tree_scroll.grid(row=1, column=2, sticky="ns")
        tree_scroll.config(command=self.recent_expenses_tree.yview,bd=0, highlightthickness=0)
        tree_scroll.grid_forget()
        self.recent_expenses_tree.grid(row=1, column=0, columnspan=2, padx=3, pady=5)
        
        #QUICK ACTIONS
        Label(quick_frame, text="Quick Actions",font=("Bahnschrift", 10), bg="gray18", fg="white").grid(row=0, column =0, sticky="w", padx=10, pady=5)
        ttk.Button(quick_frame, text = "New Expense"   , command=self.add_expense_popup, style="QuickButton.TButton").grid(row =  1, column =0, padx=27)
        ttk.Button(quick_frame, text = "Remove Expense", command=self.remove_expense, style="QuickButton.TButton").grid(row = 1, column =1, pady= 20,padx=27)  
        
        ttk.Button(quick_frame, text = "Add To Wishlist",command=self.add_to_wishlist_popup, style="QuickButton.TButton").grid(row = 1, column =2,padx=27)
        ttk.Button(quick_frame, text = "Remove from Wishlist",    command=self.remove_wishlist_item, style="QuickButton.TButton").grid(row = 1, column =3,padx=27) 
        
        #MONTHLY REPORT
        Label(report_frame, text="Monthly report",font=("Bahnschrift", 10), bg="gray18", fg="white").grid(row=0, column= 0, padx=5, pady=5, sticky="w")   

       
       
       
       
       
       
        

root = Tk()
base_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(base_dir, "icon.png")
icon = PhotoImage(file=icon_path)
root.iconphoto(True, icon)
app = myApp(root)
root.mainloop()
