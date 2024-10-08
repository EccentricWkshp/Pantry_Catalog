from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from database import (
    DATABASE,  # Import the DATABASE constant
    init_db, add_item, get_items, get_item, get_locations, add_location,
    get_packaging_types, get_categories, add_category, delete_item, edit_item,
    delete_location, edit_location, delete_category, edit_category,
    add_packaging_type, delete_packaging_type, edit_packaging_type,
    create_shopping_list, get_shopping_lists, get_shopping_list,
    add_to_shopping_list, remove_from_shopping_list, delete_shopping_list,
    rename_shopping_list, get_item_by_barcode, update_item_quantity,
    use_item, get_consumed_items, move_to_pantry, update_shopping_list_item
)
import requests
import json
import os
import shutil
from datetime import datetime
from werkzeug.utils import secure_filename
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer
import io
import atexit
from datetime import datetime

app = Flask(__name__)
init_db()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global variable to store paths of temporary files
temp_files = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    items = sorted(get_items(), key=lambda x: x['name'].lower())
    consumed_items = sorted(get_consumed_items(), key=lambda x: x['name'].lower())
    locations = sorted(get_locations(), key=lambda x: x['name'].lower())
    packaging_types = sorted(get_packaging_types(), key=lambda x: x['name'].lower())
    categories = sorted(get_categories(), key=lambda x: x['name'].lower())

    return render_template('index.html', items=items, consumed_items=consumed_items, locations=locations, packaging_types=packaging_types, categories=categories)

