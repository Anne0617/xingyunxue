/**
 * 星学堂数据对接层
 * ================
 * 将此文件引入 index.html（替换 app.js 中 localStorage 部分）
 * 实现：用户信息从星学堂获取 → 闯关数据提交到星学堂 → 排行榜从星学堂拉取
 * 
 * 配置：修改 API_BASE_URL 为星学堂实际地址
 */

const API_BASE = window.STAR_API_URL || "/api/star-course";
const TOKEN_KEY = "star_auth_token";

// ====== API 请求封装 ======
async function api(path, options = {}) {
  const token = localStorage.getItem(TOKEN_KEY);
  const res = await fetch(API_BASE + path, {
    headers: {
      "Content-Type": "application/json",
      "Authorization": token ? "Bearer " + token : "",
      ...options.headers,
    },
    ...options,
  });
  if (res.status === 401) {
    // token过期，跳转星学堂登录
    window.location.href = "/login?redirect=" + encodeURIComponent(window.location.href);
    throw new Error("未登录");
  }
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: "请求失败" }));
    throw new Error(err.error || "请求失败");
  }
  return res.json();
}

// ====== 用户信息 ======
async function fetchUserProfile() {
  const data = await api("/profile");
  return data; // { name, department, phone }
}

// ====== 闯关进度 ======
async function fetchProgress() {
  const data = await api("/progress");
  return data.days || {}; // { "d1": {score, hpLeft, answered, date}, ... }
}

async function submitProgress(day, score, hpLeft, answers) {
  return await api("/submit", {
    method: "POST",
    body: JSON.stringify({ day, score, hpLeft, answers }),
  });
}

// ====== 排行榜 ======
async function fetchLeaderboard() {
  return await api("/leaderboard"); // [{rank, name, department, daysDone, totalScore}]
}

// ====== 管理后台 ======
async function fetchOverdueList(deadlineDay) {
  return await api("/admin/overdue?deadlineDay=" + (deadlineDay || 5));
}

function getExportCsvUrl() {
  const token = localStorage.getItem(TOKEN_KEY);
  return API_BASE + "/admin/export?token=" + encodeURIComponent(token || "");
}

// ====== 集成模式下的 DB 替换层 ======
// 替换 app.js 中 DB 对象的功能，改为调用 API
const STAR_API = {
  getUser: async () => {
    try {
      const profile = await fetchUserProfile();
      // 同时从 localStorage 读取本地缓存的进度
      const cached = JSON.parse(localStorage.getItem("xa_user") || "{}");
      return { 
        name: profile.name, 
        dept: profile.department, 
        phone: profile.phone, 
        days: cached.days || {} 
      };
    } catch {
      // 离线回退：使用 localStorage
      return JSON.parse(localStorage.getItem("xa_user") || "{}");
    }
  },

  saveUser: (u) => {
    localStorage.setItem("xa_user", JSON.stringify(u));
  },

  getDay: async (day) => {
    try {
      const progress = await fetchProgress();
      const d = progress["d" + day];
      return { done: !!d, data: d || null };
    } catch {
      const u = JSON.parse(localStorage.getItem("xa_user") || "{}");
      return { done: !!u.days?.["d" + day], data: u.days?.["d" + day] || null };
    }
  },

  setDay: async (day, score, hpLeft, answered) => {
    // 提交到星学堂
    try {
      await submitProgress(day, score, hpLeft, answered);
    } catch (e) {
      console.warn("提交到星学堂失败，保存到本地:", e.message);
    }
    // 同时保存本地（离线容错）
    const u = JSON.parse(localStorage.getItem("xa_user") || "{}");
    if (!u.days) u.days = {};
    u.days["d" + day] = { score, hpLeft, answered, date: new Date().toISOString().slice(0, 10) };
    localStorage.setItem("xa_user", JSON.stringify(u));
  },

  getRank: async () => {
    try {
      return await fetchLeaderboard();
    } catch {
      return [];
    }
  },

  saveRank: async (name, dept, phone, day, score) => {
    // 排名由后端自动计算，前端不需要存储
    // 只提交闯关结果即可
    await STAR_API.setDay(day, score, 5, {});
  },

  // 管理后台
  getAdminData: async () => {
    return {
      leaderboard: await fetchLeaderboard(),
      overdue: await fetchOverdueList(5),
      exportUrl: getExportCsvUrl(),
    };
  },

  importPerson: (p) => {
    // 集成模式下不需要导入，数据已经在星学堂
    console.log("集成模式：数据在星学堂服务器，无需导入");
  },
};
