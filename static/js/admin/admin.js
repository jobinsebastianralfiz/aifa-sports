/**
 * AIFA Football Academy - Admin Dashboard JavaScript
 * Version: 1.0
 */

// ==========================================================================
// UTILITY FUNCTIONS
// ==========================================================================

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

// ==========================================================================
// SIDEBAR
// ==========================================================================

const initSidebar = () => {
    const sidebar = $('.admin-sidebar');
    const main = $('.admin-main');
    const toggleBtns = $$('.sidebar-toggle, .header-toggle');

    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            main.classList.toggle('expanded');

            // Store preference
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
        });
    });

    // Restore preference
    if (localStorage.getItem('sidebarCollapsed') === 'true') {
        sidebar.classList.add('collapsed');
        main.classList.add('expanded');
    }

    // Mobile sidebar
    const mobileToggle = $('.header-toggle');
    if (window.innerWidth <= 768) {
        mobileToggle?.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!sidebar.contains(e.target) && !mobileToggle?.contains(e.target)) {
                sidebar.classList.remove('active');
            }
        });
    }
};

// ==========================================================================
// DROPDOWN MENUS
// ==========================================================================

const initDropdowns = () => {
    $$('.dropdown').forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');

        toggle?.addEventListener('click', (e) => {
            e.stopPropagation();

            // Close other dropdowns
            $$('.dropdown.active').forEach(d => {
                if (d !== dropdown) d.classList.remove('active');
            });

            dropdown.classList.toggle('active');
        });
    });

    // Close on outside click
    document.addEventListener('click', () => {
        $$('.dropdown.active').forEach(d => d.classList.remove('active'));
    });
};

// ==========================================================================
// DATA TABLE
// ==========================================================================

const initDataTables = () => {
    $$('.data-table').forEach(table => {
        // Sortable headers
        table.querySelectorAll('th[data-sortable]').forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {
                sortTable(table, header);
            });
        });

        // Select all checkbox
        const selectAll = table.querySelector('.select-all');
        const checkboxes = table.querySelectorAll('.row-checkbox');

        if (selectAll) {
            selectAll.addEventListener('change', () => {
                checkboxes.forEach(cb => cb.checked = selectAll.checked);
                updateBulkActions(table);
            });
        }

        checkboxes.forEach(cb => {
            cb.addEventListener('change', () => {
                updateBulkActions(table);
                updateSelectAll(table);
            });
        });
    });
};

const sortTable = (table, header) => {
    const index = Array.from(header.parentElement.children).indexOf(header);
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const isAsc = header.classList.contains('sort-asc');

    // Reset all headers
    table.querySelectorAll('th').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });

    // Sort rows
    rows.sort((a, b) => {
        const aValue = a.children[index]?.textContent.trim() || '';
        const bValue = b.children[index]?.textContent.trim() || '';

        if (!isNaN(aValue) && !isNaN(bValue)) {
            return isAsc ? bValue - aValue : aValue - bValue;
        }

        return isAsc
            ? bValue.localeCompare(aValue)
            : aValue.localeCompare(bValue);
    });

    // Update DOM
    rows.forEach(row => tbody.appendChild(row));

    // Update header state
    header.classList.add(isAsc ? 'sort-desc' : 'sort-asc');
};

const updateBulkActions = (table) => {
    const checked = table.querySelectorAll('.row-checkbox:checked').length;
    const bulkActions = table.closest('.data-table-wrapper')?.querySelector('.bulk-actions');

    if (bulkActions) {
        if (checked > 0) {
            bulkActions.classList.add('active');
            bulkActions.querySelector('.selected-count').textContent = checked;
        } else {
            bulkActions.classList.remove('active');
        }
    }
};

const updateSelectAll = (table) => {
    const selectAll = table.querySelector('.select-all');
    const checkboxes = table.querySelectorAll('.row-checkbox');
    const checkedCount = table.querySelectorAll('.row-checkbox:checked').length;

    if (selectAll) {
        selectAll.checked = checkedCount === checkboxes.length;
        selectAll.indeterminate = checkedCount > 0 && checkedCount < checkboxes.length;
    }
};

// ==========================================================================
// SEARCH & FILTER
// ==========================================================================

const initSearch = () => {
    const searchInputs = $$('.table-search');

    searchInputs.forEach(input => {
        input.addEventListener('input', debounce(() => {
            const table = input.closest('.data-table-wrapper')?.querySelector('.data-table tbody');
            const searchTerm = input.value.toLowerCase();

            if (table) {
                table.querySelectorAll('tr').forEach(row => {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(searchTerm) ? '' : 'none';
                });
            }
        }, 300));
    });
};

const initFilters = () => {
    $$('.filter-select').forEach(select => {
        select.addEventListener('change', () => {
            applyFilters();
        });
    });
};

