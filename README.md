# VoltRoof Solar PV Estimator & ERP/CRM Platform

**Clean Energy. Brighter Tomorrow.**  
VoltRoof is a comprehensive solar photovoltaic engineering estimator, dynamic proposal engine, 3D rooftop visualizer, and enterprise ERP/CRM suite.

---

## 🌟 Core Features

- **Interactive 3D Solar Visualizer**: Three.js-powered 3D rooftop layout simulator with tilt, azimuth, shade, and panel density controls.
- **Solar Sizing & Electrical Engineering**:
  - Sanctioned-load priority sizing algorithms.
  - Multi-building & multi-site layout support (up to 10 buildings across multiple sites).
  - Bill of Materials (BOM) generation with module stringing, inverter selection, DC/AC cabling, and switchgear specs.
- **Enterprise ERP / CRM Administrative Portal**:
  - **Dynamic Pricing Engine**: Multi-tier pricing catalog for modules, inverters, structures, cables, and balance of system (BOS).
  - **Support Ticketing System**: End-to-end customer support ticket dispatching, priority tracking, and resolution workflow.
  - **Visitor Tracking & Analytics**: Detailed visitor session tracking, IP logs, geolocation simulation, and report counters.
  - **3-Tier Administrator Hierarchy**: Governance structure for Super Admin, Senior Admin, and Support Admins with role promotion workflows.
  - **Solar Policy Hub & Policy Desk**: Dynamic solar subsidy and regulatory policy repository.
  - **Media Library & Content Studio**: Upload, manage, and showcase project slides (up to 50 slides).
  - **Email Notification Dispatcher**: Diagnostic email ping and automated customer proposal dispatching.
- **Engineering PDF Generator**:
  - High-precision multi-page PDF generation (up to 11 pages) with generation graphs, financial models, ROI & payback calculations, and detailed BOM.
- **PWA & Offline Capability**:
  - Service worker shell caching (`sw.js`) and standalone offline HTML edition.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+ (Standard library only; no external dependencies required!)

