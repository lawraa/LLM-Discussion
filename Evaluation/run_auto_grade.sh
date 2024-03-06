#!/bin/bash

python3 auto_grade_final.py -v 3 -i AUT_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gpt-3-5-turbo_discussion_final_2024-03-06_03-29-54_10 -t sampling -s 3 -d AUT -o y
python3 auto_grade_final.py -v 3 -i Instances_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gpt-3-5-turbo_discussion_final_2024-03-06_03-14-44_10 -t sampling -s 3 -d Instances -o y
python3 auto_grade_final.py -v 3 -i Scientific_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gpt-3-5-turbo_discussion_final_2024-03-06_03-14-27_10 -t sampling -s 3 -d Scientific -o y
python3 auto_grade_final.py -v 3 -i Similarities_multi_debate-prompt-9_2_6_gpt-3-5-turbo-gpt-3-5-turbo_discussion_final_2024-03-06_12-21-17_10 -t sampling -s 3 -d Similarities -o y