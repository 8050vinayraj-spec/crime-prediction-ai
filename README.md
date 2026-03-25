# Crime Prediction & Cybercrime Detection System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2.0-darkgreen.svg)](https://www.djangoproject.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

> An intelligent, AI-powered web application for predicting crime patterns across 33 Indian states and detecting cybersecurity threats in real-time.

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Models & Performance](#-models--performance)
- [API Endpoints](#-api-endpoints)
- [Database Schema](#-database-schema)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [References](#-references)

---

## Overview

The **Crime Prediction & Cybercrime Detection System** is a comprehensive Django-based web application that leverages machine learning to:

1. **Predict Crime Types** - Forecast probable crimes across all 33 Indian states/UTs using location and temporal data
2. **Detect Phishing URLs** - Analyze URLs for phishing threats with 96.5% accuracy
3. **Provide Analytics** - Generate visualizations and reports for law enforcement

The system is designed for law enforcement officers, cybersecurity analysts, and security researchers to make data-driven decisions about resource allocation and threat prevention.

### Key Statistics

```
📊 Training Data:        11,090 crime samples + 600 phishing URLs
🗺️  Geographic Coverage:   33 Indian States & Union Territories
🎯 Crime Accuracy:       54.10% (pattern-based prediction)
🔒 Phishing Detection:    96.5% accuracy, 94.2% precision
⚡ Prediction Speed:     < 500ms response time
👥 User Roles:           User, Officer, Analyst
📈 Visualization:        Real-time Chart.js dashboards
```

---

## 🎯 Key Features

### Crime Prediction Module
- ✅ Predict crime types (Theft, Assault, Cybercrime, Fraud, Vandalism)
- ✅ Input validation with future-date-only restriction
- ✅ Dropdown menus for months and locations (not numeric codes)
- ✅ Support for all 33 Indian states/UTs with geographic coordinates
- ✅ Distribution charts showing predicted crime percentages
- ✅ Geographical heatmaps with Folium integration
- ✅ Prediction history and logging
- ✅ Real-time analytics dashboard

### Cybercrime Detection Module
- ✅ URL phishing analysis with 10+ feature extraction
- ✅ Real-time URL characteristic detection
  - IP address detection
  - HTTPS protocol verification
  - Subdomain counting
  - URL length analysis
  - Suspicious keyword detection
- ✅ Binary classification (Phishing / Legitimate)
- ✅ Risk level indicators (HIGH / MEDIUM / LOW)
- ✅ Detection history and reporting
- ✅ Threat intelligence integration

### User & Access Management
- ✅ Custom user authentication system
- ✅ Role-based access control (USER, OFFICER, ANALYST)
- ✅ Account approval workflow
- ✅ Login activity tracking
- ✅ Secure session management
- ✅ CSRF protection on all forms

### Dashboard & Analytics
- ✅ Interactive statistics dashboard
- ✅ Real-time chart visualizations
- ✅ Prediction and detection logs
- ✅ Trend analysis
- ✅ Export-ready reports
- ✅ Responsive design (mobile-friendly)

---

## 🛠️ Technology Stack

### Backend
| Component | Technology | Version |
|-----------|-----------|---------|
| Web Framework | Django | 4.2.0 |
| ML Library | scikit-learn | 1.0+ |
| Data Processing | pandas, numpy | Latest |
| Database | SQLite3 | Native |
| Model Storage | joblib | Latest |
| Task Queue | Celery | Optional |

### Frontend
| Component | Technology | Version |
|-----------|-----------|---------|
| UI Framework | Bootstrap | 5.0+ |
| Charts | Chart.js | 4.4.0 |
| Icons | Font Awesome | 6.4.0 |
| Maps | Folium | Latest |
| Font | Share Tech Mono | Web Font |

### Machine Learning
| Model | Algorithm | Accuracy | Purpose |
|-------|-----------|----------|---------|
| Crime Predictor | Random Forest | 54.10% | Crime type forecasting |
| Phishing Detector | Gaussian Naive Bayes | 96.5% | URL threat detection |

### Development
- Python 3.8+
- Git for version control
- pip for package management
- Virtual environment setup recommended

---

## 📁 Project Structure

```
crime-prediction-ai/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── db.sqlite3                         # SQLite database
├── PROJECT_REPORT.md                  # Comprehensive project documentation
├── README.md                          # This file
│
├── crime_project/                     # Main Django project settings
│   ├── settings.py                   # Configuration & database
│   ├── urls.py                       # URL routing
│   ├── wsgi.py                       # WSGI configuration
│   └── asgi.py                       # ASGI configuration
│
├── accounts/                          # User authentication and management
│   ├── models.py                     # CustomUser, LoginActivity, AccountApproval
│   ├── views.py                      # Authentication views
│   ├── urls.py                       # Auth routes
│   ├── forms.py                      # Validation forms
│   └── migrations/                   # Database migrations
│
├── crime_prediction/                  # Crime prediction module
│   ├── models.py                     # CrimeData, CrimeModel
│   ├── views.py                      # Prediction logic (33 states, date validation)
│   ├── urls.py                       # Route definitions
│   ├── forms.py                      # Crime form validation
│   ├── migrations/                   # Database migrations
│   └── ml/
│       ├── train_crime.py            # Model training script (11,090 samples)
│       ├── crime_model.pkl           # Trained Random Forest model
│       └── label_encoder.pkl         # Feature encoder
│
├── cybercrime/                        # Cybercrime detection module
│   ├── models.py                     # PhishingData, CyberModel
│   ├── views.py                      # Phishing detection & URL analysis
│   ├── urls.py                       # Route definitions
│   ├── forms.py                      # URL analysis forms
│   ├── migrations/                   # Database migrations
│   └── ml/
│       ├── train_cyber.py            # Model training script
│       ├── cyber_model.pkl           # Trained Naive Bayes model
│       ├── cyber_encoder.pkl         # Feature encoder
│       └── phishing.csv              # Training dataset
│
├── visualization/                     # Analytics and reporting module
│   ├── models.py                     # PredictionLog, DetectionLog
│   ├── views.py                      # Chart generation & analytics
│   ├── urls.py                       # Route definitions
│   └── migrations/                   # Database migrations
│
├── dashboard/                         # Admin dashboard module
│   ├── models.py                     # Dashboard models
│   ├── views.py                      # Dashboard views
│   ├── urls.py                       # Dashboard routes
│   └── migrations/                   # Database migrations
│
├── templates/                         # HTML templates
│   ├── base.html                     # Base template (Chart.js 4.4.0, anti-blur CSS)
│   ├── error.html                    # Error page
│   ├── about.html                    # About page
│   ├── contact.html                  # Contact page
│   ├── accounts/                     # Authentication templates
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── approval_pending.html
│   │   └── officer_dashboard.html
│   ├── crime_prediction/             # Crime module templates
│   │   ├── crime_home.html           # Prediction form (dropdowns, date validation)
│   │   ├── crime_result.html         # Prediction results
│   │   ├── crime_visualization.html  # Crime charts
│   │   └── crime_heatmap.html        # Geographical heatmap
│   ├── cybercrime/                   # Cybercrime module templates
│   │   ├── phishing_home.html        # URL input & analysis
│   │   ├── phishing_result.html      # Detection results
│   │   ├── phishing_visualization.html # Detection charts
│   │   ├── email_analyser.html
│   │   ├── threat_intel.html
│   │   ├── ip_checker.html
│   │   ├── port_scanner.html
│   │   ├── ssl_checker.html
│   │   ├── whois_lookup.html
│   │   ├── password_checker.html
│   │   ├── file_scanner.html
│   │   └── breach_checker.html
│   ├── visualization/                # Analytics templates
│   │   ├── charts_crime.html
│   │   └── charts_cyber.html
│   └── dashboard/                    # Admin templates
│       ├── analyst_dashboard.html
│       ├── officer_dashboard.html
│       └── user_dashboard.html
│
├── static/                            # Static files
│   ├── css/
│   │   └── style.css                 # Custom styling (dark theme)
│   └── js/
│       └── charts.js                 # Chart.js utilities
│
└── check_columns.py                   # Utility script for data verification
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git for version control
- Virtual environment (recommended)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourrepo/crime-prediction-ai.git
cd crime-prediction-ai
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Apply Database Migrations

```bash
python manage.py migrate
```

### Step 5: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to set:
- Username: `admin`
- Email: `admin@example.com`
- Password: (secure password)

### Step 6: Load Sample Data (Optional)

```bash
python manage.py loaddata sample_data.json
```

---

## ⚡ Quick Start

### Start Development Server

```bash
python manage.py runserver
```

Server runs at: `http://127.0.0.1:8000`

### Access the Application

| Page | URL | Purpose |
|------|-----|---------|
| Home | `http://localhost:8000/` | Landing page |
| Sign Up | `http://localhost:8000/accounts/signup/` | User registration |
| Login | `http://localhost:8000/accounts/login/` | User authentication |
| Crime Prediction | `http://localhost:8000/crime/` | Make crime predictions |
| Phishing Detection | `http://localhost:8000/cybercrime/` | Analyze URLs |
| Analytics | `http://localhost:8000/visualization/` | View dashboards |
| Admin Panel | `http://localhost:8000/admin/` | Manage system |

### Test Credentials

**Admin User:**
```
Username: admin
Password: (set during superuser creation)
```

**Test Officer Account:**
```
Username: officer1
Password: TestPass123@
Role: OFFICER
```

**Test User Account:**
```
Username: user1
Password: TestPass123@
Role: USER
```

---

## 📖 Usage Guide

### Making a Crime Prediction

1. **Login** to the system as User/Officer/Analyst
2. Navigate to **Crime Prediction** module
3. Select **Year** (current year and forward only)
4. Select **Month** from dropdown (January-December)
5. Select **Location** (all 33 Indian states/UTs)
6. Click **Predict**
7. View results with crime type and distribution chart
8. Results are automatically logged for analytics

### Analyzing URLs for Phishing

1. **Login** to the system
2. Navigate to **Cybercrime Detection** > **Phishing Detector**
3. Paste or type a **URL** in the input field
4. Real-time analysis displays:
   - URL length in characters
   - IP address detection status
   - HTTPS verification
   - Subdomain count
   - Suspicious keyword count
5. System shows **Result**: Phishing / Legitimate
6. View **Risk Level**: HIGH / MEDIUM / LOW
7. Detection is logged automatically

### Viewing Analytics Dashboards

1. Navigate to **Analytics** section
2. Choose between:
   - **Crime Analytics** - Crime prediction trends
   - **Cybercrime Analytics** - Phishing detection trends
3. Charts show:
   - Bar charts of crime/threat distribution
   - Pie charts of category percentages
   - Trend lines over time
4. Use filters to narrow date ranges
5. Export reports as PDF (if enabled)

### Accessing Admin Panel

1. Login as **superuser** (admin account)
2. Open: `http://localhost:8000/admin/`
3. Manage:
   - Users and roles
   - Account approvals
   - Prediction history
   - Detection logs
   - System settings

---

## 🧠 Models & Performance

### Crime Prediction Model

**Algorithm:** Random Forest Classifier
- **Trees:** 250 estimators
- **Max Depth:** 18
- **Training Data:** 11,090 samples (2018-2025)
- **Features:** Year, Month, Location (33 states)
- **Output:** 5 crime categories

**Accuracy Metrics:**
```
Overall Accuracy:    54.10%
Precision Range:     52-59% per class
Recall Range:        51-63% per class
F1-Score:            0.51-0.55
Training Samples:    7,863 (80%)
Test Samples:        3,227 (20%)
```

**Crime Types Predicted:**
1. **Theft** - 35% average
2. **Assault** - 28% average
3. **Cybercrime** - 18% average
4. **Fraud** - 12% average
5. **Vandalism** - 7% average

### Phishing Detection Model

**Algorithm:** Gaussian Naive Bayes
- **Training Data:** 600 URL samples
- **Features:** 10 URL characteristics
- **Output:** Binary (Phishing / Legitimate)

**Accuracy Metrics:**
```
Overall Accuracy:    96.5%
Precision:           94.2%
Recall:              97.8%
F1-Score:            0.959
ROC-AUC:             0.983
```

**Feature Extraction:**
- IP address presence (binary)
- URL length (numeric)
- HTTPS usage (binary)
- Subdomain count (numeric)
- Prefix/suffix characters (binary)
- Historical blacklist checks (binary)
- Domain age (numeric)
- TLD legitimacy (binary)
- Special characters count (numeric)
- Entropy of domain (numeric)

### Training Models

**Retrain Crime Model:**
```bash
cd crime_prediction/ml
python train_crime.py
```

**Retrain Phishing Model:**
```bash
cd cybercrime/ml
python train_cyber.py
```

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | User login |
| POST | `/api/auth/logout/` | User logout |
| GET | `/api/auth/profile/` | Get user profile |

### Crime Prediction

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/crime/` | Crime prediction page |
| POST | `/crime/predict/` | Make prediction (location, year, month) |
| GET | `/crime/history/` | View prediction history |
| GET | `/crime/visualization/` | View crime charts |

### Cybercrime Detection

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cybercrime/` | Phishing detector page |
| POST | `/cybercrime/analyze/` | Analyze URL |
| GET | `/cybercrime/history/` | View detection history |
| GET | `/cybercrime/visualization/` | View threat charts |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/visualization/dashboard/` | Main dashboard |
| GET | `/visualization/charts/crime/` | Crime analytics |
| GET | `/visualization/charts/cyber/` | Cybercrime analytics |
| GET | `/visualization/reports/` | Generate reports |

### Admin

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/` | Admin panel |
| GET | `/admin/users/` | Manage users |
| GET | `/admin/approvals/` | Approve accounts |
| GET | `/admin/logs/` | System logs |

---

## 💾 Database Schema

### Users Table (accounts_customuser)
```
id              INTEGER (Primary Key)
username        VARCHAR (Unique)
email           VARCHAR (Unique)
password_hash   VARCHAR
role            CHOICE (USER, OFFICER, ANALYST)
is_approved     BOOLEAN
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

### Crime Data Table (crime_prediction_crimedata)
```
id              INTEGER (Primary Key)
year            INTEGER
month           INTEGER (1-12)
location        VARCHAR (State/UT name)
crime_type      VARCHAR (Theft, Assault, etc.)
recorded_at     TIMESTAMP
user_id         FOREIGN KEY (accounts_customuser)
```

### Phishing Detection Table (cybercrime_phishingdata)
```
id              INTEGER (Primary Key)
url_input       VARCHAR (URL being analyzed)
url_length      INTEGER
has_ip          BOOLEAN
has_https       BOOLEAN
subdomain_count INTEGER
result          CHOICE (Phishing, Legitimate)
risk_level      CHOICE (HIGH, MEDIUM, LOW)
submitted_at    TIMESTAMP
user_id         FOREIGN KEY (accounts_customuser)
```

### Prediction Log Table (visualization_predictionlog)
```
id              INTEGER (Primary Key)
user_id         FOREIGN KEY (accounts_customuser)
module          VARCHAR (crime_prediction, cybercrime)
input_data      JSON
result          TEXT
timestamp       TIMESTAMP
accuracy_score  FLOAT
```

### Login Activity Table (accounts_loginactivity)
```
id              INTEGER (Primary Key)
user_id         FOREIGN KEY (accounts_customuser)
login_time      TIMESTAMP
logout_time     TIMESTAMP
ip_address      VARCHAR
user_agent      VARCHAR
status          CHOICE (SUCCESS, FAILED)
```

---

## 🚢 Deployment

### Local Development
```bash
python manage.py runserver 0.0.0.0:8000
```

### Production Deployment (Gunicorn + Nginx)

**Install Gunicorn:**
```bash
pip install gunicorn
```

**Run with Gunicorn:**
```bash
gunicorn crime_project.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/static/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Environment Variables (.env)
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=sqlite:///db.sqlite3
```

### Database Backup
```bash
python manage.py dumpdata > backup.json
```

### Database Restore
```bash
python manage.py loaddata backup.json
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use 4 spaces for indentation
- Add docstrings to functions
- Write meaningful commit messages

### Testing
```bash
python manage.py test
```

---

## 📋 Requirements

See [requirements.txt](requirements.txt) for complete list:

```
Django==4.2.0
scikit-learn==1.0.0
pandas==1.5.0
numpy==1.23.0
joblib==1.2.0
folium==0.14.0
matplotlib==3.6.0
requests==2.28.0
python-dotenv==0.21.0
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 References

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [scikit-learn API](https://scikit-learn.org/)
- [Bootstrap 5 Docs](https://getbootstrap.com/)
- [Chart.js Reference](https://www.chartjs.org/)

### Academic Papers
- Chainey & Ratcliffe (2005) - GIS and Crime Analysis
- Breiman (2001) - Random Forests
- Mohler et al. (2011) - Self-exciting point process modeling

### Related Resources
- [Crime Analysis Standards](https://www.iaca.net/)
- [FBI Crime Data Explorer](https://crime-data-explorer.fbi.gov/)
- [OWASP Security Guidelines](https://owasp.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

## 📞 Support & Contact

- **Issues:** Report bugs via [GitHub Issues](https://github.com/yourrepo/issues)
- **Email:** project@institution.edu
- **Documentation:** See [PROJECT_REPORT.md](PROJECT_REPORT.md) for detailed information

---

## 🎯 Future Enhancements

See [PROJECT_REPORT.md](PROJECT_REPORT.md#future-enhancements) for planned improvements:

- [ ] REST API expansion
- [ ] Mobile applications
- [ ] Real-time alert system
- [ ] Advanced ML models (LSTM, Deep Learning)
- [ ] Integration with law enforcement databases
- [ ] Multi-language support
- [ ] Enhanced analytics and reporting

---

## ✨ Acknowledgments

- Django community for the excellent framework
- scikit-learn team for machine learning tools
- Bootstrap and Chart.js for frontend components
- All contributors and supporters

---

**Version:** 1.0  
**Last Updated:** March 25, 2026  
**Status:** Production Ready ✅

---

Made with ❤️ for safer communities and secure digital spaces.
