import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import pointbiserialr


csv_file = r"D:\PRaFFLineDP\datasets\preprocessed_data\activemq-5.0.0_delete_commentBlack_with_metrics.csv"
df = pd.read_csv(csv_file)

required_cols = ["filename", "file-label", "line-label", "Block"]
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"miss_cols：{missing_cols}")

df["file-label"] = df["file-label"].astype(bool)
df["line-label"] = df["line-label"].astype(bool)
df["Block"] = df["Block"].astype(int)

defective_files = df[df["file-label"]]

results = []
for filename, group in defective_files.groupby("filename"):
    buggy_lines = group[group["line-label"]]
    clean_lines = group[~group["line-label"]]
    ce_lines = group[group["Block"] > 0]

    num_buggy = len(buggy_lines)
    num_clean = len(clean_lines)
    num_ce = len(ce_lines)

    buggy_ce_pct = (len(buggy_lines[buggy_lines["Block"] > 0]) / num_buggy) * 100 if num_buggy > 0 else np.nan
    clean_ce_pct = (len(clean_lines[clean_lines["Block"] > 0]) / num_clean) * 100 if num_clean > 0 else np.nan
    ce_buggy_pct = (len(ce_lines[ce_lines["line-label"]]) / num_ce) * 100 if num_ce > 0 else np.nan

    results.append({
        "filename": filename,
        "buggy_ce_percent": buggy_ce_pct,
        "clean_ce_percent": clean_ce_pct,
        "ce_buggy_percent": ce_buggy_pct
    })

results_df = pd.DataFrame(results).dropna()
if results_df.empty:
    raise ValueError("no valid file")


mean_buggy_ce = results_df["buggy_ce_percent"].mean()
mean_clean_ce = results_df["clean_ce_percent"].mean()
mean_ce_buggy = results_df["ce_buggy_percent"].mean()


plt.style.use("seaborn-v0_8-whitegrid")
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6))
# fig.suptitle("Analysis of the Relationship Between Block and Defective Lines", fontsize=20)

colors = {
    "buggy": "#FF6E3A",    
    "clean": "#4A90E2",   
    "mean_line": "red"     
}

plot_data = pd.melt(
    results_df,
    id_vars=[],
    value_vars=["buggy_ce_percent", "clean_ce_percent"],
    var_name="line_type",  
    value_name="percentage" 
)

sns.boxplot(
    x="line_type",
    y="percentage", 
    data=plot_data,
    ax=ax1,
    palette=[colors["buggy"], colors["clean"]],
    showfliers=True
)


ax1.set_xticklabels(['buggy', 'clean'], fontsize=12)
ax1.axhline(mean_buggy_ce, color=colors["buggy"], linestyle="--", label=f"Defective Line Mean: {mean_buggy_ce:.1f}%")
ax1.axhline(mean_clean_ce, color=colors["clean"], linestyle="--", label=f"Clean Line Mean: {mean_clean_ce:.1f}%")
ax1.legend(fontsize=10, loc='upper right', bbox_to_anchor=(1.032, 1.02))  # 向上移动图例
ax1.set_title("(a) Proportion distribution of Block>0\n between defective and clean lines", fontsize=15)
ax1.set_ylabel("Percentage(%)", fontsize=15)
ax1.set_ylim(0, 100)
ax1.set_xlabel("Line Type", fontsize=12)

sns.boxplot(
    y="ce_buggy_percent",
    data=results_df,
    ax=ax2,
    color="#87E8DE",
    showfliers=True,
    width=0.5
)



ax2.axhline(mean_ce_buggy, color=colors["mean_line"], linestyle="--", label=f"Mean Value: {mean_ce_buggy:.1f}%")
ax2.legend()
ax2.set_title("(b) Proportion distribution of\n defective lines among those having Block>0",fontsize=15)
ax2.set_ylabel("Percentage (%)",fontsize=15)
ax2.set_ylim(0, 100)
ax2.set_xlabel("")


mean_values = df.groupby("line-label")["Block"].mean().reset_index()
median_values = df.groupby("line-label")["Block"].median().reset_index()

non_buggy_mean = mean_values[mean_values["line-label"] == False]["Block"].values[0]
buggy_mean = mean_values[mean_values["line-label"] == True]["Block"].values[0]
non_buggy_median = median_values[median_values["line-label"] == False]["Block"].values[0]
buggy_median = median_values[median_values["line-label"] == True]["Block"].values[0]

sns.boxplot(
    x="line-label",
    y="Block",
    data=df,
    ax=ax3,
    showfliers=False,
    palette=[colors["clean"], colors["buggy"]],  
    boxprops={
        "edgecolor": "#084594",
        "linewidth": 1.5
    },
    whiskerprops={
        "color": "#084594",
        "linestyle": "-"
    },
    capprops={
        "color": "#084594"
    }
)


ax3.set_xticklabels(['clean', 'buggy'],fontsize=12)
ax3.axhline(non_buggy_mean, color=colors["clean"], linestyle="--", label=f"Clean Line Mean: {non_buggy_mean:.2f}")
ax3.axhline(buggy_mean, color=colors["buggy"], linestyle="--", label=f"Defective Line Mean: {buggy_mean:.2f}")
ax3.legend(loc='upper left', bbox_to_anchor=(0.5, 2))  
ax3.legend()  

ax3.set_title("(c) Distribution of Block values\n between defective and clean lines",fontsize=15)
ax3.set_xlabel("Line type", labelpad=10)
ax3.set_ylabel("Block Value", labelpad=10,fontsize=15)

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams["axes.unicode_minus"] = False


plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("Block_buggy_analysis.pdf", dpi=300, bbox_inches="tight")
plt.show()



