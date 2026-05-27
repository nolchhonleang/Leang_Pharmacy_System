from pathlib import Path

T = Path(__file__).resolve().parent.parent / "src" / "main" / "resources" / "templates"

HEAD = '<!DOCTYPE html>\n<html xmlns:th="http://www.thymeleaf.org" lang="en">\n'
HEAD += '<head th:replace="~{fragments/head :: head(${pageTitle})}"></head>\n<body>\n'
HEAD += '<div class="container-fluid"><div class="row">\n'
HEAD += '<nav th:replace="~{fragments/sidebar :: sidebar}"></nav>\n'
HEAD += '<main class="col-lg-10 col-md-9 main-content">\n'
HEAD += '<motion.div th:if="${success}" class="alert alert-success" th:text="${success}"></div>\n'
HEAD += '<div th:if="${error}" class="alert alert-danger" th:text="${error}"></div>\n'
HEAD = HEAD.replace("motion.div th:if", "div th:if")

TAIL = "\n</main></div></div>\n"
TAIL += '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>\n'
TAIL += "</body></html>\n"


def save(name, body):
    (T / name).parent.mkdir(parents=True, exist_ok=True)
    (T / name).write_text(HEAD + body + TAIL, encoding="utf-8")


save("medicines/list.html", '<h2 th:text="${pageTitle}"></h2><a href="/medicines/new" class="btn btn-accent mb-3">Add Medicine</a><div class="table-card table-responsive"><table class="table table-hover"><thead><tr><th>SKU</th><th>Name</th><th>Price</th><th></th></tr></thead><tbody><tr th:each="m : ${medicines}"><td th:text="${m.sku}"></td><td th:text="${m.name}"></td><td th:text="${m.unitPrice}"></td><td><a th:href="@{/medicines/{id}/edit(id=${m.id})}" class="btn btn-sm btn-outline-primary">Edit</a></td></tr></tbody></table></div>')

save("medicines/form.html", """<h2 th:text="${pageTitle}"></h2>
<form method="post" th:action="@{/medicines/save}" th:object="${medicine}">
<input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/>
<input type="hidden" th:field="*{id}"/>
<div class="row g-3">
<div class="col-md-4"><label>SKU</label><input class="form-control" th:field="*{sku}" required/></div>
<div class="col-md-8"><label>Name</label><input class="form-control" th:field="*{name}" required/></div>
<div class="col-md-4"><label>Category</label><select name="categoryId" class="form-select"><option th:each="c : ${categories}" th:value="${c.id}" th:text="${c.name}"></option></select></motion.div>
<div class="col-md-4"><label>Unit Price</label><input type="number" step="0.01" class="form-control" th:field="*{unitPrice}"/></div>
<div class="col-md-4"><label>Cost</label><input type="number" step="0.01" class="form-control" th:field="*{costPrice}"/></div>
<div class="col-md-4"><label>Reorder</label><input type="number" class="form-control" th:field="*{reorderLevel}"/></div>
<div class="col-12"><label><input type="checkbox" th:field="*{requiresPrescription}"/> Prescription required</label></div>
</div><button class="btn btn-accent mt-3">Save</button></form>""".replace("</motion.div>", "</div>").replace("<motion.div", "<div"))

save("stock/index.html", """<h2 th:text="${pageTitle}"></h2><a href="/stock/add" class="btn btn-accent mb-3">Receive Stock</a>
<div class="table-card table-responsive mb-4"><h5>Stock Overview</h5><table class="table table-sm"><thead><tr><th>SKU</th><th>Name</th><th>Qty</th><th>Reorder</th></tr></thead>
<tbody><tr th:each="s : ${overview}"><td th:text="${s.sku}"></td><td th:text="${s.name}"></td>
<td><span th:class="${s.lowStock} ? 'badge bg-danger' : 'badge bg-success'" th:text="${s.totalStock}"></span></td>
<td th:text="${s.reorderLevel}"></td></tr></tbody></table></div>
<div class="table-card"><h5>Expiring Soon</h5><table class="table table-sm"><tr th:each="b : ${expiring}">
<td th:text="${b.medicine.name}"></td><td th:text="${b.batchNumber}"></td><td th:text="${b.expiryDate}"></td><td th:text="${b.quantity}"></td></tr></table></div>""")

