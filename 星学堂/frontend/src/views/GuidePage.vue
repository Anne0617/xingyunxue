<script setup>
const employeeGuides = [
  { title: "闯关打卡", steps: [
    "登录联系方式H5学习入口",
    "进入当前培训项目，查看闯关地图",
    "按顺序完成每个节点：签到、课件观看、评估、考试",
    "全部通关后自动生成电子证书，可保存地图与证书图片"
  ]},
  { title: "线上学习", steps: [
    "在闯关地图中点击课件节点，播放课件内容",
    "支持多格式课件在线观看",
    "学习进度自动记录，可随时查看已学内容"
  ]},
  { title: "在线考试", steps: [
    "到达考试节点后，点击「开始考试」",
    "在规定时间内完成所有题目",
    "提交后自动阅卷，查看成绩与错题解析"
  ]},
  { title: "证书与学习地图", steps: [
    "通关后在个人中心查看电子证书",
    "支持保存证书为图片，分享展示",
    "学习地图可保存为图片放入培训汇报材料"
  ]},
]

const adminGuides = [
  { title: "新建培训打卡", steps: [
    "登录PC管理后台，进入培训闯关管理",
    "创建培训项目，设置起止日期",
    "添加闯关节点（签到/评估/考试），配置节点顺序",
    "导入参训员工名单，系统自动生成闯关进度"
  ]},
  { title: "敏捷做课", steps: [
    "使用PPT一键生成课程内容",
    "支持视频、文档、图文等多格式课件批量导入",
    "自定义整套培训流程，设置各节点要求"
  ]},
  { title: "题库管理", steps: [
    "创建题库，按学科/岗位分类管理",
    "新增题目：支持单选、多选、判断、填空四种题型",
    "为考试配置试卷，从题库中选题组卷"
  ]},
  { title: "批量考试", steps: [
    "创建考试任务，设置考试时长、及格分数",
    "从题库组卷，配置试卷分值",
    "推送给指定员工或全员参与",
    "考试结束后自动统计成绩，查看详细答题记录"
  ]},
  { title: "台账导出", steps: [
    "进入台账管理模块，选择需要导出的台账类型",
    "按条件筛选数据，支持按时间、分公司、项目筛选",
    "一键导出Excel报表，用于培训汇报与存档"
  ]},
  { title: "权限管理", steps: [
    "总部超级管理员拥有全集团数据权限",
    "分公司管理员仅可管理本公司数据",
    "管理员可配置员工查看权限范围"
  ]},
]
</script>

<template>
  <div>
    <div class="page-header">
      <h1>使用手册</h1>
      <p>详细操作指南，帮助您快速上手使用星学堂平台</p>
    </div>

    <div class="page-container">
      <h2 class="module-title">普通员工操作指南</h2>
      <div class="guide-section">
        <div class="guide-card" v-for="g in employeeGuides" :key="g.title">
          <div class="guide-header">
            <div class="guide-icon">&#x1F4D6;</div>
            <h3>{{ g.title }}</h3>
          </div>
          <ol class="guide-steps">
            <li v-for="(step, i) in g.steps" :key="i">{{ step }}</li>
          </ol>
        </div>
      </div>

      <h2 class="module-title" style="margin-top:60px;padding-top:40px;border-top:1px solid #e5e7eb;">管理员操作指南</h2>
      <div class="guide-section">
        <div class="guide-card" v-for="g in adminGuides" :key="g.title">
          <div class="guide-header">
            <div class="guide-icon">&#x1F4BB;</div>
            <h3>{{ g.title }}</h3>
          </div>
          <ol class="guide-steps">
            <li v-for="(step, i) in g.steps" :key="i">{{ step }}</li>
          </ol>
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
.module-title { font-size: 1.4rem; font-weight: 700; color: #111827; margin-bottom: 28px; }
.guide-section { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
.guide-card { border: 1px solid #e5e7eb; padding: 24px; }
.guide-header { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }
.guide-icon { font-size: 1.3rem; }
.guide-card h3 { font-size: 1rem; font-weight: 600; color: #111827; }
.guide-steps { list-style: none; counter-reset: step; padding: 0; }
.guide-steps li { counter-increment: step; position: relative; padding: 6px 0 6px 28px; font-size: 0.9rem; color: #4b5563; line-height: 1.6; }
.guide-steps li::before { content: counter(step); position: absolute; left: 0; top: 6px; width: 20px; height: 20px; background: #c8102e; color: #fff; font-size: 0.75rem; text-align: center; line-height: 20px; }
@media (max-width: 768px) { .guide-section { grid-template-columns: 1fr; } }
</style>


