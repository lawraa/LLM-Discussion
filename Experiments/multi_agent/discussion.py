import json
import re
from agents import OpenAIAgent, GeminiAgent, Llama2Agent
import datetime
import os

class Discussion:
    PROMPTS = {
        1: "You are in a group discussion with other teammates; as a result, answer as diversely and creatively as you can.",
        2: "You're in a brainstorming session where each idea leads to the next. Embrace the flow of creativity without limits, encouraging one another to build on each suggestion for unexpected connections.",
        3: "Pretend your team is at a think tank where unconventional ideas are the norm. Challenge each other to think from different perspectives, considering the most unusual or innovative ideas.",
        4: "Engage in a collaborative discussion where each of you contributes a unique insight or query, aiming to delve into uncharted territories of thought. Throughout the discussion, focus on expanding the scope and depth of each contribution through constructive feedback, counterpoints, and further questioning. The objective is to achieve a broad spectrum of ideas and solutions, promoting a culture of continuous learning and innovation.",
        5: "Envision your group as a crew on a mission to solve a mystery using only your creativity and wit. How would you piece together clues from each member's ideas to find the solution? And this would be crucial to your member’s life."
    }

    def __init__(self, dataset_file, rounds, prompt):
        self.dataset_file = dataset_file
        self.rounds = rounds
        self.discussion_prompt = self.PROMPTS.get(prompt, "Invalid prompt selected.")
        print("Discussion initialized with dataset: {} and {} rounds.".format(dataset_file, rounds))

    def run(self):
        pass

    def save_conversation(self, filename, conversation_data):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as file:
            json.dump(conversation_data, file, indent=4)
        print(f"Saved Conversation Data to {filename}")

    @staticmethod
    def load_config(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
        
    def extract_response(self, content):
        lines = content.split('\n')
        uses = [line.strip() for line in lines if line.strip() and re.match(r"^\d+\.", line)]
        uses = [use[use.find('.') + 2:] for use in uses]
        return uses

class LLM_Debate(Discussion):
    def __init__(self, agents_config, dataset_file, rounds, task, prompt):
        super().__init__(dataset_file, rounds, prompt)
        self.task_type = task
        self.agents = self.initialize_agents(agents_config)
        print(f"LLM_Debate initialized for task: {task} with {len(self.agents)} agents.")
    
    def initialize_agents(self, agents_config):
        agents = []
        for config in agents_config:
            if config['type'] == 'openai':
                agents.append(OpenAIAgent(model_name=config['model_name'], 
                                          agent_name = config['agent_name'], 
                                          agent_role = config['agent_role'], 
                                          agent_speciality = config['agent_speciality'], 
                                          agent_role_prompt = config['agent_role_prompt'], 
                                          speaking_rate = config['speaking_rate']))
            elif config['type'] == 'gemini':
                agents.append(GeminiAgent(model_name=config['model_name'], 
                                          agent_name = config['agent_name'],
                                          agent_role=config['agent_role'],
                                          agent_speciality=config['agent_speciality'],
                                          agent_role_prompt=config['agent_role_prompt'],
                                          speaking_rate=config['speaking_rate']))
            elif config['type'] == 'llama2':
                agents.append(Llama2Agent(ckpt_dir=config['ckpt_dir'], 
                                          tokenizer_path=config['tokenizer_path'], 
                                          agent_name = config['agent_name']))
            else:
                raise ValueError(f"Unsupported agent type: {config['type']}")
        return agents
    
    def construct_response(self, question, most_recent_responses, current_agent, is_last_round, baseline=False):
        prefix_string = "These are the solutions to the problem from other agents:\n"
        for agent_name, responses in most_recent_responses.items():
            if agent_name == current_agent.agent_name:
                continue  
            if responses and 'parts' in responses[-1]:
                response_content = responses[-1]['parts'][0]
            else:
                response_content = responses[-1]['content']
            
            other_agent_response = f"One agent solution: ```{response_content}```\n"
            prefix_string += other_agent_response
        
        if baseline:
            suffix_string = "Using the reasoning from other agents as additional advice, can you give an updated answer? Please put your answer in a list format, starting with 1. ... 2. ... 3. ... and so on."
        else:
            suffix_string = question + self.discussion_prompt
            if is_last_round:
                suffix_string += " This is the last round of the discussion, please finalize and present a list of as many creative answers as possible. Please list the final response in 1. ... 2. ... 3. ... and so on. \n\n"
        
        return prefix_string + suffix_string    

    def save_debate_conversations(self, agents, all_responses, init_results, final_results, amount_of_data, task_type="AUT", baseline = False):
        current_date, formatted_time = self.get_current_datetime()
        model_names_concatenated = self.concatenate_model_names(agents)
        role_names_concatenated = self.concatenate_role_names(agents)
        subtask = self.determine_subtask(agents, baseline)

        output_filename = self.generate_filename(task_type, subtask, "chat_log", model_names_concatenated, role_names_concatenated, current_date, formatted_time, amount_of_data, len(agents), self.rounds)
        final_ans_filename = self.generate_filename(task_type, subtask, "Output/multi_agent", model_names_concatenated, role_names_concatenated, current_date, formatted_time, amount_of_data, len(agents), self.rounds)
        init_ans_filename = self.generate_filename(task_type, subtask, "init", model_names_concatenated, role_names_concatenated, current_date, formatted_time, amount_of_data, len(agents), self.rounds)
        
        # Ensure all required directories exist
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        os.makedirs(os.path.dirname(final_ans_filename), exist_ok=True)
        os.makedirs(os.path.dirname(init_ans_filename), exist_ok=True)

        self.save_conversation(output_filename, all_responses)
        self.save_conversation(final_ans_filename, final_results)
        self.save_conversation(init_ans_filename, init_results)

        return final_ans_filename
    
    @staticmethod
    def get_current_datetime():
        current_time = datetime.datetime.now()
        current_date = current_time.strftime("%Y-%m-%d")
        formatted_time = current_time.strftime("%H-%M-%S")
        return current_date, formatted_time
    
    @staticmethod
    def concatenate_model_names(agents):
        if all(agent.model_name == agents[0].model_name for agent in agents):
            return agents[0].model_name.replace(".", "-")
        return "-".join(agent.model_name.replace(".", "-") for agent in agents)

    @staticmethod
    def concatenate_role_names(agents):
        if all(agent.agent_role == "None" for agent in agents):
            return "None"
        return "-".join(agent.agent_role.replace(" ", "") for agent in agents)

    def determine_subtask(self, agents, baseline):
        if baseline:
            return "baseline"
        if all(agent.agent_role == "None" for agent in agents):
            return "FINAL"
        return "roleplay"
    
    @staticmethod
    def generate_filename(task_type, subtask, data_type, model_names_concatenated, role_names_concatenated, current_date, formatted_time, amount_of_data, num_agents, num_rounds):
        return f"../../../Results/{task_type}/{data_type}/{task_type}_multi_debate_{subtask}_{num_agents}_{num_rounds}_{model_names_concatenated}_{role_names_concatenated}_{data_type}_{current_date}-{formatted_time}_{amount_of_data}.json"


class LLM_Debate_AUT_Baseline(LLM_Debate):    
    def run(self):
        print(f"Starting LLM_Debate.run with dataset: {self.dataset_file}")

        with open(self.dataset_file, 'r') as f:
            dataset = json.load(f)
        all_responses = {}
        init_results = []
        final_results = []
        amount_of_data = len(dataset['Examples'])
        for example in dataset['Examples']:
            # --------------->>>> set the system content
            chat_history = {agent.agent_name: [] for agent in self.agents}
            object = example['object']
            problem_template = " ".join(dataset["Task"][0]["Problem"])
            question = problem_template.replace("{object}", object)
            initial_prompt = question
            most_recent_responses = {}
            # ------------------------------------------
            for round in range(self.rounds):
                is_last_round = (round == self.rounds - 1)
                is_first_round = (round == 0)
                round_responses = {agent.agent_name: [] for agent in self.agents}
                print(f"Round {round + 1}, Object: {object}")
                for agent in self.agents:
                    if agent.agent_role != "None":
                        agent_role_prompt = f"You are a {agent.agent_role} whose specialty is {agent.agent_speciality}. {agent.agent_role_prompt} Remember to claim your role in the beginning of each conversation. "
                        print(f"agent_role = {agent.agent_role}")
                    else:
                        agent_role_prompt = ""
                    if is_first_round: 
                        formatted_initial_prompt = agent.construct_user_message(agent_role_prompt + "Can you answer the following question as creatively as possible: " + initial_prompt + " Please put your answer in a list format, starting with 1. ... 2. ... 3. ... and so on.")
                        chat_history[agent.agent_name].append(formatted_initial_prompt)
                        response = agent.generate_answer(chat_history[agent.agent_name])
                        # Save the initial response of the Agent
                        uses_list = self.extract_response(response)
                        init_result = {"item": object, "uses": uses_list, "Agent": agent.agent_name}
                        init_results.append(init_result)
                    else:
                        combined_prompt = self.construct_response(question, most_recent_responses, agent, is_last_round,baseline = True)
                        formatted_combined_prompt = agent.construct_user_message(agent_role_prompt + combined_prompt)
                        chat_history[agent.agent_name].append(formatted_combined_prompt)
                        response = agent.generate_answer(chat_history[agent.agent_name])
                        if is_last_round:
                            uses_list = self.extract_response(response)
                            final_result = {"item": object, "uses": uses_list, "Agent": agent.agent_name}
                            final_results.append(final_result)

                    formatted_response = agent.construct_assistant_message(response)
                    chat_history[agent.agent_name].append(formatted_response)  # Update the agent's chat history
                    round_responses[agent.agent_name].append(formatted_response)
                most_recent_responses = round_responses
            all_responses[question] = chat_history

        output_file = self.save_debate_conversations(self.agents, all_responses, init_results, final_results, amount_of_data, task_type=self.task_type, baseline=True)
        return output_file

class LLM_Debate_Scientific_Baseline(LLM_Debate):
    def run(self):
        with open(self.dataset_file, 'r') as f:
            dataset = json.load(f)
        all_responses = {}
        init_results = []
        final_results = []
        amount_of_data = 0
        for task in dataset['Task']:
            amount_of_data += len(task['Example'])
            for example in task['Example']:
                chat_history = {agent.agent_name: [] for agent in self.agents}
                # --------------->>>> set the system content
                question = example
                initial_prompt = question
                # ------------------------------------------
                most_recent_responses = {}
                for round in range(self.rounds):
                    is_last_round = (round == self.rounds - 1)
                    is_first_round = (round == 0)
                    round_responses = {agent.agent_name: [] for agent in self.agents}
                    print(f"Round {round + 1}: Discussion on {question}")
                    for agent in self.agents:
                        if agent.agent_role != "None":
                            agent_role_prompt = f"You are a {agent.agent_role} whose specialty is {agent.agent_speciality}. {agent.agent_role_prompt} Remember to claim your role in the beginning of each conversation. "
                            print(f"agent_role = {agent.agent_role}")
                        else:
                            agent_role_prompt = ""

                        if is_first_round:
                            formatted_initial_prompt = agent.construct_user_message(agent_role_prompt + "Can you answer the following question as creatively as possible: " + initial_prompt + " Please put your answer in a list format, starting with 1. ... 2. ... 3. ... and so on.")
                            chat_history[agent.agent_name].append(formatted_initial_prompt)
                            response = agent.generate_answer(chat_history[agent.agent_name])
                            response_list = self.extract_response(response)
                            init_result = {"question": question, "answer": response_list, "Agent": agent.agent_name}
                            init_results.append(init_result)
                        else:
                            combined_prompt = self.construct_response(question, most_recent_responses, agent, is_last_round, baseline = True)
                            formatted_combined_prompt = agent.construct_user_message(agent_role_prompt + combined_prompt)
                            chat_history[agent.agent_name].append(formatted_combined_prompt)
                            response = agent.generate_answer(chat_history[agent.agent_name])
                            if is_last_round:
                                response_list = self.extract_response(response)
                                print(f"response_list = {response_list}")
                                final_result = {"question": question, "answer": response_list, "Agent": agent.agent_name}
                                final_results.append(final_result)

                        formatted_response = agent.construct_assistant_message(response)
                        chat_history[agent.agent_name].append(formatted_response)  # Update the agent's chat history
                        round_responses[agent.agent_name].append(formatted_response)
                    most_recent_responses = round_responses
                all_responses[question] = chat_history

        output_file = self.save_debate_conversations(self.agents, all_responses, init_results, final_results, amount_of_data, task_type=self.task_type, baseline=True)
        return output_file

class LLM_Debate_Instance_Similarities_Baseline(LLM_Debate):
    def run(self):
        with open(self.dataset_file, 'r') as f:
            dataset = json.load(f)
        all_responses = {}
        init_results = []
        final_results = []
        amount_of_data = len(dataset['Examples'])
        for example in dataset['Examples']:
            chat_history = {agent.agent_name: [] for agent in self.agents}
            # --------------->>>> set the system content
            question = example
            initial_prompt = question
            # ------------------------------------------
            most_recent_responses = {}
            for round in range(self.rounds):
                is_last_round = (round == self.rounds - 1)
                is_first_round = (round == 0)
                round_responses = {agent.agent_name: [] for agent in self.agents}
                print(f"Round {round + 1}: Discussion on {question}")
                for agent in self.agents:

                    if agent.agent_role != "None":
                        agent_role_prompt = f"You are a {agent.agent_role} whose specialty is {agent.agent_speciality}. {agent.agent_role_prompt} Remember to claim your role in the beginning of each conversation. "
                        print(f"agent_role = {agent.agent_role}")
                    else:
                        agent_role_prompt = ""

                    if is_first_round:
                        formatted_initial_prompt = agent.construct_user_message(agent_role_prompt + "Can you answer the following question as creatively as possible: " + initial_prompt + " Please put your answer in a list format, starting with 1. ... 2. ... 3. ... and so on.")
                        chat_history[agent.agent_name].append(formatted_initial_prompt)
                        response = agent.generate_answer(chat_history[agent.agent_name])
                        response_list = self.extract_response(response)
                        init_result = {"question": question, "answer": response_list, "Agent": agent.agent_name}
                        init_results.append(init_result)
                    else:
                        combined_prompt = self.construct_response(question, most_recent_responses, agent, is_last_round, baseline = True)
                        formatted_combined_prompt = agent.construct_user_message(agent_role_prompt + combined_prompt)
                        chat_history[agent.agent_name].append(formatted_combined_prompt)
                        response = agent.generate_answer(chat_history[agent.agent_name])
                        # Save Final Result
                        if is_last_round:
                            response_list = self.extract_response(response)
                            final_result = {"question": question, "answer": response_list, "Agent": agent.agent_name}
                            final_results.append(final_result)

                    formatted_response = agent.construct_assistant_message(response)
                    chat_history[agent.agent_name].append(formatted_response)  # Update the agent's chat history
                    round_responses[agent.agent_name].append(formatted_response)
                most_recent_responses = round_responses
            all_responses[question] = chat_history
        output_file = self.save_debate_conversations(self.agents, all_responses, init_results, final_results, amount_of_data, task_type=self.task_type, baseline=True)
        return output_file
    
class LLM_Discussion_AUT(LLM_Debate):
    def run(self):
        print(f"Starting LLM_Debate.run with dataset: {self.dataset_file}")
        with open(self.dataset_file, 'r') as f:
            dataset = json.load(f)
        all_responses = {}
        init_results = []
        final_results = []
        amount_of_data = len(dataset['Examples'])
        for example in dataset['Examples']:
            
            # --------------->>>> set the system content
            chat_history = {agent.agent_name: [] for agent in self.agents}

            object = example['object']
            problem_template = " ".join(dataset["Task"][0]["Problem"])
            question = problem_template.replace("{object}", object)
            print("Discussion Prompt is ", self.discussion_prompt)
            initial_prompt = "Initiate a discussion with others to collectively complete the following task: " + question + self.discussion_prompt
            most_recent_responses = {}
            # ------------------------------------------
            for round in range(self.rounds):
                is_last_round = (round == self.rounds - 1)
                is_first_round = (round == 0)
                round_responses = {agent.agent_name: [] for agent in self.agents}
                print(f"Round {round + 1}, Object: {object}")
                for agent in self.agents:
                    if agent.agent_role != "None":
                        agent_role_prompt = f"You are a {agent.agent_role} whose specialty is {agent.agent_speciality}. {agent.agent_role_prompt} Remember to claim your role in the beginning of each conversation. "
                        print(f"agent_role = {agent.agent_role}")
                    else:
                        agent_role_prompt = ""

                    if is_first_round: 
                        formatted_initial_prompt = agent.construct_user_message(agent_role_prompt + initial_prompt)
                        chat_history[agent.agent_name].append(formatted_initial_prompt)
                        response = agent.generate_answer(chat_history[agent.agent_name])
                        # Save the initial response of the Agent
                        uses_list = self.extract_response(response)
                        init_result = {"item": object, "uses": uses_list, "Agent": agent.agent_name}
                        init_results.append(init_result)

                    else:
                        combined_prompt = self.construct_response(question, most_recent_responses, agent, is_last_round, object = object)
                        formatted_combined_prompt = agent.construct_user_message(agent_role_prompt + combined_prompt)
                        chat_history[agent.agent_name].append(formatted_combined_prompt)
                        response = agent.generate_answer(chat_history[agent.agent_name])
                        # Save Final Result of the Agent
                        if is_last_round:
                            uses_list = self.extract_response(response)
                            final_result = {"item": object, "uses": uses_list, "Agent": agent.agent_name}
                            final_results.append(final_result)

                    formatted_response = agent.construct_assistant_message(response)
                    chat_history[agent.agent_name].append(formatted_response)  # Update the agent's chat history
                    round_responses[agent.agent_name].append(formatted_response)
                most_recent_responses = round_responses
            all_responses[question] = chat_history

        output_file = self.save_debate_conversations(self.agents, all_responses, init_results, final_results, amount_of_data, task_type=self.task_type)
        return output_file

class LLM_Discussion_Scientific(LLM_Debate):
    def run(self):
        with open(self.dataset_file, 'r') as f:
            dataset = json.load(f)
        all_responses = {}
        init_results = []
        final_results = []
        amount_of_data = 0
        for task in dataset['Task']:
            amount_of_data += len(task['Example'])
            for example in task['Example']:
                chat_history = {agent.agent_name: [] for agent in self.agents}
                # --------------->>>> set the system content
                question = example
                initial_prompt = "Initiate a discussion with others to collectively complete the following task: " + question + self.discussion_prompt
                # ------------------------------------------
                most_recent_responses = {}
                for round in range(self.rounds):
                    is_last_round = (round == self.rounds - 1)
                    is_first_round = (round == 0)
                    round_responses = {agent.agent_name: [] for agent in self.agents}
                    print(f"Round {round + 1}: Discussion on {question}")
                    for agent in self.agents:
                        if agent.agent_role != "None":
                            agent_role_prompt = f"You are a {agent.agent_role} whose specialty is {agent.agent_speciality}. {agent.agent_role_prompt} Remember to claim your role in the beginning of each conversation. "
                            print(f"agent_role = {agent.agent_role}")
                        else:
                            agent_role_prompt = ""

                        if is_first_round:
                            formatted_initial_prompt = agent.construct_user_message(agent_role_prompt + initial_prompt)
                            chat_history[agent.agent_name].append(formatted_initial_prompt)
                            response = agent.generate_answer(chat_history[agent.agent_name])
                            response_list = self.extract_response(response)
                            init_result = {"question": question, "answer": response_list, "Agent": agent.agent_name}
                            init_results.append(init_result)
                        else:
                            combined_prompt = self.construct_response(question, most_recent_responses, agent, is_last_round)
                            formatted_combined_prompt = agent.construct_user_message(agent_role_prompt + combined_prompt)
                            chat_history[agent.agent_name].append(formatted_combined_prompt)
                            response = agent.generate_answer(chat_history[agent.agent_name])
                            # Save Final Result
                            if is_last_round:
                                response_list = self.extract_response(response)
                                print(f"response_list = {response_list}")
                                final_result = {"question": question, "answer": response_list, "Agent": agent.agent_name}
                                final_results.append(final_result)

                        formatted_response = agent.construct_assistant_message(response)
                        chat_history[agent.agent_name].append(formatted_response)  # Update the agent's chat history
                        round_responses[agent.agent_name].append(formatted_response)
                    most_recent_responses = round_responses
                all_responses[question] = chat_history

        output_file = self.save_debate_conversations(self.agents, all_responses, init_results, final_results, amount_of_data, task_type=self.task_type)
        return output_file

class LLM_Discussion_Instance_Similarities(LLM_Debate):
    def run(self):
        with open(self.dataset_file, 'r') as f:
            dataset = json.load(f)
        all_responses = {}
        init_results = []
        final_results = []
        amount_of_data = len(dataset['Examples'])
        for example in dataset['Examples']:
            chat_history = {agent.agent_name: [] for agent in self.agents}
            # print("initial chat_history: ", chat_history, "\n")
            # --------------->>>> set the system content
            question = example
            initial_prompt = "Initiate a discussion with others to collectively complete the following task: " + question + self.discussion_prompt
            # ------------------------------------------
            most_recent_responses = {}
            for round in range(self.rounds):
                is_last_round = (round == self.rounds - 1)
                is_first_round = (round == 0)
                round_responses = {agent.agent_name: [] for agent in self.agents}
                print(f"Round {round + 1}: Discussion on {question}")
                for agent in self.agents:

                    if agent.agent_role != "None":
                        agent_role_prompt = f"You are a {agent.agent_role} whose specialty is {agent.agent_speciality}. {agent.agent_role_prompt} Remember to claim your role in the beginning of each conversation. "
                        print(f"agent_role = {agent.agent_role}")
                    else:
                        agent_role_prompt = ""

                    if is_first_round:
                        formatted_initial_prompt = agent.construct_user_message(agent_role_prompt + initial_prompt)
                        chat_history[agent.agent_name].append(formatted_initial_prompt)
                        response = agent.generate_answer(chat_history[agent.agent_name])
                        response_list = self.extract_response(response)
                        init_result = {"question": question, "answer": response_list, "Agent": agent.agent_name}
                        init_results.append(init_result)
                    else:
                        combined_prompt = self.construct_response(question, most_recent_responses, agent, is_last_round)
                        formatted_combined_prompt = agent.construct_user_message(agent_role_prompt + combined_prompt)
                        chat_history[agent.agent_name].append(formatted_combined_prompt)
                        response = agent.generate_answer(chat_history[agent.agent_name])

                        # Save Final Result
                        if is_last_round:
                            response_list = self.extract_response(response)
                            print(f"response_list = {response_list}")
                            final_result = {"question": question, "answer": response_list, "Agent": agent.agent_name}
                            final_results.append(final_result)

                    formatted_response = agent.construct_assistant_message(response)
                    chat_history[agent.agent_name].append(formatted_response)  # Update the agent's chat history
                    round_responses[agent.agent_name].append(formatted_response)
                most_recent_responses = round_responses
            all_responses[question] = chat_history
        output_file = self.save_debate_conversations(self.agents, all_responses, init_results, final_results, amount_of_data, task_type=self.task_type)
        return output_file