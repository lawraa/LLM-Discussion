import json
import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau

# Function to load data from a JSON file
def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)
human_file = 'scored_fork_uses_lichun.json'
llm_file = 'evaluation_evaluation_test_rubric_3.json'
# Load human evaluations and LLM evaluations
human_evaluations = load_json(human_file)
llm_evaluations = load_json(llm_file)

print("Human File:", human_file, "\nLLM File:", llm_file)
# Assuming each LLM evaluation JSON file follows the structure shown above
# and you want to compare it against human evaluations

# Extract scores for comparison
human_originality_scores = {item["use"]: int(item["originality_score"]) for item in human_evaluations}
human_elaboration_scores = {item["use"]: int(item["elaboration_score"]) for item in human_evaluations}

llm_originality_scores = {}
llm_elaboration_scores = {}

for evaluation in llm_evaluations:
    for use in evaluation["uses"]:
        llm_originality_scores[use] = evaluation["originality"]["average_score"]
        llm_elaboration_scores[use] = evaluation["elaboration"]["average_score"]

# Prepare lists for analysis
originality_human_scores = []
originality_llm_scores = []

elaboration_human_scores = []
elaboration_llm_scores = []

for use in human_originality_scores.keys():
    if use in llm_originality_scores:
        originality_human_scores.append(human_originality_scores[use])
        originality_llm_scores.append(llm_originality_scores[use])
        
for use in human_elaboration_scores.keys():
    if use in llm_elaboration_scores:
        elaboration_human_scores.append(human_elaboration_scores[use])
        elaboration_llm_scores.append(llm_elaboration_scores[use])

# Convert lists to numpy arrays for calculation
originality_human_scores = np.array(originality_human_scores)
originality_llm_scores = np.array(originality_llm_scores)

elaboration_human_scores = np.array(elaboration_human_scores)
elaboration_llm_scores = np.array(elaboration_llm_scores)

# Calculate correlations
pearson_corr_ori, _ = pearsonr(originality_human_scores, originality_llm_scores)
spearman_corr_ori, _ = spearmanr(originality_human_scores, originality_llm_scores)
kendall_corr_ori, _ = kendalltau(originality_human_scores, originality_llm_scores)

pearson_corr_elab, _ = pearsonr(elaboration_human_scores, elaboration_llm_scores)
spearman_corr_elab, _ = spearmanr(elaboration_human_scores, elaboration_llm_scores)
kendall_corr_elab, _ = kendalltau(elaboration_human_scores, elaboration_llm_scores)

# Calculate MAE and RMSE
mae_ori = np.mean(np.abs(originality_human_scores - originality_llm_scores))
rmse_ori = np.sqrt(np.mean((originality_human_scores - originality_llm_scores) ** 2))

mae_elab = np.mean(np.abs(elaboration_human_scores - elaboration_llm_scores))
rmse_elab = np.sqrt(np.mean((elaboration_human_scores - elaboration_llm_scores) ** 2))

# Print out the results
print("Originality Correlations - Pearson:", pearson_corr_ori, "Spearman:", spearman_corr_ori, "Kendall:", kendall_corr_ori)
print("Elaboration Correlations - Pearson:", pearson_corr_elab, "Spearman:", spearman_corr_elab, "Kendall:", kendall_corr_elab)
print("MAE Originality:", mae_ori, "RMSE Originality:", rmse_ori)
print("MAE Elaboration:", mae_elab, "RMSE Elaboration:", rmse_elab)
