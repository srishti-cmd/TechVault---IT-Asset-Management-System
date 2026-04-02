# 🛡️ TechVault - Enterprise IT Asset Management System

> **A robust, full-stack solution for tracking the Chain of Custody of corporate hardware.** > *Now Live on Render with PostgreSQL.*

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue.svg)
![Render](https://img.shields.io/badge/Deployment-Render-46E3B7.svg)

---

## 🚀 Live Production Link
**[Visit TechVault Live](https://techvault-it-asset-management-system-1.onrender.com/)** *(Login required. Please contact the administrator for access.)*

---

## 📖 Overview

**TechVault** resolves the chaos of managing company equipment. It provides a centralized "Command Center" where IT Administrators can onboard assets, assign them to employees, and track their entire lifecycle.

This version has been **production-hardened**, moving from a local SQLite development environment to a cloud-based **PostgreSQL** architecture with secure environment variable management.

---

## ✨ Key Features

### ⚙️ Backend & Production Engineering
* **Cloud Database Migration:** Transitioned from SQLite to a managed **PostgreSQL** instance for high availability and data persistence.
* **State Machine Logic:** Assets move through strict states (`AVAILABLE` → `ASSIGNED` → `BROKEN`).
* **Environment Security:** Utilized `python-dotenv` and server-side environment variables to hide sensitive `SECRET_KEY` and database credentials.
* **Static File Management:** Integrated **WhiteNoise** to serve compressed CSS and JavaScript files directly from the Gunicorn server.

### 🔐 Security & Access Control
* **Role-Based Access Control (RBAC):** Strict separation between `ADMIN` and `EMPLOYEE` roles.
* **Production Deployment:** Configured with `gunicorn` for a professional-grade WSGI server.
* **Zero-Trust UI:** Sensitive buttons (Delete, Assign) are physically removed from the HTML for non-admins.

### 📊 The Dashboard
* **Real-time Stats:** Live counters for Available, Assigned, and Broken items.
* **Hybrid Architecture:** Django Templates for speed, integrated with **Chart.js** for interactive analytics.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **Framework** | Django 5.x |
| **Database** | PostgreSQL (Production) / SQLite (Dev) |
| **Frontend** | Bootstrap 5, Chart.js, Jinja Templates |
| **WSGI Server** | Gunicorn |
| **Static Assets** | WhiteNoise |

---

## 🚀 Installation & Setup

Follow these steps to run the project locally.

1. Clone the repository:
   ```bash
   git clone [https://github.com/srishti-cmd/TechVault---IT-Asset-Management-System.git](https://github.com/srishti-cmd/TechVault---IT-Asset-Management-System.git)
   cd TechVault---IT-Asset-Management-System
   ```
3. Create and Activate Virtual Environment
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```
5. Environmental Variables
   ```bash
   DEBUG=True
   SECRET_KEY=your_local_key
   DATABASE_URL=postgres://user:pass@host:port/dbname (or leave blank for SQLite)
   ```
6. Initialize Database
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
7. Run Server
   ```bash
   python manage.py runserver
   ```
