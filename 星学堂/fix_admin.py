fp = 'D:\\HuaweiMoveData\\Users\\Anna\\Documents\\星云学\\星学堂\\learning\\admin.py'
with open(fp, 'r+', encoding='utf-8') as f:
    c = f.read()
    c = c.replace('import StarDailyCheckin, *', 'import StarDailyCheckin')
    f.seek(0)
    f.write(c)
    f.truncate()
print('Fixed')
