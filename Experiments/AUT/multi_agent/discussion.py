import json
import re
from agents import OpenAIAgent, GeminiAgent, Llama2Agent
import datetime
import random


class Discussion:
    def __init__(self, dataset_file, rounds):
        self.dataset_file = dataset_file
        self.rounds = rounds
        self.discussion_prompt = " Engage in a collaborative discussion where each of you contributes a unique insight or query, aiming to delve into uncharted territories of thought. Throughout the discussion, focus on expanding the scope and depth of each contribution through constructive feedback, counterpoints, and further questioning. The objective is to achieve a broad spectrum of ideas and solutions, promoting a culture of continuous learning and innovation."
        print("Discussion initialized with dataset: {} and {} rounds.".format(dataset_file, rounds))

    def run(self):
        pass

    def save_conversation(self, filename, conversation_data):
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
    def __init__(self, agents_config, dataset_file, rounds, task):
        super().__init__(dataset_file, rounds)
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
                                          agent_name = config['agent_name']))
            elif config['type'] == 'llama2':
                agents.append(Llama2Agent(ckpt_dir=config['ckpt_dir'], 
                                          tokenizer_path=config['tokenizer_path'], 
                                          agent_name = config['agent_name']))
            else:
                raise ValueError(f"Unsupported agent type: {config['type']}")
        return agents
    
    def construct_response(self, question, most_recent_responses, current_agent, is_last_round, object = "None"):
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
        prefix_string += question
        if is_last_round:
            if self.task_type == "AUT":
                prefix_string += f"This is the last round of the discussion. Please accumulate all the valuable answers for the creative use of {object} from the entire discussion. Note that diversity, originality, number of answers, and the amount of details of each answer are all important. Please list the answer in 1. ... 2. ... 3. ... and so on.\n\n"
                # prefix_string += f"This is the last round of the discussion, please only present a list of the most creative uses of {object} as your final answers. Please list the answer in 1. ... 2. ... 3. ... and so on.\n\n"
            else:
                prefix_string += "This is the last round of the discussion. Please accumulate all the valuable answers from the entire discussion. Note that diversity, originality, number of answers, and the amount of details of each answer are all important. Please list the answer in 1. ... 2. ... 3. ... and so on.\n\n"
                #prefix_string += f"This is the last round of the discussion, please only present a list of your final answers. Please list the final response in 1. ... 2. ... 3. ... and so on. \n\n"
        else:
            prefix_string += self.discussion_prompt
        return prefix_string
    
    def save_debate_conversations(self, agents, all_responses, init_results, final_results, amount_of_data, task_type="AUT"):
        current_time = datetime.datetime.now()
        current_date = datetime.date.today().strftime("%Y-%m-%d")
        formatted_time = current_time.strftime("%H-%M-%S")
        if all(agent.model_name == agents[0].model_name for agent in agents):
            model_names_concatenated = agents[0].model_name.replace(".", "-")
        else:
            model_names_concatenated = "-".join(agent.model_name.replace(".", "-") for agent in agents)

        if all(agent.agent_role == "None" for agent in agents):
            role_names_concatenated = "None"
            subtask = "default"
        else:
            role_names_concatenated = "-".join(agent.agent_role.replace(" ", "") for agent in agents)
            subtask = "roleplay"
        
        output_filename = f"../../../Results/{task_type}/chat_log/{task_type}_multi_debate_{subtask}_{len(self.agents)}_{self.rounds}_{model_names_concatenated}_{role_names_concatenated}_log_{current_date}-{formatted_time}_{amount_of_data}.json"
        final_ans_filename = f"../../../Results/{task_type}/Output/multi_agent/{task_type}_multi_debate_{subtask}_{len(self.agents)}_{self.rounds}_{model_names_concatenated}_{role_names_concatenated}_final_{current_date}-{formatted_time}_{amount_of_data}.json"
        init_ans_filename = f"../../../Results/{task_type}/init/{task_type}_multi_debate_{subtask}_{len(self.agents)}_{self.rounds}_{model_names_concatenated}_{role_names_concatenated}_init_{current_date}-{formatted_time}_{amount_of_data}.json"
        
        self.save_conversation(output_filename, all_responses)
        self.save_conversation(final_ans_filename, final_results)
        self.save_conversation(init_ans_filename, init_results)

        return f"{task_type}_multi_debate_{subtask}_{len(self.agents)}_{self.rounds}_{model_names_concatenated}_{role_names_concatenated}_final_{current_date}-{formatted_time}_{amount_of_data}.json"

