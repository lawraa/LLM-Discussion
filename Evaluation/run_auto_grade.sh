#!/bin/bash

python3 auto_grade_final.py -v 3 -i Instances_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gpt-3-5-turbo_discussion_final_without_special_prompts_10 -t sampling -s 3 -d Instances -o y
python3 auto_grade_final.py -v 3 -i Scientific_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gpt-3-5-turbo_discussion_final_without_special_prompts_10 -t sampling -s 3 -d Scientific -o y
python3 auto_grade_final.py -v 3 -i Similarities_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gpt-3-5-turbo_discussion_final_without_special_prompts_10 -t sampling -s 3 -d Similarities -o y


# Instances_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gpt-3-5-turbo_discussion_final_without_special_prompts_10
# Scientific_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gpt-3-5-turbo_discussion_final_without_special_prompts_10
# Similarities_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gpt-3-5-turbo_discussion_final_without_special_prompts_10