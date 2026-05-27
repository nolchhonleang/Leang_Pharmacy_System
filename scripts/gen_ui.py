# -*- coding: utf-8 -*-
"""Generate professional Thymeleaf pages for Leang-Pharmacy-System."""
from pathlib import Path

T = Path(__file__).resolve().parent.parent / "src" / "main" / "resources" / "templates"
E = "div"  # HTML element tag

WRAP = f"""<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" th:replace="~{{fragments/app-layout :: layout(~{{::main}})}}">
<body>
<th:block th:fragment="main">
"""

END = """
</th:block>
</body>
</html>
"""


def ph(title, lead, btn_href="", btn_label="", btn_icon="bi-plus-lg"):
    btn = ""
    if btn_href:
        btn = f'<a class="btn btn-primary-brand" href="{btn_href}"><i class="bi {btn_icon} me-1"></i> {btn_label}</a>'
    return f"""<{E} class="page-header">
  <{E}><h1>{title}</h1><p class="lead">{lead}</p></{E}>
  {btn}
</{E}>
"""


def w(path: str, body: str):
    (T / path).write_text(WRAP + body + END, encoding="utf-8")
    print("wrote", path)


w("dashboard.html", ph("Dashboard", "Operations at a glance", "/pos", "New Sale", "bi-cart-plus") + f"""
<{E} class="stat-grid">
  <{E} class="stat-tile"><{E} class="icon-wrap teal"><i class="bi bi-capsule"></i></{E}><{E}><{E} class="label">Medicines</{E}><{E} class="value" th:text="${{stats.medicineCount}}">0</{E}></{E}></{E}>
  <{E} class="stat-tile"><{E} class="icon-wrap red"><i class="bi bi-exclamation-triangle"></i></{E}><{E}><{E} class="label">Low Stock</{E}><{E} class="value" th:text="${{stats.lowStockCount}}">0</{E}></{E}></{E}>
  <{E} class="stat-tile"><{E} class="icon-wrap amber"><i class="bi bi-calendar-x"></i></{E}><{E}><{E} class="label">Expiring Soon</{E}><{E} class="value" th:text="${{stats.expiringSoonCount}}">0</{E}></{E}></{E}>
  <{E} class="stat-tile"><{E} class="icon-wrap teal"><i class="bi bi-file-medical"></i></{E}><{E}><{E} class="label">Pending Rx</{E}><{E} class="value" th:text="${{stats.pendingPrescriptions}}">0</{E}></{E}></{E}>
  <{E} class="stat-tile"><{E} class="icon-wrap green"><i class="bi bi-currency-dollar"></i></{E}><{E}><{E} class="label">Today Sales</{E}><{E} class="value" th:text="${{#numbers.formatDecimal(stats.todaySales,1,2)}}">0</{E}></{E}></{E}>
  <{E} class="stat-tile"><{E} class="icon-wrap green"><i class="bi bi-graph-up"></i></{E}><{E}><{E} class="label">Month Sales</{E}><{E} class="value" th:text="${{#numbers.formatDecimal(stats.monthSales,1,2)}}">0</{E}></{E}></{E}>
</{E}>
<{E} class="row g-3">
  <{E} class="col-lg-6">
    <{E} class="panel">
      <{E} class="panel-header"><h2>Low stock alerts</h2><a href="/stock" class="btn btn-sm btn-outline-secondary">View stock</a></{E}>
      <{E} class="panel-body p-0 table-responsive">
        <table class="table mb-0">
          <thead><tr><th>SKU</th><th>Product</th><th>Qty</th></tr></thead>
          <tbody>
            <tr th:each="s : ${{lowStock}}">
              <td><code th:text="${{s.sku}}"></code></td>
              <td th:text="${{s.name}}"></td>
              <td><span class="badge badge-pill badge-stock-low" th:text="${{s.totalStock}}"></span></td>
            </tr>
            <tr th:if="${{#lists.isEmpty(lowStock)}}"><td colspan="3" class="text-muted text-center py-4">All stock levels healthy</td></tr>
          </tbody>
        </table>
      </{E}>
    </{E}>
  </{E}>
  <{E} class="col-lg-6">
    <{E} class="panel">
      <{E} class="panel-header"><h2>Recent sales</h2><a href="/pos/history" class="btn btn-sm btn-outline-secondary">Full history</a></{E}>
      <{E} class="panel-body p-0 table-responsive">
        <table class="table mb-0">
          <thead><tr><th>Invoice</th><th>Total</th><th>When</th></tr></thead>
          <tbody>
            <tr th:each="sale : ${{recentSales}}">
              <td class="fw-semibold" th:text="${{sale.invoiceNumber}}"></td>
              <td th:text="|$${{#numbers.formatDecimal(sale.total,1,2)}}|"></td>
              <td class="text-muted" th:text="${{#temporals.format(sale.soldAt,'MMM dd, HH:mm')}}"></td>
            </tr>
          </tbody>
        </table>
      </{E}>
    </{E}>
  </{E}>
</{E}>
<{E} class="panel mt-3" th:if="${{not #lists.isEmpty(expiring)}}">
  <{E} class="panel-header"><h2 class="text-warning mb-0"><i class="bi bi-calendar-x me-1"></i> Expiring batches</h2></{E}>
  <{E} class="panel-body p-0 table-responsive">
    <table class="table mb-0 table-sm">
      <thead><tr><th>Product</th><th>Expiry</th><th>Qty</th></tr></thead>
      <tbody>
        <tr th:each="b : ${{expiring}}">
          <td th:text="${{b.medicine.name}}"></td>
          <td th:text="${{b.expiryDate}}"></td>
          <td th:text="${{b.quantity}}"></td>
        </tr>
      </tbody>
    </table>
  </{E}>
</{E}>
""")

