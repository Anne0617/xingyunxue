<script setup>
const employeeFeatures = [
  { title: "双模式游戏化闯关打卡", items: [
    "新员工入职闯关：每人仅一套固定学习地图，无需重复创建；全部通关解锁完整可视化地图，自动生成带个人专属二维码通关电子证书，员工可保存地图、证书图片；扫码直达个人全部学习档案",
    "专项岗位/月度/季度培训打卡：每场培训独立新建打卡流程；支持打卡模板复制复用，各场次数据独立存储互不干扰"
  ]},
  { title: "标准化学习闭环", items: [
    "签到→课件观看→培训评估→线上考试，全流程自动化管理",
    "权限限制：普通学员无任何学习材料导出功能，仅可查看本人记录、证书、地图"
  ]},
  { title: "智能教学配套", items: [
    "数字人讲师授课、错题生成个性化学习方案、管理员在线陪练、学习实时咨询指导"
  ]},
  { title: "个人双证书中心", items: [
    "内部培训结业证查看、国家职业资格证书查看"
  ]},
]

const adminFeatures = [
  { title: "敏捷做课", items: [
    "PPT一键生成课程，多格式课件批量导入，自定义整套培训流程"
  ]},
  { title: "题库与大规模考试", items: [
    "独立题库管理、线上考试、培训数据可视化；支持上万人批量推送考试打卡"
  ]},
  { title: "三大台账管理", items: [
    "学员培训记录台账、培训费用台账、全员资质证书台账",
    "Excel批量导入导出、证书到期预警；集团统一管控全量数据"
  ]},
  { title: "数据导出权限", items: [
    "仅管理员可批量导出签到记录、评估问卷、考试答卷、全员学习地图、通关证书、各类台账报表"
  ]},
  { title: "培训成本管理", items: [
    "自定义培训场次，自动统计月度、年度培训费用"
  ]},
]
</script>

<template>
  <div>
    <div class="page-header">
      <h1>系统功能</h1>
      <p>覆盖培训全场景的模块化功能矩阵，满足各角色使用需求</p>
    </div>

    <div class="page-container">
      <h2 class="module-title">员工移动端功能</h2>
      <div class="features-section">
        <div class="feature-card" v-for="(f, i) in employeeFeatures" :key="f.title">
          <div class="feature-num">{{ String(i+1).padStart(2,"0") }}</div>
          <h3>{{ f.title }}</h3>
          <ul>
            <li v-for="item in f.items" :key="item">{{ item }}</li>
          </ul>
        </div>
      </div>

      <h2 class="module-title" style="margin-top:60px;padding-top:40px;border-top:1px solid #e5e7eb;">管理员 PC 后台功能</h2>
      <div class="features-section">
        <div class="feature-card" v-for="(f, i) in adminFeatures" :key="f.title">
          <div class="feature-num">{{ String(i+1).padStart(2,"0") }}</div>
          <h3>{{ f.title }}</h3>
          <ul>
            <li v-for="item in f.items" :key="item">{{ item }}</li>
          </ul>
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
.features-section { display: flex; flex-direction: column; gap: 20px; }
.feature-card { border: 1px solid #e5e7eb; padding: 24px 28px; }
.feature-num { font-size: 0.8rem; font-weight: 700; color: #c8102e; margin-bottom: 6px; }
.feature-card h3 { font-size: 1.05rem; font-weight: 600; color: #111827; margin-bottom: 10px; }
.feature-card ul { list-style: none; padding: 0; }
.feature-card ul li { position: relative; padding: 5px 0 5px 14px; font-size: 0.9rem; color: #4b5563; line-height: 1.7; }
.feature-card ul li::before { content: ""; position: absolute; left: 0; top: 12px; width: 4px; height: 4px; background: #c8102e; }
</style>

