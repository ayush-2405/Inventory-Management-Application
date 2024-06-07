
# Inventory Management System

This project is a simple Inventory Management System built using Python and Tkinter. It allows users to manage inventory items, including adding, updating, and deleting items, as well as exporting the inventory data to a CSV file.

## Features
#### Add Multiple Items:
Add multiple items with details such as item name, cost, number, and remarks.

#### Predefined Items: 
Quickly fill in item details from a predefined list.

#### Update Items: 
Update the details of existing items in the inventory.

#### Delete Items: 
Remove items from the inventory.

#### Export to CSV: 
Export the inventory data to a CSV file.

#### Database Storage: 
Uses SQLite to store inventory data persistently.

Class `InventoryManagementSystem`

```__init__(self, root)```

#### Initialization: 
The constructor initializes the main application window and sets up the initial state of the application.

#### Predefined Items: 
A dictionary of predefined items with their costs.

#### Database Setup: 
Connects to an SQLite database named inventory.db and calls ```create_table()``` to ensure the necessary table exists.

#### UI Components: 
Calls ```create_widgets()``` to set up the GUI components and ```load_data_into_tree()``` to load existing data into the tree view.

#### Keyboard Binding: 
Binds the Enter key to trigger the ```add_multiple_items()``` method.

```create_table(self)```

#### Database Schema: 
Creates the inventory table with columns for ID, item name, cost, number, and remarks if it doesn't already exist.

```create_widgets(self)```

#### UI Setup: 
Creates the main layout and components of the application.

#### Items Frame: 
A frame to input multiple items.

#### Labels and Buttons: 
Adds labels for item attributes and buttons to add items, update items, delete items, and download CSV.

#### Tree View: 
A table-like widget to display the inventory items with columns for ID, item name, cost, number, remarks, and total cost. The ID column is hidden.

```fill_cost(self, event, cost_entry)```

#### Auto-fill Cost: 
Fills the cost entry field based on the selected predefined item.

```add_item_row(self)```

#### Dynamic Row Addition: 
Adds a new row of input fields (name, cost, number, remarks) to the items frame.
add_multiple_items(self, event=None)

#### Add Items to Database: 
Loops through the input fields, validates the inputs, and inserts the items into the database. Then refreshes the tree view and clears the input fields.

```update_item(self)```

#### Update Item: 
Opens a new window with the selected item's data pre-filled in input fields. After editing, the changes are saved back to the database.

```delete_item(self, event=None)```

#### Delete Item: 
Deletes the selected item(s) from the database and refreshes the tree view.
select_item(self, event)

#### Placeholder Method: 
This method is a placeholder for future functionality (if needed).

```clear_entries(self)```

#### Clear Input Fields: 
Clears all input fields in the items frame.

```load_data_into_tree(self)```

#### Load Data: 
Clears the tree view and reloads all items from the database into it, calculating and displaying the total cost for each item.

```download_csv(self)```

#### Export to CSV: 
Exports the inventory data to a CSV file. It retrieves the data from the database, allows the user to choose the save location, and writes the data to the file.