w("medicines/list.html", ph("Medicines", "Product catalog, pricing, and stock levels", "/medicines/new", "Add medicine") + f"""
<{E} class="panel mb-3"><{E} class="panel-body">
  <form class="row g-2 align-items-end" method="get" action="/medicines">
    <{E} class="col-md-6">
      <label class="form-label">Search</label>
      <{E} class="input-group search-bar">
        <span class="input-group-text"><i class="bi bi-search"></i></span>
        <input name="q" class="form-control" th:value="${{q}}" placeholder="Name or SKU..."/>
      </{E}>
    </{E}>
    <{E} class="col-auto"><button type="submit" class="btn btn-primary-brand">Search</button></{E}>
    <{E} class="col-auto" th:if="${{q != null and !#strings.isEmpty(q)}}">
      <a href="/medicines" class="btn btn-outline-secondary">Clear</a>
    </{E}>
  </form>
</{E}></{E}>
<{E} class="panel">
  <{E} class="panel-body p-0 table-responsive">
    <table class="table table-hover mb-0">
      <thead><tr><th>SKU</th><th>Name</th><th>Category</th><th>Price</th><th>Stock</th><th>Rx</th><th></th></tr></thead>
      <tbody>
        <tr th:each="m : ${{medicines}}">
          <td><code th:text="${{m.sku}}"></code></td>
          <td class="fw-semibold" th:text="${{m.name}}"></td>
          <td th:text="${{m.category != null ? m.category.name : '—'}}"></td>
          <td th:text="|$${{#numbers.formatDecimal(m.unitPrice,1,2)}}|"></td>
          <td>
            <th:block th:each="s : ${{stock}}" th:if="${{s.id == m.id}}">
              <span th:class="${{s.lowStock ? 'badge badge-pill badge-stock-low' : 'badge badge-pill badge-stock-ok'}}" th:text="${{s.totalStock}}"></span>
            </th:block>
          </td>
          <td><span th:if="${{m.requiresPrescription}}" class="badge badge-pill badge-rx">Rx</span></td>
          <td class="text-end text-nowrap">
            <a th:href="@{{/medicines/{{id}}/edit(id=${{m.id}})}}" class="btn btn-sm btn-outline-primary">Edit</a>
            <form th:action="@{{/medicines/{{id}}/delete(id=${{m.id}})}}" method="post" class="d-inline" onsubmit="return confirm('Deactivate this medicine?');">
              <input type="hidden" th:name="${{_csrf.parameterName}}" th:value="${{_csrf.token}}"/>
              <button type="submit" class="btn btn-sm btn-outline-danger">Deactivate</button>
            </form>
          </td>
        </tr>
        <tr th:if="${{#lists.isEmpty(medicines)}}">
          <td colspan="7" class="empty-state"><i class="bi bi-inbox d-block"></i>No medicines found</td>
        </tr>
      </tbody>
    </table>
  </{E}>
</{E}>
""")

w("medicines/form.html", ph("Medicine", "Add or update catalog entry") + f"""
<{E} class="panel"><{E} class="panel-body">
<form method="post" th:action="@{{/medicines/save}}" th:object="${{medicine}}">
  <input type="hidden" th:name="${{_csrf.parameterName}}" th:value="${{_csrf.token}}"/>
  <input type="hidden" th:field="*{{id}}"/>
  <{E} class="row g-3">
    <{E} class="col-md-4"><label class="form-label">SKU</label><input class="form-control" th:field="*{{sku}}" required/></{E}>
    <{E} class="col-md-8"><label class="form-label">Name</label><input class="form-control" th:field="*{{name}}" required/></{E}>
    <{E} class="col-md-4"><label class="form-label">Category</label>
      <select name="categoryId" class="form-select">
        <option value="">— None —</option>
        <option th:each="c : ${{categories}}" th:value="${{c.id}}" th:text="${{c.name}}"
                th:selected="${{medicine.category != null and medicine.category.id == c.id}}"></option>
      </select>
    </{E}>
    <{E} class="col-md-4"><label class="form-label">Unit price ($)</label><input type="number" step="0.01" min="0" class="form-control" th:field="*{{unitPrice}}"/></{E}>
    <{E} class="col-md-4"><label class="form-label">Cost ($)</label><input type="number" step="0.01" min="0" class="form-control" th:field="*{{costPrice}}"/></{E}>
    <{E} class="col-md-4"><label class="form-label">Reorder level</label><input type="number" min="0" class="form-control" th:field="*{{reorderLevel}}"/></{E}>
    <{E} class="col-12">
      <{E} class="form-check">
        <input class="form-check-input" type="checkbox" th:field="*{{requiresPrescription}}" id="rxCheck"/>
        <label class="form-check-label" for="rxCheck">Requires prescription</label>
      </{E}>
    </{E}>
  </{E}>
  <button type="submit" class="btn btn-primary-brand mt-3">Save medicine</button>
  <a href="/medicines" class="btn btn-outline-secondary mt-3">Cancel</a>
</form>
</{E}></{E}>
""")

