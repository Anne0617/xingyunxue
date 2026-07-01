<script setup>
import { ref } from "vue";

const announcements = ref([]);
async function loadAnnouncements() {
  try {
    const r = await fetch('/api/announcements/');
    if (r.ok) announcements.value = await r.json();
  } catch(e) { /* ignore */ }
}
loadAnnouncements();
const emit = defineEmits(["open-admin-login"]);



const capabilities = [
  { title: "打卡闯关", desc: "双模式打卡闯关体系\u2014\u2014新员工入职闯关一人一套地图、终身复用；专项培训打卡每场独立新建、模板复用。完成全部节点解锁可视化学习地图，自动生成带个人专属二维码的通关电子证书。" },
  { title: "智能教学", desc: "数字人讲师授课、基于错题的个性化学习方案、管理员在线陪练、学习过程实时咨询指导。标准化学习闭环：签到→课件观看→培训评估→线上考试，全流程自动化管理。" },
  { title: "考试管理", desc: "独立题库应用支持多题型管理，线上考试模块支持上万人批量推送、统一打卡考核。智能组卷、自动阅卷、数据统计，大幅提升考试组织效率。" },
  { title: "台账管控", desc: "学员培训记录台账、培训费用成本台账、全员资质证书台账全覆盖。支持Excel批量导入导出、证书到期预警，双层分级权限确保总部/片区数据隔离。" },
  { title: "双证书中心", desc: "内部结业证书与国家职业资格证书双体系管理，个人专属二维码证书可保存图片、分享展示。扫码直达个人学习档案，资质管理全程数字化。" },
];

const downloads = [
  { name: "员工操作手册", desc: "普通员工使用指南，含闯关打卡、考试、证书查看", icon: "\uD83D\uDCC4" },
  { name: "管理员操作手册", desc: "管理员后台操作指南，含培训配置、考试管理、台账导出", icon: "\uD83D\uDCC4" },
  { name: "员工导入模板", desc: "批量导入参训员工名单的Excel模板", icon: "\uD83D\uDCC1" },
  { name: "台账导出模板", desc: "培训台账、费用台账、证书台账的统一导出格式模板", icon: "\uD83D\uDCC1" },
];
</script>