const applyFilters = () => {
    const filters = {};

    $$('.filter-select').forEach(select => {
        const key = select.dataset.filter;
        const value = select.value;
        if (key && value) {
            filters[key] = value;
        }
    });

    // Apply filters to table or trigger API call
    console.log('Applying filters:', filters);
};

// ==========================================================================
// MODALS
// ==========================================================================

const initModals = () => {
    // Open modal
    $$('[data-modal-target]').forEach(trigger => {
        trigger.addEventListener('click', () => {
            const modal = $(trigger.dataset.modalTarget);
            openModal(modal);
        });
    });

    // Close modal
    $$('.modal-close, .modal-overlay').forEach(closer => {
        closer.addEventListener('click', () => {
            closeAllModals();
        });
    });

    // Close on escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });
};

const openModal = (modal) => {
    if (!modal) return;

    const overlay = $('.modal-overlay');
    modal.classList.add('active');
    overlay?.classList.add('active');
    document.body.style.overflow = 'hidden';
};

const closeAllModals = () => {
    $$('.modal.active').forEach(m => m.classList.remove('active'));
    $('.modal-overlay')?.classList.remove('active');
    document.body.style.overflow = '';
};

window.openModal = openModal;
window.closeAllModals = closeAllModals;

// ==========================================================================
// FORM HANDLING
// ==========================================================================

const initForms = () => {
    // Auto-save drafts
    $$('form[data-autosave]').forEach(form => {
        const formId = form.id || form.dataset.autosave;

        // Restore saved data
        const savedData = localStorage.getItem(`form_${formId}`);
        if (savedData) {
            const data = JSON.parse(savedData);
            Object.keys(data).forEach(key => {
                const input = form.querySelector(`[name="${key}"]`);
                if (input) input.value = data[key];
            });
        }

        // Save on input
        form.querySelectorAll('input, textarea, select').forEach(input => {
            input.addEventListener('input', debounce(() => {
                const formData = new FormData(form);
                const data = Object.fromEntries(formData);
                localStorage.setItem(`form_${formId}`, JSON.stringify(data));
            }, 500));
        });

        // Clear on submit
        form.addEventListener('submit', () => {
            localStorage.removeItem(`form_${formId}`);
        });
    });

    // Form validation
    $$('form[data-validate]').forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!validateForm(form)) {
                e.preventDefault();
            }
        });
    });
};

const validateForm = (form) => {
    let isValid = true;

    // Clear previous errors
    form.querySelectorAll('.form-error').forEach(e => e.remove());
    form.querySelectorAll('.form-input-error').forEach(i => i.classList.remove('form-input-error'));

    // Required fields
    form.querySelectorAll('[required]').forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            showFieldError(input, 'This field is required');
        }
    });

    // Email validation
    form.querySelectorAll('[type="email"]').forEach(input => {
        if (input.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value)) {
            isValid = false;
            showFieldError(input, 'Please enter a valid email');
        }
    });

    // Phone validation
    form.querySelectorAll('[data-validate="phone"]').forEach(input => {
        if (input.value && !/^[\d\s\-+()]{10,}$/.test(input.value)) {
            isValid = false;
            showFieldError(input, 'Please enter a valid phone number');
        }
    });

    return isValid;
};

const showFieldError = (input, message) => {
    input.classList.add('form-input-error');
    const error = document.createElement('span');
    error.className = 'form-error';
    error.textContent = message;
    input.parentElement.appendChild(error);
};

// ==========================================================================
// FILE UPLOAD
// ==========================================================================

const initFileUpload = () => {
    $$('.file-upload-zone').forEach(zone => {
        const input = zone.querySelector('input[type="file"]');
        const preview = zone.querySelector('.file-preview');

        // Click to upload
        zone.addEventListener('click', () => input.click());

        // Drag and drop
        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('drag-over');
        });

        zone.addEventListener('dragleave', () => {
            zone.classList.remove('drag-over');
        });

        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('drag-over');

            const files = e.dataTransfer.files;
            if (files.length) {
                input.files = files;
                handleFileSelect(input, preview);
            }
        });

        // File selected
        input.addEventListener('change', () => {
            handleFileSelect(input, preview);
        });
    });
};

const handleFileSelect = (input, preview) => {
    if (!preview) return;

    preview.innerHTML = '';
    Array.from(input.files).forEach(file => {
        const item = document.createElement('div');
        item.className = 'file-preview-item';

        if (file.type.startsWith('image/')) {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            item.appendChild(img);
        } else {
            item.innerHTML = `
                <div class="file-icon">📄</div>
                <span class="file-name">${file.name}</span>
            `;
        }

        preview.appendChild(item);
    });
};

// ==========================================================================
// NOTIFICATIONS
// ==========================================================================

const initNotifications = () => {
    const notificationBtn = $('.notifications-btn');
    const notificationPanel = $('.notification-panel');

    if (notificationBtn && notificationPanel) {
        notificationBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            notificationPanel.classList.toggle('active');
        });

        document.addEventListener('click', (e) => {
            if (!notificationPanel.contains(e.target)) {
                notificationPanel.classList.remove('active');
            }
        });
    }
};