w("stock/index.html", ph("Stock", "Inventory levels, batches, and expiry", "/stock/add", "Receive stock") + f"""
<{E} class="row g-3">
  <{E} class="col-lg-7">
    <{E} class="panel">
      <{E} class="panel-header"><h2>Inventory overview</h2></{E}>
      <{E} class="panel-body p-0 table-responsive">
        <table class="table mb-0">
          <thead><tr><th>SKU</th><th>Product</th><th>On hand</th><th>Reorder</th><th>Price</th></tr></thead>
          <tbody>
            <tr th:each="s : ${{overview}}">
              <td><code th:text="${{s.sku}}"></code></td>
              <td th:text="${{s.name}}"></td>
              <td><span th:class="${{s.lowStock ? 'badge badge-pill badge-stock-low' : 'badge badge-pill badge-stock-ok'}}" th:text="${{s.totalStock}}"></span></td>
              <td th:text="${{s.reorderLevel}}"></td>
              <td th:text="${{'$' + #numbers.formatDecimal(s.unitPrice,1,2)}}"></td>
            </tr>
          </tbody>
        </table>
      </{E}>
    </{E}>
  </{E}>
  <{E} class="col-lg-5">
    <{E} class="panel mb-3">
      <{E} class="panel-header"><h2 class="text-warning mb-0"><i class="bi bi-calendar-x me-1"></i> Expiring soon</h2></{E}>
      <{E} class="panel-body p-0">
        <table class="table mb-0 table-sm">
          <thead><tr><th>Product</th><th>Expiry</th><th>Qty</th></tr></thead>
          <tbody>
            <tr th:each="b : ${{expiring}}">
              <td th:text="${{b.medicine.name}}"></td>
              <td th:text="${{b.expiryDate}}"></td>
              <td th:text="${{b.quantity}}"></td>
            </tr>
            <tr th:if="${{#lists.isEmpty(expiring)}}"><td colspan="3" class="text-muted text-center py-3">No batches expiring soon</td></tr>
          </tbody>
        </table>
      </{E}>
    </{E}>
    <{E} class="panel">
      <{E} class="panel-header"><h2>Recent batches</h2></{E}>
      <{E} class="panel-body p-0">
        <table class="table mb-0 table-sm">
          <thead><tr><th>Batch</th><th>Product</th><th>Qty</th></tr></thead>
          <tbody>
            <tr th:each="b, stat : ${{batches}}" th:if="${{stat.index < 8}}">
              <td><code th:text="${{b.batchNumber}}"></code></td>
              <td th:text="${{b.medicine.name}}"></td>
              <td th:text="${{b.quantity}}"></td>
            </tr>
          </tbody>
        </table>
      </{E}>
    </{E}>
  </{E}>
</{E}>
""")

w("stock/add.html", ph("Receive stock", "Add a new inventory batch") + f"""
<{E} class="panel"><{E} class="panel-body">
<form method="post" th:action="@{{/stock/add}}">
  <input type="hidden" th:name="${{_csrf.parameterName}}" th:value="${{_csrf.token}}"/>
  <{E} class="row g-3">
    <{E} class="col-md-6"><label class="form-label">Medicine</label>
      <select name="medicineId" class="form-select" required>
        <option th:each="m : ${{medicines}}" th:value="${{m.id}}" th:text="${{m.name + ' (' + m.sku + ')'}}"></option>
      </select>
    </{E}>
    <{E} class="col-md-6"><label class="form-label">Supplier (optional)</label>
      <select name="supplierId" class="form-select">
        <option value="">— None —</option>
        <option th:each="s : ${{suppliers}}" th:value="${{s.id}}" th:text="${{s.name}}"></option>
      </select>
    </{E}>
    <{E} class="col-md-4"><label class="form-label">Batch number</label><input name="batchNumber" class="form-control" required/></{E}>
    <{E} class="col-md-4"><label class="form-label">Quantity</label><input name="quantity" type="number" min="1" class="form-control" required/></{E}>
    <{E} class="col-md-4"><label class="form-label">Expiry date</label><input name="expiryDate" type="date" class="form-control" required/></{E}>
  </{E}>
  <button type="submit" class="btn btn-primary-brand mt-3">Add batch</button>
  <a href="/stock" class="btn btn-outline-secondary mt-3">Cancel</a>
</form>
</{E}></{E}>
""")

