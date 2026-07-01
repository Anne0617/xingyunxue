<template>
  <div class="checkpoint-game">
    <!-- Stars Background -->
    <div class="stars-bg">
      <div v-for="i in 50" :key="i" class="star" :style="starStyle(i)"></div>
    </div>

    <!-- Title -->
    <div class="game-header">
      <div class="game-badge">星学堂 &middot; 新员工闯关</div>
      <h1>{{ currentProgram?.name || "新员工培训闯关" }}</h1>
      <p class="game-subtitle">星学堂生活集团智慧培训平台</p>
      <div class="progress-text">
        <span class="progress-percent">{{ completedPercent }}%</span> 完成
      </div>
      <div class="progress-text-share">
        <button class="share-all-btn" v-if="displayNodes.some(n => n.employeeStatus == 'completed')" @click="showShareAll = true">📤 分享闯关进度</button>
      </div>
      <div class="progress-bar-track">
        <div class="progress-bar-fill" :style="{ width: completedPercent + '%' }"></div>
      </div>
    </div>

    <!-- Checkpoint Map -->
    <div v-if="showLogin" class="login-screen">
        <div class="login-card">
          <div class="login-logo">星学堂</div>
          <h2>新员工闯关打卡</h2>
          <p class="login-hint">请填写你的信息开始闯关打卡</p>
          <!-- list removed -->
          <div class="login-form">
            <div class="form-row double">
              <div class="form-field">
                <label>工号</label>
                <input type="text" v-model="formData.employee_id" placeholder="请输入工号" class="form-input" />
              </div>
              <div class="form-field">
                <label>姓名</label>
                <input type="text" v-model="formData.name" placeholder="请输入姓名" class="form-input" />
              </div>
            </div>
            <div class="form-row double">
              <div class="form-field">
                <label>电话</label>
                <input type="text" v-model="formData.phone" placeholder="请输入电话" class="form-input" />
              </div>
              <div class="form-field">
                <label>归属公司</label>
                <input type="text" v-model="formData.company" placeholder="请输入所属公司" class="form-input" />
              </div>
            </div>
            <div class="form-row double">
              <div class="form-field">
                <label>部门</label>
                <input type="text" v-model="formData.department" placeholder="请输入部门" class="form-input" />
              </div>
              <div class="form-field">
                <label>岗位</label>
                <input type="text" v-model="formData.position" placeholder="请输入岗位" class="form-input" />
              </div>
            </div>
            <button class="login-submit-btn" @click="submitLogin">{{ loginLoading ? '登录中...' : '进入闯关' }}</button>
            <div v-if="loginError" class="login-error">{{ loginError }}</div>
          </div>
          
        </div>
        <p class="login-footer">星学堂生活集团 &middot; 智慧培训平台</p>
      </div>

      <div class="node-track">
        <div v-for="(node, i) in displayNodes" :key="node.id" class="node-wrapper">
          <!-- Node -->
          <div class="node-card" :class="[node.node_type, node.employeeStatus]" @click="onNodeClick(node)">
            <div class="node-icon-ring">
              <div class="node-icon">
                <span v-if="node.node_type == 'checkin'" class="icon-emoji">📋</span>
                <span v-else-if="node.node_type == 'assessment'" class="icon-emoji">📝</span>
                <span v-else class="icon-emoji">📚</span>
              </div>
            </div>
            <div class="node-label">{{ node.name }}</div>
            <div class="node-badge" :class="node.node_type">
              {{ node.node_type == "checkin" ? "签到" : node.node_type == "assessment" ? "评估" : "考试" }}
            </div>
            <!-- Status Badge -->
            <div v-if="node.employeeStatus == 'completed'" class="status-badge done">
              <span class="done-icon">✓</span>
            </div>
            <div v-else-if="node.employeeStatus == 'current'" class="status-badge current">
              <span class="pulse-dot"></span>
              当前
            </div>
            <div v-else-if="node.employeeStatus == 'locked'" class="status-badge locked">
              🔒
            </div>
            <button v-if="node.employeeStatus == 'completed'" class="node-share-btn" @click.stop="openShare(node)" title="分享该节点">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
            </button>
            <div v-if="node.employeeStatus == 'completed'" class="node-share-row">
              <button class="node-share-link-btn" @click.stop="openShare(node)">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
                分享
              </button>
            </div>
          </div>
          <!-- Connector -->
          <div v-if="i < displayNodes.length - 1" class="node-connector" :class="{ active: i < completedNodes }">
            <div class="connector-line"></div>
            <div class="connector-arrow">▶</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Celebration Overlay -->
    <div v-if="showCelebration" class="celebration-overlay" @click="showCelebration = false">
      <div class="confetti-container">
        <div v-for="i in 80" :key="'c'+i" class="confetti-piece" :style="confettiStyle(i)"></div>
      </div>
      <div class="celebration-content">
        <div class="trophy">🏆</div>
        <h2>恭喜通关！</h2>
        <p>你已完成所有闯关节点</p>
        <div class="certificate-preview">
          <div class="cert-inner">
            <div class="cert-star">⭐</div>
            <div class="cert-title">闯关证书</div>
            <div class="cert-name">{{ currentProgram?.name || "新员工培训" }}</div>
            <div class="cert-line"></div>
            <div class="cert-desc">该学员已完成全部闯关任务</div>
            <img :src="getQRUrl('certificate', employeeProgram?.employee || 1)" alt="QR Code" class="cert-qr-img" />
            <p class="cert-share-hint">扫码查看完整学习档案</p>
            <button class="cert-share-btn" @click="openShare({ name: '通关证书', node_type: 'certificate' })">📤 分享证书</button>
          </div>
        </div>
        <button class="celebration-btn" @click="showCelebration = false">太棒了！</button>
      </div>
    </div>
