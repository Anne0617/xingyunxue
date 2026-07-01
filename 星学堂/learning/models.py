from django.db import models
from django.utils import timezone
import uuid


class Study(models.Model):
    name = models.CharField("姓名", max_length=50)
    company = models.CharField("所属公司", max_length=100)
    department = models.CharField("部门", max_length=100, blank=True, default="")
    position = models.CharField("岗位", max_length=50)
    wechat = models.CharField("联系方式", max_length=100, blank=True)
    description = models.TextField("问题/需求描述")
    submitted_at = models.DateTimeField("提交时间", auto_now_add=True)
    class Meta: db_table = "study"; verbose_name = "反馈记录"; verbose_name_plural = "反馈记录"
    def __str__(self): return f"{self.name} - {self.submitted_at:%Y-%m-%d %H:%M}"

class Exam(models.Model):
    title = models.CharField("考试标题", max_length=200)
    description = models.TextField("考试说明", blank=True)
    passing_score = models.IntegerField("及格分数", default=60)
    max_attempts = models.IntegerField("最大考试次数", default=3)
    slug = models.CharField("分享链接标识", max_length=32, unique=True, editable=False, default=uuid.uuid4)
    start_time = models.DateTimeField("开始时间", default=timezone.now)
    end_time = models.DateTimeField("结束时间", default=timezone.now)
    target_areas = models.CharField("推送区域", max_length=500, blank=True)
    is_published = models.BooleanField("已发布", default=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    class Meta: db_table = "exam"; ordering = ["-created_at"]; verbose_name = "考试"; verbose_name_plural = "考试管理"
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = uuid.uuid4().hex[:16]
        super().save(*args, **kwargs)
    def __str__(self): return self.title

class Question(models.Model):
    TYPE_CHOICES = [("single", "单选题"), ("multi", "多选题"), ("judge", "判断题")]
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions", verbose_name="所属考试")
    question_type = models.CharField("题型", max_length=10, choices=TYPE_CHOICES, default="single")
    content = models.TextField("题目内容")
    option_a = models.CharField(max_length=300, blank=True)
    option_b = models.CharField(max_length=300, blank=True)
    option_c = models.CharField(max_length=300, blank=True)
    option_d = models.CharField(max_length=300, blank=True)
    answer = models.CharField("正确答案", max_length=10)
    score = models.IntegerField("分值", default=2)
    sort_order = models.IntegerField("排序", default=0)
    class Meta: db_table = "question"; ordering = ["sort_order"]; verbose_name = "试题"; verbose_name_plural = "试题管理"
    def __str__(self): return f"{self.exam.title} - {self.content[:30]}"

class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name="考试")
    user_name = models.CharField("学员姓名", max_length=50)
    user_area = models.CharField("所属分公司", max_length=100, blank=True)
    employee_id = models.CharField("工号", max_length=50, blank=True, default="")
    phone = models.CharField("手机号", max_length=20, blank=True, default="")
    company = models.CharField("归属公司", max_length=100, blank=True, default="")
    department = models.CharField("部门", max_length=100, blank=True, default="")
    score = models.IntegerField("得分")
    total_score = models.IntegerField("总分")
    is_passed = models.BooleanField("是否及格")
    attempt_num = models.IntegerField("考试次数", default=1)
    answers = models.TextField("答题详情", blank=True)
    submitted_at = models.DateTimeField("提交时间", auto_now_add=True)
    class Meta: db_table = "exam_result"; ordering = ["-submitted_at"]; verbose_name = "考试成绩"; verbose_name_plural = "考试成绩"
    def __str__(self): return f"{self.user_name} - {self.exam.title} - {self.score}分"

class Badge(models.Model):
    name = models.CharField("称号名称", max_length=100)
    description = models.TextField("获取条件")
    icon = models.CharField("图标标识", max_length=50, blank=True)
    class Meta: db_table = "badge"; ordering = ["name"]; verbose_name = "称号"; verbose_name_plural = "称号管理"
    def __str__(self): return self.name

class UserBadge(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, verbose_name="称号")
    user_name = models.CharField("学员姓名", max_length=50)
    user_area = models.CharField("所属分公司", max_length=100, blank=True)
    earned_at = models.DateTimeField("获取时间", auto_now_add=True)
    class Meta: db_table = "user_badge"; ordering = ["-earned_at"]; verbose_name = "学员称号"; verbose_name_plural = "学员称号"
    constraints = [models.UniqueConstraint(fields=["badge", "user_name"], name="unique_user_badge")]
    def __str__(self): return f"{self.user_name} - {self.badge.name}"