w("pos/index.html", ph("Point of Sale", "Select quantities and complete checkout") + f"""
<form method="post" th:action="@{{/pos/checkout}}">
  <input type="hidden" th:name="${{_csrf.parameterName}}" th:value="${{_csrf.token}}"/>
  <{E} class="panel mb-3"><{E} class="panel-body">
    <{E} class="row g-3">
      <{E} class="col-md-4"><label class="form-label">Customer</label>
        <select name="customerId" class="form-select">
          <option value="">Walk-in customer</option>
          <option th:each="c : ${{customers}}" th:value="${{c.id}}" th:text="${{c.fullName}}"></option>
        </select>
      </{E}>
      <{E} class="col-md-4"><label class="form-label">Payment</label>
        <select name="paymentMethod" class="form-select"><option>CASH</option><option>CARD</option><option>INSURANCE</option></select>
      </{E}>
      <{E} class="col-md-4"><label class="form-label">Discount ($)</label><input name="discount" type="number" step="0.01" min="0" value="0" class="form-control"/></{E}>
    </{E}>
  </{E}></{E}>
  <{E} class="panel">
    <{E} class="panel-header"><h2>Cart</h2><span class="text-muted small">Enter quantity &gt; 0 to include</span></{E}>
    <{E} class="panel-body p-0 table-responsive">
      <table class="table mb-0">
        <thead><tr><th>Product</th><th>SKU</th><th class="text-end">Price</th><th class="text-center">Available</th><th style="width:110px">Qty</th></tr></thead>
        <tbody>
          <tr th:each="m : ${{medicines}}">
            <td class="fw-semibold" th:text="${{m.name}}"></td>
            <td><code th:text="${{m.sku}}"></code></td>
            <td class="text-end" th:text="|$${{#numbers.formatDecimal(m.unitPrice,1,2)}}|"></td>
            <td class="text-center">
              <th:block th:each="s : ${{stock}}" th:if="${{s.id == m.id}}">
                <span th:class="${{s.lowStock ? 'badge badge-pill badge-stock-low' : 'badge badge-pill badge-stock-ok'}}" th:text="${{s.totalStock}}"></span>
              </th:block>
            </td>
            <td><input type="hidden" name="medicineId" th:value="${{m.id}}"/><input name="quantity" type="number" min="0" value="0" class="form-control form-control-sm text-center"/></td>
          </tr>
        </tbody>
      </table>
    </{E}>
    <{E} class="pos-checkout-bar">
      <button type="submit" class="btn btn-primary-brand btn-lg"><i class="bi bi-check2-circle me-1"></i> Complete sale</button>
    </{E}>
  </{E}>
</form>
""")

w("pos/history.html", ph("Sales history", "Recent transactions and invoices") + f"""
<{E} class="panel">
  <{E} class="panel-body p-0 table-responsive">
    <table class="table table-hover mb-0">
      <thead><tr><th>Invoice</th><th>Customer</th><th>Payment</th><th>Subtotal</th><th>Discount</th><th>Total</th><th>Date</th></tr></thead>
      <tbody>
        <tr th:each="sale : ${{sales}}">
          <td class="fw-semibold" th:text="${{sale.invoiceNumber}}"></td>
          <td th:text="${{sale.customer != null ? sale.customer.fullName : 'Walk-in'}}"></td>
          <td><span class="badge bg-light text-dark" th:text="${{sale.paymentMethod}}"></span></td>
          <td th:text="|$${{#numbers.formatDecimal(sale.subtotal,1,2)}}|"></td>
          <td th:text="|$${{#numbers.formatDecimal(sale.discount,1,2)}}|"></td>
          <td class="fw-semibold" th:text="|$${{#numbers.formatDecimal(sale.total,1,2)}}|"></td>
          <td class="text-muted" th:text="${{#temporals.format(sale.soldAt,'MMM dd, yyyy HH:mm')}}"></td>
        </tr>
        <tr th:if="${{#lists.isEmpty(sales)}}"><td colspan="7" class="empty-state"><i class="bi bi-receipt d-block"></i>No sales yet</td></tr>
      </tbody>
    </table>
  </{E}>
</{E}>
""")

w("prescriptions/list.html", ph("Prescriptions", "Doctor orders and dispensing status", "/prescriptions/new", "New prescription", "bi-file-earmark-plus") + f"""
<{E} class="panel">
  <{E} class="panel-body p-0 table-responsive">
    <table class="table table-hover mb-0">
      <thead><tr><th>#</th><th>Patient</th><th>Doctor</th><th>Date</th><th>Status</th><th>Items</th><th></th></tr></thead>
      <tbody>
        <tr th:each="rx : ${{prescriptions}}">
          <td th:text="${{'RX-' + rx.id}}"></td>
          <td th:text="${{rx.customer.fullName}}"></td>
          <td th:text="${{rx.doctorName}}"></td>
          <td th:text="${{rx.prescribedDate}}"></td>
          <td><span class="badge badge-pill" th:classappend="${{rx.status.name() == 'PENDING' ? 'badge-stock-low' : 'badge-stock-ok'}}" th:text="${{rx.status}}"></span></td>
          <td th:text="${{#lists.size(rx.items)}}"></td>
          <td class="text-end">
            <form th:if="${{rx.status.name() == 'PENDING'}}" th:action="@{{/prescriptions/{{id}}/dispense(id=${{rx.id}})}}" method="post" class="d-inline">
              <input type="hidden" th:name="${{_csrf.parameterName}}" th:value="${{_csrf.token}}"/>
              <button class="btn btn-sm btn-primary-brand">Dispense</button>
            </form>
          </td>
        </tr>
      </tbody>
    </table>
  </{E}>
</{E}>
""")

