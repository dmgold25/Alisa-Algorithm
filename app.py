'''
12/23/24
Daniel Goldblatt
Algorithm for random student selection
'''
# from flask import Flask, render_template, request, jsonify
# import random

# class NameSelector:
#     def __init__(self):
#         self.names = []  # List of names
#         self.selection_order = []  # Tracks order of selections
#         self.selection_counts = {}  # Tracks how many times each name is selected

#     def add_name(self, name):
#         if name and name not in self.names:
#             self.names.append(name)
#             self.selection_counts[name] = 0  # Initialize count

#     def select_name(self):
#         if not self.names:
#             return None, "No names available to select."

#         # Assign weights inversely proportional to recency
#         weights = []
#         for name in self.names:
#             if name not in self.selection_order:
#                 weights.append(1.0)  # High weight for unselected names
#             else:
#                 recency = len(self.selection_order) - self.selection_order[::-1].index(name)
#                 weights.append(1 / recency)

#         # Normalize weights and select a name
#         total_weight = sum(weights)
#         probabilities = [w / total_weight for w in weights]
#         selected_name = random.choices(self.names, weights=probabilities, k=1)[0]

#         # Update order and counts
#         if selected_name in self.selection_order:
#             self.selection_order.remove(selected_name)
#         self.selection_order.append(selected_name)
#         self.selection_counts[selected_name] += 1

#         return selected_name, None

#     def reset(self):
#         """Reset all names and counts."""
#         self.names = []
#         self.selection_order = []
#         self.selection_counts = {}

#     def delete_name(self, name_to_delete):
#         """Delete a specific name and its count."""
#         if name_to_delete in self.names:
#             self.names.remove(name_to_delete)
#             del self.selection_counts[name_to_delete]
#             if name_to_delete in self.selection_order:
#                 self.selection_order.remove(name_to_delete)

# # Flask app setup
# app = Flask(__name__)
# selector = NameSelector()

# # Routes
# @app.route("/")
# def index():
#     return render_template("index.html", names=selector.names, counts=selector.selection_counts)

# @app.route("/add_name", methods=["POST"])
# def add_name():
#     name = request.form.get("name")
#     if name:
#         selector.add_name(name)
#     return jsonify({"success": True, "names": selector.names, "counts": selector.selection_counts})

# @app.route("/select_name", methods=["POST"])
# def select_name():
#     selected_name, error = selector.select_name()
#     if error:
#         return jsonify({"success": False, "error": error})
#     return jsonify({"success": True, "selected_name": selected_name, "counts": selector.selection_counts})

# @app.route("/reset", methods=["POST"])
# def reset():
#     """Reset all names and counts."""
#     selector.reset()
#     return jsonify({"success": True, "names": selector.names, "counts": selector.selection_counts})

# @app.route("/delete_name", methods=["POST"])
# def delete_name():
#     """Delete a specific name and its associated count."""
#     name_to_delete = request.form.get("delete_name")
#     if name_to_delete:
#         selector.delete_name(name_to_delete)
#     return jsonify({"success": True, "names": selector.names, "counts": selector.selection_counts})

# @app.route("/get_counts", methods=["GET"])
# def get_counts():
#     return jsonify(selector.selection_counts)

# # Run the app
# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)

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

    def reset(self):
        self.names = []
        self.selection_order = []
        self.selection_counts = {}

    def delete_name(self, name):
        if name in self.names:
            self.names.remove(name)
            del self.selection_counts[name]
            if name in self.selection_order:
                self.selection_order.remove(name)

# Flask app setup
app = Flask(__name__)

# Dictionary to store different classes
classes = {
    "class1": NameSelector(),  # Initialize with one class by default
}

# Routes
@app.route("/")
def index():
    return render_template("index.html", class_names=list(classes.keys()))

@app.route("/add_name", methods=["POST"])
def add_name():
    class_name = request.form.get("class_name")
    name = request.form.get("name")
    if class_name in classes and name:
        classes[class_name].add_name(name)
    return jsonify({"success": True, "names": classes[class_name].names})

@app.route("/select_name", methods=["POST"])
def select_name():
    class_name = request.form.get("class_name")
    if class_name in classes:
        selected_name, error = classes[class_name].select_name()
        if error:
            return jsonify({"success": False, "error": error})
        return jsonify({"success": True, "selected_name": selected_name, "counts": classes[class_name].selection_counts})
    return jsonify({"success": False, "error": "Class not found"})

@app.route("/get_counts", methods=["GET"])
def get_counts():
    class_name = request.args.get("class_name")
    if class_name in classes:
        return jsonify(classes[class_name].selection_counts)
    return jsonify({"success": False, "error": "Class not found"})

@app.route("/reset", methods=["POST"])
def reset():
    class_name = request.form.get("class_name")
    if class_name in classes:
        classes[class_name].reset()
    return jsonify({"success": True})

@app.route("/delete_name", methods=["POST"])
def delete_name():
    class_name = request.form.get("class_name")
    name = request.form.get("name")
    if class_name in classes and name:
        classes[class_name].delete_name(name)
    return jsonify({"success": True, "names": classes[class_name].names})

@app.route("/create_class", methods=["POST"])
def create_class():
    class_name = request.form.get("class_name")
    if class_name and class_name not in classes:
        classes[class_name] = NameSelector()
        return jsonify({"success": True, "class_names": list(classes.keys())})
    return jsonify({"success": False, "error": "Class already exists or invalid name"})

@app.route("/delete_class", methods=["POST"])
def delete_class():
    class_name = request.form.get("class_name")
    if class_name in classes and len(classes) > 1:
        del classes[class_name]
        return jsonify({"success": True, "class_names": list(classes.keys())})
    return jsonify({"success": False, "error": "Cannot delete the last class"})

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)