class LLM_Debate_AUT(LLM_Debate):
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
                        # First Round If Statement
                        formatted_initial_prompt = agent.construct_user_message(agent_role_prompt + initial_prompt)
                        chat_history[agent.agent_name].append(formatted_initial_prompt)
                        print("Round: ",round, ", Agent: ", agent.agent_name,", INPUT: ", chat_history[agent.agent_name], "\n")
                        response = agent.generate_answer(chat_history[agent.agent_name])
                        print("OUTPUT: ", response, "\n")

                        # Save the initial response of the Agent
                        uses_list = self.extract_response(response)
                        init_result = {"item": object, "uses": uses_list, "Agent": agent.agent_name}
                        init_results.append(init_result)

                    else:
                        combined_prompt = self.construct_response(question, most_recent_responses, agent, is_last_round, object = object)
                        formatted_combined_prompt = agent.construct_user_message(agent_role_prompt + combined_prompt)
                        chat_history[agent.agent_name].append(formatted_combined_prompt)
                        print("Round: ",round, ", Agent: ", agent.agent_name,", INPUT: ", chat_history[agent.agent_name], "\n")
                        response = agent.generate_answer(chat_history[agent.agent_name])
                        print("OUTPUT: ", response, "\n")
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

class LLM_Debate_Scientific(LLM_Debate):
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
                # prompt_9 = "You are in a group discussion with other teammates; as a result, you should answer as diverge and creative as you can. "
                # question_prompt_9 = question + "\n" + prompt_9
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
                            print("most_recent_responses: ", most_recent_responses)
                            combined_prompt = self.construct_response(question, most_recent_responses, agent, is_last_round)
                            formatted_combined_prompt = agent.construct_user_message(agent_role_prompt + combined_prompt)
                            chat_history[agent.agent_name].append(formatted_combined_prompt)
                            print("INPUT TO GENERATE: ", chat_history[agent.agent_name], "\n")
                            response = agent.generate_answer(chat_history[agent.agent_name])
                            print("OUTPUT FROM GENERATE: ", response, "\n")
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

class LLM_Debate_Instance_Similarities(LLM_Debate):
    def run(self):
        with open(self.dataset_file, 'r') as f:
            dataset = json.load(f)
        all_responses = {}
        init_results = []
        final_results = []
        amount_of_data = len(dataset['Examples'])
        for example in dataset['Examples']:
            chat_history = {agent.agent_name: [] for agent in self.agents}
            print("initial chat_history: ", chat_history, "\n")
            # --------------->>>> set the system content
            question = example
            # prompt_9 = "You are in a group discussion with other teammates; as a result, you should answer as diverge and creative as you can. "
            # question_prompt_9 = question + "\n" + prompt_9
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
                        print("formatted_initial_prompt: ", formatted_initial_prompt, "\n")
                        print(f"Agent {agent.agent_name} chat history: {chat_history[agent.agent_name]}","\n")
                        response = agent.generate_answer(chat_history[agent.agent_name])
                        print("OUTPUT FROM GENERATE: ", response, "\n")
                        # Save the initial response for the agent
                        response_list = self.extract_response(response)
                        print(f"response_list = {response_list}")
                        init_result = {"question": question, "answer": response_list, "Agent": agent.agent_name}
                        init_results.append(init_result)
                    else:
                        print("most_recent_responses: ", most_recent_responses)
                        combined_prompt = self.construct_response(question, most_recent_responses, agent, is_last_round)
                        formatted_combined_prompt = agent.construct_user_message(agent_role_prompt + combined_prompt)
                        chat_history[agent.agent_name].append(formatted_combined_prompt)
                        print("INPUT TO GENERATE: ", chat_history[agent.agent_name], "\n")
                        response = agent.generate_answer(chat_history[agent.agent_name])
                        print("OUTPUT FROM GENERATE: ", response, "\n")

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


