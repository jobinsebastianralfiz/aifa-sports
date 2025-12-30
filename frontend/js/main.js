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

        // Close menu on link click (except dropdown toggles)
        navMenu.querySelectorAll('a:not(.has-dropdown > a)').forEach(link => {
            link.addEventListener('click', () => {
                menuToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.classList.remove('menu-open');
            });
        });

        // Mobile dropdown toggle
        navMenu.querySelectorAll('.has-dropdown > a').forEach(link => {
            link.addEventListener('click', (e) => {
                if (window.innerWidth <= 991) {
                    e.preventDefault();
                    const parent = link.parentElement;
                    // Close other dropdowns
                    navMenu.querySelectorAll('.has-dropdown.active').forEach(item => {
                        if (item !== parent) item.classList.remove('active');
                    });
                    parent.classList.toggle('active');
                }
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
// HERO SLIDER
// ==========================================================================

const initHeroSlider = () => {
    const slides = $$('.hero-slide');
    const dots = $$('.hero-dot');
    const prevBtn = $('.hero-slider-prev');
    const nextBtn = $('.hero-slider-next');

    if (slides.length <= 1) return;

    let currentSlide = 0;
    let autoSlideInterval;
    const autoSlideDelay = 6000; // 6 seconds

    const goToSlide = (index) => {
        // Wrap around
        if (index >= slides.length) index = 0;
        if (index < 0) index = slides.length - 1;

        // Update slides
        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === index);
        });

        // Update dots
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });

        currentSlide = index;
    };

    const nextSlide = () => goToSlide(currentSlide + 1);
    const prevSlide = () => goToSlide(currentSlide - 1);

    // Auto-advance slides
    const startAutoSlide = () => {
        autoSlideInterval = setInterval(nextSlide, autoSlideDelay);
    };

    const stopAutoSlide = () => {
        clearInterval(autoSlideInterval);
    };

    // Event listeners
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            stopAutoSlide();
            nextSlide();
            startAutoSlide();
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            stopAutoSlide();
            prevSlide();
            startAutoSlide();
        });
    }

    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            stopAutoSlide();
            goToSlide(index);
            startAutoSlide();
        });
    });

    // Pause on hover
    const heroSection = $('.hero');
    if (heroSection) {
        heroSection.addEventListener('mouseenter', stopAutoSlide);
        heroSection.addEventListener('mouseleave', startAutoSlide);
    }

    // Start auto-slide
    startAutoSlide();
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
    initHeroSlider();
    initFootballCaptcha();
});

// ==========================================================================
// FOOTBALL CAPTCHA - Drag to Goal Verification
// ==========================================================================