save("stock/add.html", """<h2 th:text="${pageTitle}"></h2><form method="post" th:action="@{/stock/add}">
<input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/>
<div class="row g-3">
<div class="col-md-6"><label>Medicine</label><select name="medicineId" class="form-select"><option th:each="m : ${medicines}" th:value="${m.id}" th:text="${m.name}"></option></select></div>
<div class="col-md-6"><label>Supplier</label><select name="supplierId" class="form-select"><option value="">--</option><option th:each="s : ${suppliers}" th:value="${s.id}" th:text="${s.name}"></option></select></div>
<div class="col-md-4"><label>Batch</label><input name="batchNumber" class="form-control" required/></div>
<div class="col-md-4"><label>Quantity</label><input name="quantity" type="number" class="form-control" required/></div>
<div class="col-md-4"><label>Expiry</label><input name="expiryDate" type="date" class="form-control" required/></div>
</div><button class="btn btn-accent mt-3">Add Batch</button></form>""")

save("pos/index.html", """<h2 th:text="${pageTitle}"></h2><form method="post" th:action="@{/pos/checkout}">
<input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/>
<div class="row g-3 mb-3">
<div class="col-md-4"><label>Customer</label><select name="customerId" class="form-select"><option value="">Walk-in</option><option th:each="c : ${customers}" th:value="${c.id}" th:text="${c.fullName}"></option></select></div>
<div class="col-md-4"><label>Payment</label><select name="paymentMethod" class="form-select"><option>CASH</option><option>CARD</option><option>INSURANCE</option></select></div>
<div class="col-md-4"><label>Discount</label><input name="discount" type="number" step="0.01" value="0" class="form-control"/></div>
</div>
<div class="table-card table-responsive"><table class="table"><thead><tr><th>Medicine</th><th>Price</th><th>Qty</th></tr></thead>
<tbody><tr th:each="m : ${medicines}"><td th:text="${m.name}"></td><td th:text="${m.unitPrice}"></td>
<td><input type="hidden" name="medicineId" th:value="${m.id}"/><input name="quantity" type="number" min="0" value="0" class="form-control form-control-sm" style="max-width:90px"/></td></tr></tbody></table></div>
<button class="btn btn-accent btn-lg mt-3">Complete Sale</button></form>""")

save("pos/history.html", """<h2 th:text="${pageTitle}"></h2><div class="table-card table-responsive"><table class="table"><thead><tr><th>Invoice</th><th>Total</th><th>Cashier</th><th>Date</th></tr></thead>
<tbody><tr th:each="s : ${sales}"><td th:text="${s.invoiceNumber}"></td><td th:text="${s.total}"></td><td th:text="${s.cashier.fullName}"></td>
<td th:text="${#temporals.format(s.soldAt,'yyyy-MM-dd HH:mm')}"></td></tr></tbody></table></div>""")

save("suppliers/list.html", """<h2 th:text="${pageTitle}"></h2><a href="/suppliers/new" class="btn btn-accent mb-3">Add Supplier</a>
<div class="table-card"><table class="table"><tr th:each="s : ${suppliers}"><td th:text="${s.name}"></td><td th:text="${s.phone}"></td><td th:text="${s.email}"></td>
<td><a th:href="@{/suppliers/{id}/edit(id=${s.id})}" class="btn btn-sm btn-outline-primary">Edit</a></td></tr></table></div>""")

save("suppliers/form.html", """<h2 th:text="${pageTitle}"></h2><form method="post" th:action="@{/suppliers/save}" th:object="${supplier}">
<input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/><input type="hidden" th:field="*{id}"/>
<div class="row g-3"><div class="col-md-6"><label>Name</label><input class="form-control" th:field="*{name}" required/></div>
<div class="col-md-6"><label>Phone</label><input class="form-control" th:field="*{phone}"/></div>
<div class="col-md-6"><label>Email</label><input class="form-control" th:field="*{email}"/></div>
<div class="col-12"><label>Address</label><textarea class="form-control" th:field="*{address}"></textarea></div></div>
<button class="btn btn-accent mt-3">Save</button></form>""")