<template>
  <div class="home-page">
    <!-- Hero Banner -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">集团智慧培训<br /><span class="hero-accent">一站式解决方案</span></h1>
        <p class="hero-subtitle">星学堂为星河智善生活集团人力行政中心自研的集团内部私有化数字化培训管理平台，面向全体员工、HR管理人员、分公司管理员及总部超级管理员，<br />实现闯关打卡、在线学习、考试评估、台账管控的全流程数字化管理。数据内网私有化存储不外流，符合集团数据安全规范。</p>
        <div class="hero-actions">
          <a href="/exam/0f8d1f9a-d379-4604-a33d-7dfe4d17f741/" class="btn-employee">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 18h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" stroke-linecap="round" stroke-linejoin="round" /></svg>
            员工微信H5学习入口
          </a>
          <a href="#" class="btn-admin" @click.prevent="emit('open-admin-login')">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" stroke-linecap="round" stroke-linejoin="round" /></svg>
            HR PC管理后台登录
          </a>
        </div>
      </div>
    </section>

    <!-- Stats -->
    <section class="stats-section">
      <div class="stats-grid">
        <div class="stat-item" v-for="s in stats" :key="s.label">
          <div class="stat-value">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </div>
      </div>
    </section>

    <!-- Core Capabilities -->
    <section class="caps-section">
      <div class="section-header">
        <h2>五大核心能力</h2>
        <p>覆盖集团培训全场景的模块化功能矩阵，灵活配置，按需启用。</p>
      </div>
      <div class="caps-grid">
        <div class="cap-card" v-for="c in capabilities" :key="c.title">
          <h3>{{ c.title }}</h3>
          <p>{{ c.desc }}</p>
        </div>
      </div>
    </section>

    <!-- Dual-end Display -->
    <section class="dual-section">
      <div class="section-header">
        <h2>双端协同</h2>
        <p>员工微信H5小程序 + PC 管理后台，两端数据实时同步，满足不同角色使用场景。</p>
      </div>
      <div class="dual-grid">
        <div class="dual-card">
          <div class="dual-badge">员工移动端</div>
          <h3>微信H5学习入口</h3>
          <p>员工通过集团微信即可进入学习，无需额外安装APP，随时随地碎片化学习。</p>
          <ul>
            <li>闯关打卡与进度追踪</li>
            <li>课程在线学习与评估</li>
            <li>在线考试与成绩查询</li>
            <li>双证书中心查看与管理</li>
          </ul>
        </div>
        <div class="dual-card">
          <div class="dual-badge dual-badge-blue">PC管理后台</div>
          <h3>集团管理平台</h3>
          <p>管理员通过PC端后台进行培训全流程管理与数据分析。</p>
          <ul>
            <li>培训项目创建与闯关配置</li>
            <li>题库管理与考试推送</li>
            <li>三大台账管理与数据导出</li>
            <li>培训成本统计与权限管控</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- Download Area -->
    <section class="download-section">
      <div class="section-header">
        <h2>内部资料下载</h2>
        <p>操作手册、导入模板、台账模板，方便各分公司管理员下载使用。</p>
      </div>
      <div class="download-grid">
        <div class="download-card" v-for="d in downloads" :key="d.name">
          <div class="download-icon">{{ d.icon }}</div>
          <div class="download-info">
            <h3>{{ d.name }}</h3>
            <p>{{ d.desc }}</p>
          </div>
          <span class="download-tag">下载</span>
        </div>
      </div>
    </section>

    <!-- Announcements -->
    <section class="announce-section">
      <div class="section-header">
        <h2>系统公告</h2>
        <p>平台最新动态与运维通知。</p>
      </div>
      <div class="announce-list">
        <div class="announce-item" v-for="a in announcements" :key="a.date">
          <span class="announce-date">{{ a.date }}</span>
          <span class="announce-title">{{ a.title }}</span>
        </div>
      </div>
    </section>

    <!-- Internal Downloads -->
    <section class="download-section">
      <div class="section-header">
        <h2>内部资料下载</h2>
        <p class="section-desc">签到表、评估表、考试试卷导入模板，供管理员下载使用。</p>
      </div>
      <div class="download-grid">
        <a href="/api/download/签到表模板.xlsx" class="download-item">
          <div class="download-icon">📄</div>
          <h3>签到表模板</h3>
          <p>培训签到记录表，支持批量导入</p>
          <span class="download-link">下载模板</span>
        </a>
        <a href="/api/download/培训评估表模板.xlsx" class="download-item">
          <div class="download-icon">📋</div>
          <h3>培训评估表模板</h3>
          <p>学员培训效果评估问卷模板</p>
          <span class="download-link">下载模板</span>
        </a>
        <a href="/api/download/考试试卷导入模板.xlsx" class="download-item">
          <div class="download-icon">📝</div>
          <h3>考试试卷导入模板</h3>
          <p>批量导入试题与试卷数据模板</p>
          <span class="download-link">下载模板</span>
        </a>
      </div>
    </section>

    <!-- Achievements Badge -->
    <section class="badge-section">
      <div class="badge-content">
        <div class="badge-icon">★</div>
        <h2>星云通关达人</h2>
        <p class="badge-desc">三关学习全部完成，文化通识考试满分通关！解锁星河新人完整成长地图，开启职场新旅程。</p>
        <div class="badge-rules">
          <div class="rule-item">
            <div class="rule-num">第一关</div>
            <div class="rule-text">入职闯关学习</div>
          </div>
          <div class="rule-arrow">→</div>
          <div class="rule-item">
            <div class="rule-num">第二关</div>
            <div class="rule-text">文化通识考试</div>
          </div>
          <div class="rule-arrow">→</div>
          <div class="rule-item">
            <div class="rule-num">第三关</div>
            <div class="rule-text">满分通关</div>
          </div>
          <div class="rule-arrow">→</div>
          <div class="rule-item">
            <div class="rule-num">★</div>
            <div class="rule-text bold">星云通关达人</div>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<style scoped>
