# Evaluation API Tool
Evaluate **Fluency**, **Flexibility**, **Originality**, and **Elaboration**

## Setup and Installation


### 1. API Keys
Before you execute, export you API key (set it in your environment)
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```
   You can also write it into you ~/.bashrc or ~/.zshrc

### 2. Running the Script
  ```bash
  -v, --version: Specify the version of the OpenAI model to use. Options are "3" (for GPT-3.5) and "4" (for GPT-4). Default is "3".

  -i, --input_file: Name (without .json) of the input file located in the Results/{task}/Output/multi_agent directory. {task} is "AUT", "Scientific", "Instances", or "Similarities"

  -s, --sample: Number of times to sample the evaluation. Default is 3.

  -d, --task: Task for the evaluation. Options include "AUT", "Scientific", "Instances", and "Similarities". Default is "AUT".

  -o, --output: Choose whether to output the results into the LeaderBoard or not. Options are "y" (yes) and "n" (no). Default is "n".
  ```

For example: 
  ```bash
  python3 auto_grade_final.py -v 3 -i Instances_single_few-shot_2-0 -s 3 -d Instances -o y
  ```

## Output 
The results of the evaluation will be saved in a JSON file located in the corresponding task's `Result/{task}/Eval_Result/multi-agent` folder. 
- If the -o option is set to "y", the results will also be saved in a CSV file in the LeaderBoard folder.
`os.path.join(Path(__file__).parent, '..', 'Results', 'LeaderBoard', f'LeaderBoard-{args.task}.csv'`
-----
