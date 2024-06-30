// Utility function to show notifications
function showNotification(message, type) {
    const notificationContainer = document.getElementById('notification-container');
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notificationContainer.appendChild(notification);

    // Trigger reflow to enable CSS transition
    notification.offsetHeight;

    notification.classList.add('show');

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notificationContainer.removeChild(notification);
        }, 300);
    }, 3000);
}

// Function to add a new item
function addItem() {
    const form = document.getElementById('addItemForm');
    const formData = new FormData(form);
    
    // Handle image upload
    const imageUpload = document.getElementById('image_upload').files[0];
    if (imageUpload) {
        formData.append('image_upload', imageUpload);
    }

    // Ensure location is included
    if (!formData.get('location')) {
        showNotification('Please select a location', 'error');
        return;
    }

    axios.post('/add_item', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
    .then(response => {
        showNotification('Item added successfully', 'success');
        location.reload();
    })
    .catch(error => {
        showNotification('Error adding item: ' + (error.response?.data?.message || error.message), 'error');
        console.error('Error:', error);
    });
}

// Function to edit an item
function editItem(itemId) {
    // Fetch item details and populate the edit form
    axios.get(`/get_item/${itemId}`)
        .then(response => {
            const item = response.data;
            document.getElementById('editItemId').value = item.id;
            document.getElementById('editName').value = item.name;
            document.getElementById('editQuantity').value = item.quantity;
            document.getElementById('editLocation').value = item.location;
            document.getElementById('editBarcode').value = item.barcode || '';
            document.getElementById('editBrand').value = item.brand || '';
            document.getElementById('editPackageSize').value = item.package_size || '';
            document.getElementById('editPackaging').value = item.packaging || '';
            document.getElementById('editImageUrl').value = item.image_url || '';

            // Set selected categories
            const categoriesSelect = document.getElementById('editCategories');
            for (let option of categoriesSelect.options) {
                option.selected = item.categories.includes(option.value);
            }

            // Show the edit modal
            const editModal = new bootstrap.Modal(document.getElementById('editItemModal'));
            editModal.show();
        })
        .catch(error => {
            showNotification('Error fetching item details: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

// Function to update an item
function updateItem() {
    const form = document.getElementById('editItemForm');
    const formData = new FormData(form);
    
    // Handle image upload
    const imageUpload = document.getElementById('editImageUpload').files[0];
    if (imageUpload) {
        formData.append('image_upload', imageUpload);
    }

    axios.post('/edit_item', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
    .then(response => {
        showNotification('Item updated successfully', 'success');
        location.reload();
    })
    .catch(error => {
        showNotification('Error updating item: ' + (error.response?.data?.message || error.message), 'error');
        console.error('Error:', error);
    });
}

// Function to delete an item
function deleteItem(itemId) {
    if (confirm('Are you sure you want to delete this item?')) {
        axios.post('/delete_item', { id: itemId })
            .then(response => {
                showNotification('Item deleted successfully', 'success');
                location.reload();
            })
            .catch(error => {
                showNotification('Error deleting item: ' + (error.response?.data?.message || error.message), 'error');
                console.error('Error:', error);
            });
    }
}

// Function to lookup barcode
function lookupBarcode() {
    const barcode = document.getElementById('barcode').value;
    if (!barcode) {
        showNotification('Please enter a barcode', 'error');
        return;
    }
    axios.post('/lookup_barcode', { barcode: barcode })
        .then(response => {
            const data = response.data;
            if (data.success) {
                document.getElementById('name').value = data.name;
                document.getElementById('brand').value = data.brand;
                document.getElementById('package_size').value = data.package_size;
                document.getElementById('image_url').value = data.image_url;

                // Set selected categories
                const categoriesSelect = document.getElementById('categories');
                for (let option of categoriesSelect.options) {
                    option.selected = data.categories.includes(option.value);
                }

                showNotification('Product information retrieved successfully', 'success');
            } else {
                showNotification('Product not found', 'error');
            }
        })
        .catch(error => {
            showNotification('Error looking up barcode: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

// Function to add a new location
function addLocation() {
    const locationName = document.getElementById('locationName').value;
    if (!locationName) {
        showNotification('Please enter a location name', 'error');
        return;
    }
    axios.post('/add_location', { location: locationName })
        .then(response => {
            showNotification('Location added successfully', 'success');
            location.reload();
        })
        .catch(error => {
            showNotification('Error adding location: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

// Function to edit a location
function editLocation(locationId, locationName) {
    document.getElementById('editLocationId').value = locationId;
    document.getElementById('editLocationName').value = locationName;
    const editModal = new bootstrap.Modal(document.getElementById('editLocationModal'));
    editModal.show();
}

// Function to update a location
function updateLocation() {
    const id = document.getElementById('editLocationId').value;
    const name = document.getElementById('editLocationName').value;
    if (!name) {
        showNotification('Please enter a location name', 'error');
        return;
    }
    axios.post('/edit_location', { id: id, name: name })
        .then(response => {
            showNotification('Location updated successfully', 'success');
            location.reload();
        })
        .catch(error => {
            showNotification('Error updating location: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

// Function to delete a location
function deleteLocation(locationId) {
    if (confirm('Are you sure you want to delete this location?')) {
        axios.post('/delete_location', { id: locationId })
            .then(response => {
                showNotification('Location deleted successfully', 'success');
                location.reload();
            })
            .catch(error => {
                showNotification('Error deleting location: ' + (error.response?.data?.message || error.message), 'error');
                console.error('Error:', error);
            });
    }
}

// Functions for managing packaging types
function addPackagingType() {
    const packagingTypeName = document.getElementById('packagingTypeName').value;
    if (!packagingTypeName) {
        showNotification('Please enter a packaging type name', 'error');
        return;
    }
    axios.post('/add_packaging_type', { packaging_type: packagingTypeName })
        .then(response => {
            showNotification('Packaging type added successfully', 'success');
            location.reload();
        })
        .catch(error => {
            showNotification('Error adding packaging type: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

function editPackagingType(packagingTypeId, packagingTypeName) {
    document.getElementById('editPackagingTypeId').value = packagingTypeId;
    document.getElementById('editPackagingTypeName').value = packagingTypeName;
    const editModal = new bootstrap.Modal(document.getElementById('editPackagingTypeModal'));
    editModal.show();
}

function updatePackagingType() {
    const id = document.getElementById('editPackagingTypeId').value;
    const name = document.getElementById('editPackagingTypeName').value;
    if (!name) {
        showNotification('Please enter a packaging type name', 'error');
        return;
    }
    axios.post('/edit_packaging_type', { id: id, name: name })
        .then(response => {
            showNotification('Packaging type updated successfully', 'success');
            location.reload();
        })
        .catch(error => {
            showNotification('Error updating packaging type: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

function deletePackagingType(packagingTypeId) {
    if (confirm('Are you sure you want to delete this packaging type?')) {
        axios.post('/delete_packaging_type', { id: packagingTypeId })
            .then(response => {
                showNotification('Packaging type deleted successfully', 'success');
                location.reload();
            })
            .catch(error => {
                showNotification('Error deleting packaging type: ' + (error.response?.data?.message || error.message), 'error');
                console.error('Error:', error);
            });
    }
}

// Functions for managing categories
function addCategory() {
    const categoryName = document.getElementById('categoryName').value;
    if (!categoryName) {
        showNotification('Please enter a category name', 'error');
        return;
    }
    axios.post('/add_category', { category: categoryName })
        .then(response => {
            showNotification('Category added successfully', 'success');
            location.reload();
        })
        .catch(error => {
            showNotification('Error adding category: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

function editCategory(categoryId, categoryName) {
    document.getElementById('editCategoryId').value = categoryId;
    document.getElementById('editCategoryName').value = categoryName;
    const editModal = new bootstrap.Modal(document.getElementById('editCategoryModal'));
    editModal.show();
}

function updateCategory() {
    const id = document.getElementById('editCategoryId').value;
    const name = document.getElementById('editCategoryName').value;
    if (!name) {
        showNotification('Please enter a category name', 'error');
        return;
    }
    axios.post('/edit_category', { id: id, name: name })
        .then(response => {
            showNotification('Category updated successfully', 'success');
            location.reload();
        })
        .catch(error => {
            showNotification('Error updating category: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

function deleteCategory(categoryId) {
    if (confirm('Are you sure you want to delete this category?')) {
        axios.post('/delete_category', { id: categoryId })
            .then(response => {
                showNotification('Category deleted successfully', 'success');
                location.reload();
            })
            .catch(error => {
                showNotification('Error deleting category: ' + (error.response?.data?.message || error.message), 'error');
                console.error('Error:', error);
            });
    }
}

// Function to create a new shopping list
function createShoppingList() {
    const listName = document.getElementById('shoppingListName').value;
    if (!listName) {
        showNotification('Please enter a list name', 'error');
        return;
    }
    axios.post('/create_shopping_list', { name: listName })
        .then(response => {
            showNotification('Shopping list created successfully', 'success');
            location.reload();
        })
        .catch(error => {
            showNotification('Error creating shopping list: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

// Function to view a shopping list
function viewShoppingList(listId) {
    axios.get(`/get_shopping_list/${listId}`)
        .then(response => {
            const list = response.data;
            document.getElementById('shoppingListTitle').textContent = list.name;
            const tbody = document.getElementById('shoppingListItems');
            tbody.innerHTML = '';
            list.items.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${item.name}</td>
                    <td>${item.quantity}</td>
                    <td>
                        <button class="btn btn-sm btn-danger" onclick="removeFromShoppingList(${list.id}, ${item.id})">Remove</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
            const viewModal = new bootstrap.Modal(document.getElementById('viewShoppingListModal'));
            viewModal.show();
        })
        .catch(error => {
            showNotification('Error fetching shopping list: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

let currentShoppingListId = null;

function viewShoppingList(listId) {
    currentShoppingListId = listId;
    axios.get(`/get_shopping_list/${listId}`)
        .then(response => {
            const list = response.data;
            document.getElementById('shoppingListTitle').textContent = list.name;
            const tbody = document.getElementById('shoppingListItems');
            tbody.innerHTML = '';
            list.items.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${item.name}</td>
                    <td>${item.quantity}</td>
                    <td>
                        <button class="btn btn-sm btn-danger" onclick="removeFromShoppingList(${list.id}, ${item.id})">Remove</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
            const viewModal = new bootstrap.Modal(document.getElementById('viewShoppingListModal'));
            viewModal.show();
        })
        .catch(error => {
            showNotification('Error fetching shopping list: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

function loadShoppingListItems(listId) {
    axios.get(`/get_shopping_list/${listId}`)
        .then(response => {
            const list = response.data;
            const tbody = document.getElementById(`shoppingListItems-${listId}`);
            tbody.innerHTML = '';
            list.items.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${item.name}</td>
                    <td>${item.quantity}</td>
                    <td>
                        <button class="btn btn-sm btn-info" onclick="editShoppingListItem(${list.id}, ${item.id}, '${item.name}', ${item.quantity})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="removeFromShoppingList(${list.id}, ${item.id})">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        })
        .catch(error => {
            showNotification('Error fetching shopping list: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

function editShoppingListItem(listId, itemId, itemName, itemQuantity) {
    document.getElementById('editItemListId').value = listId;
    document.getElementById('editItemId').value = itemId;
    document.getElementById('editItemName').value = itemName;
    document.getElementById('editItemQuantity').value = itemQuantity;
    
    const modal = new bootstrap.Modal(document.getElementById('editShoppingListItemModal'));
    modal.show();
}

function updateShoppingListItem() {
    const form = document.getElementById('editShoppingListItemForm');
    const formData = new FormData(form);
    const listId = formData.get('editItemListId');
    const itemId = formData.get('editItemId');
    const itemName = formData.get('editItemName');
    const quantity = formData.get('editItemQuantity');

    axios.post('/update_shopping_list_item', {
        list_id: listId,
        item_id: itemId,
        name: itemName,
        quantity: quantity
    })
    .then(response => {
        showNotification('Item updated successfully', 'success');
        loadShoppingListItems(listId);
        const modal = bootstrap.Modal.getInstance(document.getElementById('editShoppingListItemModal'));
        modal.hide();
    })
    .catch(error => {
        showNotification('Error updating item: ' + (error.response?.data?.message || error.message), 'error');
        console.error('Error:', error);
    });
}

function showAddItemToListModal(listId) {
    const modal = new bootstrap.Modal(document.getElementById('addItemToListModal'));
    document.getElementById('addItemListId').value = listId;
    modal.show();
}

function addItemToList() {
    const form = document.getElementById('addItemToListForm');
    const formData = new FormData(form);
    const listId = formData.get('addItemListId');
    const itemName = formData.get('addItemName');
    const quantity = formData.get('addItemQuantity');

    axios.post('/add_to_shopping_list', {
        list_id: listId,
        name: itemName,
        quantity: quantity
    })
    .then(response => {
        showNotification('Item added to shopping list successfully', 'success');
        loadShoppingListItems(listId);
        const modal = bootstrap.Modal.getInstance(document.getElementById('addItemToListModal'));
        modal.hide();
    })
    .catch(error => {
        showNotification('Error adding item to shopping list: ' + (error.response?.data?.message || error.message), 'error');
        console.error('Error:', error);
    });
}

function removeFromShoppingList(listId, itemId) {
    axios.post('/remove_from_shopping_list', { list_id: listId, item_id: itemId })
        .then(response => {
            showNotification('Item removed from shopping list successfully', 'success');
            loadShoppingListItems(listId);
        })
        .catch(error => {
            showNotification('Error removing item from shopping list: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

// Update the addToShoppingList function
function addToShoppingList(itemId, itemName) {
    axios.get('/get_shopping_lists')
        .then(response => {
            const lists = response.data;
            const select = document.getElementById('shoppingListSelect');
            select.innerHTML = '';
            lists.forEach(list => {
                const option = document.createElement('option');
                option.value = list.id;
                option.textContent = list.name;
                select.appendChild(option);
            });
            
            document.getElementById('shoppingListItemId').value = itemId;
            document.getElementById('shoppingListItemName').value = itemName;
            
            // Show the modal
            const modal = new bootstrap.Modal(document.getElementById('addToShoppingListModal'));
            modal.show();
        })
        .catch(error => {
            showNotification('Error fetching shopping lists: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

// Update the confirmAddToShoppingList function
function confirmAddToShoppingList() {
    const listId = document.getElementById('shoppingListSelect').value;
    const itemId = document.getElementById('shoppingListItemId').value;
    const itemName = document.getElementById('shoppingListItemName').value;
    const quantity = document.getElementById('shoppingListItemQuantity').value;

    axios.post('/add_to_shopping_list', { list_id: listId, item_id: itemId, name: itemName, quantity: quantity })
        .then(response => {
            showNotification('Item added to shopping list successfully', 'success');
            const modal = bootstrap.Modal.getInstance(document.getElementById('addToShoppingListModal'));
            modal.hide();
        })
        .catch(error => {
            showNotification('Error adding item to shopping list: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

function renameShoppingList(listId, currentName) {
    document.getElementById('renameListId').value = listId;
    document.getElementById('newListName').value = currentName;
    const modal = new bootstrap.Modal(document.getElementById('renameShoppingListModal'));
    modal.show();
}

function confirmRenameShoppingList() {
    const listId = document.getElementById('renameListId').value;
    const newName = document.getElementById('newListName').value;

    axios.post('/rename_shopping_list', { list_id: listId, new_name: newName })
        .then(response => {
            showNotification('Shopping list renamed successfully', 'success');
            location.reload(); // Refresh the page to show the updated list name
        })
        .catch(error => {
            showNotification('Error renaming shopping list: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

// Function to delete a shopping list
function deleteShoppingList(listId) {
    if (confirm('Are you sure you want to delete this shopping list?')) {
        axios.post('/delete_shopping_list', { list_id: listId })
            .then(response => {
                showNotification('Shopping list deleted successfully', 'success');
                location.reload();
            })
            .catch(error => {
                showNotification('Error deleting shopping list: ' + (error.response?.data?.message || error.message), 'error');
                console.error('Error:', error);
            });
    }
}

function quickAdd() {
    const barcodeInput = document.getElementById('quickAddBarcode');
    const barcode = barcodeInput.value;
    if (!barcode) {
        showNotification('Please enter a barcode', 'error');
        return;
    }

    axios.post('/quick_add', { barcode: barcode })
        .then(response => {
            if (response.data.success) {
                showNotification(response.data.message, 'success');
                const item = response.data.item;
                
                const existingRow = document.querySelector(`#itemsTableBody tr[data-item-id="${item.id}"]`);
                if (existingRow) {
                    // Update existing item
                    const quantityCell = existingRow.querySelector('.item-quantity');
                    quantityCell.textContent = item.quantity;
                    
                    // If the item was previously in the consumed list, remove it from there
                    const consumedRow = document.querySelector(`#consumedItemsTableBody tr[data-item-id="${item.id}"]`);
                    if (consumedRow) {
                        consumedRow.remove();
                    }
                } else {
                    // Add new item
                    updateItemList(item);
                }

                // Clear the barcode input and set focus
                barcodeInput.value = '';
                barcodeInput.focus();
            } else {
                showNotification(response.data.message, 'error');
            }
        })
        .catch(error => {
            showNotification('Error processing quick add: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

function updateItemList(item) {
    const tbody = document.getElementById('itemsTableBody');
    let existingRow = document.querySelector(`#itemsTableBody tr[data-item-id="${item.id}"]`);

    if (existingRow) {
        // Update existing row
        existingRow.querySelector('.item-quantity').textContent = item.quantity;
    } else {
        // Check if the item is in the consumed list
        const consumedRow = document.querySelector(`#consumedItemsTableBody tr[data-item-id="${item.id}"]`);
        if (consumedRow) {
            // Move the item from consumed list to pantry list
            existingRow = createPantryItemRow(consumedRow, item);
            tbody.prepend(existingRow);
            consumedRow.remove();
        } else {
            // Add new row
            existingRow = document.createElement('tr');
            existingRow.setAttribute('data-item-id', item.id);
            existingRow.innerHTML = `
                <td>
                    ${item.image_url ? 
                        `<img src="${item.image_url}" alt="${item.name}" class="img-thumbnail product-image">` :
                        `<img src="/static/images/no-image.png" alt="No Image" class="img-thumbnail product-image">`
                    }
                </td>
                <td>${item.name}</td>
                <td class="item-quantity">${item.quantity}</td>
                <td>${item.location || 'Default Location'}</td>
                <td>
                    <button class="btn btn-sm btn-info" onclick="editItem(${item.id})">Edit</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteItem(${item.id})">Delete</button>
                    <button class="btn btn-sm btn-success" onclick="addToShoppingList(${item.id}, '${item.name}')">+ List</button>
                    <button class="btn btn-sm btn-warning" onclick="useItem(${item.id})">Use</button>
                </td>
            `;
            tbody.prepend(existingRow);
        }
    }
}

function createPantryItemRow(consumedRow, item) {
    const newRow = document.createElement('tr');
    newRow.setAttribute('data-item-id', item.id);
    
    const imageCell = consumedRow.cells[0].cloneNode(true);
    const nameCell = consumedRow.cells[1].cloneNode(true);
    const quantityCell = document.createElement('td');
    quantityCell.className = 'item-quantity';
    quantityCell.textContent = item.quantity;
    const locationCell = document.createElement('td');
    locationCell.textContent = item.location || 'Default Location';
    const actionsCell = document.createElement('td');
    
    actionsCell.innerHTML = `
        <button class="btn btn-sm btn-info" onclick="editItem(${item.id})">Edit</button>
        <button class="btn btn-sm btn-danger" onclick="deleteItem(${item.id})">Delete</button>
        <button class="btn btn-sm btn-success" onclick="addToShoppingList(${item.id}, '${item.name}')">+ List</button>
        <button class="btn btn-sm btn-warning" onclick="useItem(${item.id})">Use</button>
    `;

    newRow.appendChild(imageCell);
    newRow.appendChild(nameCell);
    newRow.appendChild(quantityCell);
    newRow.appendChild(locationCell);
    newRow.appendChild(actionsCell);

    return newRow;
}

function useItem(itemId) {
    axios.post(`/use_item/${itemId}`)
        .then(response => {
            if (response.data.success) {
                showNotification(response.data.message, 'success');
                updateItemQuantity(itemId);
            } else {
                showNotification(response.data.message, 'error');
            }
        })
        .catch(error => {
            showNotification('Error using item: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

function updateItemQuantity(itemId) {
    const row = document.querySelector(`tr[data-item-id="${itemId}"]`);
    if (row) {
        const quantityCell = row.querySelector('.item-quantity');
        let newQuantity = parseInt(quantityCell.textContent) - 1;
        if (newQuantity > 0) {
            quantityCell.textContent = newQuantity;
        } else {
            // Move the item to the consumed items list
            const consumedItemsBody = document.getElementById('consumedItemsTableBody');
            const newRow = createConsumedItemRow(row);
            consumedItemsBody.appendChild(newRow);
            row.remove();
        }
    }
}

function createConsumedItemRow(originalRow) {
    const newRow = document.createElement('tr');
    newRow.setAttribute('data-item-id', originalRow.getAttribute('data-item-id'));
    
    const imageCell = originalRow.cells[0].cloneNode(true);
    const nameCell = originalRow.cells[1].cloneNode(true);
    const actionsCell = document.createElement('td');
    
    actionsCell.innerHTML = `
        <button class="btn btn-sm btn-success" onclick="moveToPantry(${newRow.getAttribute('data-item-id')})">Move to Pantry</button>
        <button class="btn btn-sm btn-info" onclick="editItem(${newRow.getAttribute('data-item-id')})">Edit</button>
        <button class="btn btn-sm btn-danger" onclick="deleteItem(${newRow.getAttribute('data-item-id')})">Remove</button>
    `;

    newRow.appendChild(imageCell);
    newRow.appendChild(nameCell);
    newRow.appendChild(actionsCell);

    return newRow;
}

function moveToPantry(itemId) {
    axios.post(`/move_to_pantry/${itemId}`)
        .then(response => {
            if (response.data.success) {
                showNotification(response.data.message, 'success');
                moveItemToPantryList(itemId);
            } else {
                showNotification(response.data.message, 'error');
            }
        })
        .catch(error => {
            showNotification('Error moving item to pantry: ' + (error.response?.data?.message || error.message), 'error');
            console.error('Error:', error);
        });
}

function moveItemToPantryList(itemId) {
    const consumedRow = document.querySelector(`#consumedItemsTableBody tr[data-item-id="${itemId}"]`);
    if (consumedRow) {
        const pantryItemsBody = document.getElementById('itemsTableBody');
        const newRow = createPantryItemRow(consumedRow);
        pantryItemsBody.appendChild(newRow);
        consumedRow.remove();
    }
}

function createPantryItemRow(originalRow) {
    const newRow = document.createElement('tr');
    newRow.setAttribute('data-item-id', originalRow.getAttribute('data-item-id'));
    
    const imageCell = originalRow.cells[0].cloneNode(true);
    const nameCell = originalRow.cells[1].cloneNode(true);
    const quantityCell = document.createElement('td');
    quantityCell.className = 'item-quantity';
    quantityCell.textContent = '1';
    const locationCell = document.createElement('td');
    locationCell.textContent = 'Default Location'; // You might want to set this to a more appropriate value
    const actionsCell = document.createElement('td');
    
    actionsCell.innerHTML = `
        <button class="btn btn-sm btn-info" onclick="editItem(${newRow.getAttribute('data-item-id')})">Edit</button>
        <button class="btn btn-sm btn-danger" onclick="deleteItem(${newRow.getAttribute('data-item-id')})">Delete</button>
        <button class="btn btn-sm btn-success" onclick="addToShoppingList(${newRow.getAttribute('data-item-id')}, '${nameCell.textContent}')">+ List</button>
        <button class="btn btn-sm btn-warning" onclick="useItem(${newRow.getAttribute('data-item-id')})">Use</button>
    `;

    newRow.appendChild(imageCell);
    newRow.appendChild(nameCell);
    newRow.appendChild(quantityCell);
    newRow.appendChild(locationCell);
    newRow.appendChild(actionsCell);

    return newRow;
}

// Event listener for quick add button
document.addEventListener('DOMContentLoaded', function() {
    const quickAddButton = document.getElementById('quickAddButton');
    const quickAddInput = document.getElementById('quickAddBarcode');

    if (quickAddButton) {
        quickAddButton.addEventListener('click', quickAdd);
    }

    if (quickAddInput) {
        quickAddInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                quickAdd();
            }
        });
    }
});