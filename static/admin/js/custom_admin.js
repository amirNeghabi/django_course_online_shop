// اسکریپت‌های سفارشی برای پنل ادمین

(function() {
    'use strict';

    // منتظر بمان تا DOM کامل لود شود
    document.addEventListener('DOMContentLoaded', function() {
        
        // اضافه کردن تایید حذف با پیام فارسی
        enhanceDeleteConfirmation();
        
        // اضافه کردن tooltips
        addTooltips();
        
        // بهبود جداول
        enhanceTables();
        
        // اضافه کردن shortcut keys
        addKeyboardShortcuts();
        
        // نمایش تعداد آیتم‌های انتخاب شده
        updateSelectedCount();
        
        // Auto-save draft (پیش‌نویس خودکار)
        enableAutoSave();
    });

    // تایید حذف با پیام فارسی
    function enhanceDeleteConfirmation() {
        const deleteButtons = document.querySelectorAll('input[name="_delete"], a.deletelink');
        
        deleteButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                const confirmed = confirm('آیا مطمئن هستید که می‌خواهید این مورد را حذف کنید؟');
                if (!confirmed) {
                    e.preventDefault();
                    return false;
                }
            });
        });
    }

    // اضافه کردن Tooltips
    function addTooltips() {
        const elements = document.querySelectorAll('[title]');
        
        elements.forEach(el => {
            el.style.cursor = 'help';
        });
    }

    // بهبود جداول
    function enhanceTables() {
        const tables = document.querySelectorAll('table');
        
        tables.forEach(table => {
            // اضافه کردن hover effect به سطرها
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(row => {
                row.addEventListener('mouseenter', function() {
                    this.style.backgroundColor = '#f8f9fa';
                });
                row.addEventListener('mouseleave', function() {
                    this.style.backgroundColor = '';
                });
            });
        });
    }

    // Keyboard Shortcuts
    function addKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + S برای ذخیره
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                const saveButton = document.querySelector('input[name="_save"]');
                if (saveButton) {
                    saveButton.click();
                }
            }
            
            // Ctrl/Cmd + K برای فوکوس روی جستجو
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchBox = document.querySelector('#searchbar');
                if (searchBox) {
                    searchBox.focus();
                    searchBox.select();
                }
            }
            
            // Escape برای بستن پنجره‌های باز
            if (e.key === 'Escape') {
                const closeButtons = document.querySelectorAll('.close, .cancel-link');
                if (closeButtons.length > 0) {
                    closeButtons[0].click();
                }
            }
        });
    }

    // نمایش تعداد آیتم‌های انتخاب شده
    function updateSelectedCount() {
        const actionCheckboxes = document.querySelectorAll('input.action-select');
        
        if (actionCheckboxes.length === 0) return;
        
        // ایجاد counter
        const counter = document.createElement('div');
        counter.id = 'selected-counter';
        counter.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            font-weight: 600;
            display: none;
            z-index: 9999;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(counter);
        
        function updateCount() {
            const checked = document.querySelectorAll('input.action-select:checked');
            const count = checked.length;
            
            if (count > 0) {
                counter.textContent = `${count} مورد انتخاب شده`;
                counter.style.display = 'block';
            } else {
                counter.style.display = 'none';
            }
        }
        
        actionCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', updateCount);
        });
        
        // Select All checkbox
        const selectAll = document.querySelector('#action-toggle');
        if (selectAll) {
            selectAll.addEventListener('change', updateCount);
        }
    }

    // Auto-save (پیش‌نویس خودکار)
    function enableAutoSave() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, textarea, select');
            const formId = form.id || 'default-form';
            
            // بارگذاری داده‌های ذخیره شده
            inputs.forEach(input => {
                const savedValue = localStorage.getItem(`autosave_${formId}_${input.name}`);
                if (savedValue && !input.value) {
                    input.value = savedValue;
                }
            });
            
            // ذخیره خودکار هر 30 ثانیه
            let autoSaveTimer;
            inputs.forEach(input => {
                input.addEventListener('input', function() {
                    clearTimeout(autoSaveTimer);
                    autoSaveTimer = setTimeout(() => {
                        localStorage.setItem(`autosave_${formId}_${this.name}`, this.value);
                        showNotification('پیش‌نویس ذخیره شد', 'success');
                    }, 2000);
                });
            });
            
            // پاک کردن پیش‌نویس بعد از submit موفق
            form.addEventListener('submit', function() {
                inputs.forEach(input => {
                    localStorage.removeItem(`autosave_${formId}_${input.name}`);
                });
            });
        });
    }

    // نمایش Notification
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: ${type === 'success' ? '#28a745' : '#17a2b8'};
            color: white;
            padding: 12px 24px;
            border-radius: 5px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            z-index: 10000;
            animation: slideDown 0.3s ease;
            font-size: 14px;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideUp 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // افزودن CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateY(100px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        @keyframes slideDown {
            from {
                transform: translate(-50%, -100px);
                opacity: 0;
            }
            to {
                transform: translate(-50%, 0);
                opacity: 1;
            }
        }
        
        @keyframes slideUp {
            from {
                transform: translate(-50%, 0);
                opacity: 1;
            }
            to {
                transform: translate(-50%, -100px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    // Log برای debugging
    console.log('%c🚀 پنل ادمین فروشگاه آماده است!', 'color: #667eea; font-size: 16px; font-weight: bold;');
    console.log('%cکلیدهای میانبر:', 'color: #764ba2; font-weight: bold;');
    console.log('  Ctrl/Cmd + S: ذخیره');
    console.log('  Ctrl/Cmd + K: جستجو');
    console.log('  Esc: بستن');

})();
