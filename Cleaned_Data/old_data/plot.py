import matplotlib.pyplot as plt
import math as math

PIX_SIZE = 750000

exec_time = [0.5, 1.0, 5, 10, 18, 24]

log_exec_time = [math.log(exec_time[i] * 60 * 60, 10) for i in range(len(exec_time))]

#jobs1_act = [7.963217884, 55.9627558, 73.41934246, 81.37703981, 55.56862802, 88.686998]
#jobs2_4_act = [94.43358227, 90.11580801, 96.91858411, 99.25966287, 99.22210657, 99.34985385]
##jobs5_8_act = [27.76598356, 26.38814333, 69.73119802, 80.3874188, 83.75730108, 77.23999758]
#jobs9_64_act = [22.19973971, 25.45512413, 27.83451345, 27.30034085, 55.4766163, 59.24661629]
#jobs65_256_act = [17.67351853, 9.236591014, 34.57233284, 48.0362859, 57.89949042, 56.23738505]

jobs1_wait = [5.77886876, 0.78690271, 1.81019447, 2.28847845, 14.39237793, 3.06146396]
jobs2_4_wait = [0.02947266, 0.10968322, 0.1589693, 0.0745859, 0.14111857, 0.15705617]
jobs5_8_wait = [1.30076459, 2.78958075, 2.17039165, 2.43975755, 3.49066382, 7.0719844]
jobs9_64_wait = [1.75227866, 2.92848212, 12.96331022, 26.6295793, 14.44610288, 16.50864252]
jobs65_256_wait = [2.32909144, 9.82650513, 9.46243163, 10.81759614, 13.08835651, 18.67623749]


jobs1_numSub = [140735, 20166, 14330, 8254, 2613, 23633]
jobs2_4_numSub = [4822, 1324, 3102, 1759, 1215, 3185]
jobs5_8_numSub = [9738, 5028, 7432, 3589, 3136, 7194]
jobs9_64_numSub = [340596, 59192, 119278, 38765, 31056, 52993]
jobs65_256_numSub = [85559, 11110, 24663, 11505, 6637, 12136]

jobs256_total = sum(jobs1_numSub) + sum(jobs2_4_numSub) + sum(jobs5_8_numSub) + sum(jobs9_64_numSub) + sum(jobs65_256_numSub)

frac_jobs1_numSub = map(lambda x : (math.sqrt(PIX_SIZE * x / jobs256_total)), jobs1_numSub)
frac_jobs2_4_numSub = map(lambda x : (math.sqrt(PIX_SIZE * x / jobs256_total)), jobs2_4_numSub)
frac_jobs5_8_numSub = map(lambda x : (math.sqrt(PIX_SIZE * x / jobs256_total)), jobs5_8_numSub)
frac_jobs9_64_numSub = map(lambda x : (math.sqrt(PIX_SIZE * x / jobs256_total)), jobs9_64_numSub)
frac_jobs65_256_numSub = map(lambda x : (math.sqrt(PIX_SIZE * x / jobs256_total)), jobs65_256_numSub)

jobs1_r1 = [(jobs1_wait[i] / exec_time[i]) for i in range(6)]
jobs2_4_r1 = [(jobs2_4_wait[i] / exec_time[i]) for i in range(6)]
jobs5_8_r1 = [(jobs5_8_wait[i] / exec_time[i]) for i in range(6)]
jobs9_64_r1 = [(jobs9_64_wait[i] / exec_time[i]) for i in range(6)]
jobs65_256_r1 = [(jobs65_256_wait[i] / exec_time[i]) for i in range(6)]

plt.subplot(111)

plt.xlabel('Execution Time (Tx) (log_10(sec))', fontsize='x-large')
plt.tick_params(labelsize=16)
plt.ylabel('R1 = Tq/Tx', fontsize='x-large')
plt.title('R1 vs Tx by Cores', fontsize='xx-large')
plt.axis([3, 5, -0.1, 12], fontsize='x-large')
plt.grid(True)

#plt.scatter(log_exec_time, jobs1_act, s=frac_jobs1_numSub, c='k', marker='o', lw=1.5, alpha=0.4, label='Job Size = 1')
#plt.scatter(log_exec_time, jobs2_4_act, s=frac_jobs2_4_numSub, c='k', marker='D', lw=2.5, alpha=0.4, label='Jobs Size = 2-4')
#plt.scatter(log_exec_time, jobs5_8_act, s=frac_jobs5_8_numSub, c='k', marker='^', lw=2.5, alpha=0.4, label='Jobs Size = 5-8')
#plt.scatter(log_exec_time, jobs9_64_act, s=frac_jobs9_64_numSub, c='k', marker='s', lw=1.5, alpha=0.4, label='Jobs Size = 9-64')
#plt.scatter(log_exec_time, jobs65_256_act, s=frac_jobs65_256_numSub, c='k', marker='p', lw=2.5, alpha=0.4, label='Jobs Size = 65-256')

plt.scatter(log_exec_time, jobs1_r1, s=frac_jobs1_numSub, c='k', marker='o', lw=1.5, alpha=0.4, label='Cores = 1')
plt.scatter(log_exec_time, jobs2_4_r1, s=frac_jobs2_4_numSub, c='k', marker='D', lw=2.5, alpha=0.4, label='Cores = 2-4')
plt.scatter(log_exec_time, jobs5_8_r1, s=frac_jobs5_8_numSub, c='k', marker='^', lw=2.5, alpha=0.4, label='Cores = 5-8')
plt.scatter(log_exec_time, jobs9_64_r1, s=frac_jobs9_64_numSub, c='k', marker='s', lw=1.5, alpha=0.4, label='Cores = 9-64')
plt.scatter(log_exec_time, jobs65_256_r1, s=frac_jobs65_256_numSub, c='k', marker='p', lw=2.5, alpha=0.4, label='Cores = 65-256')

plt.axhline(y=1, lw='2.5', color='k')
plt.legend(loc='upper right', fontsize='x-large')



plt.show()
