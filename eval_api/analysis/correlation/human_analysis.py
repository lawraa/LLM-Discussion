import json
import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau

# Function to load data from a JSON file
def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Function to safely convert score to integer, handling empty strings or non-numeric values
def safe_int(score, default=0):
    try:
        return int(score)
    except ValueError:
        return default

# Filenames for the two sets of human evaluations
human_file_1 = 'scored_fork_uses_lichun.json'
human_file_2 = 'scored_fork_uses_bai.json'

# Load the two sets of human evaluations
human_evaluations_set1 = load_json(human_file_1)
human_evaluations_set2 = load_json(human_file_2)

print("Human File 1:", human_file_1, "\nHuman File 2:", human_file_2)

# Extract scores, handling empty or non-numeric values
human_scores_set1 = {item["use"]: (safe_int(item["originality_score"]), safe_int(item["elaboration_score"])) for item in human_evaluations_set1}
human_scores_set2 = {item["use"]: (safe_int(item["originality_score"]), safe_int(item["elaboration_score"])) for item in human_evaluations_set2}

# Prepare lists for analysis, ensuring only uses present in both sets are compared
originality_scores_set1, originality_scores_set2 = [], []
elaboration_scores_set1, elaboration_scores_set2 = [], []

for use, scores in human_scores_set1.items():
    if use in human_scores_set2:
        originality_scores_set1.append(scores[0])
        originality_scores_set2.append(human_scores_set2[use][0])
        elaboration_scores_set1.append(scores[1])
        elaboration_scores_set2.append(human_scores_set2[use][1])

# Convert lists to numpy arrays for calculation
originality_scores_set1 = np.array(originality_scores_set1)
originality_scores_set2 = np.array(originality_scores_set2)
elaboration_scores_set1 = np.array(elaboration_scores_set1)
elaboration_scores_set2 = np.array(elaboration_scores_set2)


# Calculate correlations between the two sets of human scores
pearson_corr_ori, _ = pearsonr(originality_scores_set1, originality_scores_set2)
spearman_corr_ori, _ = spearmanr(originality_scores_set1, originality_scores_set2)
kendall_corr_ori, _ = kendalltau(originality_scores_set1, originality_scores_set2)

pearson_corr_elab, _ = pearsonr(elaboration_scores_set1, elaboration_scores_set2)
spearman_corr_elab, _ = spearmanr(elaboration_scores_set1, elaboration_scores_set2)
kendall_corr_elab, _ = kendalltau(elaboration_scores_set1, elaboration_scores_set2)

# Calculate MAE and RMSE between the two sets of human scores
mae_ori = np.mean(np.abs(originality_scores_set1 - originality_scores_set2))
rmse_ori = np.sqrt(np.mean((originality_scores_set1 - originality_scores_set2) ** 2))

mae_elab = np.mean(np.abs(elaboration_scores_set1 - elaboration_scores_set2))
rmse_elab = np.sqrt(np.mean((elaboration_scores_set1 - elaboration_scores_set2) ** 2))

# Print out the results
print("Human-Human Originality Correlations - Pearson:", pearson_corr_ori, "Spearman:", spearman_corr_ori, "Kendall:", kendall_corr_ori)
print("Human-Human Elaboration Correlations - Pearson:", pearson_corr_elab, "Spearman:", spearman_corr_elab, "Kendall:", kendall_corr_elab)
print("MAE Originality (Human-Human):", mae_ori, "RMSE Originality (Human-Human):", rmse_ori)
print("MAE Elaboration (Human-Human):", mae_elab, "RMSE Elaboration (Human-Human):", rmse_elab)
