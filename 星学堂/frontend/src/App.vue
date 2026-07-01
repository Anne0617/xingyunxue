<script setup>
import { ref } from "vue";
import "./style.css";
import HomePage from "./views/HomePage.vue";
import FeaturesPage from "./views/FeaturesPage.vue";
import GuidePage from "./views/GuidePage.vue";
import FAQPage from "./views/FAQPage.vue";
import AboutPage from "./views/AboutPage.vue";
import CheckpointGame from "./views/CheckpointGame.vue";

const navItems = [
  { key: "home", label: "首页" },
  { key: "checkin", label: "闯关入口" },
  { key: "features", label: "系统功能" },
  { key: "guide", label: "使用手册" },
  { key: "faq", label: "常见问题" },
  { key: "about", label: "关于我们" },
];

const currentPage = ref("home");
const showLoginModal = ref(false);
const loginForm = ref({ username: "", password: "" });
const loginError = ref("");
const loggingIn = ref(false);

function navigate(key) {
  if (key === "checkin") { window.location.href = "/checkin/"; return; }
  currentPage.value = key;
  window.scrollTo({ top: 0 });
}

function openAdminLogin() {
  loginForm.value = { username: "", password: "" };
  loginError.value = "";
  showLoginModal.value = true;
}
async function handleLogin() {
  if (loggingIn.value) return;
  loggingIn.value = true;
  loginError.value = "";
  try {
    const r = await fetch("/api/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(loginForm.value),
    });
    const d = await r.json();
    if (d.success) { window.location.href = d.redirect; }
    else { loginError.value = d.message || "登录失败"; }
  } catch(e) { loginError.value = "网络错误，请稍后重试"; }
  finally { loggingIn.value = false; }
}

// Check URL params for direct page access
const urlParams = new URLSearchParams(window.location.search);
const pageParam = urlParams.get("page");
if (pageParam === "checkpoint") {
  currentPage.value = "checkpoint";
}
</script>

<template>
  <div class="app-layout">
    <header class="navbar" v-if="currentPage !== 'checkpoint'">
      <div class="navbar-inner">
        <div class="logo" @click="navigate('home')">
          <svg width="32" height="32" viewBox="0 0 72 72" fill="none" class="logo-icon">
            <path d="M10 52 C18 52 32 46 40 34 C48 22 54 10 56 4 C58 -2 62 -2 64 4 C66 10 64 18 58 26 C52 34 44 38 40 36 C36 34 36 28 40 22 C44 16 50 14 54 16" stroke="#c8102e" stroke-width="5" stroke-linecap="round" fill="none" />
            <path d="M44 42 C48 42 56 38 62 30 C68 22 70 14 70 8" stroke="#c8102e" stroke-width="3" stroke-linecap="round" fill="none" />
            <circle cx="68" cy="5" r="2.5" fill="#c8102e" />
          </svg>
          <span class="logo-text">星学堂</span>
        </div>
        <nav class="nav-links">
          <button v-for="item in navItems" :key="item.key" class="nav-btn" :class="{ active: currentPage === item.key }" @click="navigate(item.key)">{{ item.label }}</button>
        </nav>
        <button class="nav-login-btn" @click="openAdminLogin">管理员登录</button>
      </div>
    </header>

    <main class="main-content">
      <CheckpointGame v-if="currentPage === 'checkpoint'" />
      <HomePage v-else-if="currentPage === 'home'" @open-admin-login="openAdminLogin" />
      <FeaturesPage v-else-if="currentPage === 'features'" />
      <GuidePage v-else-if="currentPage === 'guide'" />
      <FAQPage v-else-if="currentPage === 'faq'" />
      <AboutPage v-else-if="currentPage === 'about'" />
    </main>

    <footer class="footer" v-if="currentPage !== 'checkpoint'">
      <div class="footer-inner">
        <div class="footer-col footer-brand">
          <div class="footer-logo">
            <svg width="20" height="20" viewBox="0 0 72 72" fill="none" class="footer-logo-icon">
              <path d="M10 52 C18 52 32 46 40 34 C48 22 54 10 56 4 C58 -2 62 -2 64 4 C66 10 64 18 58 26 C52 34 44 38 40 36 C36 34 36 28 40 22 C44 16 50 14 54 16" stroke="#c8102e" stroke-width="5" stroke-linecap="round" fill="none" />
              <path d="M44 42 C48 42 56 38 62 30 C68 22 70 14 70 8" stroke="#c8102e" stroke-width="3" stroke-linecap="round" fill="none" />
              <circle cx="68" cy="5" r="2.5" fill="#c8102e" />
            </svg>
            星学堂
          </div>
          <p class="footer-desc">集团智慧培训平台，用技术驱动人才培育。</p>
        </div>
        <div class="footer-col">
          <h4>功能</h4>
          <a href="#" @click.prevent="navigate('features')">系统功能</a>
          <a href="#" @click.prevent="navigate('guide')">使用手册</a>
          <a href="#" @click.prevent="navigate('faq')">常见问题</a>
        </div>
        <div class="footer-col"><h4>支持</h4><a href="#">帮助中心</a><a href="#">API 文档</a><a href="#">服务状态</a></div>
        <div class="footer-col"><h4>关于</h4><a href="#" @click.prevent="navigate('about')">关于我们</a><a href="#">隐私政策</a><a href="#">服务条款</a></div>
      </div>
      <div class="footer-bottom"><p>&copy; 2026 星学堂 &middot; 集团培训管理系统 &middot; All rights reserved.</p></div>
    </footer>

    <!-- Login Modal -->
    <div class="modal-overlay" v-if="showLoginModal" @click.self="showLoginModal = false">
      <div class="modal-box">
        <button class="modal-close" @click="showLoginModal = false">&times;</button>
        <div class="modal-header"><h2>管理员登录</h2><p class="modal-sub">HR / 分公司管理员身份验证</p></div>
        <div class="modal-body">
          <div class="form-group"><label>用户名</label><input type="text" class="form-input" placeholder="请输入用户名" v-model="loginForm.username" /></div>
          <div class="form-group"><label>密码</label><input type="password" class="form-input" placeholder="请输入密码" v-model="loginForm.password" /></div>
          <button class="modal-submit" @click="handleLogin">{{ loggingIn ? "登录中..." : "登 录" }}</button>
          <div class="modal-login-error" v-if="loginError">{{ loginError }}</div><a href="#" class="modal-forgot">忘记密码？请联系内部运维</a>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans SC", "PingFang SC", sans-serif; background: #ffffff; color: #1f2937; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
