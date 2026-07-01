import urllib.request, json
r = urllib.request.urlopen("https://xingxuetang-production.up.railway.app/api/checkin/leaderboard/", timeout=8)
data = json.loads(r.read())
print("当前有", len(data), "条数据")
for u in data:
    print("  " + u["name"] + ": " + str(u["daysDone"]) + "关 " + str(u["totalScore"]) + "分")
print()
print("排行榜API可公开访问，不需要登录")