w("prescriptions/form.html", ph("New prescription", "Record a prescription for a patient") + f"""
<{E} class="panel"><{E} class="panel-body">
<form method="post" th:action="@{{/prescriptions/save}}" id="rxForm">
  <input type="hidden" th:name="${{_csrf.parameterName}}" th:value="${{_csrf.token}}"/>
  <{E} class="row g-3">
    <{E} class="col-md-6"><label class="form-label">Patient</label>
      <select name="customerId" class="form-select" required>
        <option th:each="c : ${{customers}}" th:value="${{c.id}}" th:text="${{c.fullName}}"></option>
      </select>
    </{E}>
    <{E} class="col-md-6"><label class="form-label">Doctor</label><input name="doctorName" class="form-control" required/></{E}>
    <{E} class="col-md-6"><label class="form-label">Prescribed date</label><input name="prescribedDate" type="date" class="form-control" required/></{E}>
    <{E} class="col-12"><label class="form-label">Notes</label><textarea name="notes" class="form-control" rows="2"></textarea></{E}>
  </{E}>
  <hr class="my-4"/>
  <h3 class="h6 fw-bold mb-3">Line items</h3>
  <{E} id="rxLines">
    <{E} class="row g-2 mb-2 rx-line">
      <{E} class="col-md-8"><select name="medicineId" class="form-select"><option th:each="m : ${{medicines}}" th:value="${{m.id}}" th:text="${{m.name}}"></option></select></{E}>
      <{E} class="col-md-3"><input name="quantity" type="number" min="1" value="1" class="form-control" placeholder="Qty"/></{E}>
      <{E} class="col-md-1"><button type="button" class="btn btn-outline-danger w-100 remove-line" title="Remove"><i class="bi bi-trash"></i></button></{E}>
    </{E}>
  </{E}>
  <button type="button" class="btn btn-outline-secondary btn-sm" id="addRxLine"><i class="bi bi-plus"></i> Add line</button>
  <button type="submit" class="btn btn-primary-brand mt-3 d-block">Save prescription</button>
</form>
</{E}></{E}>
""")

w("customers/list.html", ph("Customers", "Patient and customer records", "/customers/new", "Add customer") + f"""
<{E} class="panel mb-3"><{E} class="panel-body">
  <form class="row g-2 align-items-end" method="get" action="/customers">
    <{E} class="col-md-6"><label class="form-label">Search by name</label>
      <{E} class="input-group search-bar"><span class="input-group-text"><i class="bi bi-search"></i></span>
      <input name="q" class="form-control" th:value="${{q}}" placeholder="Customer name..."/></{E}></{E}>
    <{E} class="col-auto"><button class="btn btn-primary-brand">Search</button></{E}>
  </form>
</{E}></{E}>
<{E} class="panel">
  <{E} class="panel-body p-0 table-responsive">
    <table class="table table-hover mb-0">
      <thead><tr><th>Name</th><th>Phone</th><th>Email</th><th>Allergies</th></tr></thead>
      <tbody>
        <tr th:each="c : ${{customers}}">
          <td class="fw-semibold" th:text="${{c.fullName}}"></td>
          <td th:text="${{c.phone != null ? c.phone : '—'}}"></td>
          <td th:text="${{c.email != null ? c.email : '—'}}"></td>
          <td th:text="${{c.allergies != null ? c.allergies : '—'}}"></td>
        </tr>
      </tbody>
    </table>
  </{E}>
</{E}>
""")

w("customers/form.html", ph("Add customer", "Register a new customer") + f"""
<{E} class="panel"><{E} class="panel-body">
<form method="post" th:action="@{{/customers/save}}" th:object="${{customer}}">
  <input type="hidden" th:name="${{_csrf.parameterName}}" th:value="${{_csrf.token}}"/>
  <{E} class="row g-3">
    <{E} class="col-md-6"><label class="form-label">Full name</label><input class="form-control" th:field="*{{fullName}}" required/></{E}>
    <{E} class="col-md-6"><label class="form-label">Phone</label><input class="form-control" th:field="*{{phone}}"/></{E}>
    <{E} class="col-md-6"><label class="form-label">Email</label><input type="email" class="form-control" th:field="*{{email}}"/></{E}>
    <{E} class="col-12"><label class="form-label">Address</label><input class="form-control" th:field="*{{address}}"/></{E}>
    <{E} class="col-12"><label class="form-label">Allergies</label><textarea class="form-control" th:field="*{{allergies}}" rows="2"></textarea></{E}>
  </{E}>
  <button type="submit" class="btn btn-primary-brand mt-3">Save customer</button>
  <a href="/customers" class="btn btn-outline-secondary mt-3">Cancel</a>
</form>
</{E}></{E}>
""")

