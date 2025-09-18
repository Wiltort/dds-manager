// static/admin/js/transaction_admin.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Transaction admin JS loaded');
    
    function loadSubcategories(categoryId) {
        console.log('🔄 Loading subcategories for category:', categoryId);
        
        if (categoryId) {
            // Правильный URL
            const url = `/admin/dds/api/subcategories/?category_id=${categoryId}`;
            console.log('📡 Fetching from:', url);
            
            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('✅ Received subcategories:', data);
                    
                    const select = document.getElementById('id_subcategory');
                    if (select) {
                        select.innerHTML = '<option value="">---------</option>';
                        
                        data.forEach(subcat => {
                            const option = document.createElement('option');
                            option.value = subcat.id;
                            option.textContent = subcat.name;
                            select.appendChild(option);
                        });
                    }
                })
                .catch(error => {
                    console.error('❌ Error loading subcategories:', error);
                });
        } else {
            const select = document.getElementById('id_subcategory');
            if (select) {
                select.innerHTML = '<option value="">---------</option>';
            }
        }
    }

    function init() {
        const categorySelect = document.getElementById('id_category');
        const subcategorySelect = document.getElementById('id_subcategory');
        
        console.log('Category select found:', !!categorySelect);
        console.log('Subcategory select found:', !!subcategorySelect);
        
        if (categorySelect && subcategorySelect) {
            // Обработчик изменения категории
            categorySelect.addEventListener('change', function() {
                console.log('🎯 Category changed to:', this.value);
                loadSubcategories(this.value);
            });
            
            // Инициализация при загрузке
            console.log('🏁 Initial category value:', categorySelect.value);
            if (categorySelect.value) {
                loadSubcategories(categorySelect.value);
            }
            
            console.log('✅ Transaction form initialized successfully');
        } else {
            console.log('⏳ Elements not found yet, retrying...');
            setTimeout(init, 100);
        }
    }
    
    // Запускаем инициализацию
    setTimeout(init, 100);
});