const initFootballCaptcha = () => {
    const ball = document.getElementById('captcha-ball');
    const goal = document.getElementById('captcha-goal');
    const container = document.getElementById('captcha-container');
    const successDiv = document.getElementById('captcha-success');
    const hiddenInput = document.getElementById('human_verified');
    const captchaError = document.getElementById('captcha-error');
    const captchaField = document.querySelector('.captcha-field');
    const captchaInstruction = document.querySelector('.captcha-instruction');
    const form = ball?.closest('form');

    if (!ball || !goal || !container) return;

    let isDragging = false;
    let isVerified = false;

    // Generate a verification token
    const generateToken = () => {
        const timestamp = Date.now();
        const random = Math.random().toString(36).substring(2, 15);
        return btoa(`goal_${timestamp}_${random}`);
    };

    // Desktop Drag Events
    ball.addEventListener('dragstart', (e) => {
        if (isVerified) return;
        isDragging = true;
        ball.classList.add('dragging');
        e.dataTransfer.setData('text/plain', 'football');
        e.dataTransfer.effectAllowed = 'move';
    });

    ball.addEventListener('dragend', () => {
        isDragging = false;
        ball.classList.remove('dragging');
    });

    goal.addEventListener('dragover', (e) => {
        if (isVerified) return;
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        goal.classList.add('drag-over');
    });

    goal.addEventListener('dragleave', () => {
        goal.classList.remove('drag-over');
    });

    goal.addEventListener('drop', (e) => {
        e.preventDefault();
        if (isVerified) return;

        goal.classList.remove('drag-over');
        completeVerification();
    });

    // Touch Events for Mobile
    let touchStartX, touchStartY;
    let ballRect, goalRect;

    ball.addEventListener('touchstart', (e) => {
        if (isVerified) return;
        e.preventDefault();

        const touch = e.touches[0];
        touchStartX = touch.clientX;
        touchStartY = touch.clientY;

        ballRect = ball.getBoundingClientRect();
        goalRect = goal.getBoundingClientRect();

        ball.classList.add('dragging');
        ball.style.position = 'fixed';
        ball.style.zIndex = '1000';
        ball.style.left = `${ballRect.left}px`;
        ball.style.top = `${ballRect.top}px`;
    }, { passive: false });

    ball.addEventListener('touchmove', (e) => {
        if (isVerified || !ball.classList.contains('dragging')) return;
        e.preventDefault();

        const touch = e.touches[0];
        const deltaX = touch.clientX - touchStartX;
        const deltaY = touch.clientY - touchStartY;

        ball.style.left = `${ballRect.left + deltaX}px`;
        ball.style.top = `${ballRect.top + deltaY}px`;

        // Check if over goal
        const ballCenter = {
            x: ballRect.left + deltaX + ballRect.width / 2,
            y: ballRect.top + deltaY + ballRect.height / 2
        };

        goalRect = goal.getBoundingClientRect();

        if (ballCenter.x >= goalRect.left &&
            ballCenter.x <= goalRect.right &&
            ballCenter.y >= goalRect.top &&
            ballCenter.y <= goalRect.bottom) {
            goal.classList.add('drag-over');
        } else {
            goal.classList.remove('drag-over');
        }
    }, { passive: false });

    ball.addEventListener('touchend', (e) => {
        if (isVerified) return;

        ball.classList.remove('dragging');

        const ballCurrentRect = ball.getBoundingClientRect();
        goalRect = goal.getBoundingClientRect();

        const ballCenter = {
            x: ballCurrentRect.left + ballCurrentRect.width / 2,
            y: ballCurrentRect.top + ballCurrentRect.height / 2
        };

        // Check if dropped on goal
        if (ballCenter.x >= goalRect.left &&
            ballCenter.x <= goalRect.right &&
            ballCenter.y >= goalRect.top &&
            ballCenter.y <= goalRect.bottom) {
            goal.classList.remove('drag-over');
            completeVerification();
        } else {
            // Reset ball position
            ball.style.position = '';
            ball.style.zIndex = '';
            ball.style.left = '';
            ball.style.top = '';
            goal.classList.remove('drag-over');
        }
    });

    // Complete verification
    const completeVerification = () => {
        isVerified = true;

        // Set hidden input with verification token
        hiddenInput.value = generateToken();

        // Update UI
        container.classList.add('verified');
        captchaField.classList.add('hidden');
        captchaInstruction.classList.add('hidden');
        successDiv.classList.add('show');

        // Reset ball position
        ball.style.position = '';
        ball.style.zIndex = '';
        ball.style.left = '';
        ball.style.top = '';

        // Hide error if shown
        if (captchaError) {
            captchaError.style.display = 'none';
        }

        // Play success sound (optional)
        try {
            const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1rZWdrf4F3b25vaGlrbXF1d3l7fX5/gIGCg4WGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+');
            audio.volume = 0.3;
            audio.play().catch(() => {});
        } catch (e) {}
    };

    // Form validation
    if (form) {
        form.addEventListener('submit', (e) => {
            if (!isVerified) {
                e.preventDefault();
                if (captchaError) {
                    captchaError.style.display = 'block';
                }
                container.scrollIntoView({ behavior: 'smooth', block: 'center' });
                container.classList.add('shake');
                setTimeout(() => container.classList.remove('shake'), 500);
                return false;
            }
        });
    }
};

// ==========================================================================
// CHATBOT
// ==========================================================================