w("suppliers/list.html", ph("Suppliers", "Vendors and purchase contacts", "/suppliers/new", "Add supplier") + f"""
<{E} class="panel">
  <{E} class="panel-body p-0 table-responsive">
    <table class="table table-hover mb-0">
      <thead><tr><th>Name</th><th>Contact</th><th>Phone</th><th>Email</th><th></th></tr></thead>
      <tbody>
        <tr th:each="s : ${{suppliers}}">
          <td class="fw-semibold" th:text="${{s.name}}"></td>
          <td th:text="${{s.contactPerson != null ? s.contactPerson : '—'}}"></td>
          <td th:text="${{s.phone != null ? s.phone : '—'}}"></td>
          <td th:text="${{s.email != null ? s.email : '—'}}"></td>
          <td class="text-end"><a th:href="@{{/suppliers/{{id}}/edit(id=${{s.id}})}}" class="btn btn-sm btn-outline-primary">Edit</a></td>
        </tr>
      </tbody>
    </table>
  </{E}>
</{E}>
""")

w("suppliers/form.html", ph("Supplier", "Vendor details") + f"""
<{E} class="panel"><{E} class="panel-body">
<form method="post" th:action="@{{/suppliers/save}}" th:object="${{supplier}}">
  <input type="hidden" th:name="${{_csrf.parameterName}}" th:value="${{_csrf.token}}"/>
  <input type="hidden" th:field="*{{id}}"/>
  <{E} class="row g-3">
    <{E} class="col-md-6"><label class="form-label">Name</label><input class="form-control" th:field="*{{name}}" required/></{E}>
    <{E} class="col-md-6"><label class="form-label">Contact person</label><input class="form-control" th:field="*{{contactPerson}}"/></{E}>
    <{E} class="col-md-6"><label class="form-label">Phone</label><input class="form-control" th:field="*{{phone}}"/></{E}>
    <{E} class="col-md-6"><label class="form-label">Email</label><input type="email" class="form-control" th:field="*{{email}}"/></{E}>
    <{E} class="col-12"><label class="form-label">Address</label><textarea class="form-control" th:field="*{{address}}" rows="2"></textarea></{E}>
  </{E}>
  <button type="submit" class="btn btn-primary-brand mt-3">Save supplier</button>
  <a href="/suppliers" class="btn btn-outline-secondary mt-3">Cancel</a>
</form>
</{E}></{E}>
""")

w("categories/list.html", ph("Categories", "Organize medicines by type") + f"""
<{E} class="row g-3">
  <{E} class="col-lg-5">
    <{E} class="panel"><{E} class="panel-header"><h2>Add category</h2></{E}>
      <{E} class="panel-body">
        <form method="post" th:action="@{{/categories/save}}">
          <input type="hidden" th:name="${{_csrf.parameterName}}" th:value="${{_csrf.token}}"/>
          <label class="form-label">Name</label>
          <input name="name" class="form-control mb-3" required/>
          <button class="btn btn-primary-brand">Add</button>
        </form>
      </{E}>
    </{E}>
  </{E}>
  <{E} class="col-lg-7">
    <{E} class="panel"><{E} class="panel-header"><h2>All categories</h2></{E}>
      <{E} class="panel-body p-0">
        <ul class="list-group list-group-flush">
          <li class="list-group-item d-flex justify-content-between align-items-center" th:each="cat : ${{categories}}">
            <span th:text="${{cat.name}}"></span>
            <span class="badge bg-light text-muted">ID <span th:text="${{cat.id}}"></span></span>
          </li>
        </ul>
      </{E}>
    </{E}>
  </{E}>
</{E}>
""")

w("purchases/list.html", ph("Purchase orders", "Supplier orders and receiving", "/purchases/new", "New order") + f"""
<{E} class="panel">
  <{E} class="panel-body p-0 table-responsive">
    <table class="table table-hover mb-0">
      <thead><tr><th>PO #</th><th>Supplier</th><th>Status</th><th>Total</th><th>Expected</th><th></th></tr></thead>
      <tbody>
        <tr th:each="po : ${{orders}}">
          <td class="fw-semibold" th:text="${{po.orderNumber}}"></td>
          <td th:text="${{po.supplier.name}}"></td>
          <td><span class="badge bg-light text-dark" th:text="${{po.status}}"></span></td>
          <td th:text="${{po.totalAmount != null ? '$' + #numbers.formatDecimal(po.totalAmount,1,2) : '—'}}"></td>
          <td th:text="${{po.expectedDate != null ? po.expectedDate : '—'}}"></td>
          <td class="text-end"><a th:href="@{{/purchases/{{id}}(id=${{po.id}})}}" class="btn btn-sm btn-outline-primary">Open</a></td>
        </tr>
      </tbody>
    </table>
  </{E}>
</{E}>
""")

w("purchases/new.html", ph("New purchase order", "Create an order for a supplier") + f"""
<{E} class="panel"><{E} class="panel-body">
<form method="post" th:action="@{{/purchases/create}}">
  <input type="hidden" th:name="${{_csrf.parameterName}}" th:value="${{_csrf.token}}"/>
  <{E} class="row g-3">
    <{E} class="col-md-6"><label class="form-label">Supplier</label>
      <select name="supplierId" class="form-select" required>
        <option th:each="s : ${{suppliers}}" th:value="${{s.id}}" th:text="${{s.name}}"></option>
      </select>
    </{E}>
    <{E} class="col-md-6"><label class="form-label">Expected delivery</label><input name="expectedDate" type="date" class="form-control"/></{E}>
  </{E}>
  <button type="submit" class="btn btn-primary-brand mt-3">Create order</button>
</form>
</{E}></{E}>
""")