</template>

<script>
export default {
  data() {
    return {
      programs: [],
      currentProgram: null,
      nodes: [],
      employeeProgress: [],
      showCelebration: false,
      shareModal: { show: false, type: '', typeLabel: '', qrUrl: '', linkUrl: '' },
      showShareAll: false,
      searchResults: [],
      searchLoading: false,
      employee: null,
      employeeProgram: null,
      completedNodes: 0,
      completedPercent: 0,
    };
  },
  computed: {
    displayNodes() {
      return this.nodes.map(node => {
        const prog = (this.employeeProgress || []).find(p => p.node == node.id);
        return { ...node, employeeStatus: prog ? prog.status : 'locked' };
      });
    },
  },
  async mounted() {
    // Load employee context
    const empId = this.getQueryParam('employee_id') || 1;
    await this.loadGame(empId);
  },
  methods: {
    getQueryParam(name) {
      const url = new URL(window.location.href);
      return url.searchParams.get(name);
    },
    async loadGame(empId) {
      try {
        const progsRes = await fetch('/api/programs/');
        const progs = await progsRes.json();
        this.programs = Array.isArray(progs) ? progs : progs.results || [];
        if (this.programs.length === 0) {
          this.currentProgram = { id: 0, name: "示例培训", description: "" };
          this.nodes = [
            { id: 1, name: "签到打卡", node_type: "checkin", order: 1 },
            { id: 2, name: "培训评估", node_type: "assessment", order: 2 },
            { id: 3, name: "结业考试", node_type: "exam", order: 3 },
          ];
          return;
        }
        this.currentProgram = this.programs[0];
        const params = '?program=' + this.currentProgram.id;
        const [nodesRes, progRes] = await Promise.all([
          fetch('/api/nodes/' + params),
          fetch('/api/employee-programs/?program=' + this.currentProgram.id + '&employee=' + empId),
        ]);
        const nodesData = await nodesRes.json();
        this.nodes = (Array.isArray(nodesData) ? nodesData : nodesData.results || []).sort((a,b) => a.order - b.order);
        const progData = await progRes.json();
        const arr = Array.isArray(progData) ? progData : progData.results || [];
        this.employeeProgram = arr[0];
        if (this.employeeProgram) {
          const cpRes = await fetch('/api/employee-checkpoints/?employee=' + empId);
          const cpData = await cpRes.json();
          this.employeeProgress = Array.isArray(cpData) ? cpData : cpData.results || [];
        }
        this.updateProgress();
      } catch(e) {
        console.error(e);
        this.nodes = [
          { id: 1, name: "签到打卡", node_type: "checkin", order: 1 },
          { id: 2, name: "培训评估", node_type: "assessment", order: 2 },
          { id: 3, name: "结业考试", node_type: "exam", order: 3 },
        ];
      }
    },
    updateProgress() {
      const completed = this.displayNodes.filter(n => n.employeeStatus == 'completed').length;
      this.completedNodes = completed;
      this.completedPercent = this.displayNodes.length > 0
        ? Math.round((completed / this.displayNodes.length) * 100) : 0;
    },
    onNodeClick(node) {
      if (node.employeeStatus == 'completed') return;
      if (node.employeeStatus == 'locked') return;
      if (!this.employeeProgram) return;
      const msg = node.node_type == 'checkin' ? '📋 请前往签到' : node.node_type == 'assessment' ? '📝 请填写评估问卷' : '📚 请参加考试';
      // For demo: simulate completing this node
      this.completeNode(node);
    },
    async completeNode(node) {
      if (!node || !this.employeeProgram) return;
      // Find the employee progress record
      const prog = (this.employeeProgress || []).find(p => p.node == node.id);
      if (prog && prog.status == 'current') {
        try {
          await fetch('/api/employee-checkpoints/' + prog.id + '/', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: 'completed' }),
          });
        } catch(e) {}
      }
      // Refresh
      await this.loadGame(this.employeeProgram?.employee || 1);
      // Check if all done
      if (this.displayNodes.every(n => n.employeeStatus == 'completed')) {
        setTimeout(() => { this.showCelebration = true; }, 300);
      }
    },
    openShare(node) {
        var types = { checkin: '签到记录', assessment: '评估记录', exam: '考试成绩', certificate: '通关证书' };
        var type = types[node.node_type] || node.node_type;
        this.shareModal = {
          show: true,
          typeLabel: type,
          qrUrl: this.getQRUrl(node.node_type, this.employeeProgram?.employee || 1),
          linkUrl: this.getShareLink(node.node_type, this.employeeProgram?.employee || 1),
        };
      },
      closeShare() { this.shareModal.show = false; },
      getQRUrl(typeId, empId) {
        var link = this.getShareLink(typeId, empId);
        return 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=' + encodeURIComponent(link);
      },
      getShareLink(typeId, empId) {
        var base = window.location.origin + '/?page=checkpoint&employee_id=' + empId;
        if (typeId == 'all') return base + '&view=progress';
        return base + '&share=' + typeId;
      },
      async copyShareLink() {
        try { await navigator.clipboard.writeText(this.shareModal.linkUrl); alert('链接已复制到剪贴板！'); }
        catch(e) { prompt('请手动复制链接：', this.shareModal.linkUrl); }
      },
      async copyShareAllLink() {
        var url = this.getShareLink('all', this.currentProgram?.id || 0);
        try { await navigator.clipboard.writeText(url); alert('链接已复制到剪贴板！'); }
        catch(e) { prompt('请手动复制链接：', url); }
      },
      submitLogin: async function() {
      var id = this.formData.employee_id;
      if (!id) { this.loginError = "请输入工号"; return; }
      this.loginLoading = true;
      this.loginError = "";
      try {
        var r = await fetch("/api/employees/?search=" + encodeURIComponent(id));
        var d = await r.json();
        var list = Array.isArray(d) ? d : d.results || [];
        var found = list.find(function(e) { return e.employee_id == id; });
        if (found) {
          window.location.href = "?page=checkpoint&employee_id=" + found.id;
        } else {
          this.loginError = "未找到对应员工，请联系管理员";
        }
      } catch(e) { this.loginError = "网络异常，请稍后重试"; }
      this.loginLoading = false;
    },
    starStyle(i) {
      const size = Math.random() * 3 + 1;
      return {
        left: Math.random() * 100 + '%',
        top: Math.random() * 100 + '%',
        width: size + 'px',
        height: size + 'px',
        animationDelay: Math.random() * 3 + 's',
        animationDuration: (Math.random() * 2 + 2) + 's',
      };
    },
    confettiStyle(i) {
      const colors = ['#c8102e','#f59e0b','#10b981','#3b82f6','#8b5cf6','#ec4899'];
      return {
        left: Math.random() * 100 + '%',
        backgroundColor: colors[i % colors.length],
        width: (Math.random() * 8 + 4) + 'px',
        height: (Math.random() * 12 + 6) + 'px',
        animationDelay: Math.random() * 2 + 's',
        animationDuration: (Math.random() * 3 + 2) + 's',
        transform: 'rotate(' + (Math.random() * 360) + 'deg)',
      };
    },
  },
};
</script>

