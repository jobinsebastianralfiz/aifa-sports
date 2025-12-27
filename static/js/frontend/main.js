/**
 * AIFA Football Academy - Main JavaScript
 * Version: 1.0
 */

// ==========================================================================
// UTILITY FUNCTIONS
// ==========================================================================

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

// Debounce function
const debounce = (func, wait = 100) => {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
};

// Throttle function
const throttle = (func, limit = 100) => {
    let inThrottle;
    return (...args) => {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
};

// ==========================================================================
// PRELOADER
// ==========================================================================

const initPreloader = () => {
    const preloader = $('.preloader');
    if (!preloader) return;

    // Prevent scrolling during preloader
    document.body.style.overflow = 'hidden';

    window.addEventListener('load', () => {
        // Wait for penalty shootout animation to complete
        // Timeline: keeper ready (0.5s) + dive (1s) + ball shoot (1.2s) + goal text (2.3s) + logo (2.6s) + line (3.8s)
        setTimeout(() => {
            preloader.classList.add('loaded');
            // Re-enable scrolling after preloader slides out
            setTimeout(() => {
                document.body.style.overflow = 'visible';
                preloader.style.display = 'none';
            }, 800);
        }, 4000);
    });
};

// ==========================================================================
// NAVBAR
// ==========================================================================

const initNavbar = () => {
    const navbar = $('.navbar');
    const menuToggle = $('.menu-toggle');
    const navMenu = $('.navbar-menu');

    if (!navbar) return;

    // Scroll effect
    window.addEventListener('scroll', throttle(() => {
        if (window.scrollY > 100) {
            navbar.classList.add('navbar-scrolled', 'scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled', 'scrolled');
        }
    }, 50));

    // Mobile menu toggle
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            menuToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
            document.body.classList.toggle('menu-open');
        });

        // Close menu on link click
        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                menuToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.classList.remove('menu-open');
            });
        });
    }

    // Active link on scroll
    const sections = $$('section[id]');
    const navLinks = $$('.navbar-link, .nav-menu a');

    window.addEventListener('scroll', throttle(() => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 150;
            if (window.scrollY >= sectionTop) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    }, 100));
};

// ==========================================================================
// SMOOTH SCROLL
// ==========================================================================

