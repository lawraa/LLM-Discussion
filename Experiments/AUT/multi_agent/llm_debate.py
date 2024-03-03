import argparse
from discussion import LLM_Debate_AUT, LLM_Debate_Scientific, LLM_Debate_Instance_Similarities


def main():
    parser = argparse.ArgumentParser(description="Orchestrate a discussion with multiple AI agents.")
    parser.add_argument("-c", "--config", required=True, help="Path to the configuration file for agents.")
    parser.add_argument("-d", "--dataset", required=True, help="Path to the dataset file.")
    parser.add_argument("-r", "--rounds", type=int, default=3, help="Number of rounds in the discussion.")
    parser.add_argument("-t", "--type", choices= ["AUT", "Scientific","Similarities", "Instances"], help="Type of task to run.")
    args = parser.parse_args()
    
    if args.type == "AUT":
        agents_config = LLM_Debate_AUT.load_config(args.config)
        discussion_runner = LLM_Debate_AUT(agents_config, args.dataset, args.rounds)
    elif args.type == "Scientific":
        agents_config = LLM_Debate_Scientific.load_config(args.config)
        discussion_runner = LLM_Debate_Scientific(agents_config, args.dataset, args.rounds)
    elif args.type == "Similarities" or args.type == "Instances":
        agents_config = LLM_Debate_Instance_Similarities.load_config(args.config)
        discussion_runner = LLM_Debate_Instance_Similarities(agents_config, args.dataset, args.rounds, args.type)
    discussion_runner.run()

if __name__ == "__main__":
    main()
