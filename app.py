import tkinter as tk
from tkinter import ttk, messagebox


class DadsDunkin:
    def __init__(self, root):
        self.root = root
        self.root.title("Dad's Dunkin")
        self.root.configure(bg='#D9B08C')  # Mocha color background

        self.inputs_locked = True  # Initialize with inputs locked
        self.max_sugar_intake = 25.0  # Adjusted healthy sugar intake limit
        self.total_sugar = 0
        self.sugar_intake_by_time = {"Morning": 0.0, "Evening": 0.0, "Night": 0.0}
        self.setup_gui()
        self.toggle_inputs()  # Lock inputs initially

    def setup_gui(self):
        # Style configuration
        style = ttk.Style()
        style.configure("TLabel", background="#D9B08C", font=("Comic Sans MS", 10), foreground="black")
        style.configure("TButton", background="#FF8C42", font=("Comic Sans MS", 10), foreground="#FFFFFF")
        style.configure("TRadiobutton", background="#FF8C42", font=("Comic Sans MS", 10), foreground="black")
        style.configure("TEntry", font=("Comic Sans MS", 10), foreground="black")
        style.configure("Treeview", background="#F7CAC9", fieldbackground="#F7CAC9", font=("Comic Sans MS", 10), foreground="black")
        style.configure("Treeview.Heading", background="#FF8C42", font=("Comic Sans MS", 10, "bold"), foreground="#FFFFFF")

        # Time of Day Selection
        self.time_of_day_var = tk.StringVar()
        self.time_of_day_var.set("Morning")

        times_of_day = ["Morning", "Evening", "Night"]
        for i, time in enumerate(times_of_day):
            rb = ttk.Radiobutton(self.root, text=time, variable=self.time_of_day_var, value=time,
                                 command=self.update_sugar_labels)
            rb.grid(row=0, column=i, padx=10, pady=10)

        # Sugar Intake Entry
        self.sugar_intake_var = tk.DoubleVar()
        ttk.Label(self.root, text="Sugar Intake (g):").grid(row=1, column=0, padx=10, pady=10)
        self.sugar_entry = ttk.Entry(self.root, textvariable=self.sugar_intake_var)
        self.sugar_entry.grid(row=1, column=1, padx=10, pady=10)

        # Submit Button
        submit_btn = ttk.Button(self.root, text="Submit", command=self.submit_sugar_intake)
        submit_btn.grid(row=1, column=2, padx=10, pady=10)

        # Message Label
        self.message_label = ttk.Label(self.root, text="", foreground="black")
        self.message_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Scroll Selectors
        self.size_var = tk.StringVar(value="S")
        self.dairy_var = tk.StringVar(value="none")
        self.flavor_var = tk.StringVar(value="none")
        self.sweetener_var = tk.StringVar(value="none")

        ttk.Label(self.root, text="Size:").grid(row=3, column=0, padx=10, pady=5)
        self.size_option = ttk.OptionMenu(self.root, self.size_var, "S", "M", "L", "XL", command=self.load_coffee_menu)
        self.size_option.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Dairy:").grid(row=4, column=0, padx=10, pady=5)
        self.dairy_option = ttk.OptionMenu(self.root, self.dairy_var, "none", "Oatmilk", "skim milk", "whole milk",
                                           "almond milk", "cream")
        self.dairy_option.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Flavor:").grid(row=5, column=0, padx=10, pady=5)
        self.flavor_option = ttk.OptionMenu(self.root, self.flavor_var, "none", "pecan butter swirl", "caramel swirl",
                                            "french vanilla swirl", "mocha swirl")
        self.flavor_option.grid(row=5, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Sweetener:").grid(row=6, column=0, padx=10, pady=5)
        self.sweetener_option = ttk.OptionMenu(self.root, self.sweetener_var, "none", "sugar")
        self.sweetener_option.grid(row=6, column=1, padx=10, pady=5)

        # Time of Day Sugar Intake Labels
        self.morning_sugar_label = ttk.Label(self.root, text="Morning Sugar Intake: 0.0g")
        self.morning_sugar_label.grid(row=7, column=0, padx=10, pady=5)
        self.evening_sugar_label = ttk.Label(self.root, text="Evening Sugar Intake: 0.0g")
        self.evening_sugar_label.grid(row=7, column=1, padx=10, pady=5)
        self.night_sugar_label = ttk.Label(self.root, text="Night Sugar Intake: 0.0g")
        self.night_sugar_label.grid(row=7, column=2, padx=10, pady=5)

        # Coffee Menu Table with Scrollbar
        coffee_frame = ttk.Frame(self.root)
        coffee_frame.grid(row=8, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
        self.coffee_menu = ttk.Treeview(coffee_frame, columns=("Name", "Cost", "Sugar"), show="headings")
        self.coffee_menu.heading("Name", text="Name")
        self.coffee_menu.heading("Cost", text="Cost ($)")
        self.coffee_menu.heading("Sugar", text="Sugar (g)")

        coffee_scrollbar = ttk.Scrollbar(coffee_frame, orient="vertical", command=self.coffee_menu.yview)
        self.coffee_menu.configure(yscroll=coffee_scrollbar.set)
        self.coffee_menu.pack(side="left", fill="both", expand=True)
        coffee_scrollbar.pack(side="right", fill="y")

        self.load_coffee_menu()

        # Donut Menu Table with Scrollbar
        donut_frame = ttk.Frame(self.root)
        donut_frame.grid(row=9, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
        self.donut_menu = ttk.Treeview(donut_frame, columns=("Name", "Cost", "Sugar"), show="headings")
        self.donut_menu.heading("Name", text="Name")
        self.donut_menu.heading("Cost", text="Cost ($)")
        self.donut_menu.heading("Sugar", text="Sugar (g)")

        donut_scrollbar = ttk.Scrollbar(donut_frame, orient="vertical", command=self.donut_menu.yview)
        self.donut_menu.configure(yscroll=donut_scrollbar.set)
        self.donut_menu.pack(side="left", fill="both", expand=True)
        donut_scrollbar.pack(side="right", fill="y")

        self.load_donut_menu()

        # Power Button
        self.power_button = ttk.Button(self.root, text="Unlock", command=self.toggle_inputs)
        self.power_button.grid(row=10, column=0, columnspan=3, padx=10, pady=10)

    def load_coffee_menu(self, *args):
        # Clear existing data
        for item in self.coffee_menu.get_children():
            self.coffee_menu.delete(item)

        # Data for small size
        coffee_items = [
            {"name": "Cold Brew Coffee with Caramel Cold Foam", "cost": 3.99, "sugar": 0},
            {"name": "Toasted Almond Mocha Cold Brew", "cost": 3.99, "sugar": 0},
            {"name": "Churro Frozen Coffee", "cost": 3.39, "sugar": 83},
            {"name": "Frozen Coffee with Almondmilk", "cost": 3.39, "sugar": 56},
            {"name": "Vanilla Frosted Donut Frozen Coffee", "cost": 3.39, "sugar": 81},
            {"name": "Frozen Matcha Latte with Almondmilk", "cost": 3.49, "sugar": 54},
            {"name": "Vanilla Frosted Donut Signature Hot Latte with Whole Milk", "cost": 3.39, "sugar": 39},
            {"name": "Iced Cappuccino with Almondmilk", "cost": 3.89, "sugar": 6},
            {"name": "Blueberry Donut Iced Coffee", "cost": 3.89, "sugar": 26},
            {"name": "Coconut Donut Iced Coffee", "cost": 3.89, "sugar": 26},
            {"name": "Raspberry Jelly Donut Iced Coffee", "cost": 3.89, "sugar": 27},
            {"name": "Blueberry Pecan Signature Iced Latte with Whole Milk", "cost": 3.89, "sugar": 38},
            {"name": "Caramel Toasted Almond Iced Latte", "cost": 3.89, "sugar": 34},
            {"name": "Iced Vanilla Chai Latte with Sweet Cold Foam", "cost": 3.49, "sugar": 38},
            {"name": "Pecan Vanilla Iced Latte", "cost": 3.89, "sugar": 33},
            {"name": "Vanilla Frosted Donut Signature Iced Latte with Whole Milk", "cost": 3.89, "sugar": 33},
            {"name": "Iced Cappuccino with Whole Milk", "cost": 3.89, "sugar": 30},
            {"name": "Butter Pecan Iced Cappuccino with Skim Milk", "cost": 3.89, "sugar": 30},
            {"name": "Caramel Swirl Iced Cappuccino with Whole Milk", "cost": 3.89, "sugar": 31},
            {"name": "Caramel Swirl Iced Cappuccino with Skim Milk", "cost": 3.89, "sugar": 32},
            {"name": "French Vanilla Iced Cappuccino with Whole Milk", "cost": 3.89, "sugar": 30},
            {"name": "French Vanilla Iced Cappuccino with Skim Milk", "cost": 3.89, "sugar": 30},
            {"name": "Mocha Iced Cappuccino with Whole Milk", "cost": 3.89, "sugar": 29},
            {"name": "Mocha Iced Cappuccino with Skim Milk", "cost": 3.89, "sugar": 28},
            {"name": "Classic Hot Cappuccino with Whole Milk", "cost": 3.89, "sugar": 9},
            {"name": "Classic Hot Cappuccino with Whole Milk", "cost": 3.89, "sugar": 8},
            {"name": "Butter Pecan Hot Cappuccino with Whole Milk", "cost": 3.89, "sugar": 45},
            {"name": "Butter Pecan Hot Cappuccino with Skim Milk", "cost": 3.89, "sugar": 45},
            {"name": "Caramel Hot Cappuccino with Whole Milk", "cost": 3.89, "sugar": 47},
            {"name": "Caramel Hot Cappuccino with Skim Milk", "cost": 3.89, "sugar": 47},
            {"name": "French vanilla Hot Cappuccino with Whole Milk", "cost": 3.89, "sugar": 45},
            {"name": "French Vanilla Hot Cappuccino with Skim Milk", "cost": 3.89, "sugar": 46},
            {"name": "There's too many coffees lol", "cost": 0.00, "sugar": 100},
        ]

        selected_size = self.size_var.get()

        if selected_size == "M":
            for item in coffee_items:
                item["cost"] += 0.50
                item["sugar"] += 35
        elif selected_size == "L":
            for item in coffee_items:
                item["cost"] += 0.40
                item["sugar"] += 40
        elif selected_size == "XL":
            for item in coffee_items:
                item["cost"] += 0.60
                item["sugar"] += 50

        for item in coffee_items:
            self.coffee_menu.insert("", "end", values=(item["name"], item["cost"], item["sugar"]))

    def load_donut_menu(self):
        # Updated Donut Menu with provided data
        donut_items = [
            {"name": "Everything Bagel Minis", "cost": 3.79, "sugar": 0},
            {"name": "Plain Stuffed Bagel Minis", "cost": 3.79, "sugar": 0},
            {"name": "English Muffin", "cost": 2.29, "sugar": 0},
            {"name": "Croissant", "cost": 2.69, "sugar": 0},
            {"name": "Apple Fritter", "cost": 2.79, "sugar": 0},
            {"name": "Coffee Roll", "cost": 2.79, "sugar": 0},
            {"name": "Bagel With Cream Cheese", "cost": 4.39, "sugar": 0},
            {"name": "Bagels", "cost": 2.29, "sugar": 0},
            {"name": "4 Muffins", "cost": 11.49, "sugar": 0},
            {"name": "Muffins", "cost": 2.89, "sugar": 0},
            {"name": "Dozen Donuts", "cost": 16.89, "sugar": 0},
            {"name": "Half Dozen Donuts", "cost": 10.19, "sugar": 0},
            {"name": "Munchkins Donut Hole Treats", "cost": 2.29, "sugar": 0},
            {"name": "Apple n’ Spice", "cost": 2.29, "sugar": 0},
            {"name": "Apple Crumb", "cost": 2.29, "sugar": 0},
            {"name": "Apple Stick", "cost": 2.29, "sugar": 0},
            {"name": "Bavarian Kreme", "cost": 2.29, "sugar": 0},
            {"name": "Bismark", "cost": 2.29, "sugar": 0},
            {"name": "Boston Kreme", "cost": 2.29, "sugar": 0},
            {"name": "Butternut", "cost": 2.29, "sugar": 0},
            {"name": "Chocolate Butternut", "cost": 2.29, "sugar": 0},
            {"name": "Chocolate Creme", "cost": 2.29, "sugar": 0},
            {"name": "Chocolate Dipped French Cruller", "cost": 2.29, "sugar": 0},
            {"name": "Chocolate Frosted", "cost": 2.29, "sugar": 0},
            {"name": "Chocolate Frosted Cake Donut", "cost": 2.29, "sugar": 0},
            {"name": "Chocolate Frosted with Sprinkles", "cost": 2.29, "sugar": 0},
            {"name": "Chocolate Headlight", "cost": 2.29, "sugar": 0},
            {"name": "Chocolate Long John", "cost": 2.29, "sugar": 0},
            {"name": "Cinnamon", "cost": 2.29, "sugar": 0},
            {"name": "Cinnamon Stick", "cost": 2.29, "sugar": 0},
            {"name": "Coconut", "cost": 2.29, "sugar": 0},
            {"name": "Double Chocolate", "cost": 2.29, "sugar": 0},
            {"name": "Eclair", "cost": 2.29, "sugar": 0},
            {"name": "French Cruller", "cost": 2.29, "sugar": 0},
            {"name": "Frosted Vanilla Creme", "cost": 2.29, "sugar": 0},
            {"name": "Glazed", "cost": 2.29, "sugar": 0},
            {"name": "Glazed Blueberry", "cost": 2.29, "sugar": 0},
            {"name": "Glazed Chocolate", "cost": 2.29, "sugar": 0},
            {"name": "Glazed Chocolate Stick", "cost": 2.29, "sugar": 0},
            {"name": "Glazed Jelly", "cost": 2.29, "sugar": 0},
            {"name": "Glazed Jelly Stick", "cost": 2.29, "sugar": 0},
            {"name": "Glazed Stick", "cost": 2.29, "sugar": 0},
            {"name": "Glazed Strawberry", "cost": 2.29, "sugar": 0},
            {"name": "Jelly Donut", "cost": 2.29, "sugar": 0},
            {"name": "Jelly Stick", "cost": 2.29, "sugar": 0},
            {"name": "Lemon", "cost": 2.29, "sugar": 0},
            {"name": "Lemon Stick", "cost": 2.29, "sugar": 0},
            {"name": "Maple Creme", "cost": 2.29, "sugar": 0},
            {"name": "Maple Creme Stick", "cost": 2.29, "sugar": 0},
            {"name": "Maple Frosted", "cost": 2.29, "sugar": 0},
            {"name": "Maple Vanilla Creme", "cost": 2.29, "sugar": 0},
            {"name": "Old Fashioned", "cost": 2.29, "sugar": 0},
            {"name": "Peanut", "cost": 2.29, "sugar": 0},
            {"name": "Plain Stick", "cost": 2.29, "sugar": 0},
            {"name": "Powdered Donut", "cost": 2.29, "sugar": 0},
            {"name": "Powdered Stick", "cost": 2.29, "sugar": 0},
            {"name": "Sour Cream", "cost": 2.29, "sugar": 0},
            {"name": "Strawberry Frosted", "cost": 2.29, "sugar": 0},
            {"name": "Strawberry Frosted with Sprinkles", "cost": 2.29, "sugar": 0},
            {"name": "Sugared Donut", "cost": 2.29, "sugar": 0},
            {"name": "Sugared Stick", "cost": 2.29, "sugar": 0},
            {"name": "Taillight Donut", "cost": 2.29, "sugar": 0},
            {"name": "Toasted Coconut", "cost": 2.29, "sugar": 0},
            {"name": "Vanilla Creme", "cost": 2.29, "sugar": 0},
            {"name": "Vanilla Frosted", "cost": 2.29, "sugar": 0},
            {"name": "Vanilla Frosted Sprinkles", "cost": 2.29, "sugar": 0},
            {"name": "Vanilla Headlight", "cost": 2.29, "sugar": 0},
            {"name": "Vanilla Long John", "cost": 2.29, "sugar": 0}
        ]

        for item in donut_items:
            self.donut_menu.insert("", "end", values=(item["name"], item["cost"], item["sugar"]))

    def submit_sugar_intake(self):
        try:
            sugar_intake = self.sugar_intake_var.get()
            current_time = self.time_of_day_var.get()
            self.sugar_intake_by_time[current_time] += sugar_intake
            self.update_sugar_labels()
            self.total_sugar = sum(self.sugar_intake_by_time.values())
            self.check_sugar_intake()
            self.sugar_entry.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number for sugar intake.")

    def update_sugar_labels(self):
        self.morning_sugar_label.config(text=f"Morning Sugar Intake: {self.sugar_intake_by_time['Morning']:.1f}g")
        self.evening_sugar_label.config(text=f"Evening Sugar Intake: {self.sugar_intake_by_time['Evening']:.1f}g")
        self.night_sugar_label.config(text=f"Night Sugar Intake: {self.sugar_intake_by_time['Night']:.1f}g")

    def check_sugar_intake(self):
        if self.total_sugar > self.max_sugar_intake:
            self.message_label.config(
                text=f"Warning: Your total sugar intake is {self.total_sugar:.1f}g. Watch your sugar intake for the day!",
                foreground="red")
        else:
            self.message_label.config(text=f"Your total sugar intake is {self.total_sugar:.1f}g.", foreground="green")

        self.suggest_low_sugar_options()

    def suggest_low_sugar_options(self):
        low_sugar_coffee = []
        for item in self.coffee_menu.get_children():
            values = self.coffee_menu.item(item, "values")
            if float(values[2]) <= 10:  # Sugar content less than or equal to 10g
                low_sugar_coffee.append(values[0])

        low_sugar_donuts = []
        for item in self.donut_menu.get_children():
            values = self.donut_menu.item(item, "values")
            if float(values[2]) <= 10:  # Sugar content less than or equal to 10g
                low_sugar_donuts.append(values[0])

        coffee_message = "Consider these low sugar coffee options: " + ", ".join(low_sugar_coffee)
        donut_message = "Consider these low sugar donut options: " + ", ".join(low_sugar_donuts)

        if low_sugar_coffee or low_sugar_donuts:
            message = coffee_message + "\n" + donut_message
        else:
            message = "No low sugar options available."

        messagebox.showinfo("Suggestions", message)

    def toggle_inputs(self):
        self.inputs_locked = not self.inputs_locked

        state = 'disabled' if self.inputs_locked else 'normal'

        for widget in [self.sugar_entry, self.size_option, self.dairy_option, self.flavor_option, self.sweetener_option]:
            widget.configure(state=state)

        for rb in self.root.grid_slaves():
            if isinstance(rb, ttk.Radiobutton):
                rb.configure(state=state)

        self.power_button.configure(text="Unlock" if self.inputs_locked else "Lock")

        if not self.inputs_locked:
            messagebox.showinfo("Hi dad!!", "Hi dad!! Happy Father's Day! Hope this helps you choose your next Dunkin order lol :p")

if __name__ == "__main__":
    root = tk.Tk()
    app = DadsDunkin(root)
    root.mainloop()
