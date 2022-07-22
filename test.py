import time
t = time.time()
print(t) # 1436428326.207596
t_10 = int(t)# 10位时间戳
t_13 = int(round(time.time() * 1000))# 13位时间戳
print(t_10)# 1436428326
print(t_13)# 1436428326207



print('------',str(int(time.time())))