@app.route('/use_item/<int:item_id>', methods=['POST'])
def use_item_route(item_id):
    try:
        updated_item = use_item(item_id)
        if updated_item:
            return jsonify({"success": True, "message": "Item used successfully", "item": updated_item}), 200
        else:
            return jsonify({"success": False, "message": "Item not found or quantity already zero"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/move_to_pantry/<int:item_id>', methods=['POST'])
def move_to_pantry_route(item_id):
    try:
        updated_item = move_to_pantry(item_id)
        if updated_item:
            return jsonify({"success": True, "message": "Item moved to pantry successfully", "item": updated_item}), 200
        else:
            return jsonify({"success": False, "message": "Item not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
@app.route('/add_item', methods=['POST'])
def add_item_route():
    try:
        name = request.form['name']
        quantity = request.form['quantity']
        location = request.form['location']
        barcode = request.form.get('barcode')
        brand = request.form.get('brand')
        package_size = request.form.get('package_size')
        packaging = request.form.get('packaging')
        categories = request.form.getlist('categories')
        image_url = request.form.get('image_url')

        # Handle image upload
        if 'image_upload' in request.files:
            file = request.files['image_upload']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_url = f'/static/uploads/{filename}'

        new_item = add_item(name, quantity, location, barcode, brand, package_size, packaging, categories, image_url)

        return jsonify({"success": True, "message": "Item added successfully", "item": get_item(new_item)}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/get_item/<int:item_id>', methods=['GET'])
def get_item_route(item_id):
    try:
        item = get_item(item_id)
        if item:
            return jsonify(item), 200
        else:
            return jsonify({"success": False, "message": "Item not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/edit_item', methods=['POST'])
def edit_item_route():
    try:
        id = request.form['editItemId']
        name = request.form['editName']
        quantity = request.form['editQuantity']
        location = request.form['editLocation']
        barcode = request.form.get('editBarcode')
        brand = request.form.get('editBrand')
        package_size = request.form.get('editPackageSize')
        packaging = request.form.get('editPackaging')
        categories = request.form.getlist('editCategories')
        
        # Handle image update
        if 'image_upload' in request.files:
            file = request.files['image_upload']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_url = f'/static/uploads/{filename}'
            else:
                image_url = None
        elif 'image_url' in request.form:
            image_url = request.form['image_url']
        else:
            # If no new image is provided, keep the existing one
            existing_item = get_item(id)
            image_url = existing_item['image_url'] if existing_item else None

        edit_item(id, name, quantity, location, barcode, brand, package_size, packaging, categories, image_url)
        return jsonify({"success": True, "message": "Item updated successfully", "item": get_item(id)}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/delete_item', methods=['POST'])
def delete_item_route():
    item_id = request.json['id']
    delete_item(item_id)
    return jsonify({"success": True, "message": "Item deleted successfully"}), 200

@app.route('/add_location', methods=['POST'])
def add_location_route():
    try:
        location = request.json['location']
        add_location(location)
        return jsonify({"success": True, "message": "Location added successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/edit_location', methods=['POST'])
def edit_location_route():
    data = request.json
    edit_location(data['id'], data['name'])
    return jsonify({"success": True, "message": "Location updated successfully"}), 200

@app.route('/delete_location', methods=['POST'])
def delete_location_route():
    location_id = request.json['id']
    delete_location(location_id)
    return jsonify({"success": True, "message": "Location deleted successfully"}), 200

@app.route('/add_category', methods=['POST'])
def add_category_route():
    try:
        category = request.json['category']
        add_category(category)
        return jsonify({"success": True, "message": "Category added successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/edit_category', methods=['POST'])
def edit_category_route():
    data = request.json
    edit_category(data['id'], data['name'])
    return jsonify({"success": True, "message": "Category updated successfully"}), 200

@app.route('/delete_category', methods=['POST'])
def delete_category_route():
    category_id = request.json['id']
    delete_category(category_id)
    return jsonify({"success": True, "message": "Category deleted successfully"}), 200

@app.route('/add_packaging_type', methods=['POST'])
def add_packaging_type_route():
    try:
        packaging_type = request.json['packaging_type']
        add_packaging_type(packaging_type)
        return jsonify({"success": True, "message": "Packaging type added successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/edit_packaging_type', methods=['POST'])
def edit_packaging_type_route():
    data = request.json
    edit_packaging_type(data['id'], data['name'])
    return jsonify({"success": True, "message": "Packaging type updated successfully"}), 200

@app.route('/delete_packaging_type', methods=['POST'])
def delete_packaging_type_route():
    packaging_type_id = request.json['id']
    delete_packaging_type(packaging_type_id)
    return jsonify({"success": True, "message": "Packaging type deleted successfully"}), 200

@app.route('/lookup_barcode', methods=['POST'])
def lookup_barcode():
    barcode = request.json['barcode']
    # Use Open Food Facts API to look up the barcode
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    headers = {
        'User-Agent': 'PantryCatalogApp/1.0 (https://example.com)'  # Replace with your app's user agent
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 1:
            product = data['product']
            return jsonify({
                "success": True,
                "name": product.get('product_name', ''),
                "brand": product.get('brands', ''),
                "package_size": product.get('quantity', ''),
                "image_url": product.get('image_url', ''),
                "categories": product.get('categories_tags', [])
            }), 200
        else:
            return jsonify({"success": False, "message": "Product not found"}), 404
    else:
        return jsonify({"success": False, "message": "Error looking up barcode"}), 500

@app.route('/manage_data')
def manage_data():
    locations = sorted(get_locations(), key=lambda x: x['name'].lower())
    packaging_types = sorted(get_packaging_types(), key=lambda x: x['name'].lower())
    categories = sorted(get_categories(), key=lambda x: x['name'].lower())
    return render_template('manage_data.html', locations=locations, packaging_types=packaging_types, categories=categories)

@app.route('/shopping_lists')
def shopping_lists():
    lists = sorted(get_shopping_lists(), key=lambda x: x['name'].lower())
    return render_template('shopping_lists.html', lists=lists)

@app.route('/get_shopping_lists', methods=['GET'])
def get_shopping_lists_route():
    try:
        lists = get_shopping_lists()
        return jsonify(lists), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/create_shopping_list', methods=['POST'])
def create_shopping_list_route():
    try:
        name = request.json['name']
        list_id = create_shopping_list(name)
        return jsonify({"success": True, "message": "Shopping list created successfully", "id": list_id}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/get_shopping_list/<int:list_id>', methods=['GET'])
def get_shopping_list_route(list_id):
    try:
        shopping_list = get_shopping_list(list_id)
        if shopping_list:
            shopping_list['items'] = sorted(shopping_list['items'], key=lambda x: x['name'].lower())
            return jsonify(shopping_list), 200
        else:
            return jsonify({"success": False, "message": "Shopping list not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/add_to_shopping_list', methods=['POST'])
def add_to_shopping_list_route():
    try:
        list_id = request.json['list_id']
        name = request.json['name']
        quantity = request.json['quantity']
        add_to_shopping_list(list_id, None, name, quantity)
        return jsonify({"success": True, "message": "Item added to shopping list successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/remove_from_shopping_list', methods=['POST'])
def remove_from_shopping_list_route():
    try:
        list_id = request.json['list_id']
        item_id = request.json['item_id']
        remove_from_shopping_list(list_id, item_id)
        return jsonify({"success": True, "message": "Item removed from shopping list successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/update_shopping_list_item', methods=['POST'])
def update_shopping_list_item_route():
    try:
        list_id = request.json['list_id']
        item_id = request.json['item_id']
        name = request.json['name']
        quantity = request.json['quantity']
        update_shopping_list_item(list_id, item_id, name, quantity)
        return jsonify({"success": True, "message": "Item updated successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/rename_shopping_list', methods=['POST'])
def rename_shopping_list_route():
    try:
        list_id = request.json['list_id']
        new_name = request.json['new_name']
        rename_shopping_list(list_id, new_name)
        return jsonify({"success": True, "message": "Shopping list renamed successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/delete_shopping_list', methods=['POST'])
def delete_shopping_list_route():
    try:
        list_id = request.json['list_id']
        delete_shopping_list(list_id)
        return jsonify({"success": True, "message": "Shopping list deleted successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/print_shopping_list/<int:list_id>')
def print_shopping_list(list_id):
    shopping_list = get_shopping_list(list_id)
    if shopping_list:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Add title
        styles = getSampleStyleSheet()
        elements.append(Paragraph(f"{shopping_list['name']}", styles['Title']))
        elements.append(Spacer(1, 12))

        # Create table data
        data = [['Item', 'Quantity']]
        for item in shopping_list['items']:
            data.append([item['name'], str(item['quantity'])])

        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)

        # Build PDF
        doc.build(elements)

        buffer.seek(0)
        
        # Generate filename using shopping list name and current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        safe_filename = "".join([c for c in shopping_list['name'] if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        filename = f"{safe_filename}_{current_date}.pdf"
        
        return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')
    else:
        return jsonify({"success": False, "message": "Shopping list not found"}), 404

@app.route('/quick_add', methods=['POST'])
def quick_add():
    try:
        barcode = request.json['barcode']
        location = request.json['location']
        
        # Check if the item already exists
        existing_item = get_item_by_barcode(barcode)
        
        if existing_item:
            # Update the quantity of the existing item
            new_quantity = existing_item['quantity'] + 1
            update_item_quantity(existing_item['id'], new_quantity)
            existing_item['quantity'] = new_quantity
            return jsonify({"success": True, "message": "Item quantity updated successfully", "item": existing_item}), 200
        
        # If the item doesn't exist, look up the barcode
        url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 1:
                product = data['product']
                name = product.get('product_name', '')
                brand = product.get('brands', '')
                package_size = product.get('quantity', '')
                image_url = product.get('image_url', '')
                categories = product.get('categories', '').split(',')
                
                # Add the new item
                new_item_id = add_item(name, 1, location, barcode, brand, package_size, None, categories, image_url)
                
                new_item = {
                    "id": new_item_id,
                    "name": name,
                    "quantity": 1,
                    "location": location,
                    "barcode": barcode,
                    "brand": brand,
                    "package_size": package_size,
                    "image_url": image_url,
                    "categories": categories
                }
                
                return jsonify({
                    "success": True,
                    "message": "New item added successfully",
                    "item": new_item
                }), 200
            else:
                print(f"Product not found {barcode}: {response.status_code}")
                return jsonify({"success": False, "message": "Product not found"}), 404
        elif response.status_code == 404:
            data = response.json()
            if data.get('status') == 0:
                return jsonify({"success": False, "message": "Product not found"}), 404
            else:
                return jsonify({"success": False, "message": "Unexpected error"}), 500
    except Exception as e:
        print(f"Exception: {e}")  # Add logging for the exception
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/download_database')
def download_database():
    global temp_files
    try:
        # Create a backup copy of the database
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f'pantry_catalog_backup_{timestamp}.db'
        backup_path = os.path.join(app.root_path, 'temp', backup_filename)
        
        # Ensure the temp directory exists
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        # Copy the database file
        shutil.copy2(DATABASE, backup_path)
        
        # Add the backup file path to the list of temporary files
        temp_files.append(backup_path)
        
        # Send the backup file
        return send_file(backup_path,
                         as_attachment=True, 
                         download_name=backup_filename, 
                         mimetype='application/x-sqlite3')
    except Exception as e:
        return str(e)

def cleanup_temp_files():
    global temp_files
    for file_path in temp_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting temporary file {file_path}: {str(e)}")
    temp_files = []

# Register the cleanup function to run when the application exits
atexit.register(cleanup_temp_files)

@app.route('/get_items', methods=['GET'])
def get_items_route():
    try:
        items = get_items()
        return jsonify(items), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == '__main__':
    # Clean up any leftover temporary files from previous runs
    cleanup_temp_files()

    app.run(debug=True, host="127.0.0.1", port=5000)  # Modify the port if needed