# Evaluation Tool 

## Requirements:
```
pip install python-dotenv
pip install openai
```

Before you execute the code, create a file name .env in the same folder. It must contain:
```
api_key="YOUR_API_KEY"
```

## Input/Output
The input file should be change to path to file.
```
#TODO: Path to file
filename = "response.json"
```

The output file should be change to your desired name.
```
with open(f"evaluation_results_version_{args.version}_4.json", "w") as outfile:
        json.dump(evaluation_results, outfile, indent=4)
```


## To execute the code, run:
```
python3 auto_grade_aut.py --version 3 --input_file <filename>
# 3 for ChatGPT 3.5, 4 for GPT4
# example of <filename>, if file is test.json, the just type test for <filename>
```

Almost in all scenarios, GPT4 is better than 3.5.

By default, each part will be sampled 3 times each with different random seeds.
