<script setup>
import { ref } from "vue";

const form = ref({ name: "", area: "", position: "", wechat: "", description: "" });
const showSuccess = ref(false);
const submitting = ref(false);

function handleSubmit() {
  submitting.value = true;
  setTimeout(() => {
    submitting.value = false;
    showSuccess.value = true;
    form.value = { name: "", area: "", position: "", wechat: "", description: "" };
  }, 600);
}
</script>

<template>
  <div>
    <div class="page-header">
      <h1>关于我们</h1>
      <p>星河智善生活集团智慧培训平台</p>
    </div>

    <div class="page-container">
      <!-- Team Intro -->
      <section class="about-section">
        <h2>团队简介</h2>
        <p>星学堂由星河智善生活集团人力行政中心牵头自研，统筹集团人才培育、数字化培训、资质台账标准化管理工作。技术团队与培训管理人员深度协作，以「用技术驱动人才培育」为使命，打造符合集团业务需求的数字化培训管理平台。</p>
      </section>

      <section class="about-section">
        <h2>平台建设背景</h2>
        <p>传统线下培训管理方式存在效率低、流程不规范等痛点：培训资源分散、进度难以追踪、台账管理复杂、效果无法量化。星学堂培训管理平台应运而生，旨在通过数字化手段实现培训全流程标准化、自动化管理，提升培训效率与管理水平。</p>
      </section>

      <section class="about-section">
        <h2>系统迭代规划</h2>
        <div class="roadmap">
          <div class="roadmap-item">
            <div class="roadmap-phase">第一期</div>
            <div class="roadmap-desc">闯关打卡系统上线，实现签到\u2192课件\u2192评估\u2192考试全流程闭环管理</div>
          </div>
          <div class="roadmap-item">
            <div class="roadmap-phase">第二期</div>
            <div class="roadmap-desc">智能教学模块接入，数字人讲师授课、错题生成学习方案、AI陪练</div>
          </div>
          <div class="roadmap-item">
            <div class="roadmap-phase">第三期</div>
            <div class="roadmap-desc">三大台账管理系统上线，费用管控、资质预警、报表可视化</div>
          </div>
          <div class="roadmap-item">
            <div class="roadmap-phase">第四期</div>
            <div class="roadmap-desc">移动端全面升级，小程序学习入口、消息推送、离线学习支持</div>
          </div>
        </div>
      </section>

      <!-- Feedback Form -->
      <section class="about-section feedback-section">
        <h2>学习反馈</h2>
        <p class="feedback-desc">提交BUG反馈、功能优化建议、业务咨询，我们将及时回复处理</p>
        <div class="feedback-form">
          <div class="form-row">
            <div class="form-field">
              <label>姓名</label>
              <input type="text" v-model="form.name" placeholder="请输入姓名" class="field-input" />
            </div>
            <div class="form-field">
              <label>所属分公司</label>
              <input type="text" v-model="form.area" placeholder="请输入所属分公司" class="field-input" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-field">
              <label>岗位</label>
              <input type="text" v-model="form.position" placeholder="请输入岗位" class="field-input" />
            </div>
            <div class="form-field">
              <label>联系方式</label>
              <input type="text" v-model="form.wechat" placeholder="请输入联系方式账号" class="field-input" />
            </div>
          </div>
          <div class="form-field">
            <label>问题 / 需求描述</label>
            <textarea v-model="form.description" placeholder="请详细描述您遇到的问题或优化建议……" class="field-textarea"></textarea>
          </div>
          <button class="form-submit" @click="handleSubmit">{{ submitting ? "提交中..." : "提交反馈" }}</button>
        </div>
      </section>
    </div>

    <!-- Success Modal -->
    <div class="modal-overlay" v-if="showSuccess" @click.self="showSuccess = false">
      <div class="modal-box">
        <button class="modal-close" @click="showSuccess = false">&times;</button>
        <div class="modal-body">
          <div class="success-icon">&#x2714;</div>
          <h3>提交成功</h3>
          <p>感谢您的反馈，我们将及时处理！</p>
          <button class="modal-btn" @click="showSuccess = false">我知道了</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header { text-align: left; padding: 48px 24px 40px; border-bottom: 1px solid #e5e7eb; margin-bottom: 40px; }
.page-header h1 { font-size: 1.8rem; font-weight: 700; color: #111827; margin-bottom: 8px; }
.page-header p { color: #6b7280; max-width: 560px; line-height: 1.7; }
.page-container { max-width: 900px; margin: 0; padding: 0 24px 80px; }

.about-section { margin-bottom: 40px; padding-bottom: 40px; border-bottom: 1px solid #e5e7eb; }
.about-section:last-of-type { border-bottom: none; }
.about-section h2 { font-size: 1.3rem; font-weight: 700; color: #111827; margin-bottom: 14px; }
.about-section p { font-size: 0.92rem; color: #4b5563; line-height: 1.8; }

.roadmap { display: flex; flex-direction: column; gap: 12px; }
.roadmap-item { display: flex; gap: 20px; padding: 14px 0; border-bottom: 1px solid #f3f4f6; }
.roadmap-item:last-child { border-bottom: none; }
.roadmap-phase { flex-shrink: 0; width: 60px; height: 26px; background: #c8102e; color: #fff; text-align: center; line-height: 26px; font-size: 0.8rem; font-weight: 600; }
.roadmap-desc { font-size: 0.9rem; color: #4b5563; line-height: 1.6; padding-top: 2px; }

.feedback-desc { margin-bottom: 24px !important; font-size: 0.88rem !important; color: #9ca3af !important; }
.feedback-form { max-width: 600px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
.form-field { display: flex; flex-direction: column; gap: 6px; margin-bottom: 16px; }
.form-field label { font-size: 0.85rem; color: #6b7280; font-weight: 500; }
.field-input { background: #f9fafb; border: 1px solid #d1d5db; padding: 10px 12px; font-size: 0.92rem; color: #1f2937; font-family: inherit; outline: none; }
.field-input:focus { border-color: #c8102e; }
.field-textarea { background: #f9fafb; border: 1px solid #d1d5db; padding: 10px 12px; font-size: 0.92rem; color: #1f2937; font-family: inherit; outline: none; resize: vertical; min-height: 100px; }
.field-textarea:focus { border-color: #c8102e; }
.form-submit { background: #c8102e; color: #fff; border: none; padding: 11px 32px; font-size: 0.95rem; font-weight: 600; cursor: pointer; font-family: inherit; }
.form-submit:hover { background: #b0102a; }

.modal-overlay { position: fixed; inset: 0; z-index: 200; background: rgba(0,0,0,0.45); display: flex; align-items: center; justify-content: center; }
.modal-box { background: #fff; border: 1px solid #e5e7eb; width: 100%; max-width: 360px; padding: 40px 32px 32px; position: relative; }
.modal-close { position: absolute; top: 12px; right: 14px; background: none; border: none; color: #9ca3af; cursor: pointer; font-size: 1.5rem; line-height: 1; }
.modal-close:hover { color: #c8102e; }
.modal-body { text-align: center; }
.success-icon { font-size: 2.5rem; color: #10b981; margin-bottom: 12px; }
.modal-body h3 { font-size: 1.15rem; font-weight: 700; color: #111827; margin-bottom: 8px; }
.modal-body p { font-size: 0.9rem; color: #6b7280; margin-bottom: 24px; }
.modal-btn { background: #c8102e; color: #fff; border: none; padding: 10px 36px; font-size: 0.92rem; font-weight: 600; cursor: pointer; font-family: inherit; }
.modal-btn:hover { background: #b0102a; }

@media (max-width: 768px) { .form-row { grid-template-columns: 1fr; } }
</style>

