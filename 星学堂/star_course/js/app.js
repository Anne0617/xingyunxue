/** ===== 星途大冒险 · 核心游戏引擎 v2 ===== */

const APP = { userName: "", userDept: "", userPhone: "", currentPage: "home", currentDay: null, currentTab: "knowledge", answers: {}, answered: false, hp: 5, maxHp: 5, logoTaps: 0 };

const DB = {
  get(k, d) { try { const v = JSON.parse(localStorage.getItem("xa_" + k)); return v !== null ? v : d; } catch { return d; } },
  set(k, v) { localStorage.setItem("xa_" + k, JSON.stringify(v)); },
  getUser() { return DB.get("user", { name: "", dept: "", phone: "", days: {} }); },
  saveUser(u) { DB.set("user", u); },
  getDay(d) { const u = DB.getUser(); return { done: !!u.days["d" + d], data: u.days["d" + d] || null }; },
  setDay(d, score, hpLeft, answered) {
    const u = DB.getUser(); u.days["d" + d] = { score, hpLeft, answered, date: new Date().toISOString().slice(0, 10) }; DB.saveUser(u);
  },
  // 排行榜存储（按人）: { "姓名": { dept, phone, days: {"d1":5,...}, total: 99 } }
  getRank() { return DB.get("rank", {}); },
  saveRank(name, dept, phone, d, s) {
    const r = DB.getRank();
    if (!r[name]) r[name] = { dept, phone, days: {}, total: 0 };
    r[name].dept = dept; r[name].phone = phone;
    if (!r[name].days["d" + d]) { r[name].days["d" + d] = s; r[name].total += s; }
    DB.set("rank", r);
  },
  // 管理后台导入数据 { name, dept, phone, days:{"d1":5,...}, total }
  importPerson(p) { const r = DB.getRank(); r[p.name] = { dept: p.dept, phone: p.phone, days: p.days, total: p.total }; DB.set("rank", r); },
  clearRank() { DB.set("rank", {}); }
};

// ====== 截止日期系统 ======
const WEEK_DEADLINES = [
  { week: 1, endDate: "2026-06-26", label: "星火篇" },
  { week: 2, endDate: "2026-07-03", label: "破冰篇" },
  { week: 3, endDate: "2026-07-10", label: "智慧篇" },
  { week: 4, endDate: "2026-07-17", label: "超越篇" },
  { week: 5, endDate: "2026-07-24", label: "将帅篇" },
  { week: 6, endDate: "2026-07-31", label: "决胜篇" }
];

function getWeekDeadline(day) {
  const w = Math.ceil(day / 5);
  return WEEK_DEADLINES[w - 1] || WEEK_DEADLINES[5];
}

function isOverdue(day) {
  const dl = getWeekDeadline(day);
  return !DB.getDay(day).done && new Date() > new Date(dl.endDate);
}

function isDueSoon(day) {
  const dl = getWeekDeadline(day);
  const diff = Math.ceil((new Date(dl.endDate) - new Date()) / 86400000);
  return !DB.getDay(day).done && diff >= 0 && diff <= 2;
}
function createStars() {
  const c = document.querySelector(".adventure-bg");
  if (!c) return;
  for (let i = 0; i < 80; i++) {
    const s = document.createElement("div");
    s.className = "star";
    s.style.left = Math.random() * 100 + "%";
    s.style.top = Math.random() * 100 + "%";
    const sz = Math.random() * 2.5 + 0.5;
    s.style.width = sz + "px"; s.style.height = sz + "px";
    s.style.setProperty("--d", (Math.random() * 3 + 2) + "s");
    s.style.animationDelay = Math.random() * 5 + "s";
    c.appendChild(s);
  }
}

function showPage(id) {
  document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
  const el = document.getElementById("page-" + id);
  if (el) el.classList.add("active");
  APP.currentPage = id;
  document.querySelectorAll(".nav-item").forEach(n => n.classList.toggle("active", n.dataset.page === id));
}

function closeModal(id) { document.getElementById(id).classList.remove("show"); }

