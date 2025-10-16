import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#df = pd.read_csv('./new/Dis_result/all_different_threshold_median_recall.csv', index_col=0)
#df = pd.read_csv('./new/Dis_result/all_different_threshold_mean_recall.csv', index_col=0)
#df = pd.read_csv('./new/Dis_result/all_different_threshold_median_effort.csv', index_col=0)
df = pd.read_csv('./new/Dis_result/all_different_threshold_mean_effort.csv', index_col=0)

df.columns = ['threshold', 'GLANCE-MD', 'DeepLineDP', 'SPLICE_F', 'PRaFFLineDP']


threshold_labels = [
    'effort10%', 'effort20%', 'effort30%', 'effort40%',
    'effort50%', 'effort60%', 'effort70%', 'effort80%',
    'effort90%', 'effort100%'
]
threshold_values = np.arange(10, 101, 10)  # 10, 20, ..., 100


plt.figure(figsize=(12, 6), dpi=100)
plt.grid(True, linestyle='--', alpha=0.6)
plt.title('Mean Effort@k Comparison', fontsize=14)
plt.xlabel('Effort Threshold (%)', fontsize=12)
plt.ylabel('Mean Effort', fontsize=12)


methods = ['GLANCE-MD', 'DeepLineDP', 'SPLICE_F', 'PRaFFLineDP']
markers = ['o', 's', '^', 'D']  
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']  

for method, marker, color in zip(methods, markers, colors):
    plt.plot(
        threshold_values,
        df[method],
        label=method,
        marker=marker,
        markersize=8,
        linewidth=2.5,
        color=color,
        markeredgecolor='white',
        markeredgewidth=1.2
    )


plt.xticks(threshold_values, threshold_labels, rotation=45)
plt.xlim(5, 105)


plt.legend(loc='lower right', fontsize=10)
plt.tight_layout()


plt.savefig('mean_effort_comparison.pdf', bbox_inches='tight')


plt.show()