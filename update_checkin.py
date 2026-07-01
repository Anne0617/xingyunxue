import re
base = "D:/HuaweiMoveData/Users/Anna/Documents/星云学/星学堂"

# Read files
with open(base + "/star_course/checkin.html", "r", encoding="utf-8") as f:
    html = f.read()

with open(base + "/star_course/js/app.js", "r", encoding="utf-8") as f:
    app = f.read()

# === UPDATE checkin.html ===

# 1. Add admin nav button
nav_end = html.find("</nav>")
if nav_end > 0:
    btn = '<button class="nav-item" data-page="admin"><div class="nav-icon">📊</div><div class="nav-label">管理</div></button>\n  '
    last_btn = html.rfind("<button", 0, nav_end)
    if last_btn > 0:
        html = html[:last_btn] + btn + html[last_btn:]

# 2. Add admin modals before </body>
admin_modals = '''
<!-- Admin Login -->
<div class="modal-overlay" id="admin-login-modal">
  <div class="modal" style="text-align:left;max-width:380px">
    <h3 style="text-align:center;margin-bottom:12px">🔐 管理员登录</h3>
    <p style="text-align:center;color:#aab;font-size:12px;margin-bottom:16px">请输入密码查看数据</p>
    <input type="password" id="admin-pwd-input" placeholder="管理员密码" style="width:100%;padding:12px;border-radius:8px;border:1px solid rgba(255,255,255,.15);background:rgba(0,0,0,.3);color:#fff;font-size:15px;box-sizing:border-box;margin-bottom:8px">
    <div id="admin-pwd-error" style="color:#e74c3c;font-size:12px;margin-bottom:8px;display:none">密码错误</div>
    <button class="btn btn-gold modal-btn" style="width:100%" onclick="verifyAdminPassword()">验证登录</button>
    <button class="btn btn-ghost modal-btn" style="width:100%;margin-top:6px" onclick="closeModal('admin-login-modal')">取消</button>
  </div>
</div>
<!-- Admin Dashboard -->
<div class="modal-overlay" id="admin-data-modal">
  <div class="modal" style="text-align:left;max-width:520px;padding:24px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
      <h3 style="margin:0">📊 闯关数据管理</h3>
      <span style="font-size:10px;color:#666">星河智善 · 星途行动</span>
    </div>
    <div style="display:flex;gap:8px;margin-bottom:14px">
      <div style="flex:1;background:rgba(255,255,255,.06);border-radius:8px;padding:10px;text-align:center">
        <div style="font-size:20px;font-weight:900;color:#f0b429" id="admin-panel-users">0</div>
        <div style="font-size:10px;color:#889">参与人数</div>
      </div>
      <div style="flex:1;background:rgba(255,255,255,.06);border-radius:8px;padding:10px;text-align:center">
        <div style="font-size:20px;font-weight:900;color:#2ecc71" id="admin-panel-total">0</div>
        <div style="font-size:10px;color:#889">总通关任务</div>
      </div>
      <div style="flex:1;background:rgba(255,255,255,.06);border-radius:8px;padding:10px;text-align:center">
        <div style="font-size:20px;font-weight:900;color:#00bcd4" id="admin-panel-avg">0</div>
        <div style="font-size:10px;color:#889">平均积分</div>
      </div>
    </div>
    <div style="max-height:260px;overflow-y:auto;margin-bottom:12px;font-size:12px">
      <table style="width:100%;border-collapse:collapse" id="admin-data-table">
        <thead><tr style="border-bottom:1px solid rgba(255,255,255,.1)">
          <th style="padding:6px 4px;text-align:left;color:#f0b429">排名</th>
          <th style="padding:6px 4px;text-align:left;color:#f0b429">姓名</th>
          <th style="padding:6px 4px;text-align:center;color:#f0b429">通关数</th>
          <th style="padding:6px 4px;text-align:center;color:#f0b429">积分</th>
        </tr></thead>
        <tbody id="admin-data-tbody"></tbody>
      </table>
    </div>
    <div style="display:flex;gap:8px">
      <button class="btn btn-gold modal-btn" style="flex:1" onclick="exportAdminCSV()">📥 导出CSV</button>
      <button class="btn btn-ghost modal-btn" style="flex:1" onclick="closeModal('admin-data-modal')">关闭</button>
    </div>
  </div>
</div>
'''
body_close = html.find("</body>")
if body_close > 0:
    html = html[:body_close] + admin_modals + html[body_close:]

with open(base + "/star_course/checkin.html", "w", encoding="utf-8") as f:
    f.write(html)