// ====== Home ======
function renderHome() {
  const u = DB.getUser();
  if (!u.name) { showNameModal(); return; }
  const days = DAYS_DATA;
  const done = days.filter(d => DB.getDay(d.day).done);
  const total = done.reduce((s, d) => s + (DB.getDay(d.day).data?.score || 0), 0);
  document.getElementById("stat-done").textContent = done.length;
  document.getElementById("stat-streak").textContent = total;
  document.getElementById("stat-score").textContent = done.length > 0 ? Math.round((done.length / days.length) * 100) + "%" : "0%";
  const pct = Math.round((done.length / days.length) * 100);
  document.getElementById("energy-pct").textContent = pct + "%";
  const fill = document.getElementById("energy-fill");
  fill.style.width = pct + "%";
  fill.className = "energy-fill" + (pct > 60 ? " high" : pct > 30 ? " medium" : " low");
  document.getElementById("energy-text").textContent = done.length + "/30 任务";
  document.getElementById("user-name").textContent = u.name + (u.dept ? " · " + u.dept : "");
  document.getElementById("user-avatar-text").textContent = u.name.charAt(0);
  renderMap();
}

// ====== Adventure map ======
function renderMap() {
  const days = DAYS_DATA;
  let html = "", lastEp = "";
  days.forEach((d, idx) => {
    const m = MISSION_CODENAMES[d.day - 1];
    if (!m) return;
    if (m.ep !== lastEp) {
      const icons = ["🔥", "💎", "⚡", "🏆", "👑", "🎯"];
      const epIdx = Math.ceil(d.day / 5) - 1;
      html += `<div class="episode-header"><span class="episode-icon">${icons[epIdx] || "⭐"}</span><span class="episode-name">${m.ep}</span><span class="episode-line"></span></div>`;
      lastEp = m.ep;
    }
    const done = DB.getDay(d.day).done;
    const prev = idx === 0 ? true : DB.getDay(days[idx - 1].day).done;
    const unlock = idx === 0 || prev;
    const overdue = !done && unlock && isOverdue(d.day);
    const dueSoon = !done && unlock && isDueSoon(d.day);
    const cls = done ? "done" : overdue ? "overdue" : unlock ? "active" : "locked";
    const stars = done && DB.getDay(d.day).data ? getStars(DB.getDay(d.day).data.score) : "";
    const statusText = done ? "✅ 通关" : overdue ? "🔴 逾期!" : dueSoon ? "⏰ 即将截止" : unlock ? "⚔️ 挑战" : "🔒";
    html += `<div class="mission-node ${cls}" onclick="openMission(${d.day})">
      <div class="path-line-wrap">${idx > 0 ? `<div class="path-line ${done || (unlock && idx > 0 && DB.getDay(days[idx-1].day).done) ? "done" : unlock ? "active" : ""}"></div>` : '<div style="min-height:10px"></div>'}
        <div class="mission-marker"><span class="day-num">${done ? "✓" : d.day}</span><span class="day-label">${done ? "通关" : "M" + String(d.day).padStart(2,"0")}</span></div>
      </div>
      <div class="mission-info">
        <div class="mission-code">${m.icon} ${m.code} · ${m.name}</div>
        <div class="mission-title">${d.title}</div>
        ${stars ? `<div class="mission-stars">${stars}</div>` : ""}
        <span class="mission-status-badge ${cls}">${statusText}</span>
      </div>
    </div>`;
  });
  document.getElementById("map-container").innerHTML = html;
}

function getStars(score) { return score >= 5 ? "⭐⭐⭐" : score >= 4 ? "⭐⭐" : "⭐"; }

// ====== Login ======
function showNameModal() { document.getElementById("name-modal").classList.add("show"); document.getElementById("input-name").focus(); }

function saveProfile() {
  const n = document.getElementById("input-name").value.trim();
  const d = document.getElementById("input-dept").value.trim();
  const p = document.getElementById("input-phone").value.trim();
  if (!n) { showToast("请输入姓名！"); return; }
  if (!d) { showToast("请输入部门名称！"); return; }
  const u = DB.getUser();
  u.name = n; u.dept = d; u.phone = p;
  DB.saveUser(u);
  document.getElementById("name-modal").classList.remove("show");
  renderHome();
}

