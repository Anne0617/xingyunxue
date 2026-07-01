<template>
  <div class="training-admin">
    <!-- Stats Overview -->
    <div class="stats-row">
      <div class="stat-card" v-for="s in stats" :key="s.label">
        <div class="stat-num">{{ s.value }}</div>
        <div class="stat-label">{{ s.label }}</div>
      </div>
    </div>

    <!-- Program Selector -->
    <div class="section-header">
      <h2>培训项目</h2>
      <div class="program-tabs">
        <button v-for="p in programs" :key="p.id" class="program-tab" :class="{ active: currentProgram?.id === p.id }" @click="selectProgram(p)">
          {{ p.name }}
        </button>
      </div>
    </div>

    <!-- Checkpoint Map -->
    <div v-if="currentProgram" class="checkpoint-map">
      <div class="map-title">{{ currentProgram.name }} — 闯关地图</div>
      <div class="node-track">
        <div v-for="(node, i) in checkpointNodes" :key="node.id" class="node-item" :class="node.node_type">
          <div class="node-icon-wrap">
            <div class="node-icon">
              <span v-if="node.node_type == 'checkin'" class="icon-text">&#x1F4CB;</span>
              <span v-else-if="node.node_type == 'assessment'" class="icon-text">&#x1F4DD;</span>
              <span v-else class="icon-text">&#x1F4DA;</span>
            </div>
            <div v-if="i < checkpointNodes.length - 1" class="node-connector"></div>
          </div>
          <div class="node-info">
            <div class="node-name">{{ node.name }}</div>
            <div class="node-type-badge">{{ node.node_type == 'checkin' ? '签到' : node.node_type == 'assessment' ? '评估' : '考试' }}</div>
            <div v-if="node.checkin_date" class="node-meta">{{ node.checkin_date }} {{ node.location }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Employee Progress -->
    <div v-if="currentProgram && participantCount > 0" class="progress-section">
      <h2>员工闯关进度</h2>
      <div class="progress-table-wrap">
        <table class="progress-table">
          <thead>
            <tr>
              <th>员工</th>
              <th>公司</th>
              <th>状态</th>
              <th v-for="n in checkpointNodes" :key="'h-'+n.id" class="node-col">{{ n.name }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ep in employeeProgress" :key="ep.employee_id">
              <td class="emp-cell">{{ ep.employee_name }}</td>
              <td>{{ ep.company }}</td>
              <td>
                <span class="status-badge" :class="ep.status">{{ ep.status == 'completed' ? '已完成' : ep.status == 'in_progress' ? '进行中' : '未开始' }}</span>
              </td>
              <td v-for="n in checkpointNodes" :key="'c-'+n.id" class="node-col">
                <span v-if="getNodeStatus(ep, n)" class="node-status" :class="getNodeStatus(ep, n)">
                  {{ getNodeStatus(ep, n) == 'completed' ? '✓' : getNodeStatus(ep, n) == 'current' ? '→' : '🔒' }}
                </span>
                <span v-else class="node-status locked">🔒</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="!currentProgram" class="empty-state">
      <div class="empty-icon">&#x1F4CB;</div>
      <p>请先创建一个培训项目，然后配置闯关节点</p>
      <p class="empty-hint">管理后台 → 培训闯关管理 → 培训项目</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      programs: [],
      currentProgram: null,
      checkpointNodes: [],
      employeeProgress: [],
      stats: [
        { label: '培训项目', value: '0' },
        { label: '闯关节点', value: '0' },
        { label: '参与员工', value: '0' },
        { label: '已完成', value: '0' },
      ],
    };
  },
  computed: {
    participantCount() {
      return this.employeeProgress.length;
    },
  },
  async mounted() {
    await this.loadPrograms();
  },
  methods: {
    async loadPrograms() {
      try {
        const r = await fetch('/api/programs/');
        const d = await r.json();
        this.programs = Array.isArray(d) ? d : d.results || [];
        this.stats[0].value = String(this.programs.length);
        if (this.programs.length > 0) {
          await this.selectProgram(this.programs[0]);
        }
      } catch (e) {
        console.error('Failed to load programs', e);
      }
    },
    async selectProgram(p) {
      this.currentProgram = p;
      this.checkpointNodes = [];
      this.employeeProgress = [];
      try {
        const [nodesRes, progressRes] = await Promise.all([
          fetch('/api/nodes/?program=' + p.id),
          fetch('/api/employee-progress/?program=' + p.id),
        ]);
        const nodesData = await nodesRes.json();
        this.checkpointNodes = (Array.isArray(nodesData) ? nodesData : nodesData.results || []).sort((a,b) => a.order - b.order);
        this.stats[1].value = String(this.checkpointNodes.length);
      } catch (e) {
        console.error('Failed to load nodes', e);
      }
      try {
        const r = await fetch('/api/employee-programs/?program=' + p.id);
        const d = await r.json();
        const eps = Array.isArray(d) ? d : d.results || [];
        const detailReqs = eps.map(ep =>
          fetch('/api/employees/' + ep.employee + '/').then(r => r.json()).catch(() => ({}))
        );
        const empDetails = await Promise.all(detailReqs);
        this.employeeProgress = eps.map((ep, i) => ({
          ...ep,
          employee_name: empDetails[i]?.name || '未知',
          company: empDetails[i]?.company || '',
        }));
        this.stats[2].value = String(this.employeeProgress.length);
        this.stats[3].value = String(this.employeeProgress.filter(ep => ep.status == 'completed').length);
      } catch (e) {
        console.error('Failed to load progress', e);
      }
    },
    getNodeStatus(ep, node) {
      const cp = ep.checkpoints || [];
      const found = cp.find(c => c.node == node.id);
      return found ? found.status : null;
    },
  },
};
</script>

