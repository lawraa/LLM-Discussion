import argparse
from discussion import RolePlayDiscussion_AUT
import argparse
import sys
from pathlib import Path
from types import SimpleNamespace
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Orchestrate a discussion with multiple AI agents.")
    parser.add_argument("-c", "--config", required=True, help="Path to the configuration file for agents.")
    parser.add_argument("-d", "--dataset", required=True, help="Path to the dataset file.")
    parser.add_argument("-r", "--rounds", type=int, default=3, help="Number of rounds in the discussion.")
    parser.add_argument("-t", "--type", choices= ["AUT", "Scientific","Similarities", "Instances"], help="Type of task to run.")
    args = parser.parse_args()

    agents_config = RolePlayDiscussion_AUT.load_config(args.config)
    discussion_runner = RolePlayDiscussion_AUT(agents_config, args.dataset, args.rounds, args.type)
    discussion_output = discussion_runner.run()

    if args.eval_mode:
        project_root = Path(__file__).resolve().parents[3]
        evaluation_path = project_root / 'Evaluation'
        sys.path.append(str(evaluation_path))
        # Now you can import auto_grade directly
        import json
        import os
        import csv
        import numpy as np
        from utils.openai_model import OpenAIModel
        from eval_functions.eval_criterion import evaluate_aut, evaluate_scientific, evaluate_wkct
        from eval_functions.pairwise_comparison import pairwise_judgement
        from automation_csv import calculate_mean_std, write_results_to_csv
        import logging
        from auto_grade_final import auto_grade

        #Call Evaluation
        input_file_name = discussion_output.split('.')[0]
        args = SimpleNamespace(
            version="3", 
            input_file=input_file_name, 
            type="sampling", 
            sample=3, 
            task=args.type, 
            output="y"
        )
        auto_grade(args)


if __name__ == "__main__":
    main()