// ====== Open mission ======
function openMission(day) {
  const u = DB.getUser();
  if (!u.name) { showNameModal(); return; }
  if (day > 1) { if (!DB.getDay(day - 1).done) { showToast("请先完成上一任务！"); return; } }
  showBriefing(day);
}

function showBriefing(day) {
  const d = DAYS_DATA[day - 1]; const m = MISSION_CODENAMES[day - 1];
  if (!d || !m) return;
  document.getElementById("b-icon").textContent = m.icon;
  document.getElementById("b-code").textContent = m.code;
  document.getElementById("b-title").innerHTML = `「<span class="highlight">${m.name}</span>」`;
  document.getElementById("b-desc").textContent = d.title + " · 阅读5条简报，通过5道挑战之门";
  document.getElementById("b-btn").onclick = () => { document.getElementById("briefing-overlay").classList.remove("show"); enterMission(day); };
  document.getElementById("briefing-overlay").classList.add("show");
}

function enterMission(day) {
  APP.currentDay = day; APP.answers = {}; APP.answered = false; APP.hp = 5;
  renderMission(day); showPage("detail");
}

function renderMission(day) {
  const d = DAYS_DATA[day - 1]; const m = MISSION_CODENAMES[day - 1];
  if (!d || !m) return;
  const done = DB.getDay(day).done;
  document.getElementById("detail-title").textContent = m.icon + " " + m.name;
  document.getElementById("detail-code").textContent = m.code + " · DAY " + day;
  let kh = "";
  d.knowledge.forEach((k, i) => { kh += `<div class="briefing-card" onclick="this.classList.toggle('read')"><div class="briefing-label">📋 简报 ${i+1}/5</div><div class="briefing-text">${k}</div></div>`; });
  document.getElementById("briefing-list").innerHTML = kh;
  let qz = `<div class="challenge-header-info">⚔️ 你有 ${"❤️".repeat(APP.maxHp)} 条命，答错扣命！至少答对 4 题通关</div><div class="hp-display" id="hp-display">${drawHp()}</div>`;
  d.questions.forEach((q, qi) => {
    qz += `<div class="gate-card" id="gate-${qi}"><div class="gate-header"><div class="gate-number">🚩 挑战 ${qi+1}/5</div><div class="gate-text">${q.question}</div></div>
      <div class="gate-options" data-q="${qi}">${q.options.map((o, oi) => `<div class="gate-option" data-q="${qi}" data-opt="${oi}" onclick="pickOption(${qi},${oi})"><div class="option-letter">${"ABCD"[oi]}</div><span>${o}</span></div>`).join("")}</div></div>`;
  });
  document.getElementById("challenge-content").innerHTML = qz;
  if (done) {
    const data = DB.getDay(day).data;
    if (data.score >= 4) {
      APP.answered = true; APP.hp = data.hpLeft || 0;
      if (data.answered) Object.entries(data.answered).forEach(([qi, ai]) => {
        APP.answers[qi] = ai;
        document.querySelectorAll(`.gate-option[data-q="${qi}"]`).forEach(o => { o.classList.add("disabled"); const oi = parseInt(o.dataset.opt); if (oi === d.questions[qi].correctIndex) o.classList.add("correct"); if (oi === ai && ai !== d.questions[qi].correctIndex) o.classList.add("wrong"); if (oi === ai) o.classList.add("selected"); });
      });
      document.getElementById("hp-display").innerHTML = drawHp();
      document.getElementById("submit-btn").textContent = "✅ 已通关 — 查看成绩"; document.getElementById("submit-btn").disabled = true;
    } else {
      APP.answered = false; APP.hp = 5;
      document.getElementById("hp-display").innerHTML = drawHp();
      document.getElementById("submit-btn").textContent = "⚔️ 再试一次（上次" + data.score + "/5）"; document.getElementById("submit-btn").disabled = false;
    }
  } else {
    document.getElementById("submit-btn").textContent = "⚔️ 提交挑战"; document.getElementById("submit-btn").disabled = false;
  }
}