class Conversational(Discussion):
    def __init__(self, agents_config, dataset_file, rounds, task, agent_role_str=""):
        super().__init__(dataset_file, rounds)
        self.agent_roles_str = agent_role_str
        self.agents = self.initialize_agents(agents_config)
        self.task_type = task
        
    def initialize_agents(self, agents_config):
        agents = []
        for config in agents_config:
            if config['type'] == 'openai':
                agents.append(OpenAIAgent(model_name=config['model_name'], agent_name = config['agent_name'], agent_role = config['agent_role'], agent_speciality = config['agent_speciality'], agent_role_prompt = config['agent_role_prompt'], speaking_rate = config['speaking_rate']))
            # elif config['type'] == 'gemini':
            #     agents.append(GeminiAgent(model_name=config['model_name'], agent_name = config['agent_name']))
            # elif config['type'] == 'llama2':
            #     agents.append(Llama2Agent(ckpt_dir=config['ckpt_dir'], tokenizer_path=config['tokenizer_path'], agent_name = config['agent_name']))
                self.agent_roles_str += config['agent_role'].replace(" ", "") + "-"
            else:
                raise ValueError(f"Unsupported agent type: {config['type']}")
        print(f"Initialized {len(agents)} agents.")
        print("The agents are: ", agents)
        return agents
    
    def construct_response(self, question, most_recent_responses, current_agent, is_last_round, object = "None"):
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
        prefix_string += question
        if is_last_round:
            if self.task_type == "AUT":
                prefix_string += f"This is the last round of the discussion, please only present a list of the most creative uses of {object} as your final answers. Please list the answer in 1. ... 2. ... 3. ... and so on.\n\n"
            else:
                prefix_string += f"This is the last round of the discussion, please only present a list of your final answers. Please list the final response in 1. ... 2. ... 3. ... and so on. \n\n"
        
        return prefix_string
    
    def save_convo_conversations(self, agents, all_responses, init_results, final_results, amount_of_data, task_type="AUT"):
        current_time = datetime.datetime.now()
        current_date = datetime.date.today().strftime("%Y-%m-%d")
        formatted_time = current_time.strftime("%H-%M-%S")
        if all(agent.model_name == agents[0].model_name for agent in agents):
            model_names_concatenated = agents[0].model_name.replace(".", "-")
        else:
            model_names_concatenated = "-".join(agent.model_name.replace(".", "-") for agent in agents)

        if all(agent.agent_role == "None" for agent in agents):
            role_names_concatenated = "None"
            subtask = "default"
        else:
            role_names_concatenated = "-".join(agent.agent_role.replace(" ", "") for agent in agents)
            subtask = "roleplay"
        
        output_filename = f"../../../Results/{task_type}/chat_log/{task_type}_multi_convo_{subtask}_{len(self.agents)}_{self.rounds}_{model_names_concatenated}_{role_names_concatenated}_log_{current_date}-{formatted_time}_{amount_of_data}.json"
        final_ans_filename = f"../../../Results/{task_type}/Output/multi_agent/{task_type}_multi_convo_{subtask}_{len(self.agents)}_{self.rounds}_{model_names_concatenated}_{role_names_concatenated}_final_{current_date}-{formatted_time}_{amount_of_data}.json"
        init_ans_filename = f"../../../Results/{task_type}/init/{task_type}_multi_convo_{subtask}_{len(self.agents)}_{self.rounds}_{model_names_concatenated}_{role_names_concatenated}_init_{current_date}-{formatted_time}_{amount_of_data}.json"
        
        self.save_conversation(output_filename, all_responses)
        self.save_conversation(final_ans_filename, final_results)
        self.save_conversation(init_ans_filename, init_results)

        return f"{task_type}_multi_convo_{subtask}_{len(self.agents)}_{self.rounds}_{model_names_concatenated}_{role_names_concatenated}_final_{current_date}-{formatted_time}_{amount_of_data}.json"

