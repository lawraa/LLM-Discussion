#!/bin/bash

# python3 llm_debate.py -c agents_config_2.json -d /home/chenlawrance/LLM-Creativity/Datasets/AUT/aut_10.json -r 6 -t AUT
# python3 llm_debate.py -c agents_config_4.json -d /home/chenlawrance/LLM-Creativity/Datasets/AUT/aut_10.json -r 6 -t AUT
# python3 llm_debate.py -c agents_config_6.json -d /home/chenlawrance/LLM-Creativity/Datasets/AUT/aut_10.json -r 6 -t AUT
python3 llm_debate.py -c agents_config_2.json -d /home/chenlawrance/LLM-Creativity/Datasets/Instances/instances_10.json -r 6 -t Instances
python3 llm_debate.py -c agents_config_2.json -d /home/chenlawrance/LLM-Creativity/Datasets/Scientific/scientific_10.json -r 6 -t Scientific
python3 llm_debate.py -c agents_config_2.json -d /home/chenlawrance/LLM-Creativity/Datasets/Similarities/similarities_10.json -r 6 -t Similarities