<style scoped>
@keyframes twinkle {
  0%, 100% { opacity: 0.2; }
  50% { opacity: 1; }
}
@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.3); opacity: 0.7; }
}
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-6px); }
}
@keyframes connectorFlow {
  0% { background-position: 0 0; }
  100% { background-position: 20px 0; }
}
@keyframes confettiFall {
  0% { transform: translateY(-10vh) rotate(0deg); opacity: 1; }
  100% { transform: translateY(110vh) rotate(720deg); opacity: 0; }
}
@keyframes progressFill {
  from { width: 0; }
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.checkpoint-game {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
  position: relative;
  overflow: hidden;
  padding-bottom: 40px;
}
.stars-bg { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.star {
  position: absolute;
  background: #fff;
  border-radius: 50%;
  animation: twinkle 3s ease-in-out infinite;
}

.game-header {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 40px 20px 24px;
  background: linear-gradient(180deg, rgba(15,12,41,0.95) 0%, rgba(48,43,99,0.8) 100%);
  border-bottom: 1px solid rgba(255,255,255,0.1);
}
.game-badge {
  display: inline-block;
  background: linear-gradient(135deg, #f59e0b, #ef4444);
  color: #fff;
  padding: 4px 16px;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 2px;
  margin-bottom: 12px;
}
.game-header h1 {
  color: #fff;
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 12px;
}
.progress-text {
  color: rgba(255,255,255,0.7);
  font-size: 0.85rem;
  margin-bottom: 10px;
}
.progress-percent {
  color: #f59e0b;
  font-weight: 700;
  font-size: 1.1rem;
}
.progress-bar-track {
  max-width: 300px;
  margin: 0 auto;
  height: 6px;
  background: rgba(255,255,255,0.15);
  overflow: hidden;
}
.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #f59e0b, #ef4444);
  animation: progressFill 1s ease-out;
}

.checkpoint-scroll {
  position: relative;
  z-index: 1;
  max-width: 600px;
  margin: 0 auto;
  padding: 32px 20px;
}
.node-track { display: flex; flex-direction: column; align-items: center; gap: 0; }
.node-wrapper { display: flex; flex-direction: column; align-items: center; width: 100%; animation: slideUp 0.5s ease-out both; }
.node-wrapper:nth-child(1) { animation-delay: 0.1s; }
.node-wrapper:nth-child(2) { animation-delay: 0.2s; }
.node-wrapper:nth-child(3) { animation-delay: 0.3s; }
.node-wrapper:nth-child(4) { animation-delay: 0.4s; }
.node-wrapper:nth-child(5) { animation-delay: 0.5s; }
.node-wrapper:nth-child(6) { animation-delay: 0.6s; }
.node-wrapper:nth-child(7) { animation-delay: 0.7s; }
.node-wrapper:nth-child(8) { animation-delay: 0.8s; }

.node-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 32px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  max-width: 320px;
}
.node-card:not(.locked):hover {
  background: rgba(255,255,255,0.12);
  transform: translateY(-2px);
  border-color: rgba(255,255,255,0.25);
}
.node-card.locked { cursor: not-allowed; opacity: 0.5; }
.node-card.completed { border-color: rgba(16,185,129,0.4); background: rgba(16,185,129,0.08); }
.node-card.current { border-color: rgba(245,158,11,0.5); animation: float 2s ease-in-out infinite; }

.node-icon-ring {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
  background: rgba(255,255,255,0.08);
  transition: all 0.3s ease;
}
.node-card.completed .node-icon-ring { background: rgba(16,185,129,0.3); }
.node-card.current .node-icon-ring { background: rgba(245,158,11,0.3); }
.node-icon { font-size: 1.5rem; }
.node-label { font-size: 1rem; font-weight: 600; color: #fff; margin-bottom: 6px; }
.node-badge {
  font-size: 0.72rem;
  padding: 2px 10px;
  color: #fff;
  font-weight: 500;
}
.node-badge.checkin { background: #10b981; }
.node-badge.assessment { background: #f59e0b; }
.node-badge.exam { background: #3b82f6; }

.status-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
}
.status-badge.done { background: #10b981; animation: pulse 1s ease-in-out; }
.status-badge.current { background: #f59e0b; }
.status-badge.locked { background: rgba(255,255,255,0.15); font-size: 0.7rem; }
.done-icon { color: #fff; font-weight: 700; font-size: 0.85rem; }
.pulse-dot {
  width: 8px;
  height: 8px;
  background: #fff;
  border-radius: 50%;
  animation: pulse 1.5s ease-in-out infinite;
}

.node-connector {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4px 0;
  width: 2px;
}
.connector-line {
  width: 2px;
  height: 32px;
  background: rgba(255,255,255,0.15);
  transition: all 0.5s;
}
.node-share-btn { position: absolute; top: -8px; left: -8px; width: 26px; height: 26px; background: #3b82f6; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; color: #fff; z-index: 2; }
.node-share-btn:hover { background: #2563eb; }
.node-share-row { margin-top: 8px; }
.node-share-link-btn { background: rgba(59,130,246,0.2); border: 1px solid rgba(59,130,246,0.3); color: #93c5fd; cursor: pointer; font-size: 0.75rem; padding: 3px 10px; display: inline-flex; align-items: center; gap: 4px; font-family: inherit; }
.node-share-link-btn:hover { background: rgba(59,130,246,0.3); }
.share-overlay { position: fixed; inset: 0; z-index: 999; background: rgba(0,0,0,0.8); display: flex; align-items: center; justify-content: center; }
.share-modal { background: #1e1b4b; border: 1px solid rgba(255,255,255,0.15); padding: 32px; max-width: 380px; width: 90%; text-align: center; position: relative; }
.share-close { position: absolute; top: 12px; right: 14px; background: none; border: none; color: rgba(255,255,255,0.5); cursor: pointer; font-size: 1.5rem; }
.share-close:hover { color: #fff; }
.share-modal h3 { color: #fff; font-size: 1.1rem; margin-bottom: 20px; }
.share-qr-section { margin-bottom: 20px; }
.share-qr-img { width: 180px; height: 180px; border: 2px solid rgba(255,255,255,0.1); }
.share-link-section { text-align: left; }
.share-link-section label { color: rgba(255,255,255,0.6); font-size: 0.8rem; display: block; margin-bottom: 6px; }
.share-link-row { display: flex; gap: 8px; }
.share-link-input { flex: 1; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); padding: 8px 10px; color: #93c5fd; font-size: 0.78rem; font-family: inherit; }
.share-copy-btn { background: #3b82f6; color: #fff; border: none; padding: 8px 14px; font-size: 0.8rem; cursor: pointer; font-family: inherit; white-space: nowrap; }
.share-copy-btn:hover { background: #2563eb; }
.share-hint { color: rgba(255,255,255,0.4); font-size: 0.75rem; margin-top: 8px; }
.cert-qr-img { width: 100px; height: 100px; margin: 0 auto 8px; border: 1px solid #e5e7eb; display: block; }
.cert-share-hint { font-size: 0.72rem; color: #9ca3af; margin-bottom: 10px; }
.cert-share-btn { background: #c8102e; color: #fff; border: none; padding: 6px 20px; font-size: 0.8rem; cursor: pointer; font-family: inherit; }
.cert-share-btn:hover { background: #b0102a; }
.share-all-btn { background: rgba(59,130,246,0.15); border: 1px solid rgba(59,130,246,0.3); color: #93c5fd; cursor: pointer; font-size: 0.78rem; padding: 4px 14px; font-family: inherit; vertical-align: middle; }
.share-all-btn:hover { background: rgba(59,130,246,0.25); }

.login-screen { position: relative; z-index: 1; min-height: calc(100vh - 120px); display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
.login-card { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); padding: 40px 32px; max-width: 400px; width: 100%; text-align: center; }
.login-logo { font-size: 0.9rem; font-weight: 700; color: #c8102e; padding: 4px 14px; border: 1px solid #c8102e; display: inline-block; margin-bottom: 20px; }
.login-card h2 { color: #fff; font-size: 1.3rem; font-weight: 700; margin-bottom: 8px; }
.login-hint { color: rgba(255,255,255,0.5); font-size: 0.88rem; margin-bottom: 24px; }
.search-box { display: flex; gap: 8px; margin-bottom: 20px; }
.search-input { flex: 1; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); padding: 12px 14px; color: #fff; font-size: 0.95rem; font-family: inherit; outline: none; }
.search-input:focus { border-color: #c8102e; }
.search-input::placeholder { color: rgba(255,255,255,0.3); }
.search-btn { background: #c8102e; color: #fff; border: none; padding: 12px 20px; font-size: 0.9rem; font-weight: 600; cursor: pointer; font-family: inherit; white-space: nowrap; }
.search-btn:hover { background: #b0102a; }
.search-results { max-height: 260px; overflow-y: auto; }
.result-item { display: flex; align-items: center; gap: 14px; padding: 12px; cursor: pointer; border-bottom: 1px solid rgba(255,255,255,0.06); transition: background 0.2s; }
.result-item:hover { background: rgba(255,255,255,0.08); }
.result-avatar { width: 38px; height: 38px; background: #c8102e; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; font-weight: 700; flex-shrink: 0; }
.result-info { flex: 1; min-width: 0; text-align: left; }
.result-name { color: #fff; font-size: 0.95rem; font-weight: 600; }
.result-dept { color: rgba(255,255,255,0.4); font-size: 0.78rem; margin-top: 2px; }
.result-arrow { color: rgba(255,255,255,0.3); font-size: 0.7rem; }
.no-result { color: rgba(255,255,255,0.4); font-size: 0.85rem; padding: 20px 0; }
.login-form { margin-bottom: 20px; }
.form-row.double { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px; }
.form-field { display: flex; flex-direction: column; gap: 4px; text-align: left; }
.form-field label { color: rgba(255,255,255,0.5); font-size: 0.78rem; }
.form-input { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); padding: 10px 12px; color: #fff; font-size: 0.88rem; font-family: inherit; outline: none; }
.form-input:focus { border-color: #c8102e; }
.form-input::placeholder { color: rgba(255,255,255,0.25); font-size: 0.82rem; }
.login-submit-btn { background: #c8102e; color: #fff; border: none; padding: 12px; font-size: 1rem; font-weight: 600; cursor: pointer; font-family: inherit; width: 100%; margin-top: 8px; }
.login-submit-btn:hover { background: #b0102a; }
.login-error { color: #ef4444; font-size: 0.85rem; margin-top: 12px; }
.login-footer { color: rgba(255,255,255,0.25); font-size: 0.75rem; margin-top: 24px; text-align: center; }

.node-connector.active .connector-line {
  background: linear-gradient(180deg, #10b981, #f59e0b);
  background-size: 2px 20px;
  animation: connectorFlow 1s linear infinite;
}
.connector-arrow {
  color: rgba(255,255,255,0.3);
  font-size: 0.5rem;
  margin-top: 2px;
}

/* Celebration */
.celebration-overlay {
  position: fixed;
  inset: 0;
  z-index: 999;
  background: rgba(0,0,0,0.85);
  display: flex;
  align-items: center;
  justify-content: center;
}
.confetti-container { position: fixed; inset: 0; pointer-events: none; overflow: hidden; }
.confetti-piece {
  position: absolute;
  top: -20px;
  animation: confettiFall 4s ease-in forwards;
}
.celebration-content { text-align: center; padding: 40px; animation: slideUp 0.6s ease-out; }
.trophy { font-size: 4rem; margin-bottom: 16px; animation: pulse 1.5s ease-in-out infinite; }
.celebration-content h2 { color: #f59e0b; font-size: 2rem; font-weight: 700; margin-bottom: 8px; }
.celebration-content p { color: rgba(255,255,255,0.6); margin-bottom: 24px; }
.certificate-preview {
  background: #fff;
  padding: 24px;
  margin: 0 auto 24px;
  max-width: 280px;
}
.cert-inner { text-align: center; }
.cert-star { font-size: 2rem; margin-bottom: 8px; }
.cert-title { font-size: 1.2rem; font-weight: 700; color: #c8102e; margin-bottom: 4px; }
.cert-name { font-size: 0.95rem; color: #4b5563; margin-bottom: 12px; }
.cert-line { width: 60px; height: 2px; background: #c8102e; margin: 0 auto 12px; }
.cert-desc { font-size: 0.82rem; color: #9ca3af; margin-bottom: 12px; }
.cert-qr { width: 60px; height: 60px; background: #f3f4f6; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-size: 0.65rem; color: #9ca3af; }
.celebration-btn {
  background: linear-gradient(135deg, #f59e0b, #ef4444);
  color: #fff;
  border: none;
  padding: 12px 48px;
  font-size: 1.05rem;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
}
.celebration-btn:hover { opacity: 0.9; }
</style>
