'''
12/23/24
Daniel Goldblatt
Algorithm for random student selection
'''

# import tkinter as tk
# from tkinter import messagebox
# import random


# class NameSelector:
#     def __init__(self):
#         self.names = []  # List of names
#         self.selection_order = []  # Keeps track of the order in which names were selected
#         self.selection_counts = {}  # Dictionary to track the count of selections for each name

#     def add_name(self, name):
#         if name and name not in self.names:
#             self.names.append(name)
#             self.selection_counts[name] = 0  # Initialize selection count

#     def select_name(self):
#         if not self.names:
#             return None, "No names available to select."

#         # Assign weights based on recency: less recent => higher weight
#         weights = []
#         for name in self.names:
#             if name not in self.selection_order:
#                 weights.append(1.0)  # High weight for names not yet selected
#             else:
#                 recency = len(self.selection_order) - self.selection_order[::-1].index(name)
#                 weights.append(1 / recency)

#         # Normalize weights to probabilities
#         total_weight = sum(weights)
#         probabilities = [w / total_weight for w in weights]

#         # Randomly select a name
#         selected_name = random.choices(self.names, weights=probabilities, k=1)[0]

#         # Update the selection order
#         if selected_name in self.selection_order:
#             self.selection_order.remove(selected_name)
#         self.selection_order.append(selected_name)

#         # Increment the selection count for the chosen name
#         self.selection_counts[selected_name] += 1

#         return selected_name, None


# # Tkinter GUI
# class NameSelectorApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Name Selector")
#         self.selector = NameSelector()

#         # Input field and Add button
#         self.name_entry = tk.Entry(root, width=30)
#         self.name_entry.grid(row=0, column=0, padx=10, pady=10)

#         self.add_button = tk.Button(root, text="Add Name", command=self.add_name)
#         self.add_button.grid(row=0, column=1, padx=10, pady=10)

#         # Listbox to display added names
#         self.names_listbox = tk.Listbox(root, width=50, height=10)
#         self.names_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

#         # Button to select a name
#         self.select_button = tk.Button(root, text="Select Name", command=self.select_name)
#         self.select_button.grid(row=2, column=0, columnspan=2, pady=10)

#         # Label to display the selected name
#         self.selected_name_label = tk.Label(root, text="", font=("Arial", 14))
#         self.selected_name_label.grid(row=3, column=0, columnspan=2, pady=10)

#         # Frame to display selection counts
#         self.counts_frame = tk.Frame(root)
#         self.counts_frame.grid(row=4, column=0, columnspan=2, pady=10)
#         self.counts_label = tk.Label(self.counts_frame, text="Selection Counts:", font=("Arial", 12))
#         self.counts_label.pack(anchor="w")

#         self.counts_listbox = tk.Listbox(self.counts_frame, width=50, height=10)
#         self.counts_listbox.pack()

#     def add_name(self):
#         name = self.name_entry.get().strip()
#         if name:
#             self.selector.add_name(name)
#             self.name_entry.delete(0, tk.END)
#             self.update_names_listbox()
#             self.update_counts_listbox()
#         else:
#             messagebox.showwarning("Input Error", "Please enter a valid name.")

#     def update_names_listbox(self):
#         self.names_listbox.delete(0, tk.END)
#         for name in self.selector.names:
#             self.names_listbox.insert(tk.END, name)

#     def update_counts_listbox(self):
#         self.counts_listbox.delete(0, tk.END)
#         for name, count in self.selector.selection_counts.items():
#             self.counts_listbox.insert(tk.END, f"{name}: {count} times")

#     def select_name(self):
#         selected_name, error = self.selector.select_name()
#         if error:
#             messagebox.showwarning("Selection Error", error)
#         else:
#             self.selected_name_label.config(text=f"Selected: {selected_name}")
#             self.update_counts_listbox()


# # Run the application
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = NameSelectorApp(root)
#     root.mainloop()


from flask import Flask, render_template, request, jsonify
import random

# Core logic for name selection
class NameSelector:
    def __init__(self):
        self.names = []  # List of names
        self.selection_order = []  # Tracks order of selections
        self.selection_counts = {}  # Tracks how many times each name is selected

    def add_name(self, name):
        if name and name not in self.names:
            self.names.append(name)
            self.selection_counts[name] = 0  # Initialize count

    def select_name(self):
        if not self.names:
            return None, "No names available to select."

        # Assign weights inversely proportional to recency
        weights = []
        for name in self.names:
            if name not in self.selection_order:
                weights.append(1.0)  # High weight for unselected names
            else:
                recency = len(self.selection_order) - self.selection_order[::-1].index(name)
                weights.append(1 / recency)

        # Normalize weights and select a name
        total_weight = sum(weights)
        probabilities = [w / total_weight for w in weights]
        selected_name = random.choices(self.names, weights=probabilities, k=1)[0]

        # Update order and counts
        if selected_name in self.selection_order:
            self.selection_order.remove(selected_name)
        self.selection_order.append(selected_name)
        self.selection_counts[selected_name] += 1

        return selected_name, None

# Flask app setup
app = Flask(__name__)
selector = NameSelector()

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_name", methods=["POST"])
def add_name():
    name = request.form.get("name")
    if name:
        selector.add_name(name)
    return jsonify({"success": True, "names": selector.names})

@app.route("/select_name", methods=["POST"])
def select_name():
    selected_name, error = selector.select_name()
    if error:
        return jsonify({"success": False, "error": error})
    return jsonify({"success": True, "selected_name": selected_name, "counts": selector.selection_counts})

@app.route("/get_counts", methods=["GET"])
def get_counts():
    return jsonify(selector.selection_counts)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=5001)