.hero { padding: 60px 24px 48px; text-align: left; border-bottom: 1px solid #e5e7eb; }
.hero-content { max-width: 800px; }
.hero-title { font-size: 2.4rem; font-weight: 700; line-height: 1.3; margin-bottom: 16px; color: #111827; }
.hero-accent { color: #c8102e; }
.hero-subtitle { font-size: 1rem; color: #6b7280; line-height: 1.8; max-width: 640px; margin: 0 0 32px; }
.hero-actions { display: flex; gap: 16px; flex-wrap: wrap; }
.btn-employee { display: inline-flex; align-items: center; gap: 8px; border: 1px solid #d1d5db; color: #374151; padding: 10px 22px; font-size: 0.93rem; font-weight: 500; }
.btn-employee:hover { border-color: #c8102e; color: #c8102e; }
.btn-admin { display: inline-flex; align-items: center; gap: 8px; background: #c8102e; color: #fff; padding: 10px 24px; font-size: 0.95rem; font-weight: 500; }
.btn-admin:hover { background: #b0102a; }

.stats-section { padding: 40px 24px; background: #f9fafb; border-bottom: 1px solid #e5e7eb; }
.stats-grid { max-width: 900px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
.stat-item { text-align: left; }
.stat-value { font-size: 2rem; font-weight: 700; color: #c8102e; }
.stat-label { font-size: 0.9rem; color: #6b7280; margin-top: 4px; }

.section-header { text-align: left; margin-bottom: 32px; }
.section-header h2 { font-size: 1.5rem; font-weight: 700; margin-bottom: 8px; color: #111827; }
.section-header p { color: #6b7280; max-width: 600px; line-height: 1.7; font-size: 0.95rem; }

.caps-section { padding: 60px 24px; border-bottom: 1px solid #e5e7eb; }
.caps-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 20px; max-width: 1100px; }
.cap-card { padding: 28px 20px; border: 1px solid #e5e7eb; }
.cap-card h3 { font-size: 1rem; font-weight: 600; margin-bottom: 10px; color: #111827; }
.cap-card p { font-size: 0.85rem; color: #6b7280; line-height: 1.7; }

.dual-section { padding: 60px 24px; border-bottom: 1px solid #e5e7eb; }
.dual-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; max-width: 900px; }
.dual-card { padding: 32px; border: 1px solid #e5e7eb; }
.dual-badge { display: inline-block; background: #c8102e; color: #fff; padding: 3px 10px; font-size: 0.78rem; margin-bottom: 14px; }
.dual-badge-blue { background: #2563eb; }
.dual-card h3 { font-size: 1.1rem; font-weight: 600; margin-bottom: 8px; color: #111827; }
.dual-card > p { font-size: 0.9rem; color: #6b7280; line-height: 1.6; margin-bottom: 16px; }
.dual-card ul { list-style: none; padding: 0; }
.dual-card ul li { position: relative; padding: 5px 0 5px 16px; font-size: 0.88rem; color: #4b5563; }
.dual-card ul li::before { content: ""; position: absolute; left: 0; top: 12px; width: 5px; height: 5px; background: #c8102e; }

.download-section { padding: 60px 24px; border-bottom: 1px solid #e5e7eb; }
.download-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; max-width: 700px; }
.download-card { display: flex; align-items: center; gap: 16px; padding: 20px; border: 1px solid #e5e7eb; }
.download-icon { font-size: 1.5rem; flex-shrink: 0; }
.download-info { flex: 1; min-width: 0; }
.download-info h3 { font-size: 0.95rem; font-weight: 600; color: #111827; margin-bottom: 4px; }
.download-info p { font-size: 0.82rem; color: #9ca3af; line-height: 1.5; }
.download-tag { flex-shrink: 0; border: 1px solid #c8102e; color: #c8102e; padding: 3px 12px; font-size: 0.8rem; cursor: default; }

.announce-section { padding: 60px 24px; background: #f9fafb; }
.announce-list { max-width: 700px; }
.announce-item { display: flex; gap: 16px; padding: 12px 0; border-bottom: 1px solid #e5e7eb; }
.announce-date { color: #9ca3af; font-size: 0.85rem; white-space: nowrap; flex-shrink: 0; }
.announce-title { color: #374151; font-size: 0.92rem; }
.announce-item:hover .announce-title { color: #c8102e; }

/* Download Section */
.download-section { padding: 60px 24px; border-top: 1px solid #e5e7eb; }
.download-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; max-width: 900px; margin: 0; }
.download-item { border: 1px solid #e5e7eb; padding: 24px; }
.download-item:hover { border-color: #c8102e; }
.download-icon { font-size: 1.8rem; margin-bottom: 8px; }
.download-item h3 { font-size: 1rem; font-weight: 600; color: #111827; margin-bottom: 6px; }
.download-item p { font-size: 0.85rem; color: #6b7280; margin-bottom: 12px; }
.download-link { font-size: 0.85rem; color: #c8102e; font-weight: 500; }

/* Badge Section */
.badge-section { padding: 60px 24px; background: #f9fafb; border-top: 1px solid #e5e7eb; }
.badge-content { max-width: 800px; margin: 0; }
.badge-icon { font-size: 2.5rem; margin-bottom: 12px; }
.badge-content h2 { font-size: 1.4rem; font-weight: 700; color: #111827; margin-bottom: 8px; }
.badge-desc { color: #6b7280; line-height: 1.7; font-size: 0.93rem; margin-bottom: 24px; max-width: 600px; }
.badge-rules { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
.rule-item { text-align: center; }
.rule-num { font-size: 0.9rem; font-weight: 700; color: #c8102e; margin-bottom: 4px; }
.rule-text { font-size: 0.85rem; color: #4b5563; }
.rule-text.bold { color: #c8102e; font-weight: 600; }
.rule-arrow { font-size: 1.2rem; color: #d1d5db; }

@media (max-width: 768px) {
  .hero-title { font-size: 1.6rem; }
  .stats-grid, .caps-grid { grid-template-columns: repeat(2, 1fr); }
  .dual-grid, .download-grid { grid-template-columns: 1fr; }
}
@media (max-width: 480px) { .caps-grid { grid-template-columns: 1fr; } }
</style>