print("checkin.html done")

# === UPDATE app.js ===

# Add admin functions at the end
admin_js = '''

// ==== 管理员面板 ====
function showAdminLogin() {
  document.getElementById("admin-pwd-input").value = "";
  document.getElementById("admin-pwd-error").style.display = "none";
  document.getElementById("admin-login-modal").classList.add("show");
}

function verifyAdminPassword() {
  var pwd = document.getElementById("admin-pwd-input").value.trim();
  if (!pwd) return;
  fetch(API_BASE + "/admin-verify/", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({password: pwd})
  }).then(function(r) {
    if (r.status === 200) {
      document.getElementById("admin-login-modal").classList.remove("show");
      loadAdminData();
    } else {
      document.getElementById("admin-pwd-error").style.display = "block";
    }
  }).catch(function() {
    document.getElementById("admin-pwd-error").style.display = "block";
  });
}

function loadAdminData() {
  fetch(API_BASE + "/leaderboard/")
    .then(function(r) { return r.json(); })
    .then(function(data) {
      renderAdminPanel(data);
      document.getElementById("admin-data-modal").classList.add("show");
    });
}

function renderAdminPanel(data) {
  document.getElementById("admin-panel-users").textContent = data.length;
  var total = 0, scores = 0;
  data.forEach(function(u) { total += u.daysDone; scores += u.totalScore; });
  document.getElementById("admin-panel-total").textContent = total;
  document.getElementById("admin-panel-avg").textContent = data.length ? Math.round(scores / data.length) : 0;

  var tbody = document.getElementById("admin-data-tbody");
  tbody.innerHTML = data.map(function(u, i) {
    var medal = i === 0 ? "👑" : i === 1 ? "🥈" : i === 2 ? "🥉" : "#" + (i + 1);
    return "<tr>" +
      '<td style="padding:5px 4px;border-bottom:1px solid rgba(255,255,255,.05)">' + medal + "</td>" +
      '<td style="padding:5px 4px;border-bottom:1px solid rgba(255,255,255,.05)">' + (u.name || "未知") + "</td>" +
      '<td style="padding:5px 4px;border-bottom:1px solid rgba(255,255,255,.05);text-align:center">' + u.daysDone + "</td>" +
      '<td style="padding:5px 4px;border-bottom:1px solid rgba(255,255,255,.05);text-align:center">' + u.totalScore + "</td>" +
      "</tr>";
  }).join("");
}

function exportAdminCSV() {
  var rows = document.querySelectorAll("#admin-data-tbody tr");
  if (!rows.length) return;
  var csv = "\\uFEFF排名,姓名,通关数,积分\\n";
  rows.forEach(function(r) {
    var cells = r.querySelectorAll("td");
    if (cells.length >= 4) csv += cells[0].textContent + "," + cells[1].textContent + "," + cells[2].textContent + "," + cells[3].textContent + "\\n";
  });
  var blob = new Blob([csv], {type: "text/csv;charset=utf-8"});
  var url = URL.createObjectURL(blob);
  var a = document.createElement("a");
  a.href = url; a.download = "xingxuetang_data.csv"; a.click();
  URL.revokeObjectURL(url);
}

// Handle admin nav click
document.addEventListener("DOMContentLoaded", function() {
  setTimeout(function() {
    var navs = document.querySelectorAll(".nav-item");
    navs.forEach(function(n) {
      if (n.dataset.page === "admin") {
        n.addEventListener("click", function() { showAdminLogin(); });
      }
    });
  }, 100);
});
'''

app += admin_js

with open(base + "/star_course/js/app.js", "w", encoding="utf-8") as f:
    f.write(app)
print("app.js done")

# === UPDATE views.py ===
with open(base + "/learning/views.py", "a", encoding="utf-8") as f:
    f.write('''

@api_view(["POST"])
@csrf_exempt
def api_checkin_admin_verify(request):
    """验证管理员密码（闯关页面内嵌管理面板用）"""
    from django.conf import settings
    pwd = request.data.get("password", "")
    expected = getattr(settings, "ADMIN_PANEL_PASSWORD", "admin123")
    if pwd == expected:
        return Response({"valid": True})
    return Response({"valid": False}, status=403)
''')
print("views.py done")

# === UPDATE urls.py ===
with open(base + "/learning/urls.py", "a", encoding="utf-8") as f:
    f.write('''
    path('checkin/admin-verify/', views.api_checkin_admin_verify, name='api_checkin_admin_verify'),
''')
print("urls.py done")

print("ALL DONE!")
