import argparse
from discussion import RolePlayDiscussion

def main():
    parser = argparse.ArgumentParser(description="Orchestrate a discussion with multiple AI agents.")
    parser.add_argument("-c", "--config", required=True, help="Path to the configuration file for agents.")
    parser.add_argument("-d", "--dataset", required=True, help="Path to the dataset file.")
    parser.add_argument("-r", "--rounds", type=int, default=3, help="Number of rounds in the discussion.")
    parser.add_argument("-t", "--type", choices= ["AUT", "Scientific","Similarities", "Instances"], help="Type of task to run.")
    args = parser.parse_args()

    agents_config = RolePlayDiscussion.load_config(args.config)
    discussion_runner = RolePlayDiscussion(agents_config, args.dataset, args.rounds, args.type)
    discussion_runner.run()


if __name__ == "__main__":
    main()