save("customers/list.html", """<h2 th:text="${pageTitle}"></h2><a href="/customers/new" class="btn btn-accent mb-3">Add Customer</a>
<div class="table-card"><table class="table"><tr th:each="c : ${customers}"><td th:text="${c.fullName}"></td><td th:text="${c.phone}"></td><td th:text="${c.email}"></td></tr></table></div>""")

save("customers/form.html", """<h2 th:text="${pageTitle}"></h2><form method="post" th:action="@{/customers/save}" th:object="${customer}">
<input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/>
<div class="row g-3"><div class="col-md-6"><label>Full Name</label><input class="form-control" th:field="*{fullName}" required/></div>
<div class="col-md-6"><label>Phone</label><input class="form-control" th:field="*{phone}"/></div>
<div class="col-md-6"><label>Email</label><input class="form-control" th:field="*{email}"/></div>
<div class="col-12"><label>Allergies</label><textarea class="form-control" th:field="*{allergies}"></textarea></div></div>
<button class="btn btn-accent mt-3">Save</button></form>""")

save("prescriptions/list.html", """<h2 th:text="${pageTitle}"></h2><a href="/prescriptions/new" class="btn btn-accent mb-3">New Prescription</a>
<div class="table-card"><table class="table"><tr th:each="p : ${prescriptions}"><td th:text="${p.customer.fullName}"></td><td th:text="${p.doctorName}"></td>
<td th:text="${p.status}"></td><td><form th:if="${p.status.name() == 'PENDING'}" th:action="@{/prescriptions/{id}/dispense(id=${p.id})}" method="post" class="d-inline">
<input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/><button class="btn btn-sm btn-success">Dispense</button></form></td></tr></table></div>""")

save("prescriptions/form.html", """<h2 th:text="${pageTitle}"></h2><form method="post" th:action="@{/prescriptions/save}">
<input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/>
<div class="row g-3"><div class="col-md-6"><label>Customer</label><select name="customerId" class="form-select" required><option th:each="c : ${customers}" th:value="${c.id}" th:text="${c.fullName}"></option></select></div>
<div class="col-md-6"><label>Doctor</label><input name="doctorName" class="form-control" required/></div>
<div class="col-md-6"><label>Date</label><input name="prescribedDate" type="date" class="form-control" required/></div>
<div class="col-12"><label>Notes</label><textarea name="notes" class="form-control"></textarea></div></div>
<p class="mt-3 text-muted">Add line items on save (first medicine):</p>
<div class="row g-2"><div class="col-md-8"><select name="medicineId" class="form-select"><option th:each="m : ${medicines}" th:value="${m.id}" th:text="${m.name}"></option></select></div>
<div class="col-md-4"><input name="quantity" type="number" value="1" class="form-control"/></div></div>
<button class="btn btn-accent mt-3">Save Prescription</button></form>""")

save("purchases/list.html", """<h2 th:text="${pageTitle}"></h2><a href="/purchases/new" class="btn btn-accent mb-3">New Purchase Order</a>
<div class="table-card"><table class="table"><tr th:each="o : ${orders}"><td th:text="${o.orderNumber}"></td><td th:text="${o.supplier.name}"></td>
<td th:text="${o.status}"></td><td th:text="${o.totalAmount}"></td><td><a th:href="@{/purchases/{id}(id=${o.id})}">View</a></td></tr></table></motion.div>""".replace("</motion.div>", "</motion.div>").replace("motion.div", "motion.div").replace("</motion.div>", "</div>"))

save("purchases/new.html", """<h2 th:text="${pageTitle}"></h2><form method="post" th:action="@{/purchases/create}">
<input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/>
<div class="row g-3"><div class="col-md-6"><label>Supplier</label><select name="supplierId" class="form-select" required><option th:each="s : ${suppliers}" th:value="${s.id}" th:text="${s.name}"></option></select></div>
<div class="col-md-6"><label>Expected</label><input name="expectedDate" type="date" class="form-control"/></div></motion.div>
<button class="btn btn-accent mt-3">Create PO</button></form>""".replace("</motion.div>", "</div>").replace("<motion.div", "<div"))

