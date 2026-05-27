from pathlib import Path

T = Path(__file__).resolve().parent.parent / "src" / "main" / "resources" / "templates"

START = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" xmlns:sec="http://www.thymeleaf.org/extras/spring-security" lang="en">
<head th:replace="~{fragments/head :: head(${pageTitle})}"></head>
<body>
<div class="app-wrapper">
<div id="sidebarBackdrop" class="sidebar-backdrop"></div>
<aside th:replace="~{fragments/sidebar :: sidebar}"></aside>
<div class="app-main">
<header class="app-topbar">
  <button type="button" class="topbar-menu-btn" id="sidebarToggle"><i class="bi bi-list"></i></button>
  <nav aria-label="breadcrumb"><ol class="breadcrumb mb-0">
    <li class="breadcrumb-item"><a href="/dashboard">Home</a></li>
    <li class="breadcrumb-item active" th:text="${pageTitle}">Page</li>
  </ol></nav>
</header>
<main class="app-content">
<div th:if="${success}" class="alert alert-success alert-toast alert-dismissible fade show" data-auto-dismiss>
  <span th:text="${success}"></span><button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
<div th:if="${error}" class="alert alert-danger alert-toast alert-dismissible fade show">
  <span th:text="${error}"></span><button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
"""

END = """
</main></motion.div></div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script th:src="@{/js/app.js}"></script>
</body></html>
""".replace("</motion.div></div>", "</div></div>")


def save(path, body):
    p = T / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(START + body + END, encoding="utf-8")


def header(title, lead, action_html=""):
    return f'<div class="page-header"><div><h1>{title}</h1><p class="lead">{lead}</p></div>{action_html}</div>'


save("dashboard.html", header("Dashboard", "Real-time pharmacy operations overview",
    '<a href="/pos" class="btn btn-primary-brand"><i class="bi bi-cart-plus me-1"></i> New Sale</a>') + """
<div class="stat-grid">
  <div class="stat-tile"><div class="icon-wrap teal"><i class="bi bi-capsule"></i></div><motion.div><div class="label">Medicines</div><div class="value" th:text="${stats.medicineCount}">0</div></div></div>
""".replace("<motion.div>", "<div>").replace("</motion.div>", "</div>") + """
  <motion.div class="stat-tile"><div class="icon-wrap red"><i class="bi bi-exclamation-triangle"></i></div><div><motion.div class="label">Low Stock</div><div class="value" th:text="${stats.lowStockCount}">0</div></div></div>
""".replace("<motion.div", "<div").replace("</motion.div>", "</div>") + """
  <div class="stat-tile"><div class="icon-wrap amber"><i class="bi bi-calendar-x"></i></div><div><div class="label">Expiring</motion.div><div class="value" th:text="${stats.expiringSoonCount}">0</div></div></div>
""".replace("<motion.div", "<div").replace("</motion.div>", "</div>") + """
  <div class="stat-tile"><div class="icon-wrap teal"><i class="bi bi-file-medical"></i></div><div><div class="label">Pending Rx</div><div class="value" th:text="${stats.pendingPrescriptions}">0</div></div></div>
  <div class="stat-tile"><div class="icon-wrap green"><i class="bi bi-currency-dollar"></i></div><div><div class="label">Today</div><div class="value" th:text="${#numbers.formatDecimal(stats.todaySales,1,2)}">0</div></div></div>
  <div class="stat-tile"><div class="icon-wrap green"><i class="bi bi-graph-up"></i></div><div><div class="label">This Month</div><div class="value" th:text="${#numbers.formatDecimal(stats.monthSales,1,2)}">0</div></div></div>
</div>
<div class="row g-3">
  <div class="col-lg-6"><div class="panel"><div class="panel-header"><h2>Low Stock</h2></div><div class="panel-body p-0">
    <table class="table mb-0"><thead><tr><th>SKU</th><th>Product</th><th>Qty</th></tr></thead>
    <tbody><tr th:each="s : ${lowStock}"><td><code th:text="${s.sku}"></code></td><td th:text="${s.name}"></td>
    <td><span class="badge badge-pill badge-stock-low" th:text="${s.totalStock}"></span></td></tr></tbody></table>
  </div></div></div>
  <div class="col-lg-6"><div class="panel"><div class="panel-header"><h2>Recent Sales</h2></div><motion.div class="panel-body p-0">
    <table class="table mb-0"><thead><tr><th>Invoice</th><th>Total</th><th>Time</th></tr></thead>
    <tbody><tr th:each="sale : ${recentSales}"><td th:text="${sale.invoiceNumber}"></td><td th:text="${#numbers.formatDecimal(sale.total,1,2)}"></td>
    <td th:text="${#temporals.format(sale.soldAt,'MMM dd HH:mm')}"></td></tr></tbody></table>
  </div></div></div>
</div>
""".replace("<motion.div", "<div").replace("</motion.div>", "</div>"))

# I'll write remaining pages in a cleaner way below without replace hacks
