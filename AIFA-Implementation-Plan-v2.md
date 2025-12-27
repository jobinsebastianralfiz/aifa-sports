# AIFA Football Academy - Implementation Plan v2

## Project Overview

| Field | Details |
|-------|---------|
| **Project Name** | AIFA Football Academy Website |
| **Tech Stack** | HTML5, CSS3, JavaScript, Django, Flutter |
| **Scope** | Landing Page + Backend + Mobile App + Admin Dashboard |
| **Excluded** | Payment Gateway, Fee Collection, Financial Reports |

---

## Project Structure

```
aifa_sports/
├── frontend/
│   ├── index.html
│   ├── css/
│   │   ├── main.css
│   │   ├── animations.css
│   │   └── responsive.css
│   ├── js/
│   │   ├── main.js
│   │   ├── animations.js
│   │   ├── slider.js
│   │   └── particles.js
│   └── assets/
│       ├── images/
│       ├── videos/
│       ├── icons/
│       └── fonts/
│
├── backend/
│   ├── aifa_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── core/
│   │   ├── students/
│   │   ├── coaches/
│   │   ├── programs/
│   │   ├── admissions/
│   │   ├── gallery/
│   │   ├── blog/
│   │   └── notifications/
│   ├── templates/
│   ├── static/
│   └── media/
│
├── mobile_app/
│   └── aifa_app/
│       ├── lib/
│       │   ├── screens/
│       │   ├── widgets/
│       │   ├── models/
│       │   ├── services/
│       │   └── providers/
│       └── assets/
│
└── docs/
```

---

## Phase 1: Landing Page

### 1.1 Sections to Build

| # | Section | Description |
|---|---------|-------------|
| 1 | Preloader | Loading counter (0-100%), floating logo, split reveal |
| 2 | Navigation | Sticky header, transparent to solid on scroll |
| 3 | Hero | Video/image slider with Ken Burns effect |
| 4 | Marquee | Infinite scrolling text banner |
| 5 | About | Academy introduction with stats |
| 6 | Programs | 4 program cards with hover effects |
| 7 | Stats | Animated counters (students, coaches, years, etc.) |
| 8 | Gallery | Infinite scroll image gallery |
| 9 | Coaches | 3 coach profiles with social links |
| 10 | Testimonials | Auto-rotating review carousel |
| 11 | CTA | Call-to-action section |
| 12 | Footer | Contact info, links, social media |
| 13 | WhatsApp | Floating button with pulse animation |

### 1.2 Animations

```
Cursor Effects:
├── Custom golden ring cursor
├── Cursor expand on hover
└── 15-particle mouse trail

Preloader:
├── 0-100% counter animation
├── Floating logo
└── Split screen reveal

Hero Section:
├── Ken Burns zoom/pan effect
├── Pulsing grid overlay
├── 50-60 rising particles
├── 3 glowing orbs with parallax
├── Split text reveal
├── Glitch text effect
└── Gradient flowing text

Interactive Effects:
├── Magnetic buttons (follow mouse)
├── 3D tilt on cards
├── Ripple on click
└── Multi-layer parallax

Scroll Animations:
├── Fade up from bottom
├── Slide from left/right
├── Scale up (0.85 to 1)
├── Staggered children
└── Scroll progress bar

Other:
├── Number counter animation
├── Infinite marquee
├── Floating badges
├── Gallery auto-scroll
└── Testimonial carousel
```

### 1.3 Design Specifications

**Color Scheme:**
```css
:root {
  --primary: #d4a418;
  --primary-dark: #b8910f;
  --primary-light: #f0c929;
  --gold: #ffd700;
  --dark: #0a0a0a;
  --darker: #030303;
  --glass: rgba(255, 255, 255, 0.05);
  --glass-border: rgba(255, 255, 255, 0.1);
}
```

**Typography:**
```
Headings: 'Bebas Neue' (bold, uppercase)
Body: 'Outfit' (300-800 weights)
Accent: 'Playfair Display' (italic)
```

### 1.4 Deliverables

- [ ] index.html - Complete landing page structure
- [ ] main.css - Core styles and layout
- [ ] animations.css - All animation keyframes
- [ ] responsive.css - Mobile/tablet breakpoints
- [ ] main.js - Core functionality
- [ ] animations.js - Animation controllers
- [ ] slider.js - Hero slider logic
- [ ] particles.js - Particle system

---

## Phase 2: Django Backend

### 2.1 Apps Overview

| App | Purpose |
|-----|---------|
| core | Site settings, hero slides, testimonials |
| students | Student profiles, batches, attendance |
| coaches | Coach profiles and assignments |
| programs | Training programs and schedules |
| admissions | Application forms and trial management |
| gallery | Photo albums and videos |
| blog | News and articles |
| notifications | Announcements and alerts |

### 2.2 Models