class Conversational_AUT(Conversational):
    def run(self):
        with open(self.dataset_file, 'r') as f:
            dataset = json.load(f)
        all_responses = {}
        init_results = []
        final_results = []
        amount_of_data = len(dataset['Examples'])
        for example in dataset['Examples']:
            round_empty = True
            chat_history = {agent.agent_name: [] for agent in self.agents}
            # --------------->>>> set the system content
            object = example['object']
            problem_template = " ".join(dataset["Task"][0]["Problem"])
            question = problem_template.replace("{object}", object)
            #prompt_9 = "You are in a group discussion with other teammates; as a result, you should answer as diverge and creative as you can. "
            #question_prompt_9 = question + "\n" + prompt_9
            initial_prompt = "Initiate a discussion with others to collectively complete the following task: " + question
            # ------------------------------------------
            most_recent_responses = {}
            for round in range(self.rounds):
                is_last_round = (round == self.rounds - 1)
                is_first_round = (round == 0)
                print(f"Round {round + 1}: Discussion on {object}")
                for agent in self.agents:
                    skip = False
                    if agent.agent_role != "None":
                        agent_role_prompt = f"You are a {agent.agent_role} whose specialty is {agent.agent_speciality}. {agent.agent_role_prompt} Remember to claim your role in the beginning of each conversation. "
                        print(f"agent_role = {agent.agent_role}")
                    else:
                        agent_role_prompt = ""
                    # if random.random() <= agent.speaking_rate:
                    if is_first_round and round_empty:
                        round_empty = False
                        formatted_initial_prompt = agent.construct_user_message(agent_role_prompt + initial_prompt)
                        chat_history[agent.agent_name].append(formatted_initial_prompt)
                        response = agent.generate_answer(chat_history[agent.agent_name])
                        
                        # Save to initial result
                        uses_list = self.extract_response(response)
                        init_result = {"item": object, "uses": uses_list, "Agent": agent.agent_name}
                        init_results.append(init_result)
                    elif is_first_round:
                        # print("most_recent_responses: ", most_recent_responses)
                        # self, question, most_recent_responses, current_agent, is_last_round, object = "None"
                        combined_prompt = self.construct_response("", most_recent_responses, agent, is_last_round, object = object)
                        formatted_combined_prompt = agent.construct_user_message(agent_role_prompt +"Initiate a discussion with others to collectively complete the following task: " + question + " "+ combined_prompt)
                        chat_history[agent.agent_name].append(formatted_combined_prompt)
                        # print("INPUT TO GENERATE: ", chat_history[agent.agent_name], "\n")
                        response = agent.generate_answer(chat_history[agent.agent_name])
                        print("OUTPUT FROM GENERATE: ", response, "\n")
                    elif is_last_round:

                        if agent.missing_history: 
                            #this agent was skipped 
                            missing_prompt = agent.construct_missing_history(agent.missing_history, agent)
                            agent.missing_history = [] #reset to empty
                        else:
                            missing_prompt = ""
                        # print("most_recent_responses: ", most_recent_responses)
                        combined_prompt = self.construct_response(question, most_recent_responses, agent, is_last_round, object=object)
                        formatted_combined_prompt = agent.construct_user_message(agent_role_prompt + missing_prompt + combined_prompt)
                        chat_history[agent.agent_name].append(formatted_combined_prompt)
                        # print("INPUT TO GENERATE: ", chat_history[agent.agent_name], "\n")
                        response = agent.generate_answer(chat_history[agent.agent_name])
                        print("OUTPUT FROM GENERATE: ", response, "\n")
                        uses_list = self.extract_response(response)
                        # print(f"uses_list = {uses_list}")
                        final_result = {"item": object, "uses": uses_list, "Agent": agent.agent_name}
                        final_results.append(final_result)
                    else:
                        prob = random.random()
                        print (f"prob = {prob}")
                        if prob > agent.speaking_rate:
                            #agent skip this round
                            skip = True
                            print(f"######################## S K I P P E D ########################")
                        if skip:
                            #skip for this round
                            agent.missing_history.append(most_recent_responses)

                            if most_recent_responses.get(agent.agent_name):
                                del most_recent_responses[agent.agent_name]
                                continue
                        else: #agent speaking
                            
                            if agent.missing_history: 
                                #this agent was skipped 
                                missing_prompt = agent.construct_missing_history(agent.missing_history, agent)
                                agent.missing_history = [] #reset to empty
                            else:
                                missing_prompt = ""
                            combined_prompt = self.construct_response(question, most_recent_responses, agent, is_last_round, object= object)
                            formatted_combined_prompt = agent.construct_user_message(agent_role_prompt + missing_prompt + combined_prompt)
                            chat_history[agent.agent_name].append(formatted_combined_prompt)
                            # print("INPUT TO GENERATE: ", chat_history[agent.agent_name], "\n")
                            response = agent.generate_answer(chat_history[agent.agent_name])
                            print("OUTPUT FROM GENERATE: ", response, "\n")
                
                    if not skip:
                        formatted_response = agent.construct_assistant_message(response)
                        chat_history[agent.agent_name].append(formatted_response)    
                        most_recent_responses[agent.agent_name] = [formatted_response]
                        # print(f"most_recent_responses = {most_recent_responses}")
            all_responses[question] = chat_history
        output_file = self.save_convo_conversations(self.agents, all_responses, init_results, final_results, amount_of_data, task_type=self.task_type)
        return output_file
    

    def construct_missing_history(self, missing_history, current_agent):
        prefix_string = "These are the previous rounds of discussion to the problem from other agents:\n"
        for round_history in missing_history:
            prefix_string += "One round discussion:{"
            for agent_name, responses in round_history.items():
                if agent_name == current_agent.agent_name:
                    continue
                print("-----------------------------------------")
                print(agent_name)
                print(responses)
                if responses and 'parts' in responses[-1]:
                    print("IN GEMINI")
                    response_content = responses[-1]['parts'][0]
                else:
                    print("IN GPT")
                    response_content = responses[-1]['content']

                other_agent_response = f"One agent solution: ```{response_content}```\n"
                prefix_string += other_agent_response
            prefix_string += "}. \n"
        return prefix_string
    