// ==========================================================================
// TOAST NOTIFICATIONS
// ==========================================================================

const showToast = (message, type = 'info', duration = 3000) => {
    let container = $('.toast-container');

    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const icons = {
        success: '✓',
        error: '✕',
        warning: '⚠',
        info: 'ℹ'
    };

    toast.innerHTML = `
        <div class="toast-icon">${icons[type] || icons.info}</div>
        <div class="toast-message">${message}</div>
        <button class="toast-close">&times;</button>
    `;

    container.appendChild(toast);

    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);

    // Auto dismiss
    const timer = setTimeout(() => dismissToast(toast), duration);

    // Manual dismiss
    toast.querySelector('.toast-close').addEventListener('click', () => {
        clearTimeout(timer);
        dismissToast(toast);
    });
};

const dismissToast = (toast) => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
};

window.showToast = showToast;

// ==========================================================================
// CONFIRM DIALOGS
// ==========================================================================

const confirmAction = (message, onConfirm, onCancel) => {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay active';

    const dialog = document.createElement('div');
    dialog.className = 'modal modal-sm active';
    dialog.innerHTML = `
        <div class="modal-body text-center py-8">
            <div class="confirm-icon mb-4">⚠️</div>
            <h4 class="mb-3">${message}</h4>
            <div class="flex justify-center gap-3 mt-6">
                <button class="btn btn-secondary" id="confirmCancel">Cancel</button>
                <button class="btn btn-primary" id="confirmOk">Confirm</button>
            </div>
        </div>
    `;

    document.body.appendChild(overlay);
    document.body.appendChild(dialog);
    document.body.style.overflow = 'hidden';

    const cleanup = () => {
        overlay.remove();
        dialog.remove();
        document.body.style.overflow = '';
    };

    dialog.querySelector('#confirmOk').addEventListener('click', () => {
        cleanup();
        onConfirm?.();
    });

    dialog.querySelector('#confirmCancel').addEventListener('click', () => {
        cleanup();
        onCancel?.();
    });

    overlay.addEventListener('click', () => {
        cleanup();
        onCancel?.();
    });
};

window.confirmAction = confirmAction;

// ==========================================================================
// DELETE ACTIONS
// ==========================================================================

const initDeleteActions = () => {
    $$('.delete-btn, [data-action="delete"]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const itemName = btn.dataset.itemName || 'this item';

            confirmAction(
                `Are you sure you want to delete ${itemName}?`,
                () => {
                    // Perform delete
                    const url = btn.dataset.url || btn.href;
                    if (url) {
                        fetch(url, { method: 'DELETE' })
                            .then(response => {
                                if (response.ok) {
                                    showToast('Item deleted successfully', 'success');
                                    // Remove row if in table
                                    btn.closest('tr')?.remove();
                                } else {
                                    showToast('Failed to delete item', 'error');
                                }
                            })
                            .catch(() => {
                                showToast('An error occurred', 'error');
                            });
                    }
                }
            );
        });
    });
};

// ==========================================================================
// CHARTS (placeholder for Chart.js integration)
// ==========================================================================

const initCharts = () => {
    // This would integrate with Chart.js or similar library
    // Example initialization for when charts are needed

    const chartContainers = $$('.chart-container[data-chart]');

    chartContainers.forEach(container => {
        const chartType = container.dataset.chart;
        const chartData = container.dataset.chartData;

        // Initialize chart based on type
        console.log(`Initializing ${chartType} chart with data:`, chartData);
    });
};

// ==========================================================================
// DATE PICKER (placeholder for flatpickr integration)
// ==========================================================================

const initDatePickers = () => {
    $$('[data-datepicker]').forEach(input => {
        // Would integrate with flatpickr or similar
        input.type = 'date';
    });

    $$('[data-timepicker]').forEach(input => {
        input.type = 'time';
    });

    $$('[data-datetimepicker]').forEach(input => {
        input.type = 'datetime-local';
    });
};

// ==========================================================================
// RICH TEXT EDITOR (placeholder for TinyMCE/Quill integration)
// ==========================================================================

const initRichTextEditors = () => {
    $$('[data-editor]').forEach(textarea => {
        // Would integrate with TinyMCE, Quill, or similar
        textarea.classList.add('rich-editor');
    });
};

// ==========================================================================
// UTILITY: Debounce
// ==========================================================================

const debounce = (func, wait = 300) => {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
};

// ==========================================================================
// INITIALIZE ALL
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
    initSidebar();
    initDropdowns();
    initDataTables();
    initSearch();
    initFilters();
    initModals();
    initForms();
    initFileUpload();
    initNotifications();
    initDeleteActions();
    initCharts();
    initDatePickers();
    initRichTextEditors();
});

// ==========================================================================
// EXPORT FOR MODULE USE
// ==========================================================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        showToast,
        confirmAction,
        openModal,
        closeAllModals
    };
}