save("purchases/detail.html", """<h2 th:text="${pageTitle}"></h2><p><strong th:text="${order.orderNumber}"></strong> - <span th:text="${order.status}"></span></p>
<form th:action="@{/purchases/{id}/receive(id=${order.id})}" method="post" class="mb-3" th:if="${order.status.name() != 'RECEIVED'}">
<input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/><button class="btn btn-success">Receive into Stock</button></form>
<form th:action="@{/purchases/{id}/add-item(id=${order.id})}" method="post" class="row g-2 mb-4">
<input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/>
<div class="col-md-5"><select name="medicineId" class="form-select"><option th:each="m : ${medicines}" th:value="${m.id}" th:text="${m.name}"></option></select></div>
<div class="col-md-2"><input name="quantity" type="number" class="form-control" placeholder="Qty"/></div>
<div class="col-md-3"><input name="unitCost" type="number" step="0.01" class="form-control" placeholder="Unit cost"/></div>
<div class="col-md-2"><button class="btn btn-accent">Add</button></div></form>
<table class="table"><tr th:each="i : ${order.items}"><td th:text="${i.medicine.name}"></td><td th:text="${i.quantity}"></td><td th:text="${i.unitCost}"></td></tr></table>""")

save("users/list.html", """<h2 th:text="${pageTitle}"></h2><a href="/users/new" class="btn btn-accent mb-3">Add User</a>
<div class="table-card"><table class="table"><tr th:each="u : ${users}"><td th:text="${u.username}"></td><td th:text="${u.fullName}"></td><td th:text="${u.role}"></td><td th:text="${u.active}"></td></tr></table></div>""")

save("users/form.html", """<h2 th:text="${pageTitle}"></h2><form method="post" th:action="@{/users/save}" th:object="${user}">
<input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/><input type="hidden" name="id" th:value="${user.id}"/>
<div class="row g-3"><div class="col-md-4"><label>Username</label><input class="form-control" th:field="*{username}" required/></div>
<div class="col-md-4"><label>Password</label><input name="password" type="password" class="form-control"/></div>
<div class="col-md-4"><label>Full Name</label><input class="form-control" th:field="*{fullName}" required/></div>
<div class="col-md-4"><label>Email</label><input class="form-control" th:field="*{email}"/></div>
<div class="col-md-4"><label>Role</label><select th:field="*{role}" class="form-select"><option th:each="r : ${roles}" th:value="${r}" th:text="${r}"></option></select></div>
<div class="col-md-4"><label><input type="checkbox" th:field="*{active}"/> Active</label></div></div>
<button class="btn btn-accent mt-3">Save</button></form>""")

save("reports/index.html", """<h2 th:text="${pageTitle}"></h2>
<div class="row g-3 mb-4"><div class="col-md-4"><div class="card p-3 stat-card">Today sales<br/><strong th:text="${stats.todaySales}"></strong></div></div>
<div class="col-md-4"><div class="card p-3 stat-card">Month sales<br/><strong th:text="${stats.monthSales}"></strong></div></div>
<div class="col-md-4"><div class="card p-3 stat-card danger">Low stock<br/><strong th:text="${stats.lowStockCount}"></strong></div></div></div>
<div class="table-card"><h5>Inventory</h5><table class="table table-sm"><tr th:each="s : ${stock}"><td th:text="${s.name}"></td><td th:text="${s.totalStock}"></td><td th:text="${s.unitPrice}"></td></tr></table></div>""")

save("audit/list.html", """<h2 th:text="${pageTitle}"></h2><div class="table-card table-responsive"><table class="table table-sm"><thead><tr><th>When</th><th>User</th><th>Action</th><th>Details</th></tr></thead>
<tbody><tr th:each="l : ${logs}"><td th:text="${#temporals.format(l.createdAt,'yyyy-MM-dd HH:mm')}"></td><td th:text="${l.username}"></td>
<td th:text="${l.action}"></td><td th:text="${l.details}"></td></tr></tbody></table></div>""")

save("categories/list.html", """<h2 th:text="${pageTitle}"></h2>
<form method="post" th:action="@{/categories/save}" class="row g-2 mb-4"><input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/>
<div class="col-md-4"><input name="name" class="form-control" placeholder="Name" required/></div>
<div class="col-md-4"><input name="description" class="form-control" placeholder="Description"/></div>
<div class="col-md-2"><button class="btn btn-accent">Add</button></div></form>
<div class="table-card"><table class="table"><tr th:each="c : ${categories}"><td th:text="${c.name}"></td><td th:text="${c.description}"></td></tr></table></div>""")

print("All templates generated")