const initChatbot = () => {
    const widget = $('#chatbot-widget');
    const toggle = $('#chatbot-toggle');
    const closeBtn = $('#chatbot-close');
    const messagesContainer = $('#chatbot-messages');
    const input = $('#chatbot-input');
    const sendBtn = $('#chatbot-send');
    const quickReplies = $$('.quick-reply-btn');
    const badge = $('.chatbot-badge');

    if (!widget || !toggle) return;

    const API_URL = '/api/chatbot/';

    // Add message to chat
    const addMessage = (text, isBot = true) => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message ${isBot ? 'bot' : 'user'}`;
        // Convert newlines to <br> for proper display
        messageDiv.innerHTML = text.replace(/\n/g, '<br>');
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    };

    // Show typing indicator
    const showTyping = () => {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chatbot-message bot typing';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>';
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    };

    // Hide typing indicator
    const hideTyping = () => {
        const typing = $('#typing-indicator');
        if (typing) typing.remove();
    };

    // Fetch response from API
    const fetchBotResponse = async (query, topic = '') => {
        try {
            const params = new URLSearchParams();
            if (topic) params.append('topic', topic);
            if (query) params.append('query', query);

            const response = await fetch(`${API_URL}?${params.toString()}`);
            const data = await response.json();

            if (data.success) {
                return data.message;
            }
            return "Sorry, I couldn't process your request. Please try again.";
        } catch (error) {
            console.error('Chatbot API error:', error);
            return "Sorry, I'm having trouble connecting. Please try again later.";
        }
    };

    // Handle send message
    const sendMessage = async (message) => {
        if (!message.trim()) return;

        // Add user message
        addMessage(message, false);
        input.value = '';

        // Show typing indicator
        showTyping();

        // Fetch response from API
        const response = await fetchBotResponse(message);

        // Small delay for natural feel
        setTimeout(() => {
            hideTyping();
            addMessage(response, true);
        }, 300);
    };

    // Handle quick reply click
    const handleQuickReply = async (topic, displayText) => {
        // Add user message
        addMessage(displayText, false);

        // Show typing indicator
        showTyping();

        // Fetch response from API with topic
        const response = await fetchBotResponse('', topic);

        setTimeout(() => {
            hideTyping();
            addMessage(response, true);
        }, 300);
    };

    // Toggle chat window
    toggle.addEventListener('click', async () => {
        widget.classList.toggle('open');
        if (widget.classList.contains('open')) {
            badge.classList.add('hidden');
            // Add welcome message if first time
            if (messagesContainer.children.length === 0) {
                showTyping();
                const greeting = await fetchBotResponse('', 'greeting');
                setTimeout(() => {
                    hideTyping();
                    addMessage(greeting, true);
                }, 300);
            }
            input.focus();
        }
    });

    // Close button
    closeBtn.addEventListener('click', () => {
        widget.classList.remove('open');
    });

    // Send button
    sendBtn.addEventListener('click', () => {
        sendMessage(input.value);
    });

    // Enter key to send
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage(input.value);
        }
    });

    // Quick reply buttons
    quickReplies.forEach(btn => {
        btn.addEventListener('click', () => {
            const topic = btn.dataset.question;
            const displayText = btn.textContent;
            handleQuickReply(topic, displayText);
        });
    });

    // Close on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && widget.classList.contains('open')) {
            widget.classList.remove('open');
        }
    });

    // Mobile bottom nav chat toggle
    const mobileChatToggle = $('#mobile-chat-toggle');
    if (mobileChatToggle) {
        mobileChatToggle.addEventListener('click', async (e) => {
            e.preventDefault();
            widget.classList.add('open');
            badge.classList.add('hidden');
            // Hide the nav badge too
            const navBadge = mobileChatToggle.querySelector('.nav-badge');
            if (navBadge) navBadge.style.display = 'none';
            // Add welcome message if first time
            if (messagesContainer.children.length === 0) {
                showTyping();
                const greeting = await fetchBotResponse('', 'greeting');
                setTimeout(() => {
                    hideTyping();
                    addMessage(greeting, true);
                }, 300);
            }
            input.focus();
        });
    }
};

// Initialize chatbot on DOM ready
document.addEventListener('DOMContentLoaded', initChatbot);

// ==========================================================================
// GALLERY & LIGHTBOX
// ==========================================================================

const initGallery = () => {
    const filterBtns = $$('.filter-btn');
    const galleryItems = $$('.gallery-item');
    const lightbox = $('#gallery-lightbox');

    // Media tabs (Photos/Videos toggle)
    const mediaTabs = $$('.media-tab');
    const mediaContents = $$('.media-content');

    if (mediaTabs.length) {
        mediaTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const targetTab = tab.dataset.tab;

                // Update active tab
                mediaTabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');

                // Show corresponding content
                mediaContents.forEach(content => {
                    content.classList.remove('active');
                    if (content.id === `${targetTab}-content`) {
                        content.classList.add('active');
                    }
                });
            });
        });
    }

    // Video items and modal
    const videoItems = $$('.video-item');
    const videoModal = $('#video-modal');

    if (videoItems.length && videoModal) {
        const videoIframe = videoModal.querySelector('#video-iframe');
        const videoWrapper = videoModal.querySelector('.video-modal-wrapper');
        const closeBtn = videoModal.querySelector('.video-modal-close');

        const openVideoModal = (embedUrl, isVertical) => {
            videoIframe.src = embedUrl;
            if (isVertical) {
                videoWrapper.classList.add('vertical');
            } else {
                videoWrapper.classList.remove('vertical');
            }
            videoModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        };

        const closeVideoModal = () => {
            videoModal.classList.remove('active');
            videoIframe.src = '';
            document.body.style.overflow = '';
        };

        // Click on video items to open modal
        videoItems.forEach(item => {
            item.addEventListener('click', () => {
                const embedUrl = item.dataset.embed;
                const isVertical = item.classList.contains('vertical');
                if (embedUrl) {
                    openVideoModal(embedUrl, isVertical);
                }
            });
        });

        // Close button
        if (closeBtn) {
            closeBtn.addEventListener('click', closeVideoModal);
        }

        // Click outside to close
        videoModal.addEventListener('click', (e) => {
            if (e.target === videoModal) {
                closeVideoModal();
            }
        });

        // Escape key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && videoModal.classList.contains('active')) {
                closeVideoModal();
            }
        });
    }

    // Video filtering (within Videos tab)
    const videosContent = $('#videos-content');
    if (videosContent) {
        const videoFilterBtns = videosContent.querySelectorAll('.filter-btn');
        const videoItemsInTab = videosContent.querySelectorAll('.video-item');

        videoFilterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Update active button within this tab only
                videoFilterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const filter = btn.dataset.filter;

                // Filter video items
                videoItemsInTab.forEach(item => {
                    const category = item.dataset.category;

                    if (filter === 'all' || category === filter) {
                        item.style.display = '';
                        item.style.opacity = '0';
                        item.style.transform = 'scale(0.8)';
                        setTimeout(() => {
                            item.style.opacity = '1';
                            item.style.transform = 'scale(1)';
                        }, 50);
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        });
    }

    // Photo filtering (within Photos tab)
    const photosContent = $('#photos-content');
    if (photosContent) {
        const photoFilterBtns = photosContent.querySelectorAll('.filter-btn');
        const photoItems = photosContent.querySelectorAll('.gallery-item');

        photoFilterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Update active button within this tab only
                photoFilterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const filter = btn.dataset.filter;

                // Filter photo items
                photoItems.forEach(item => {
                    const category = item.dataset.category;

                    if (filter === 'all' || category === filter) {
                        item.style.display = '';
                        item.style.opacity = '0';
                        item.style.transform = 'scale(0.8)';
                        setTimeout(() => {
                            item.style.opacity = '1';
                            item.style.transform = 'scale(1)';
                        }, 50);
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        });
    }

    if (!galleryItems.length) return;

    // Lightbox functionality
    if (lightbox) {
        const lightboxImg = lightbox.querySelector('.lightbox-image');
        const lightboxCaption = lightbox.querySelector('.lightbox-caption');
        const closeBtn = lightbox.querySelector('.lightbox-close');
        const prevBtn = lightbox.querySelector('.lightbox-prev');
        const nextBtn = lightbox.querySelector('.lightbox-next');

        let currentIndex = 0;
        let visibleItems = [];

        const updateVisibleItems = () => {
            visibleItems = Array.from(galleryItems).filter(item => item.style.display !== 'none');
        };

        const openLightbox = (index) => {
            updateVisibleItems();
            currentIndex = index;
            const item = visibleItems[currentIndex];
            if (!item) return;

            const img = item.querySelector('img');
            const title = item.querySelector('.gallery-item-title');

            lightboxImg.src = img.src;
            lightboxImg.alt = img.alt;
            lightboxCaption.textContent = title ? title.textContent : img.alt;

            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
        };

        const closeLightbox = () => {
            lightbox.classList.remove('active');
            document.body.style.overflow = '';
        };

        const showPrev = () => {
            updateVisibleItems();
            currentIndex = (currentIndex - 1 + visibleItems.length) % visibleItems.length;
            openLightbox(currentIndex);
        };

        const showNext = () => {
            updateVisibleItems();
            currentIndex = (currentIndex + 1) % visibleItems.length;
            openLightbox(currentIndex);
        };

        // Click on gallery items to open lightbox
        galleryItems.forEach((item, index) => {
            item.style.cursor = 'pointer';
            item.addEventListener('click', () => {
                updateVisibleItems();
                const visibleIndex = visibleItems.indexOf(item);
                if (visibleIndex !== -1) {
                    openLightbox(visibleIndex);
                }
            });
        });

        // Close button
        if (closeBtn) {
            closeBtn.addEventListener('click', closeLightbox);
        }

        // Click outside to close
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) {
                closeLightbox();
            }
        });

        // Navigation buttons
        if (prevBtn) prevBtn.addEventListener('click', showPrev);
        if (nextBtn) nextBtn.addEventListener('click', showNext);

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (!lightbox.classList.contains('active')) return;

            if (e.key === 'Escape') closeLightbox();
            if (e.key === 'ArrowLeft') showPrev();
            if (e.key === 'ArrowRight') showNext();
        });
    }
};

// Initialize gallery on DOM ready
document.addEventListener('DOMContentLoaded', initGallery);

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
