#!/bin/bash

#python3 auto_grade_final.py -v 3 -i Instances_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gpt-3-5-turbo_discussion_final_without_special_prompts_10 -t sampling -s 3 -d Instances -o y
#python3 auto_grade_final.py -v 3 -i Scientific_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gpt-3-5-turbo_discussion_final_without_special_prompts_10 -t sampling -s 3 -d Scientific -o y
#python3 auto_grade_final.py -v 3 -i Similarities_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gpt-3-5-turbo_discussion_final_without_special_prompts_10 -t sampling -s 3 -d Similarities -o y
#python3 auto_grade_final.py -v 3 -i AUT_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gemini-pro_discussion_final_without_special_prompts_10 -t sampling -s 3 -d AUT -o y

# python3 auto_grade_final.py -v 3 -s 3 -d AUT -t sampling -o y -i AUT_single_single_roleplay_1_1_gpt-3.5-turbo-0125_AcademicResearcher_final_2024-03-19-20-06-45_10
# python3 auto_grade_final.py -v 3 -s 3 -d AUT -t sampling -o y -i AUT_single_single_roleplay_1_1_gpt-3.5-turbo-0125_CreativeProfessional_final_2024-03-19-20-04-35_10
# python3 auto_grade_final.py -v 3 -s 3 -d AUT -t sampling -o y -i AUT_single_single_roleplay_1_1_gpt-3.5-turbo-0125_Environmentalist_final_2024-03-19-20-05-39_10
# python3 auto_grade_final.py -v 3 -s 3 -d AUT -t sampling -o y -i AUT_single_single_roleplay_1_1_gpt-3.5-turbo-0125_Futurist_final_2024-03-19-20-07-51_10
# python3 auto_grade_final.py -v 3 -s 3 -d AUT -t sampling -o y -i AUT_single_single_roleplay_1_1_gpt-3.5-turbo-0125_SocialEntrepreneur_final_2024-03-19-20-03-28_10
# python3 auto_grade_final.py -v 3 -s 3 -d AUT -t sampling -o y -i AUT_single_single_roleplay_1_1_gpt-3.5-turbo-0125_VisionaryMillionaire_final_2024-03-19-20-02-14_10

# python3 auto_grade_final.py -v 3 -s 3 -d AUT -t sampling -o y -i AUT_single_single_baseline_1_1_gpt-3.5-turbo-0125_None_final_2024-03-20-17-34-30_30
# python3 auto_grade_final.py -v 3 -s 3 -d Scientific -t sampling -o y -i Scientific_single_single_baseline_1_1_gpt-3.5-turbo-0125_None_final_2024-03-20-17-36-21_30
# python3 auto_grade_final.py -v 3 -s 3 -d Similarities -t sampling -o y -i Similarities_single_single_baseline_1_1_gpt-3.5-turbo-0125_None_final_2024-03-20-17-38-39_30
# python3 auto_grade_final.py -v 3 -s 3 -d Instances -t sampling -o y -i Instances_single_single_baseline_1_1_gpt-3.5-turbo-0125_None_final_2024-03-20-17-40-02_30

# python3 auto_grade_final.py -v 3 -s 3 -d Scientific -t sampling -o y -i Scientific_multi_debate_roleplay_4_5_gpt-3-5-turbo-0125_Environmentalist-CreativeProfessional-Futurist-Futurist_final_2024-03-21-02-03-04-newversion_30

# python3 auto_grade_final.py -v 3 -s 3 -d Scientific -t sampling -o y -i Scientific_multi_debate_baseline_4_5_gpt-3-5-turbo-0125_None_final_2024-03-29-09-28-52_30