function drawHp() { let h = ""; for (let i = 0; i < APP.maxHp; i++) h += `<span class="${i < APP.hp ? "" : "lost"}">❤️</span>`; return h; }

function pickOption(qi, oi) {
  if (APP.answered) return;
  document.querySelectorAll(`.gate-option[data-q="${qi}"]`).forEach(o => o.classList.remove("selected"));
  document.querySelectorAll(`.gate-option[data-q="${qi}"][data-opt="${oi}"]`).forEach(o => o.classList.add("selected"));
  APP.answers[qi] = oi;
}


// Submit score to server
function submitScoreToServer(day, score, hpLeft, answers) {
    var name = DB.get('name', '');
    var dept = DB.get('department', '');
    fetch('/api/checkin/submit/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            name: name,
            department: dept,
            day: day,
            score: score,
            hpLeft: hpLeft,
            answers: answers
        })
    }).then(function(r) { return r.json(); })
    .then(function(d) {
        if (d.success) {
            console.log('Day ' + day + ' submitted to server');
        }
    }).catch(function(e) {
        console.error('Submit failed:', e);
    });
}

function submitChallenge() {
  if (APP.answered) { const data = DB.getDay(APP.currentDay).data; if (data) { showResult(APP.currentDay, data.score, data.hpLeft, data.answered); return; } return; }
  const d = DAYS_DATA[APP.currentDay - 1]; if (!d) return;
  for (let i = 0; i < d.questions.length; i++) { if (APP.answers[i] === undefined) { showToast("请完成所有挑战之门！"); return; } }
  let correct = 0; let hp = 5; const answered = {};
  d.questions.forEach((q, qi) => {
    answered[qi] = APP.answers[qi]; const isCorrect = APP.answers[qi] === q.correctIndex;
    if (isCorrect) correct++; else hp--;
    document.querySelectorAll(`.gate-option[data-q="${qi}"]`).forEach(o => { o.classList.add("disabled"); const oi = parseInt(o.dataset.opt); if (oi === q.correctIndex) o.classList.add("correct"); if (oi === APP.answers[qi] && oi !== q.correctIndex) o.classList.add("wrong"); if (oi === APP.answers[qi]) o.classList.add("selected"); });
    const card = document.getElementById("gate-" + qi); if (card) card.classList.add(isCorrect ? "correct" : "wrong");
  });
  APP.hp = Math.max(0, hp); APP.correctCount = correct; APP.answered = true;
  document.getElementById("hp-display").innerHTML = drawHp();
  if (correct >= 4) {
    const u = DB.getUser();
    DB.setDay(APP.currentDay, correct, APP.hp, answered);
    DB.saveRank(u.name, u.dept, u.phone, APP.currentDay, correct);
  }
  showResult(APP.currentDay, correct, APP.hp, answered);
}

function showResult(day, correct, hpLeft, answered) {
  const d = DAYS_DATA[day - 1]; if (!d) return;
  const passed = correct >= 4; const stars = getStars(correct);
  document.getElementById("result-icon").textContent = passed ? "🎉" : "💪";
  document.getElementById("result-title").textContent = passed ? "🎊 任务通关！" : "😤 再接再厉！";
  document.getElementById("result-stars").textContent = stars;
  document.getElementById("result-score-big").textContent = correct + "/5";
  document.getElementById("result-hp").textContent = "❤️".repeat(hpLeft) + "🖤".repeat(5 - hpLeft);
  document.getElementById("result-detail").innerHTML = passed ? `精英！通过了「${MISSION_CODENAMES[day-1].name}」！<br>剩余 ${hpLeft} 条命，${stars}` : `只答对 ${correct} 题（至少需4题），再战！`;
  const overlay = document.getElementById("result-overlay"); overlay.classList.add("show");
  const btn = document.getElementById("result-btn");
  if (passed) {
    btn.textContent = "🗺️ 返回闯关版图"; btn.className = "btn btn-success";
    btn.onclick = () => { overlay.classList.remove("show"); renderHome(); showPage("home"); };
  } else {
    btn.textContent = "🔄 再试一次"; btn.className = "btn btn-gold";
    btn.onclick = () => { overlay.classList.remove("show"); enterMission(day); };
  }
}

