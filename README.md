# Leang-Pharmacy-System

Full-stack pharmacy management (Spring Boot 3 + Spring Security + Thymeleaf + H2).

## Developer

Developed by **Nol Chhonleang**.

If you found this project from Google, feel free to connect with me:
- Name: **Nol Chhonleang**
- Role: Java/Spring Boot Developer

## Features

- **Security**: Role-based login (Admin, Pharmacist, Cashier), BCrypt passwords, CSRF protection, audit log
- **Medicines & categories**: SKU catalog, pricing, Rx flag
- **Stock**: Batch tracking, expiry alerts, low-stock warnings, FIFO deduction on sales
- **POS / Sales**: Checkout, invoices, payment methods
- **Prescriptions**: Create, dispense workflow
- **Customers & suppliers**
- **Purchase orders**: Create PO, add lines, receive into stock
- **Reports**: Sales summary, inventory overview
- **Professional UI**: Plus Jakarta Sans, teal brand theme, sidebar shell, stat tiles, panel tables, mobile sidebar toggle
- **Performance**: Single-query stock aggregation, Caffeine caching (dashboard + stock), paginated lists, fast POS search API, DB indexes, static asset caching, response compression
- **REST API**: `/api/v1/pos/search`, `/api/v1/dashboard/stats`, `/api/v1/stock/overview`
- **POS**: Live product search cart (no full-page medicine load), printable receipts
- **Ops**: Spring Actuator health/metrics/caches

## Requirements

- Java 17+
- Maven 3.9+

## Run

```bash
cd E:\Leang_Pharmacy_System
.\mvnw.cmd spring-boot:run
```

Open **http://localhost:8082**

| User | Password | Role |
|------|----------|------|
| admin | admin123 | Admin (full access) |
| pharmacist | pharma123 | Pharmacist |
| cashier | cash123 | Cashier (POS, customers) |

H2 console (admin only): http://localhost:8082/h2-console  
JDBC URL: `jdbc:h2:file:./data/pharmacy`

## Screenshots

Add your screenshots to `docs/screenshots/` and keep these filenames:

- `login.png`
- `dashboard.png`
- `pos.png`
- `inventory.png`

Then they will render here:

<img width="1919" height="1011" alt="image" src="https://github.com/user-attachments/assets/db536a62-77c1-4d29-89a8-861b97332c2d" />

<img width="1919" height="1005" alt="image" src="https://github.com/user-attachments/assets/db4228f2-db75-4318-bf7c-e27a1f7d4e8e" />

<img width="1917" height="1013" alt="image" src="https://github.com/user-attachments/assets/29df81c9-879a-4eac-9fee-387650bcf206" />

<img width="1919" height="1016" alt="image" src="https://github.com/user-attachments/assets/b4397a7c-d16f-4e23-bd42-d9ee263c9e4a" />


## Project structure

```
src/main/java/com/hug/pharmacy/
  config/       Security, seed data
  controller/   Web MVC
  entity/       JPA models
  repository/
  service/
  security/
src/main/resources/
  templates/    Thymeleaf pages
  static/css/   app.css
  static/js/    app.js
  templates/fragments/  app-layout, sidebar, head
```

Regenerate all page templates after layout changes:

```bash
python scripts/gen_ui.py
```

## API note

This build uses server-rendered pages. REST APIs can be added under `/api/v1` with JWT in a future phase.
