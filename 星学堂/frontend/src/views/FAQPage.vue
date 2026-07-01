<script setup>
const faqs = [
  { q: "如何参加新员工入职闯关培训？", a: "新员工入职后会收到培训通知，通过联系方式H5进入星学堂学习入口，系统会自动分配闯关学习地图，按顺序完成各节点即可。" },
  { q: "闯关过程中可以跳过某个节点吗？", a: "不可以。闯关地图按管理员预设的顺序依次解锁，必须完成当前节点才能进入下一节点，确保培训流程完整。" },
  { q: "忘记签到/迟到如何处理？", a: "签到由管理员设置的签到时间段自动判定状态（正常/迟到/早退）。如因特殊情况未签到，请联系所在分公司管理员手动补录。" },
  { q: "考试可以重考吗？", a: "管理员在创建考试时可设置最大尝试次数（默认为1次）。如果管理员开启了多次尝试权限，在规定次数内可以重考，取最高分。" },
  { q: "如何查看和保存通关证书？", a: "全部闯关节点完成后，系统自动生成带个人专属二维码的电子证书。在个人中心可查看证书，支持保存为图片分享或打印。" },
  { q: "个人学习地图可以保存吗？", a: "可以在个人中心将学习地图保存为图片。每张地图都包含个人专属二维码，扫码可查看完整学习档案。" },
  { q: "管理员如何给全员批量推送考试？", a: "在管理后台创建考试任务，配置组卷和分值设定后，选择推送范围为「全员」或指定片区/岗位，系统自动将考试派发到每位员工的学习任务中。" },
  { q: "批量考试支持多少同时在线？", a: "系统支持上万人同时在线考试，考试数据实时保存，如中途断网，重连后可继续作答，已答题目不会丢失。" },
  { q: "如何导出学习地图和台账报表？", a: "在管理后台的台账管理模块，选择需要导出的台账类型，按条件筛选数据后，点击导出按钮即可生成Excel报表。学习地图和通关证书支持批量导出图片。" },
  { q: "新员工入职闯关地图每人可以使用多套吗？", a: "不可以。新员工入职闯关每名员工仅有一套固定的学习地图，即来即用，无需重复创建。全部通关后地图解锁完成。终身复用，是每名员工唯一的入职培训记录。" },
  { q: "分公司管理员和总部管理员权限有什么区别？", a: "总部超级管理员拥有全集团数据查看与管理权限；分公司管理员仅可管理本公司内的培训项目、员工数据和台账信息。项目级权限支持自定义配置，三级架构确保数据安全与隔离。" },
  { q: "登录系统时提示账号错误怎么办？", a: "管理员账号由系统管理员统一创建。如忘记账号或密码，请联系内部运维人员重置。员工无需登录系统，通过联系方式H5即可参与培训。" },
  { q: "培训费用如何统计？", a: "管理员可自定义每场培训的场次名称和费用信息，系统自动按月、按年汇总统计培训费用，生成培训成本台账报表。" },
  { q: "系统遇到BUG或功能优化建议如何反馈？", a: "可在关于我们页面填写学习反馈表单提交，或直接联系归属管理员。提交的反馈将统一归集处理，用于系统迭代优化。" },
  { q: "我的数据安全吗？", a: "星学堂为集团内网私有化部署平台，所有培训、证书、人事、反馈、费用数据均在集团内网服务器本地存储，不外流，符合集团数据安全规范。" },
]
</script>

<template>
  <div>
    <div class="page-header">
      <h1>常见问题</h1>
      <p>平台高频操作问题与解决方案，帮助您快速排忧解难</p>
    </div>

    <div class="page-container">
      <div class="faq-list">
        <div class="faq-item" v-for="faq in faqs" :key="faq.q">
          <div class="faq-q">{{ faq.q }}</div>
          <div class="faq-a">{{ faq.a }}</div>
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
.faq-list { display: flex; flex-direction: column; gap: 0; }
.faq-item { padding: 20px 0; border-bottom: 1px solid #e5e7eb; }
.faq-item:last-child { border-bottom: none; }
.faq-q { font-size: 1rem; font-weight: 600; color: #111827; margin-bottom: 8px; position: relative; padding-left: 20px; }
.faq-q::before { content: "Q"; position: absolute; left: 0; top: 1px; color: #c8102e; font-weight: 700; font-size: 0.85rem; }
.faq-a { font-size: 0.9rem; color: #6b7280; line-height: 1.7; padding-left: 20px; position: relative; }
.faq-a::before { content: "A"; position: absolute; left: 0; top: 1px; color: #2563eb; font-weight: 700; font-size: 0.85rem; }
</style>

