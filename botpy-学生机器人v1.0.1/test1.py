roles = [  
    {'id': '4', 'name': '频道主', 'color': 4294917938, 'hoist': 1, 'number': 1, 'member_limit': 1},  
    {'id': '2', 'name': '超级管理员', 'color': 4294936110, 'hoist': 1, 'number': 9, 'member_limit': 50}  
]  
  
# 使用for循环遍历列表中的每一项  
for role in roles:  
    # 输出每一项的id和name  
    m1="ID:"+role['id']+"Name:"+role['name']
    print(m1)  # 可选，用于分隔输出结果