// ====== Tab ======
function switchTab(t) {
  APP.currentTab = t || "knowledge";
  document.querySelectorAll(".tab").forEach(el => el.classList.toggle("active", el.dataset.tab === t));
  document.querySelectorAll(".tab-content").forEach(el => el.classList.toggle("active", el.id === "tab-" + t));
}



// ====== 荣誉榜 ======
function renderLeaderboard() {
  const r = DB.getRank();
  const sorted = Object.entries(r).map(([n, d]) => ({ n, dept: d.dept || "", phone: d.phone || "", s: d.total || 0, c: Object.keys(d.days || {}).length })).sort((a, b) => b.s - a.s || b.c - a.c);
  const topN = Math.min(sorted.length, 10);
  const c = document.getElementById("rank-list");
  if (!sorted.length) {
    c.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-muted)">暂无排行<br><span style="font-size:10px">完成冒险后自动上榜，或点击上方上报</span></div>';
    return;
  }
  c.innerHTML = sorted.slice(0, 10).map((u, i) => `<div class="rank-card">
    <div class="rank-num">${i === 0 ? "👑" : i === 1 ? "🥈" : i === 2 ? "🥉" : "#" + (i + 1)}</div>
    <div class="rank-avatar">${u.n.charAt(0)}</div>
    <div class="rank-info">
      <div class="rank-name">${u.n}</div>
      <div class="rank-stat">${u.dept || "(未填部门)"} · 通关 ${u.c} 任务 · ${u.s} 积分</div>
    </div>
    <div class="rank-score">${u.s}</div>
  </div>`).join("");
  if (sorted.length > 10) c.innerHTML += `<div style="text-align:center;font-size:10px;color:var(--text-muted);padding:8px">...仅显示前10名</div>`;
}

// ====== 管理后台 ======
let logoTimer = null;
function onLogoTap() {
  APP.logoTaps++;
  if (logoTimer) clearTimeout(logoTimer);
  logoTimer = setTimeout(() => { APP.logoTaps = 0; }, 3000);
  if (APP.logoTaps >= 5) {
    APP.logoTaps = 0;
    document.getElementById("admin-entry").style.display = "block";
    showToast("🔐 管理入口已开启");
  }
}

function showAdminPanel() {
  const r = DB.getRank();
  const entries = Object.entries(r);
  document.getElementById("admin-users").textContent = entries.length;
  let totalDays = 0; let totalPossible = entries.length * 30;
  entries.forEach(([n, d]) => { totalDays += Object.keys(d.days || {}).length; });
  document.getElementById("admin-total-done").textContent = totalDays;
  document.getElementById("admin-avg").textContent = totalPossible > 0 ? Math.round((totalDays / totalPossible) * 100) + "%" : "0%";

  const list = document.getElementById("admin-list");
  if (!entries.length) {
    list.innerHTML = '<div style="text-align:center;color:var(--text-muted);padding:12px">暂无数据，请导入成员上报的进度</div>';
  } else {
    list.innerHTML = entries.map(([n, d]) => `<div style="display:flex;justify-content:space-between;padding:6px 8px;border-bottom:1px solid rgba(255,255,255,0.04);font-size:11px">
      <span><strong>${n}</strong> ${d.dept ? "· " + d.dept : ""}</span>
      <span style="color:var(--gold)">${d.total || 0}分 · ${Object.keys(d.days || {}).length}关</span>
    </div>`).join("");
  }
  document.getElementById("admin-modal").classList.add("show");
}

function importData() {
  const text = document.getElementById("import-text").value.trim();
  if (!text) { showToast("请粘贴要导入的数据"); return; }
  try {
    const data = JSON.parse(text);
    // Support single person object or array of persons
    const persons = Array.isArray(data) ? data : [data];
    persons.forEach(p => { if (p.name) DB.importPerson(p); });
    document.getElementById("import-text").value = "";
    showToast("✅ 成功导入 " + persons.length + " 人数据");
    showAdminPanel(); // Refresh
  } catch (e) {
    showToast("❌ 数据格式错误，请检查");
  }
}

