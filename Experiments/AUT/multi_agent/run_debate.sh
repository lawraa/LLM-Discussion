#!/bin/bash

python3 llm_debate.py -c agents_config.json -d /home/chenlawrance/LLM-Creativity/Datasets/AUT/aut_10.json -r 6 -t AUT
python3 llm_debate.py -c agents_config_4.json -d /home/chenlawrance/LLM-Creativity/Datasets/AUT/aut_10.json -r 6 -t AUT
python3 llm_debate.py -c agents_config_6.json -d /home/chenlawrance/LLM-Creativity/Datasets/AUT/aut_10.json -r 6 -t AUT