w("purchases/detail.html", ph("Purchase order", "Add items and receive stock") + f"""
<{E} class="row g-3 mb-3">
  <{E} class="col-md-3"><{E} class="panel panel-body text-center">
    <{E} class="text-muted small">Order</{E}><{E} class="fw-bold" th:text="${{order.orderNumber}}"></{E}>
  </{E}></{E}>
  <{E} class="col-md-3"><{E} class="panel panel-body text-center">
    <{E} class="text-muted small">Supplier</{E}><{E} class="fw-bold" th:text="${{order.supplier.name}}"></{E}>
  </{E}></{E}>
  <{E} class="col-md-3"><{E} class="panel panel-body text-center">
    <{E} class="text-muted small">Status</{E}><{E} class="fw-bold" th:text="${{order.status}}"></{E}>
  </{E}></{E}>
  <{E} class="col-md-3"><{E} class="panel panel-body text-center">
    <{E} class="text-muted small">Total</{E}><{E} class="fw-bold" th:text="${{order.totalAmount != null ? '$' + #numbers.formatDecimal(order.totalAmount,1,2) : '—'}}"></{E}>
  </{E}></{E}>
</{E}>
<{E} class="row g-3">
  <{E} class="col-lg-7">
    <{E} class="panel">
      <{E} class="panel-header"><h2>Order items</h2></{E}>
      <{E} class="panel-body p-0 table-responsive">
        <table class="table mb-0">
          <thead><tr><th>Medicine</th><th>Qty</th><th>Unit cost</th><th>Line total</th></tr></thead>
          <tbody>
            <tr th:each="item : ${{order.items}}">
              <td th:text="${{item.medicine.name}}"></td>
              <td th:text="${{item.quantity}}"></td>
              <td th:text="|$${{#numbers.formatDecimal(item.unitCost,1,2)}}|"></td>
              <td th:text="|$${{#numbers.formatDecimal(item.unitCost.multiply(T(java.math.BigDecimal).valueOf(item.quantity)),1,2)}}|"></td>
            </tr>
            <tr th:if="${{#lists.isEmpty(order.items)}}"><td colspan="4" class="text-muted text-center py-3">No items yet</td></tr>
          </tbody>
        </table>
      </{E}>
    </{E}>
  </{E}>
  <{E} class="col-lg-5">
    <{E} class="panel mb-3"><{E} class="panel-header"><h2>Add item</h2></{E}>
      <{E} class="panel-body">
        <form th:action="@{{/purchases/{{id}}/add-item(id=${{order.id}})}}" method="post">
          <input type="hidden" th:name="${{_csrf.parameterName}}" th:value="${{_csrf.token}}"/>
          <label class="form-label">Medicine</label>
          <select name="medicineId" class="form-select mb-2" required>
            <option th:each="m : ${{medicines}}" th:value="${{m.id}}" th:text="${{m.name}}"></option>
          </select>
          <label class="form-label">Quantity</label>
          <input name="quantity" type="number" min="1" class="form-control mb-2" required/>
          <label class="form-label">Unit cost ($)</label>
          <input name="unitCost" type="number" step="0.01" min="0" class="form-control mb-3" required/>
          <button class="btn btn-primary-brand w-100">Add to order</button>
        </form>
      </{E}>
    </{E}>
    <form th:if="${{order.status.name() != 'RECEIVED'}}" th:action="@{{/purchases/{{id}}/receive(id=${{order.id}})}}" method="post">
      <input type="hidden" th:name="${{_csrf.parameterName}}" th:value="${{_csrf.token}}"/>
      <button class="btn btn-success w-100 py-2"><i class="bi bi-box-arrow-in-down me-1"></i> Receive into stock</button>
    </form>
  </{E}>
</{E}>
<a href="/purchases" class="btn btn-outline-secondary mt-3"><i class="bi bi-arrow-left me-1"></i> Back to orders</a>
""")