function exportCSV() {
  const r = DB.getRank();
  const entries = Object.entries(r);
  if (!entries.length) { showToast("暂无数据可导出"); return; }
  // Build CSV
  const headers = ["姓名", "部门", "联系方式", "总积分", "通关数"];
  for (let i = 1; i <= 30; i++) headers.push("第" + i + "关");
  let csv = headers.join(",") + "\n";
  entries.forEach(([n, d]) => {
    const row = [n, d.dept || "", d.phone || "", d.total || 0, Object.keys(d.days || {}).length];
    for (let i = 1; i <= 30; i++) row.push(d.days && d.days["d" + i] !== undefined ? d.days["d" + i] : "");
    csv += row.join(",") + "\n";
  });
  const blob = new Blob(["\uFEFF" + csv], { type: "text/csv;charset=utf-8" }); // BOM for Excel
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a"); a.href = url; a.download = "星河智善_十五五数据_" + new Date().toISOString().slice(0, 10) + ".csv";
  a.click(); URL.revokeObjectURL(url);
  showToast("✅ CSV已导出");
}

// ====== Toast ======
function showToast(msg) {
  const old = document.querySelector(".toast"); if (old) old.remove();
  const t = document.createElement("div"); t.className = "toast"; t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => { t.style.opacity = "0"; t.style.transition = "opacity 0.3s"; setTimeout(() => t.remove(), 300); }, 2500);
}

// ====== Init ======
document.addEventListener("DOMContentLoaded", () => {
  createStars();
  const u = DB.getUser();
  if (u.name) {
    document.getElementById("user-name").textContent = u.name + (u.dept ? " · " + u.dept : "");
    document.getElementById("user-avatar-text").textContent = u.name.charAt(0);
    renderHome();
  } else { showNameModal(); renderHome(); }

  document.querySelectorAll(".nav-item").forEach(n => {
    n.addEventListener("click", () => {
      const p = n.dataset.page;
      if (p === "home") { renderHome(); showPage("home"); }
      else if (p === "leaderboard") { renderLeaderboard(); showPage("leaderboard"); }
    });
  });
  document.getElementById("back-btn").addEventListener("click", () => { renderHome(); showPage("home"); });
});



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
      var individual = data.individual || data;
      renderAdminPanel(individual);
      renderDeptPanel(data.department || []);
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


function renderDeptPanel(deptData) {
  var html = "<h4 style=\"margin:16px 0 8px;color:var(--gold)\">\\u90E8\\u95E8\\u6392\\u884C</h4>";
  html += "<table class=\"admin-table\"><thead><tr><th>\\u6392\\u540D</th><th>\\u90E8\\u95E8</th><th>\\u603B\\u79EF\\u5206</th><th>\\u4EBA\\u6570</th><th>\\u5E73\\u5747\\u5206</th></tr></thead><tbody>";
  deptData.forEach(function(d) {
    var avg = d.userCount > 0 ? (d.totalScore / d.userCount).toFixed(1) : 0;
    html += "<tr><td>" + d.rank + "</td><td>" + d.department + "</td><td>" + d.totalScore + "</td><td>" + d.userCount + "</td><td>" + avg + "</td></tr>";
  });
  html += "</tbody></table>";
  var container = document.getElementById("dept-ranking");
  if (!container) {
    container = document.createElement("div");
    container.id = "dept-ranking";
    document.getElementById("admin-data-modal").querySelector(".modal-content").appendChild(container);
  }
  container.innerHTML = html;
}

function exportAdminCSV() {
  var rows = document.querySelectorAll("#admin-data-tbody tr");
  if (!rows.length) return;
  var csv = "\uFEFF排名,姓名,通关数,积分\n";
  rows.forEach(function(r) {
    var cells = r.querySelectorAll("td");
    if (cells.length >= 4) csv += cells[0].textContent + "," + cells[1].textContent + "," + cells[2].textContent + "," + cells[3].textContent + "\n";
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
