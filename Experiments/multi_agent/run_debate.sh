# 5 Rounds, X Agents, No Role, No Hat, LLM Discussion, Val Dataset, AUT Task
python3 llm_discussion.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/AUT/aut_10_val.json -r 5 -t AUT -e
python3 llm_discussion.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/AUT/aut_10_val.json -r 5 -t AUT -e
python3 llm_discussion.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/AUT/aut_10_val.json -r 5 -t AUT -e
python3 llm_discussion.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/AUT/aut_10_val.json -r 5 -t AUT -e

# 5 Rounds, X Agents, No Role, No Hat, LLM Discussion, Val Dataset, Instances Task
python3 llm_discussion.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Instances/instances_10_val.json -r 5 -t Instances -e
python3 llm_discussion.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Instances/instances_10_val.json -r 5 -t Instances -e
python3 llm_discussion.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Instances/instances_10_val.json -r 5 -t Instances -e
python3 llm_discussion.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Instances/instances_10_val.json -r 5 -t Instances -e

# 5 Rounds, X Agents, No Role, No Hat, LLM Discussion, Val Dataset, Scientific Task
python3 llm_discussion.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Scientific/scientific_10_val.json -r 5 -t Scientific -e
python3 llm_discussion.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Scientific/scientific_10_val.json -r 5 -t Scientific -e
python3 llm_discussion.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Scientific/scientific_10_val.json -r 5 -t Scientific -e
python3 llm_discussion.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Scientific/scientific_10_val.json -r 5 -t Scientific -e

# 5 Rounds, X Agents, No Role, No Hat, LLM Discussion, Val Dataset, Similarities Task
python3 llm_discussion.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Similarities/similarities_10_val.json -r 5 -t Similarities -e
python3 llm_discussion.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Similarities/similarities_10_val.json -r 5 -t Similarities -e
python3 llm_discussion.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Similarities/similarities_10_val.json -r 5 -t Similarities -e
python3 llm_discussion.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Similarities/similarities_10_val.json -r 5 -t Similarities -e


# LLM Debate
python3 llm_debate_baseline.py -c agents_config.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Scientific/scientific_30_test.json -r 5 -t Scientific -e -p 1
python3 llm_debate_baseline.py -c agents_config.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Similarities/similarities_30_test.json -r 5 -t Similarities -e -p 1
python3 llm_debate_baseline.py -c agents_config.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Scientific/scientific_30_test.json -r 5 -t Scientific -e 
python3 llm_debate_baseline.py -c agents_config.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Similarities/similarities_30_test.json -r 5 -t Similarities -e


# LLM Debate with Role
python3 llm_debate_baseline.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Scientific/scientific_30_test.json -r 5 -t Scientific -e -p 1
python3 llm_debate_baseline.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Similarities/similarities_30_test.json -r 5 -t Similarities -e -p 1
python3 llm_debate_baseline.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Scientific/scientific_30_test.json -r 5 -t Scientific -e 
python3 llm_debate_baseline.py -c agents_config_role_final.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Similarities/similarities_30_test.json -r 5 -t Similarities -e

# LLM Debate with Role
python3 llm_discussion.py -c agents_config.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Similarities/similarities_10_val.json -r 5 -t Similarities -e
python3 llm_discussion.py -c agents_config.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Similarities/similarities_10_val.json -r 5 -t Similarities -e
python3 llm_discussion.py -c agents_config.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Similarities/similarities_10_val.json -r 5 -t Similarities -e
python3 llm_discussion.py -c agents_config.json -d /home/chenlawrance/exp_repo/LLM-Creativity/Datasets/Similarities/similarities_10_val.json -r 5 -t Similarities -e

