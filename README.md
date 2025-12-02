# 🛡️ TechVault - Enterprise IT Asset Management System

> **A robust, full-stack solution for tracking the Chain of Custody of corporate hardware.** > *Built with Django 5, Django REST Framework, and Bootstrap 5.*

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![Bootstrap](https://img.shields.io/badge/Frontend-Bootstrap%205-purple.svg)
![DRF](https://img.shields.io/badge/API-REST%20Framework-red.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

---

## 📖 Overview

**TechVault** resolves the chaos of managing company equipment using spreadsheets. It provides a centralized "Command Center" where IT Administrators can onboard assets, assign them to employees, and track their entire lifecycle.

Unlike simple CRUD apps, TechVault enforces **Business Logic Validation** (preventing illegal asset moves) and features an **Automated "Ghost" Audit Log** that tracks history in the background without human intervention.

---

## ✨ Key Features

### ⚙️ Backend Engineering
* **State Machine Logic:** Assets move through strict states (`AVAILABLE` → `ASSIGNED` → `BROKEN`). The system prevents invalid transitions (e.g., assigning a broken item).
* **"Ghost" Audit Log:** Implemented using **Django Signals** and **Polymorphism** (`GenericForeignKey`). Every database change is recorded silently to ensure data integrity.
* **Performance Optimization:** Utilized `select_related` to fetch related data (Users, Categories) in a single query, solving the N+1 problem.

### 🔐 Security & Access Control
* **Role-Based Access Control (RBAC):** Strict separation between `ADMIN` and `EMPLOYEE` roles.
* **Zero-Trust UI:** Sensitive buttons (Delete, Assign) are physically removed from the HTML for non-admins.
* **Custom Authentication:** Corporate-style Email/Password login instead of Usernames.

### 📊 The Dashboard
* **Hybrid Architecture:** Server-side rendered Django Templates for speed, integrated with **Chart.js** for interactive analytics.
* **Real-time Stats:** Live counters for Available, Assigned, and Broken items.
* **Quick Actions:** AJAX-free Modals for instant asset and user onboarding.

### Snapshot
![Sample Output](https://github.com/srishti-cmd/TechVault---IT-Asset-Management-System/blob/main/TechVault-Dashboard.png)

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **Framework** | Django 5.x |
| **API** | Django REST Framework (DRF) |
| **Frontend** | Bootstrap 5, Chart.js, Jinja Templates |
| **Database** | SQLite (Dev) / PostgreSQL Ready |
| **Authentication** | SimpleJWT (API) / Session Auth (Web) |

---

## 🚀 Installation & Setup

Follow these steps to run the project locally.

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/techvault.git
   cd techvault
   ```
2. Create Virtual Environment
   ```bash
   python -m venv venv
   ```
3. Activate Virtual Environment
   ```bash
   venv\Scripts\activate
   ```
4. Install Dependencies
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt Pillow
   ```
   OR (If you have a requirements.txt file)
   ```bash
   pip install -r requirements.txt
   ```
5. Initialize Database
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Create Admin User
   ```bash
   python manage.py createsuperuser
   ```
7. Run Server
   ```bash
   python manage.py runserver
   ```