**Core App:**
```python
SiteSettings
├── site_name, logo, logo_white
├── email, phone, whatsapp
├── address
└── social_links (facebook, instagram, youtube, twitter)

HeroSlide
├── title, subtitle
├── media_type (video/image)
├── video, image
├── cta_text, cta_link
├── order, is_active

Testimonial
├── name, role, photo
├── content, rating
├── is_featured, order

ContactMessage
├── name, email, phone
├── subject, message
├── created_at, is_read
```

**Students App:**
```python
Student
├── Personal: first_name, last_name, dob, gender, photo
├── Contact: email, phone, address
├── Guardian: name, phone, email, relation
├── Academy: student_id, program, batch, joined_date, status
├── Medical: blood_group, conditions, emergency_contact

Batch
├── name, program, coach
├── schedule, max_students
├── start_time, end_time, days

Attendance
├── student, batch, date
├── status (present/absent/late)
├── notes
```

**Coaches App:**
```python
Coach
├── user (OneToOne)
├── photo, bio
├── qualification, experience_years
├── specialization, achievements
├── phone, social_links
├── order, is_active
```

**Programs App:**
```python
Program
├── name, slug, age_group
├── description, short_description
├── image, icon
├── duration, sessions_per_week
├── features (JSON)
├── order, is_active
```

**Admissions App:**
```python
Admission
├── Applicant: first_name, last_name, dob, gender
├── Contact: email, phone, address
├── Guardian: name, phone, email
├── Program: program, preferred_batch
├── Status: application_date, status, trial_date, trial_status
├── Conversion: converted_to_student, student (FK)
```

**Gallery App:**
```python
Album
├── title, slug, description
├── cover_image, date
├── is_featured, is_active

Photo
├── album (FK), image
├── caption, order

Video
├── title, youtube_url
├── thumbnail, description
├── is_featured
```

**Blog App:**
```python
Category
├── name, slug

Post
├── title, slug, category
├── content, excerpt
├── featured_image
├── author, published_date
├── is_published, views
```

**Notifications App:**
```python
Notification
├── title, message
├── notification_type
├── recipients (all/program/batch/individual)
├── target_program, target_batch, target_students
├── send_email, send_push
├── scheduled_time, sent_at, status
```

### 2.3 API Endpoints

**Public APIs:**
```
GET  /api/site-settings/
GET  /api/hero-slides/
GET  /api/programs/
GET  /api/programs/<slug>/
GET  /api/coaches/
GET  /api/testimonials/
GET  /api/gallery/albums/
GET  /api/gallery/albums/<slug>/
GET  /api/gallery/videos/
GET  /api/blog/posts/
GET  /api/blog/posts/<slug>/
GET  /api/stats/
POST /api/contact/
POST /api/admissions/apply/
```

**Authentication:**
```
POST /api/auth/login/
POST /api/auth/logout/
POST /api/auth/register/
POST /api/auth/forgot-password/
POST /api/auth/reset-password/
GET  /api/auth/me/
```

**Student Portal:**
```
GET  /api/student/profile/
PUT  /api/student/profile/
GET  /api/student/attendance/
GET  /api/student/attendance/monthly/<year>/<month>/
GET  /api/student/schedule/
GET  /api/student/notifications/
PUT  /api/student/notifications/<id>/read/
```

**Admin APIs:**
```
GET  /api/admin/dashboard/
CRUD /api/admin/students/
CRUD /api/admin/coaches/
CRUD /api/admin/programs/
CRUD /api/admin/batches/
CRUD /api/admin/admissions/
CRUD /api/admin/gallery/albums/
CRUD /api/admin/gallery/photos/
CRUD /api/admin/gallery/videos/
CRUD /api/admin/blog/posts/
CRUD /api/admin/notifications/
POST /api/admin/attendance/mark/
GET  /api/admin/attendance/report/
POST /api/admin/admissions/<id>/convert/
```

### 2.4 Deliverables

- [ ] Django project setup with all apps
- [ ] All models with migrations
- [ ] Django REST Framework serializers
- [ ] API views and viewsets
- [ ] Authentication (JWT)
- [ ] Admin panel customization
- [ ] Media file handling
- [ ] Email integration (SendGrid/SMTP)
- [ ] Unit tests

---

## Phase 3: Flutter Mobile App

### 3.1 Screens

```
App Structure:
├── Splash Screen
├── Onboarding (3 slides)
├── Auth
│   ├── Login (email/phone)
│   └── Forgot Password
├── Home Dashboard
│   ├── Welcome banner
│   ├── Quick stats
│   ├── Today's schedule
│   └── Recent notifications
├── Profile
│   ├── Student info
│   ├── Guardian info
│   └── Edit profile
├── Attendance
│   ├── Monthly calendar view
│   ├── Attendance percentage
│   └── Daily breakdown
├── Schedule
│   ├── Weekly timetable
│   ├── Upcoming sessions
│   └── Holiday calendar
├── Notifications
│   ├── All notifications
│   └── Mark as read
├── Gallery
│   ├── Photo albums
│   └── Videos
└── Settings
    ├── Language
    ├── Notification preferences
    ├── About app
    └── Logout
```