const initSmoothScroll = () => {
    $$('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = $(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
};

// ==========================================================================
// SCROLL ANIMATIONS
// ==========================================================================

const initScrollAnimations = () => {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');

                // Animate counters
                if (entry.target.hasAttribute('data-count')) {
                    animateCounter(entry.target);
                }

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all animated elements
    $$('.animate-on-scroll, .animate-left, .animate-right, .animate-scale, .animate-fade, .stagger-children, [data-count]').forEach(el => {
        observer.observe(el);
    });
};

// ==========================================================================
// COUNTER ANIMATION
// ==========================================================================

const animateCounter = (element) => {
    const target = parseInt(element.getAttribute('data-count'));
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;

    const updateCounter = () => {
        current += step;
        if (current < target) {
            element.textContent = Math.ceil(current);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target + '+';
        }
    };

    updateCounter();
};

// ==========================================================================
// PARTICLES
// ==========================================================================

const initParticles = () => {
    const container = $('#particles');
    if (!container) return;

    const particleCount = 50;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            left: ${Math.random() * 100}%;
            animation-delay: ${Math.random() * 15}s;
            animation-duration: ${Math.random() * 10 + 10}s;
        `;
        container.appendChild(particle);
    }
};

// ==========================================================================
// TESTIMONIALS CAROUSEL
// ==========================================================================

const initTestimonials = () => {
    const testimonials = window.testimonialData || [
        {
            text: "My son's transformation has been incredible. Not just as a player, but as a person. The coaches here genuinely care about each child's development. Best decision we ever made!",
            name: "Rahul Sharma",
            role: "Parent of Arjun, Age 12",
            avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&q=80"
        },
        {
            text: "The professional approach and individual attention each player receives is outstanding. My daughter has improved tremendously in just 6 months. Highly recommend!",
            name: "Priya Menon",
            role: "Parent of Anika, Age 10",
            avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200&q=80"
        },
        {
            text: "World-class facilities and coaching. The academy has produced many district and state level players. Proud to be part of the AIFA family!",
            name: "Anil Kumar",
            role: "Parent of Rohan, Age 15",
            avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200&q=80"
        }
    ];

    let currentIndex = 0;
    const textEl = $('#testimonialText');
    const nameEl = $('#testimonialName');
    const roleEl = $('#testimonialRole');
    const avatarEl = $('#testimonialAvatar');
    const prevBtn = $('#prevBtn');
    const nextBtn = $('#nextBtn');

    if (!textEl) return;

    const updateTestimonial = () => {
        const t = testimonials[currentIndex];
        textEl.textContent = t.text;
        nameEl.textContent = t.name;
        roleEl.textContent = t.role;
        if (avatarEl) avatarEl.src = t.avatar;
    };

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            currentIndex = (currentIndex - 1 + testimonials.length) % testimonials.length;
            updateTestimonial();
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            currentIndex = (currentIndex + 1) % testimonials.length;
            updateTestimonial();
        });
    }

    // Auto rotate
    setInterval(() => {
        currentIndex = (currentIndex + 1) % testimonials.length;
        updateTestimonial();
    }, 6000);
};

// ==========================================================================
// SCROLL PROGRESS BAR
// ==========================================================================

const initScrollProgress = () => {
    const progressBar = $('.scroll-progress');
    if (!progressBar) return;

    window.addEventListener('scroll', throttle(() => {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = (scrollTop / docHeight) * 100;
        progressBar.style.width = `${progress}%`;
    }, 50));
};

// ==========================================================================
// RIPPLE EFFECT
// ==========================================================================

const initRippleEffect = () => {
    $$('.ripple-effect, .btn').forEach(element => {
        element.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            ripple.className = 'ripple';

            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);

            ripple.style.cssText = `
                width: ${size}px;
                height: ${size}px;
                left: ${e.clientX - rect.left - size / 2}px;
                top: ${e.clientY - rect.top - size / 2}px;
            `;

            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });
};

// ==========================================================================
// TABS
// ==========================================================================

const initTabs = () => {
    $$('.tabs').forEach(tabContainer => {
        const tabs = tabContainer.querySelectorAll('.tab');
        const contentContainer = tabContainer.nextElementSibling;
        const panes = contentContainer?.querySelectorAll('.tab-pane');

        tabs.forEach((tab, index) => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');

                if (panes) {
                    panes.forEach(p => p.classList.remove('active'));
                    panes[index]?.classList.add('active');
                }
            });
        });
    });
};

// ==========================================================================
// ACCORDION
// ==========================================================================

const initAccordion = () => {
    $$('.accordion-header').forEach(header => {
        header.addEventListener('click', () => {
            const item = header.parentElement;
            const isActive = item.classList.contains('active');

            // Close all items
            item.parentElement.querySelectorAll('.accordion-item').forEach(i => {
                i.classList.remove('active');
            });

            // Toggle current
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });
};

// ==========================================================================
// DROPDOWN
// ==========================================================================

const initDropdowns = () => {
    $$('.dropdown').forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');

        toggle?.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdown.classList.toggle('active');
        });
    });

    // Close on outside click
    document.addEventListener('click', () => {
        $$('.dropdown.active').forEach(d => d.classList.remove('active'));
    });
};

// ==========================================================================
// MODAL
// ==========================================================================

const initModals = () => {
    // Open modal
    $$('[data-modal-target]').forEach(trigger => {
        trigger.addEventListener('click', () => {
            const modal = $(trigger.dataset.modalTarget);
            const overlay = $('.modal-overlay');

            if (modal) {
                modal.classList.add('active');
                overlay?.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        });
    });

    // Close modal
    $$('.modal-close, .modal-overlay').forEach(closer => {
        closer.addEventListener('click', () => {
            $$('.modal.active').forEach(m => m.classList.remove('active'));
            $('.modal-overlay')?.classList.remove('active');
            document.body.style.overflow = '';
        });
    });

    // Close on escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            $$('.modal.active').forEach(m => m.classList.remove('active'));
            $('.modal-overlay')?.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
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
    toast.innerHTML = `
        <div class="toast-icon">${getToastIcon(type)}</div>
        <div class="toast-message">${message}</div>
        <button class="toast-close">&times;</button>
    `;

    container.appendChild(toast);

    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);

    // Auto dismiss
    const dismissTimer = setTimeout(() => dismissToast(toast), duration);

    // Manual dismiss
    toast.querySelector('.toast-close')?.addEventListener('click', () => {
        clearTimeout(dismissTimer);
        dismissToast(toast);
    });
};

const dismissToast = (toast) => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
};

const getToastIcon = (type) => {
    const icons = {
        success: '✓',
        error: '✕',
        warning: '⚠',
        info: 'ℹ'
    };
    return icons[type] || icons.info;
};

// Export for global use
window.showToast = showToast;

// ==========================================================================
// FORM VALIDATION
// ==========================================================================

const initFormValidation = () => {
    $$('form[data-validate]').forEach(form => {
        form.addEventListener('submit', (e) => {
            let isValid = true;

            form.querySelectorAll('[required]').forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    showInputError(input, 'This field is required');
                } else {
                    clearInputError(input);
                }
            });

            form.querySelectorAll('[type="email"]').forEach(input => {
                if (input.value && !isValidEmail(input.value)) {
                    isValid = false;
                    showInputError(input, 'Please enter a valid email');
                }
            });

            if (!isValid) {
                e.preventDefault();
            }
        });
    });
};

const showInputError = (input, message) => {
    input.classList.add('form-input-error');
    let error = input.parentElement.querySelector('.form-error');
    if (!error) {
        error = document.createElement('span');
        error.className = 'form-error';
        input.parentElement.appendChild(error);
    }
    error.textContent = message;
};

const clearInputError = (input) => {
    input.classList.remove('form-input-error');
    input.parentElement.querySelector('.form-error')?.remove();
};

const isValidEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

// ==========================================================================
// IMAGE LAZY LOADING
// ==========================================================================

const initLazyLoading = () => {
    const images = $$('img[data-src]');

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        }, { rootMargin: '100px' });

        images.forEach(img => observer.observe(img));
    } else {
        // Fallback
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
};

// ==========================================================================
// BACK TO TOP
// ==========================================================================

const initBackToTop = () => {
    const btn = $('.back-to-top');
    if (!btn) return;

    window.addEventListener('scroll', throttle(() => {
        if (window.scrollY > 500) {
            btn.classList.add('visible');
        } else {
            btn.classList.remove('visible');
        }
    }, 100));

    btn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
};

// ==========================================================================
// INITIALIZE ALL
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
    initPreloader();
    initNavbar();
    initSmoothScroll();
    initScrollAnimations();
    initParticles();
    initTestimonials();
    initScrollProgress();
    initRippleEffect();
    initTabs();
    initAccordion();
    initDropdowns();
    initModals();
    initFormValidation();
    initLazyLoading();
    initBackToTop();
});

// ==========================================================================
// EXPORT FOR MODULE USE
// ==========================================================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        showToast,
        animateCounter,
        debounce,
        throttle
    };
}
