# Evaluation API Tool
Evaluate Results using **Fluency**, **Flexibility**, **Originality**, and **Elaboration**
Evaluation Results using **Pairwise**, **Sampling**, **Criteria**, and **Fewshot**
## Setup and Installation

1. **Clone the Repository:**
   Clone or download this repository to your local machine.

2. **Install Dependencies:**
   Navigate to the project directory and run:
   ```bash
   pip install -r requirements.txt
   ```
3. Before you execute, export you API key (set it in your environment)
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```
   You can also write it into you ~/.bashrc or ~/.zshrc

### 1. Setting File Paths:
For `auto_grade.py`, you don't have to edit path
  ```bash
  Put your input json file into "/dataset/AUT/discussion_result/" folder
  ```
Output for `auto_grade.py` will be stored in `eval_api/result` folder <br /><br />

For `box_plot.py`, set the file paths for the data you want to analyze:
  ```bash
  Choose 2 Files from "/result" Folder
  filename1  = "your_first_filename"
  filename2 = "your_second_filename"
  # e.g. filename = "file1"
  ```
Output for `box_plot.py` will be stored in `analysis_img/boxplot` folder <br /><br />

For `mean_std.py`, set the file path to the dataset you want to analyze:
  ```bash
  Choose 1 File from "/result" Folder
  filename = "your_filename"
  # e.g. filename = "file2"
  ```
### 2. Running the Script
  Args Parser for `auto_grade.py`:
  

   -v, --version: Version of the OpenAI model to use (3 for GPT-3, 4 for GPT-4). <br />
   -i, --input_file: Name of the input file located in the dataset/AUT/ directory. <br />
   -c, --criterion: Criterion for evaluation (options: fluency, flexibility, criteria, originality, elaboration, all). <br />
   -t, --type: Variant of the evaluation (options: default, fewshot, criteria, pairwise, sampling). <br />
   -s, --sample: Number of times to sample the evaluation.<br />
   -d, --dataset: which dataset we used. (AUT, Instances, Similarities and Scientific)  
   -o, --output: output in oue leader board or not

For example: 
  ```bash
  python3 auto_grade_final.py -v 3 -i Instances_single_few-shot_2-0 -t sampling -s 3 -d Instances -o y
  ```
  <!-- # Evaluate using GPT-3, pairwise comparison, for all criteria
  python3 auto_grade.py -v 3 -i dataname -c all -t pairwise -s 1 -d AUT -o y
   
  # Evaluate using GPT-4, sampling method, for all criteria
  python3 auto_grade.py -v 4 -i dataname -c all -t sampling -s 1 -d Scientific -o n
   
  # Evaluate using GPT-3, for all criteria in the default evaluation type
  python3 auto_grade.py -v 3 -i dataname -c all -t criteria -s 3 -d Instances -o y -->

  - This would use auto_grade_final.py in Instances_single_few-shot_2-0.json with sampling=3 and dataset = Instances while automatically output the results into LeaderBoard-Instances.csv
  - File Name Format:
    - single agent: ```{Task_Type}_{single}_{Subtask_Type}_{other info}_{data #}.json```
    - multi agent: ```{Task_Type}_{multi}_{Subtask_Type}_{agent #}_{round #}_{Agent Description}_{other info}_{data #}.json```
  - The default model for single agent is chatGPT-3.5
    - Need to fix the format if we wanna use other model in single agent test


-----
