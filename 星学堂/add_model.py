import os
base = 'D:\\HuaweiMoveData\\Users\\Anna\\Documents\\星云学\\星学堂'
models_file = os.path.join(base, 'learning', 'models.py')
with open(models_file, 'a', encoding='utf-8') as f:
    f.write('''

class StarDailyCheckin(models.Model):
    """每日打卡记录"""
    name = models.CharField("\u59d3\u540d", max_length=50)
    department = models.CharField("\u90e8\u95e8", max_length=100, blank=True, default="")
    phone = models.CharField("\u8054\u7cfb\u65b9\u5f0f", max_length=50, blank=True, default="")
    checkin_date = models.DateField("\u6253\u5361\u65e5\u671f", auto_now_add=True)
    checkin_time = models.DateTimeField("\u6253\u5361\u65f6\u95f4", auto_now_add=True)
    ip_address = models.GenericIPAddressField("IP\u5730\u5740", blank=True, null=True)
    class Meta:
        db_table = "star_daily_checkin"
        unique_together = [["name", "checkin_date"]]
        verbose_name = "\u6253\u5361\u8bb0\u5f55"
        verbose_name_plural = "\u6253\u5361\u8bb0\u5f55"
        ordering = ["-checkin_time"]
    def __str__(self):
        return f"{self.name} - {self.checkin_date}"
''')
print('Model added to models.py')
