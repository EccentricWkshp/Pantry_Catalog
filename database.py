import sqlite3
import json

DATABASE = 'pantry.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  quantity INTEGER NOT NULL,
                  location TEXT NOT NULL,
                  barcode TEXT,
                  brand TEXT,
                  package_size TEXT,
                  packaging TEXT,
                  categories TEXT,
                  image_url TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS locations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS packaging_types
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS categories
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS shopping_lists
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS shopping_list_items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  list_id INTEGER,
                  item_id INTEGER,
                  name TEXT NOT NULL,
                  quantity INTEGER NOT NULL,
                  FOREIGN KEY (list_id) REFERENCES shopping_lists(id),
                  FOREIGN KEY (item_id) REFERENCES items(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS consumed_items
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              location TEXT NOT NULL,
              image_url TEXT)''')
    conn.commit()
    conn.close()

def add_item(name, quantity, location, barcode=None, brand=None, package_size=None, packaging=None, categories=None, image_url=None):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO items (name, quantity, location, barcode, brand, package_size, packaging, categories, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (name, quantity, location, barcode, brand, package_size, packaging, json.dumps(categories), image_url))
    new_item_id = c.lastrowid
    conn.commit()
    conn.close()
    return new_item_id

def get_item_by_barcode(barcode):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE barcode=?", (barcode,))
    item = c.fetchone()
    conn.close()
    if item:
        return {'id': item[0], 'name': item[1], 'quantity': item[2], 'location': item[3], 'barcode': item[4],
                'brand': item[5], 'package_size': item[6], 'packaging': item[7], 'categories': json.loads(item[8] or '[]'), 'image_url': item[9]}
    return None

def update_item_quantity(item_id, new_quantity):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE items SET quantity=? WHERE id=?", (new_quantity, item_id))
    conn.commit()
    conn.close()

def get_items():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM items")
    items = c.fetchall()
    conn.close()
    return [{'id': item[0], 'name': item[1], 'quantity': item[2], 'location': item[3], 'barcode': item[4],
             'brand': item[5], 'package_size': item[6], 'packaging': item[7], 'categories': json.loads(item[8] or '[]'), 'image_url': item[9]} for item in items]

def get_item(item_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE id=?", (item_id,))
    item = c.fetchone()
    conn.close()
    if item:
        return {'id': item[0], 'name': item[1], 'quantity': item[2], 'location': item[3], 'barcode': item[4],
                'brand': item[5], 'package_size': item[6], 'packaging': item[7], 'categories': json.loads(item[8] or '[]'), 'image_url': item[9]}
    return None

def edit_item(id, name, quantity, location, barcode=None, brand=None, package_size=None, packaging=None, categories=None, image_url=None):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE items SET name=?, quantity=?, location=?, barcode=?, brand=?, package_size=?, packaging=?, categories=?, image_url=? WHERE id=?",
              (name, quantity, location, barcode, brand, package_size, packaging, json.dumps(categories), image_url, id))
    conn.commit()
    conn.close()

def delete_item(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE id=?", (id,))
    conn.commit()
    conn.close()

def get_locations():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM locations")
    locations = c.fetchall()
    conn.close()
    return [{'id': loc[0], 'name': loc[1]} for loc in locations]

def add_location(name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO locations (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def edit_location(id, name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE locations SET name=? WHERE id=?", (name, id))
    conn.commit()
    conn.close()

def delete_location(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM locations WHERE id=?", (id,))
    conn.commit()
    conn.close()

def get_packaging_types():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM packaging_types")
    packaging_types = c.fetchall()
    conn.close()
    return [{'id': pt[0], 'name': pt[1]} for pt in packaging_types]

def add_packaging_type(name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO packaging_types (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def edit_packaging_type(id, name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE packaging_types SET name=? WHERE id=?", (name, id))
    conn.commit()
    conn.close()

def delete_packaging_type(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM packaging_types WHERE id=?", (id,))
    conn.commit()
    conn.close()

def get_categories():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM categories")
    categories = c.fetchall()
    conn.close()
    return [{'id': cat[0], 'name': cat[1]} for cat in categories]

def add_category(name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def edit_category(id, name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE categories SET name=? WHERE id=?", (name, id))
    conn.commit()
    conn.close()

def delete_category(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM categories WHERE id=?", (id,))
    conn.commit()
    conn.close()

def create_shopping_list(name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO shopping_lists (name) VALUES (?)", (name,))
    list_id = c.lastrowid
    conn.commit()
    conn.close()
    return list_id

def get_shopping_lists():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM shopping_lists")
    lists = c.fetchall()
    conn.close()
    return [{'id': lst[0], 'name': lst[1]} for lst in lists]

def get_shopping_list(list_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM shopping_lists WHERE id=?", (list_id,))
    shopping_list = c.fetchone()
    c.execute("SELECT * FROM shopping_list_items WHERE list_id=?", (list_id,))
    items = c.fetchall()
    conn.close()
    if shopping_list:
        return {
            'id': shopping_list[0],
            'name': shopping_list[1],
            'items': [{'id': item[0], 'item_id': item[2], 'name': item[3], 'quantity': item[4]} for item in items]
        }
    return None

def add_to_shopping_list(list_id, item_id, name, quantity):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO shopping_list_items (list_id, item_id, name, quantity) VALUES (?, ?, ?, ?)",
              (list_id, item_id, name, quantity))
    conn.commit()
    conn.close()

def remove_from_shopping_list(list_id, item_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM shopping_list_items WHERE list_id=? AND id=?", (list_id, item_id))
    conn.commit()
    conn.close()

def delete_shopping_list(list_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM shopping_list_items WHERE list_id=?", (list_id,))
    c.execute("DELETE FROM shopping_lists WHERE id=?", (list_id,))
    conn.commit()
    conn.close()

def rename_shopping_list(list_id, new_name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE shopping_lists SET name=? WHERE id=?", (new_name, list_id))
    conn.commit()
    conn.close()

def use_item(item_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # First, check if the item exists and has a quantity > 0
    c.execute("SELECT * FROM items WHERE id = ? AND quantity > 0", (item_id,))
    item = c.fetchone()
    
    if item:
        # Decrease the quantity by 1
        new_quantity = item[2] - 1  # Assuming quantity is at index 2
        c.execute("UPDATE items SET quantity = ? WHERE id = ?", (new_quantity, item_id))
        conn.commit()
        
        # Fetch the updated item
        c.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        updated_item = c.fetchone()
        conn.close()
        
        if updated_item:
            return {
                'id': updated_item[0],
                'name': updated_item[1],
                'quantity': updated_item[2],
                'location': updated_item[3],
                'barcode': updated_item[4],
                'brand': updated_item[5],
                'package_size': updated_item[6],
                'packaging': updated_item[7],
                'categories': json.loads(updated_item[8] or '[]'),
                'image_url': updated_item[9]
            }
    
    conn.close()
    return None

def get_consumed_items():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE quantity = 0")
    items = c.fetchall()
    conn.close()
    return [{'id': item[0], 'name': item[1], 'quantity': item[2], 'location': item[3], 'barcode': item[4],
             'brand': item[5], 'package_size': item[6], 'packaging': item[7], 'categories': json.loads(item[8] or '[]'), 'image_url': item[9]} for item in items]

def move_to_pantry(item_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE items SET quantity = 1 WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def update_shopping_list_item(list_id, item_id, name, quantity):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE shopping_list_items SET name=?, quantity=? WHERE list_id=? AND id=?", 
              (name, quantity, list_id, item_id))
    conn.commit()
    conn.close()

def move_to_pantry(item_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Check if the item exists
    c.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = c.fetchone()
    
    if item:
        # Set the quantity to 1
        c.execute("UPDATE items SET quantity = 1 WHERE id = ?", (item_id,))
        conn.commit()
        
        # Fetch the updated item
        c.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        updated_item = c.fetchone()
        conn.close()
        
        if updated_item:
            return {
                'id': updated_item[0],
                'name': updated_item[1],
                'quantity': updated_item[2],
                'location': updated_item[3],
                'barcode': updated_item[4],
                'brand': updated_item[5],
                'package_size': updated_item[6],
                'packaging': updated_item[7],
                'categories': json.loads(updated_item[8] or '[]'),
                'image_url': updated_item[9]
            }
    
    conn.close()
    return None