w("reports/index.html", ph("Reports", "Sales and inventory insights") + f"""
<{E} class="stat-grid">
  <{E} class="stat-tile"><{E} class="icon-wrap green"><i class="bi bi-currency-dollar"></i></{E}><{E}><{E} class="label">Today</{E}><{E} class="value" th:text="|$${{#numbers.formatDecimal(stats.todaySales,1,2)}}|"></{E}></{E}></{E}>
  <{E} class="stat-tile"><{E} class="icon-wrap green"><i class="bi bi-graph-up"></i></{E}><{E}><{E} class="label">This month</{E}><{E} class="value" th:text="|$${{#numbers.formatDecimal(stats.monthSales,1,2)}}|"></{E}></{E}></{E}>
  <{E} class="stat-tile"><{E} class="icon-wrap red"><i class="bi bi-exclamation-triangle"></i></{E}><{E}><{E} class="label">Low stock SKUs</{E}><{E} class="value" th:text="${{stats.lowStockCount}}"></{E}></{E}></{E}>
  <{E} class="stat-tile"><{E} class="icon-wrap amber"><i class="bi bi-calendar-x"></i></{E}><{E}><{E} class="label">Expiring batches</{E}><{E} class="value" th:text="${{stats.expiringSoonCount}}"></{E}></{E}></{E}>
</{E}>
<{E} class="row g-3">
  <{E} class="col-lg-6">
    <{E} class="panel"><{E} class="panel-header"><h2>Recent sales</h2></{E}>
      <{E} class="panel-body p-0 table-responsive">
        <table class="table mb-0"><thead><tr><th>Invoice</th><th>Total</th></tr></thead>
        <tbody><tr th:each="sale : ${{sales}}"><td th:text="${{sale.invoiceNumber}}"></td><td th:text="|$${{#numbers.formatDecimal(sale.total,1,2)}}|"></td></tr></tbody>
        </table>
      </{E}>
    </{E}>
  </{E}>
  <{E} class="col-lg-6">
    <{E} class="panel"><{E} class="panel-header"><h2>Low stock</h2></{E}>
      <{E} class="panel-body p-0 table-responsive">
        <table class="table mb-0"><thead><tr><th>Product</th><th>Qty</th></tr></thead>
        <tbody><tr th:each="s : ${{stock}}" th:if="${{s.lowStock}}"><td th:text="${{s.name}}"></td><td><span class="badge badge-pill badge-stock-low" th:text="${{s.totalStock}}"></span></td></tr></tbody>
        </table>
      </{E}>
    </{E}>
  </{E}>
</{E}>
""")

w("users/list.html", ph("Users", "Staff accounts and roles", "/users/new", "Add user") + f"""
<{E} class="panel">
  <{E} class="panel-body p-0 table-responsive">
    <table class="table table-hover mb-0">
      <thead><tr><th>Username</th><th>Name</th><th>Role</th><th>Active</th><th></th></tr></thead>
      <tbody>
        <tr th:each="u : ${{users}}">
          <td><code th:text="${{u.username}}"></code></td>
          <td th:text="${{u.fullName}}"></td>
          <td th:text="${{#strings.replace(u.role.name(), 'ROLE_', '')}}"></td>
          <td><span th:class="${{u.active ? 'badge badge-pill badge-stock-ok' : 'badge badge-pill badge-stock-low'}}" th:text="${{u.active ? 'Yes' : 'No'}}"></span></td>
          <td class="text-end"><a th:href="@{{/users/{{id}}/edit(id=${{u.id}})}}" class="btn btn-sm btn-outline-primary">Edit</a></td>
        </tr>
      </tbody>
    </table>
  </{E}>
</{E}>
""")

w("users/form.html", ph("User account", "Create or update staff login") + f"""
<{E} class="panel"><{E} class="panel-body">
<form method="post" th:action="@{{/users/save}}">
  <input type="hidden" th:name="${{_csrf.parameterName}}" th:value="${{_csrf.token}}"/>
  <input type="hidden" name="id" th:value="${{user.id}}"/>
  <{E} class="row g-3">
    <{E} class="col-md-6"><label class="form-label">Username</label><input name="username" class="form-control" th:value="${{user.username}}" required/></{E}>
    <{E} class="col-md-6"><label class="form-label">Full name</label><input name="fullName" class="form-control" th:value="${{user.fullName}}" required/></{E}>
    <{E} class="col-md-6"><label class="form-label">Password</label><input name="password" type="password" class="form-control" th:placeholder="${{user.id != null ? 'Leave blank to keep' : 'Required'}}" th:required="${{user.id == null}}"/></{E}>
    <{E} class="col-md-6"><label class="form-label">Role</label>
      <select name="role" class="form-select" required>
        <option th:each="r : ${{roles}}" th:value="${{r}}" th:text="${{#strings.replace(r.name(), 'ROLE_', '')}}" th:selected="${{user.role == r}}"></option>
      </select>
    </{E}>
    <{E} class="col-12"><{E} class="form-check">
      <input type="hidden" name="active" value="false"/>
      <input class="form-check-input" type="checkbox" name="active" value="true" th:checked="${{user.active}}"/>
      <label class="form-check-label">Account active</label>
    </{E}></{E}>
  </{E}>
  <button type="submit" class="btn btn-primary-brand mt-3">Save user</button>
  <a href="/users" class="btn btn-outline-secondary mt-3">Cancel</a>
</form>
</{E}></{E}>
""")

w("audit/list.html", ph("Audit log", "Security and change history") + f"""
<{E} class="panel">
  <{E} class="panel-body p-0 table-responsive">
    <table class="table table-sm mb-0">
      <thead><tr><th>Time</th><th>User</th><th>Action</th><th>Entity</th><th>Details</th></tr></thead>
      <tbody>
        <tr th:each="log : ${{logs}}">
          <td class="text-muted text-nowrap" th:text="${{#temporals.format(log.createdAt,'MMM dd HH:mm:ss')}}"></td>
          <td th:text="${{log.username}}"></td>
          <td><code th:text="${{log.action}}"></code></td>
          <td th:text="${{log.entityType}}"></td>
          <td th:text="${{log.details}}"></td>
        </tr>
      </tbody>
    </table>
  </{E}>
</{E}>
""")

print("All templates generated.")