<style scoped>
.training-admin { max-width: 1100px; margin: 0; padding: 32px 24px 80px; }
.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px; }
.stat-card { background: #fff; border: 1px solid #e5e7eb; padding: 20px; text-align: center; }
.stat-num { font-size: 2rem; font-weight: 700; color: #c8102e; }
.stat-label { font-size: 0.85rem; color: #6b7280; margin-top: 4px; }
.section-header { display: flex; align-items: center; gap: 24px; margin-bottom: 20px; }
.section-header h2 { font-size: 1.2rem; font-weight: 700; color: #111; margin: 0; white-space: nowrap; }
.program-tabs { display: flex; gap: 8px; flex-wrap: wrap; }
.program-tab { background: #f3f4f6; border: 1px solid transparent; padding: 6px 16px; font-size: 0.85rem; cursor: pointer; color: #6b7280; font-family: inherit; }
.program-tab:hover { border-color: #c8102e; color: #c8102e; }
.program-tab.active { background: #c8102e; color: #fff; border-color: #c8102e; }
.checkpoint-map { background: #f9fafb; border: 1px solid #e5e7eb; padding: 28px; margin-bottom: 32px; }
.map-title { font-size: 1rem; font-weight: 600; color: #111; margin-bottom: 20px; }
.node-track { display: flex; flex-direction: column; gap: 0; }
.node-item { display: flex; align-items: flex-start; gap: 16px; position: relative; padding: 12px 0; }
.node-icon-wrap { display: flex; flex-direction: column; align-items: center; flex-shrink: 0; }
.node-icon { width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; background: #fff; border: 2px solid #e5e7eb; }
.node-item.checkin .node-icon { border-color: #10b981; }
.node-item.assessment .node-icon { border-color: #f59e0b; }
.node-item.exam .node-icon { border-color: #3b82f6; }
.node-connector { width: 2px; height: 24px; background: #d1d5db; }
.node-info { padding-top: 8px; }
.node-name { font-size: 0.95rem; font-weight: 600; color: #111; }
.node-type-badge { display: inline-block; font-size: 0.75rem; padding: 1px 8px; margin-top: 4px; color: #fff; border-radius: 2px; }
.node-item.checkin .node-type-badge { background: #10b981; }
.node-item.assessment .node-type-badge { background: #f59e0b; }
.node-item.exam .node-type-badge { background: #3b82f6; }
.node-meta { font-size: 0.8rem; color: #9ca3af; margin-top: 4px; }
.progress-section { margin-bottom: 32px; }
.progress-section h2 { font-size: 1.2rem; font-weight: 700; margin-bottom: 16px; color: #111; }
.progress-table-wrap { overflow-x: auto; border: 1px solid #e5e7eb; }
.progress-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.progress-table th, .progress-table td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #e5e7eb; white-space: nowrap; }
.progress-table th { background: #f9fafb; color: #6b7280; font-weight: 600; }
.progress-table tbody tr:hover { background: #f9fafb; }
.node-col { text-align: center !important; min-width: 40px; }
.emp-cell { font-weight: 500; color: #111; }
.status-badge { display: inline-block; padding: 2px 8px; font-size: 0.75rem; }
.status-badge.completed { background: #d1fae5; color: #065f46; }
.status-badge.in_progress { background: #fef3c7; color: #92400e; }
.status-badge.pending { background: #f3f4f6; color: #6b7280; }
.node-status { font-size: 1rem; }
.node-status.completed { color: #10b981; }
.node-status.current { color: #f59e0b; }
.node-status.locked { color: #d1d5db; }
.empty-state { text-align: center; padding: 60px 24px; }
.empty-icon { font-size: 3rem; margin-bottom: 16px; }
.empty-state p { color: #6b7280; font-size: 0.95rem; }
.empty-hint { color: #9ca3af; font-size: 0.85rem; margin-top: 8px; }
</style>