a { color: inherit; text-decoration: none; }
button { font-family: inherit; }

.navbar { position: sticky; top: 0; z-index: 100; background: #ffffff; border-bottom: 1px solid #e5e7eb; }
.navbar-inner { max-width: 1100px; margin: 0; display: flex; align-items: center; justify-content: space-between; padding: 0 24px; height: 60px; }
.logo { cursor: pointer; user-select: none; display: flex; align-items: center; gap: 6px; }
.logo-text { font-size: 1.2rem; font-weight: 700; color: #c8102e; letter-spacing: 2px; }
.nav-links { display: flex; gap: 2px; }
.nav-btn { background: none; border: none; color: #6b7280; font-size: 0.9rem; padding: 8px 16px; cursor: pointer; }
.nav-btn:hover { color: #c8102e; }
.nav-btn.active { color: #c8102e; font-weight: 600; }
.nav-login-btn { background: none; border: 1px solid #c8102e; color: #c8102e; padding: 6px 14px; font-size: 0.85rem; font-family: inherit; cursor: pointer; margin-right: 8px; white-space: nowrap; }
.nav-login-btn:hover { background: #fff5f5; }
.main-content { min-height: calc(100vh - 60px - 280px); }
.page-header { text-align: left; padding: 48px 24px 40px; border-bottom: 1px solid #e5e7eb; margin-bottom: 40px; }
.page-header h1 { font-size: 1.8rem; font-weight: 700; color: #111827; margin-bottom: 8px; }
.page-header p { color: #6b7280; max-width: 560px; line-height: 1.7; }
.page-container { max-width: 900px; margin: 0; padding: 0 24px 80px; }

.footer { background: #f9fafb; border-top: 1px solid #e5e7eb; padding: 48px 24px 0; }
.footer-inner { max-width: 1100px; margin: 0; display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 40px; padding-bottom: 32px; }
.footer-logo { font-size: 1.1rem; font-weight: 700; margin-bottom: 8px; color: #c8102e; letter-spacing: 2px; }
.footer-desc { color: #9ca3af; font-size: 0.88rem; line-height: 1.6; }
.footer-col h4 { font-size: 0.85rem; font-weight: 600; color: #6b7280; margin-bottom: 12px; letter-spacing: 0.06em; }
.footer-col a { display: block; color: #9ca3af; font-size: 0.88rem; padding: 4px 0; }
.footer-col a:hover { color: #c8102e; }
.footer-bottom { border-top: 1px solid #e5e7eb; padding: 16px 24px; text-align: left; color: #9ca3af; font-size: 0.82rem; }

.modal-overlay { position: fixed; inset: 0; z-index: 200; background: rgba(0,0,0,0.45); display: flex; align-items: center; justify-content: flex-start; padding: 24px; }
.modal-box { background: #ffffff; border: 1px solid #e5e7eb; width: 100%; max-width: 380px; padding: 36px 32px 28px; position: relative; }
.modal-close { position: absolute; top: 12px; right: 14px; background: none; border: none; color: #9ca3af; cursor: pointer; font-size: 1.5rem; line-height: 1; }
.modal-close:hover { color: #c8102e; }
.modal-header { text-align: left; margin-bottom: 28px; }
.modal-header h2 { font-size: 1.2rem; font-weight: 700; color: #111827; margin-bottom: 4px; }
.modal-sub { font-size: 0.85rem; color: #9ca3af; }
.modal-body { display: flex; flex-direction: column; gap: 20px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 0.85rem; color: #6b7280; font-weight: 500; }
.form-input { background: #f9fafb; border: 1px solid #d1d5db; padding: 10px 12px; font-size: 0.92rem; color: #1f2937; font-family: inherit; outline: none; }
.form-input:focus { border-color: #c8102e; }
.modal-submit { background: #c8102e; color: #fff; border: none; padding: 12px; font-size: 1rem; font-weight: 600; cursor: pointer; font-family: inherit; letter-spacing: 4px; margin-top: 4px; }
.modal-submit:hover { background: #b0102a; }
.modal-forgot { text-align: left; font-size: 0.82rem; color: #9ca3af; }
.modal-forgot:hover { color: #c8102e; }

@media (max-width: 768px) { .nav-links { gap: 0; } .nav-btn { padding: 8px 10px; font-size: 0.8rem; } .nav-login-btn { display: none; } .footer-inner { grid-template-columns: 1fr 1fr; } }
</style>

