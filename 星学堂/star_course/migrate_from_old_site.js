// ===== 旧站 → 星学堂 数据迁移工具 =====
// 在旧站 https://anne0617.github.io/star-course-checkin/ 的浏览器按F12
// 粘贴到 Console 执行，复制输出结果

(function() {
  var data = localStorage.getItem("xa_user");
  if (!data) { console.log("未找到数据"); return; }
  var user = JSON.parse(data);
  var result = [{
    name: user.name || "",
    dept: user.dept || "",
    phone: user.phone || "",
    days: user.days || {}
  }];
  console.log("✅ 找到 " + Object.keys(user.days||{}).length + " 天数据");
  console.log("复制以下内容，然后执行导入命令：");
  console.log(JSON.stringify(result, null, 2));
  console.log("\n导入命令（在终端执行）：");
  console.log('curl -X POST http://127.0.0.1:8000/api/checkin/import/');
  console.log('  -H "Content-Type: application/json"');
  console.log('  -d \'' + JSON.stringify(result) + "'");
})();