class Announcement(models.Model):
    title = models.CharField("公告标题", max_length=200)
    date = models.DateField("发布日期")
    is_published = models.BooleanField("是否显示", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    class Meta: db_table = "announcement"; ordering = ["-date"]; verbose_name = "系统公告"; verbose_name_plural = "系统公告"
    def __str__(self): return self.title

# ===== 闯关系统模型 =====

class Employee(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联账号')
    employee_id = models.CharField('工号', max_length=50, unique=True)
    name = models.CharField('姓名', max_length=50)
    company = models.CharField('所属公司', max_length=100, blank=True)
    department = models.CharField('部门', max_length=100, blank=True)
    position = models.CharField('岗位', max_length=50, blank=True)
    phone = models.CharField('手机号', max_length=20, blank=True)
    hired_date = models.DateField('入职日期', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    class Meta: db_table='employee'; verbose_name='员工'; verbose_name_plural='员工'
    def __str__(self): return f'{self.name}({self.employee_id})'

class TrainingProgram(models.Model):
    name = models.CharField('项目名称', max_length=200)
    description = models.TextField('描述', blank=True, default='')
    start_date = models.DateField('开始日期', null=True, blank=True)
    end_date = models.DateField('结束日期', null=True, blank=True)
    is_active = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    class Meta: db_table='training_program'; verbose_name='培训项目'; verbose_name_plural='培训项目'; ordering=['-created_at']
    def __str__(self): return self.name

class CheckpointNode(models.Model):
    NODE_TYPES = [('checkin','签到'),('assessment','评估'),('exam','考试')]
    program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE, related_name='nodes', verbose_name='所属项目')
    name = models.CharField('节点名称', max_length=200)
    node_type = models.CharField('节点类型', max_length=20, choices=NODE_TYPES)
    order = models.IntegerField('排序', default=0)
    exam = models.ForeignKey('Exam', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联考试')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    class Meta: db_table='checkpoint_node'; verbose_name='闯关节点'; verbose_name_plural='闯关节点'; ordering=['program','order']
    def __str__(self): return f'[{self.program.name}] {self.name}'

class EmployeeProgram(models.Model):
    STATUS = [('pending','未开始'),('in_progress','进行中'),('completed','已完成')]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='programs', verbose_name='员工')
    program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE, related_name='participants', verbose_name='培训项目')
    status = models.CharField('状态', max_length=20, choices=STATUS, default='pending')
    enrolled_at = models.DateTimeField('加入时间', auto_now_add=True)
    completed_at = models.DateTimeField('完成时间', null=True, blank=True)
    class Meta: db_table='employee_program'; verbose_name='员工培训记录'; verbose_name_plural='员工培训记录'; unique_together=[('employee','program')]
    def __str__(self): return f'{self.employee.name} - {self.program.name}'

class EmployeeCheckpoint(models.Model):
    STATUS = [('locked','未解锁'),('current','当前关卡'),('completed','已完成')]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='checkpoint_progress', verbose_name='员工')
    node = models.ForeignKey(CheckpointNode, on_delete=models.CASCADE, related_name='employee_progress', verbose_name='节点')
    status = models.CharField('状态', max_length=20, choices=STATUS, default='locked')
    completed_at = models.DateTimeField('完成时间', null=True, blank=True)
    class Meta: db_table='employee_checkpoint'; verbose_name='员工闯关进度'; verbose_name_plural='员工闯关进度'; unique_together=[('employee','node')]
    def __str__(self): return f'{self.employee.name} - {self.node.name}'

class StarDailyCheckin(models.Model):
    """每日打卡记录"""
    name = models.CharField("姓名", max_length=50)
    department = models.CharField("部门", max_length=100, blank=True, default="")
    phone = models.CharField("联系方式", max_length=50, blank=True, default="")
    checkin_date = models.DateField("打卡日期", auto_now_add=True)
    checkin_time = models.DateTimeField("打卡时间", auto_now_add=True)
    ip_address = models.GenericIPAddressField("IP地址", blank=True, null=True)
    class Meta:
        db_table = "star_daily_checkin"
        unique_together = [["name", "checkin_date"]]
        verbose_name = "打卡记录"
        verbose_name_plural = "打卡记录"
        ordering = ["-checkin_time"]
    def __str__(self):
        return f"{self.name} - {self.checkin_date}"


class CheckinContent(models.Model):
    """闯关题目内容（可在后台编辑）"""
    day_number = models.IntegerField("天数", unique=True)
    title = models.CharField("标题", max_length=200)
    knowledge = models.TextField("知识简报（每行一条）", help_text="每行一条简报内容，最多5条", blank=True)
    questions_json = models.TextField("题目JSON", blank=True,
        help_text='[{"question":"题目","options":["A","B","C","D"],"correctIndex":1}]')
    updated_at = models.DateTimeField("更新时间", auto_now=True)
    class Meta:
        db_table = "checkin_content"
        ordering = ["day_number"]
        verbose_name = "闯关题目"
        verbose_name_plural = "闯关题目管理"
    def __str__(self):
        return f"第{self.day_number}天 - {self.title}"
class CheckinMission(models.Model):
    """闯关任务元数据"""
    day_number = models.IntegerField("天数", unique=True)
    code = models.CharField("代号", max_length=10, default="M-01")
    name = models.CharField("名称", max_length=50)
    icon = models.CharField("图标", max_length=10, default="🔥")
    episode = models.CharField("篇章", max_length=50, default="星火篇")
    class Meta:
        db_table = "checkin_mission"
        ordering = ["day_number"]
        verbose_name = "闯关任务"
        verbose_name_plural = "闯关任务管理"
    def __str__(self):
        return f"{self.code} {self.name}"
# === 十五五闯关系统 ===
class StarCheckinScore(models.Model):
    """十五五闯关成绩"""
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="用户")
    day_number = models.IntegerField("天数")
    score = models.IntegerField("得分", default=0)
    hp_left = models.IntegerField("剩余生命", default=5)
    answers_json = models.TextField("答案JSON", blank=True, default="")
    completed_at = models.DateTimeField("完成时间", auto_now_add=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = "star_checkin_score"
        unique_together = [("user", "day_number")]
        verbose_name = "闯关成绩"
        verbose_name_plural = "闯关成绩"
        ordering = ["day_number"]

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - 第{self.day_number}关"