### Launching the Application
```powershell
python solar_pv_estimator.py
```
Open your browser and navigate to:
- **Web App**: [http://localhost:8000](http://localhost:8000)
- **Admin Portal**: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## 🔐 Default Administrator Credentials

| Role | Username | Password | Email |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `Adarsha KM` | `Adarsh@123321` | `adarshakm@jnnce.ac.in` |
| **Super Admin (Alt)** | `admin` | `admin123` | `admin@voltroof.in` |
| **Operations Admin** | `Prathapa R` | `Prathap@123` | `prathaparprathapar6@gmail.com` |
| **Operations Admin** | `D Nihar` | `Nihar@123` | `nihar333k@gmail.com` |

---

## 🧪 Automated Verification & Health Checks

1. **Master API & PDF Engine Health Check**:
   ```powershell
   python test_master_suite.py
   ```
   *Verifies all 16 GET endpoints, 13 POST routes, database persistence, and PDF report generator.*

2. **Full End-to-End Live Browser Test (Chrome CDP)**:
   ```powershell
   python run_live_browser_test.py
   ```
   *Launches headless Chrome, tests Admin button hit-testing, navigation, login, and portal transition with zero errors.*

---

## 📂 Key Files & Directories

- `solar_pv_estimator.py` — Standalone HTTP server, route dispatcher, and PDF reporting engine.
- `backend_ext.py` — ERP/CRM business logic, dynamic pricing catalog, tickets, and database storage.
- `VoltRoof_Combined.html` — Full single-page application (3D visualizer, customer calculator, and admin portal).
- `index.html` — Primary entry point.
- `voltroof_solar_pv_estimator_standalone.html` — Standalone offline single-file edition.
- `sw.js` — Service worker for offline asset caching.
- `user_manual.pdf` — Embedded user and technical manual.
- `uploads/` — Uploaded showcase images, project photos, and technical documentation.

---

## 🔄 End-to-End Project Flow

This project is designed as a full-stack web estimator with a lightweight Python backend and a front-end UI served from the same process.

### 1) Application Startup

Run the project from the project folder:

```powershell
cd solar_estimator
python solar_pv_estimator.py
```

The app starts an embedded HTTP server on `127.0.0.1:5050` by default.

- Main customer UI: `http://localhost:5050/`
- Admin portal: `http://localhost:5050/admin`
- Optional custom port:

```powershell
python solar_pv_estimator.py 8000
```

### 2) Front-End Experience

The user lands on the VoltRoof interface, where they can:

- enter rooftop dimensions, building data, and site details,
- select panel type and design mode,
- calculate solar PV capacity and expected energy output,
- review BOM, pricing, and system specs,
- generate PDF estimate documents,
- submit feedback or support requests.

The frontend is served from the embedded HTML assets and JavaScript generated within the project.

### 3) Backend Calculation Engine

The actual sizing logic is executed in `solar_pv_estimator.py` and includes:

- rooftop area and usable area calculation,
- KERC / ESCOM LT capacity checks,
- sanctioned-load validation,
- panel and inverter selection,
- DC/AC calculations,
- BOM generation,
- cost estimation and PDF reporting.

The backend stores and retrieves data using JSON-backed databases for:

- admin accounts,
- pricing,
- tickets,
- visitors,
- feedback,
- audit logs.

### 4) Admin & ERP Workflow

The application includes a multi-tier admin flow:

- Super Admin
- Senior Admin
- Support Admin / Operations Admin

Admins can:

- login to the portal,
- approve pending access requests,
- manage pricing,
- review ticketing and support operations,
- access visitor analytics,
- review policy and portal content,
- manage the admin audit trail.

### 5) Data Persistence

The project stores operational data in local JSON database files, for example:

- `admins_db.json`
- `admin_audit_db.json`
- `pricing_db.json`
- `feedback_db.json`
- `tickets_db.json`
- `visitors_db.json`

This makes the app portable and simple to run without external setup or database services.

### 6) PDF & Download Output

The system can generate professional multi-page PDF reports including:

- project overview,
- system sizing,
- site and building details,
- PV bill of materials,
- financial summary,
- approval / utility details,
- portfolio-level cost analysis.

### 7) End-to-End Operational Flow

A typical user journey is:

1. Open the web app.
2. Enter building and site details.
3. Choose panel specification and design mode.
4. Run the solar estimator.
5. Review capacity, pricing, and electrical assumptions.
6. Export/download the engineering report.
7. Admins review requests, calculate costs, and manage administrative tasks.

---

## 🧩 Project Architecture Summary

```
solar_estimator/
├── solar_pv_estimator.py        # Core server, app logic, calculation engine, PDF generation
├── backend_ext.py               # Supporting ERP / CRM logic and JSON data handling
├── index.html                   # Primary frontend entry
├── VoltRoof_Combined.html        # Combined customer + admin portal page
├── solar_gui.py                 # GUI entry wrapper
├── sw.js                        # Offline PWA service worker
├── README.md                    # Project documentation
├── uploads/                     # Uploaded project and media files
├── *.json                       # Local database and app state files
├── *.py                         # Utility scripts, checks, verification scripts, and patch tools
└── user_manual.pdf              # Embedded documentation
```

---

## 🛠️ Common Commands

Start the application:

```powershell
python solar_pv_estimator.py
```

Run a verification suite:

```powershell
python test_master_suite.py
```

Run the live browser validation:

```powershell
python run_live_browser_test.py
```

Check if the service is responding:

```powershell
curl http://localhost:5050
```

---

## 🔐 Default Admin Credentials

| Role | Username | Password |
| :--- | :--- | :--- |
| Super Admin | `Adarsha KM` | `Adarsh@123321` |
| Super Admin (Alt) | `admin` | `admin123` |
| Operations Admin | `Prathapa R` | `Prathap@123` |
| Operations Admin | `D Nihar` | `Nihar@123` |

Use the admin login screen after starting the app.

---

## ✅ Notes for Development and Usage

- The project is self-contained and does not require a separate external database.
- Most operations are JSON-based and work out of the box for demo or local deployment.
- The system is intended for local execution and internal business demos.
- For production hardening, you would typically move JSON storage to a proper database and add stronger security controls.

---

## 📌 Summary

VoltRoof Solar PV Estimator is a complete local web application that covers:

- solar design and estimation,
- rooftop sizing and compliance logic,
- admin portal workflows,
- pricing and support operations,
- customer reporting and PDF export.

It is best used as a standalone engineering and business demo, with the backend and UI running in one Python HTTP server process.