# python3 auto_grade_final.py -v 3 -s 3 -d Scientific -t sampling -o y -i Scientific_single_single_final_1_1_gpt-3.5-turbo-0125_None_final_2024-03-18-16-44-22_10
# python3 auto_grade_final.py -v 3 -s 3 -d Similarities -t sampling -o y -i Similarities_single_single_final_1_1_gpt-3.5-turbo-0125_None_final_2024-03-18-16-45-02_10
# python3 auto_grade_final.py -v 3 -s 3 -d Instances -t sampling -o y -i Instances_single_single_final_1_1_gpt-3.5-turbo-0125_None_final_2024-03-18-16-45-27_10
# AUT_single_basic-10-0
# AUT_single_CoT_10-0
# AUT_single_deep-breath_10-0
# AUT_single_few_shot_10-0
# AUT_single_stimuli_10-0
# Instances_single_basic_10-0
# Instances_single_CoT_10-0
# Instances_single_deep-breath_10-0
# Instances_single_few_shot_10-0
# Instances_single_stimuli_10-0
# Scientific_single_basic_10-0
# Scientific_single_CoT_10-0
# Scientific_single_deep-breath_10-0
# Scientific_single_few_shot_10-0
# Scientific_single_stimuli_10-0
# Similarities_single_basic_10-0
# Similarities_single_CoT_10-0
# Similarities_single_deep-breath_10-0
# Similarities_single_few_shot_10-0
# Similarities_single_stimuli_10-0
# python3 auto_grade_ff.py -v 3 -s 3 -d AUT -t sampling -o y -i AUT_multi_debate_roleplay_4_5_gpt-3-5-turbo-0125_Environmentalist-CreativeProfessional-Futurist-Futurist_final_2024-03-20-18-54-01-filtered_30 &
# python3 auto_grade_ff.py -v 3 -s 3 -d AUT -t sampling -o y -i AUT_multi_debate_baseline_4_5_gpt-3-5-turbo-0125_None_final_2024-03-29-04-48-59-filtered_30 &
# python3 auto_grade_ff.py -v 3 -s 3 -d AUT -t sampling -o y -i AUT_single_single_baseline_1_1_gpt-3.5-turbo-0125_None_final_2024-03-20-17-34-30-filtered_30 &
# python3 auto_grade_ff.py -v 3 -s 3 -d Instances -t sampling -o y -i Instances_multi_debate_roleplay_4_5_gpt-3-5-turbo-0125_Environmentalist-CreativeProfessional-Futurist-Futurist_final_2024-03-20-21-54-52-filtered_30 &
# python3 auto_grade_ff.py -v 3 -s 3 -d Similarities -t sampling -o y -i Similarities_multi_debate_roleplay_4_5_gpt-3-5-turbo-0125_Environmentalist-CreativeProfessional-Futurist-Futurist_final_2024-03-21-04-53-54-filtered_30 &
# python3 auto_grade_ff.py -v 3 -s 3 -d Scientific -t sampling -o y -i Scientific_multi_debate_roleplay_4_5_gpt-3-5-turbo-0125_Environmentalist-CreativeProfessional-Futurist-Futurist_final_2024-03-21-02-03-04-newversion-filtered_30 &
# python3 auto_grade_ff.py -v 3 -s 3 -d Instances -t sampling -o y -i Instances_multi_debate_baseline_4_5_gpt-3-5-turbo-0125_None_final_2024-03-29-07-17-53-filtered_30 &
# python3 auto_grade_ff.py -v 3 -s 3 -d Scientific -t sampling -o y -i Scientific_multi_debate_baseline_4_5_gpt-3-5-turbo-0125_None_final_2024-03-29-09-28-52-filtered_30 &
# python3 auto_grade_ff.py -v 3 -s 3 -d Similarities -t sampling -o y -i Similarities_multi_debate_baseline_4_5_gpt-3-5-turbo-0125_None_final_2024-03-29-10-21-04-filtered_30 &
# python3 auto_grade_ff.py -v 3 -s 3 -d Instances -t sampling -o y -i Instances_single_single_baseline_1_1_gpt-3.5-turbo-0125_None_final_2024-03-20-17-40-02-filtered_30 &
# python3 auto_grade_ff.py -v 3 -s 3 -d Scientific -t sampling -o y -i Scientific_single_single_baseline_1_1_gpt-3.5-turbo-0125_None_final_2024-03-20-17-36-21-filtered_30 &
# python3 auto_grade_ff.py -v 3 -s 3 -d Similarities -t sampling -o y -i Similarities_single_single_baseline_1_1_gpt-3.5-turbo-0125_None_final_2024-03-20-17-38-39-filtered_30_sampling_3 &
# wait

python3 auto_grade_ff.py -v 3 -s 3 -d AUT -t sampling -o y -i AUT_single_single_brainstorm_baseline_1_1_gpt-35turbo-0125_None_final-yesfilter_03-25-06-13-53_10
#/home/chenlawrance/LLM-Creativity/Results/AUT/Output/multi_agent/AUT_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gemini-pro_discussion_final_without_special_prompts_10.json
# Instances_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gpt-3-5-turbo_discussion_final_without_special_prompts_10
# Scientific_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gpt-3-5-turbo_discussion_final_without_special_prompts_10
# Similarities_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gpt-3-5-turbo_discussion_final_without_special_prompts_10