class Conversational_Scientific(Conversational):
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
                round_empty = True
                chat_history = {agent.agent_name: [] for agent in self.agents}
                # --------------->>>> set the system content
                question = example
                initial_prompt = "Initiate a discussion with others to collectively complete the following task: " + question
                # ------------------------------------------
                most_recent_responses = {}
                for round in range(self.rounds):
                    is_last_round = (round == self.rounds - 1)
                    is_first_round = (round == 0)
                    print(f"Round {round + 1}: Discussion on {question}")
                    for agent in self.agents:
                        skip = False
                        if agent.agent_role != "None":
                            agent_role_prompt = f"You are a {agent.agent_role} whose specialty is {agent.agent_speciality}. {agent.agent_role_prompt} Remember to claim your role in the beginning of each conversation. "
                            print(f"agent_role = {agent.agent_role}")
                        else:
                            agent_role_prompt = ""
                        if is_first_round and round_empty:
                            round_empty = False
                            formatted_initial_prompt = agent.construct_user_message(agent_role_prompt + initial_prompt)
                            chat_history[agent.agent_name].append(formatted_initial_prompt)
                            response = agent.generate_answer(chat_history[agent.agent_name])
                            
                            # Save to initial result
                            response_list = self.extract_response(response)
                            init_result = {"question": question, "answer": response_list, "Agent": agent.agent_name}
                            init_results.append(init_result)
                        elif is_first_round:
                            # print("most_recent_responses: ", most_recent_responses)
                            combined_prompt = self.construct_response("", most_recent_responses, agent, is_last_round)
                            formatted_combined_prompt = agent.construct_user_message(agent_role_prompt +"Initiate a discussion with others to collectively complete the following task: " + question + " "+ combined_prompt)
                            chat_history[agent.agent_name].append(formatted_combined_prompt)
                            # print("INPUT TO GENERATE: ", chat_history[agent.agent_name], "\n")
                            response = agent.generate_answer(chat_history[agent.agent_name])
                            print("OUTPUT FROM GENERATE: ", response, "\n")
                        elif is_last_round:

                            if agent.missing_history: 
                                #this agent was skipped 
                                missing_prompt = agent.construct_missing_history(agent.missing_history, agent)
                                agent.missing_history = [] #reset to empty
                            else:
                                missing_prompt = ""
                            # print("most_recent_responses: ", most_recent_responses)
                            combined_prompt = self.construct_response(question, most_recent_responses, agent, is_last_round)
                            formatted_combined_prompt = agent.construct_user_message(agent_role_prompt + missing_prompt + combined_prompt)
                            chat_history[agent.agent_name].append(formatted_combined_prompt)
                            # print("INPUT TO GENERATE: ", chat_history[agent.agent_name], "\n")
                            response = agent.generate_answer(chat_history[agent.agent_name])
                            print("OUTPUT FROM GENERATE: ", response, "\n")
                            response_list = self.extract_response(response)
                            # print(f"uses_list = {uses_list}")
                            final_result = {"question": question, "answer": response_list, "Agent": agent.agent_name}
                            final_results.append(final_result)
                        else:
                            prob = random.random()
                            # print (f"prob = {prob}")
                            if prob > agent.speaking_rate:
                                #agent skip this round
                                skip = True
                                print(f"######################## S K I P P E D ########################")
                            if skip:
                                #skip for this round
                                agent.missing_history.append(most_recent_responses)

                                if most_recent_responses.get(agent.agent_name):
                                    del most_recent_responses[agent.agent_name]
                                    continue
                            else: #agent speaking
                                
                                if agent.missing_history: 
                                    #this agent was skipped 
                                    missing_prompt = agent.construct_missing_history(agent.missing_history, agent)
                                    agent.missing_history = [] #reset to empty
                                else:
                                    missing_prompt = ""
                                combined_prompt = self.construct_response(question, most_recent_responses, agent, is_last_round)
                                formatted_combined_prompt = agent.construct_user_message(agent_role_prompt + missing_prompt + combined_prompt)
                                chat_history[agent.agent_name].append(formatted_combined_prompt)
                                # print("INPUT TO GENERATE: ", chat_history[agent.agent_name], "\n")
                                response = agent.generate_answer(chat_history[agent.agent_name])
                                print("OUTPUT FROM GENERATE: ", response, "\n")
                    
                        if not skip:
                            formatted_response = agent.construct_assistant_message(response)
                            chat_history[agent.agent_name].append(formatted_response)    
                            most_recent_responses[agent.agent_name] = [formatted_response]
                            # print(f"most_recent_responses = {most_recent_responses}")
                all_responses[question] = chat_history
        output_file = self.save_convo_conversations(self.agents, all_responses, init_results, final_results, amount_of_data, task_type=self.task_type)
        return output_file
    

    def construct_missing_history(self, missing_history, current_agent):
        prefix_string = "These are the previous rounds of discussion to the problem from other agents:\n"
        for round_history in missing_history:
            prefix_string += "One round discussion:{"
            for agent_name, responses in round_history.items():
                if agent_name == current_agent.agent_name:
                    continue
                print("-----------------------------------------")
                print(agent_name)
                print(responses)
                if responses and 'parts' in responses[-1]:
                    print("IN GEMINI")
                    response_content = responses[-1]['parts'][0]
                else:
                    print("IN GPT")
                    response_content = responses[-1]['content']

                other_agent_response = f"One agent solution: ```{response_content}```\n"
                prefix_string += other_agent_response
            prefix_string += "}. \n"
        return prefix_string


    
    