### 3.2 Features

| Feature | Description |
|---------|-------------|
| Authentication | Email/phone login with JWT tokens |
| Dashboard | Overview of student's academy life |
| Profile | View and edit student/guardian info |
| Attendance | Calendar view with color-coded days |
| Schedule | Weekly timetable and upcoming sessions |
| Notifications | Push notifications and in-app alerts |
| Gallery | Browse academy photos and videos |
| Offline Support | Cache essential data locally |

### 3.3 Technical Stack

```
State Management: Provider / Riverpod
HTTP Client: Dio
Local Storage: SharedPreferences / Hive
Push Notifications: Firebase Cloud Messaging
Image Caching: cached_network_image
Charts: fl_chart
Calendar: table_calendar
```

### 3.4 Deliverables

- [ ] Flutter project setup
- [ ] App theming (gold/dark theme)
- [ ] Authentication flow
- [ ] All screens implemented
- [ ] API integration
- [ ] Push notifications
- [ ] Offline caching
- [ ] App icons and splash screen

---

## Phase 4: Admin Dashboard

### 4.1 Sections

```
Dashboard:
├── Overview
│   ├── Total students count
│   ├── Active programs count
│   ├── Pending admissions count
│   ├── Attendance chart (weekly)
│   └── Recent activities
│
├── Students
│   ├── List with search/filter
│   ├── Add new student
│   ├── View/Edit student
│   ├── Batch assignment
│   └── Attendance history
│
├── Coaches
│   ├── List all coaches
│   ├── Add new coach
│   └── View/Edit profile
│
├── Programs & Batches
│   ├── Programs list
│   ├── Add/Edit program
│   ├── Batches list
│   └── Add/Edit batch
│
├── Admissions
│   ├── Pending applications
│   ├── Schedule trial
│   ├── Approve/Reject
│   └── Convert to student
│
├── Attendance
│   ├── Mark attendance (batch-wise)
│   ├── View reports
│   └── Export data
│
├── Gallery
│   ├── Manage albums
│   ├── Upload photos
│   └── Manage videos
│
├── Blog
│   ├── All posts
│   ├── Create/Edit post
│   └── Categories
│
├── Notifications
│   ├── Send notification
│   ├── Scheduled notifications
│   └── History
│
├── Website Content
│   ├── Hero slides
│   ├── Testimonials
│   ├── Site settings
│   └── Contact messages
│
└── Reports
    ├── Student reports
    ├── Attendance reports
    └── Export options
```

### 4.2 Deliverables

- [ ] Admin dashboard UI
- [ ] All CRUD operations
- [ ] Data tables with sorting/filtering
- [ ] Charts and analytics
- [ ] Bulk operations
- [ ] Export functionality (CSV/PDF)

---

## Phase 5: Deployment

### 5.1 Infrastructure

```yaml
Production Stack:
├── Web Server: Nginx
├── App Server: Gunicorn
├── Database: PostgreSQL
├── Cache: Redis
├── Task Queue: Celery
├── Storage: AWS S3 / Cloudinary
└── CDN: Cloudflare
```

### 5.2 Hosting Options

| Component | Recommended |
|-----------|-------------|
| Frontend | Vercel / Netlify |
| Backend | DigitalOcean / Railway |
| Database | Supabase / Neon |
| Storage | Cloudinary |
| Domain | Namecheap |

### 5.3 Deliverables

- [ ] Docker configuration
- [ ] CI/CD pipeline
- [ ] SSL certificate
- [ ] Domain setup
- [ ] Environment variables
- [ ] Backup strategy
- [ ] Monitoring setup

---

## Implementation Order

### Step 1: Project Setup
1. Create project directory structure
2. Initialize Git repository
3. Set up development environment

### Step 2: Landing Page
1. Create HTML structure
2. Implement CSS styles
3. Add all animations
4. Make responsive
5. Optimize performance

### Step 3: Django Backend
1. Create Django project
2. Create all apps
3. Define models and migrations
4. Build API endpoints
5. Set up authentication
6. Configure admin panel
7. Add email integration
8. Write tests

### Step 4: Mobile App
1. Create Flutter project
2. Set up app architecture
3. Implement authentication
4. Build all screens
5. Integrate APIs
6. Add push notifications
7. Test on devices

### Step 5: Admin Dashboard
1. Set up React/Vue project
2. Build dashboard layout
3. Implement all sections
4. Connect to backend APIs
5. Add charts and reports

### Step 6: Deployment
1. Set up servers
2. Configure domain and SSL
3. Deploy all components
4. Test thoroughly
5. Go live

---

## Third-Party Services

| Service | Purpose | Provider |
|---------|---------|----------|
| Email | Transactional emails | SendGrid / SMTP |
| Push Notifications | Mobile alerts | Firebase Cloud Messaging |
| Cloud Storage | Images/videos | Cloudinary / AWS S3 |
| Analytics | Usage tracking | Google Analytics |

---

*Document Version: 2.0*
*Scope: Excluding Payment Features*
