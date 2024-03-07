import json
import re
from agents import OpenAIAgent, GeminiAgent, Llama2Agent
import datetime


class Discussion:
    def __init__(self, agents_config, dataset_file, rounds):
        self.agents = self.initialize_agents(agents_config)
        self.dataset_file = dataset_file
        self.rounds = rounds

    def initialize_agents(self, agents_config):
        agents = []
        for config in agents_config:
            if config['type'] == 'openai':
                agents.append(OpenAIAgent(model_name=config['model_name'], agent_name = config['agent_name']))
            elif config['type'] == 'gemini':
                agents.append(GeminiAgent(model_name=config['model_name'], agent_name = config['agent_name']))
            elif config['type'] == 'llama2':
                agents.append(Llama2Agent(ckpt_dir=config['ckpt_dir'], tokenizer_path=config['tokenizer_path'], agent_name = config['agent_name']))
            else:
                raise ValueError(f"Unsupported agent type: {config['type']}")
        print(f"Initialized {len(agents)} agents.")
        print("The agents are: ", agents)
        return agents

    def run(self):
        pass

    def save_conversation(self, filename, conversation_data):
        with open(filename, 'w') as file:
            json.dump(conversation_data, file, indent=4)
        print(f"Saved data to {filename}")

    @staticmethod
    def load_config(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
        
    def extract_response(self, content):
        lines = content.split('\n')
        uses = [line.strip() for line in lines if line.strip() and re.match(r"^\d+\.", line)]
        uses = [use[use.find('.') + 2:] for use in uses]
        return uses
    
    def save_debate_conversations(self, agents, all_responses, init_results, final_results, amount_of_data, task_type="AUT"):
        current_time = datetime.datetime.now()
        current_date = datetime.date.today().strftime("%Y-%m-%d_")
        formatted_time = current_time.strftime("%H-%M-%S")
        model_names_concatenated = "-".join(agent.model_name.replace(".", "-") for agent in agents)
            
        output_filename = f"../../../Results/{task_type}/chat_log/{task_type}_multi_debate-prompt-9_{len(self.agents)}_{self.rounds}_{model_names_concatenated}_log_{current_date}{formatted_time}_{amount_of_data}.json"
        final_ans_filename = f"../../../Results/{task_type}/Output/multi_agent/{task_type}_multi_debate-prompt-9_{len(self.agents)}_{self.rounds}_{model_names_concatenated}_discussion_final_{current_date}{formatted_time}_{amount_of_data}.json"
        init_ans_filename = f"../../../Results/{task_type}/Output/multi_agent/{task_type}_multi_debate-prompt-9_{len(self.agents)}_{self.rounds}_{model_names_concatenated}_discussion_init_{current_date}{formatted_time}_{amount_of_data}.json"
        self.save_conversation(output_filename, all_responses)
        self.save_conversation(final_ans_filename, final_results)
        self.save_conversation(init_ans_filename, init_results)


class LLM_Debate_AUT(Discussion):
    # def __init__(self, agents_config, dataset_file, rounds, additional_param):
    #     super().__init__(agents_config, dataset_file, rounds)
    #     self.additional_param = additional_param

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
            object = example['object']
            problem_template = " ".join(dataset["Task"][0]["Problem"])
            question = problem_template.replace("{object}", object)
            prompt_9 = "You would be in a group discussion with other teammates as a result, you should answer as diverge and creative as you can."
            question_prompt_9 = question + "\n" + prompt_9
            initial_prompt = "Initiate a discussion with others to collectively complete the following task: " + question_prompt_9
            # ------------------------------------------
            most_recent_responses = {}
            for round in range(self.rounds):
                is_last_round = (round == self.rounds - 1)
                is_first_round = (round == 0)
                round_responses = {agent.agent_name: [] for agent in self.agents}
                print(f"Round {round + 1}: Discussion on {object}")
                for agent in self.agents:
                    if is_first_round:
                        formatted_initial_prompt = agent.construct_user_message(initial_prompt)
                        chat_history[agent.agent_name].append(formatted_initial_prompt)
                        print("formatted_initial_prompt: ", formatted_initial_prompt, "\n")
                        print(f"Agent {agent.agent_name} chat history: {chat_history[agent.agent_name]}","\n")
                        response = agent.generate_answer(chat_history[agent.agent_name])
                        print("OUTPUT FROM GENERATE: ", response, "\n")
                        # Save the initial response for the agent
                        uses_list = self.extract_response(response)
                        print(f"uses_list = {uses_list}")
                        init_result = {"item": object, "uses": uses_list, "Agent": agent.agent_name}
                        init_results.append(init_result)
                    else:
                        print("most_recent_responses: ", most_recent_responses)
                        combined_prompt = self.construct_response(question_prompt_9, most_recent_responses, agent, object, is_last_round)
                        formatted_combined_prompt = agent.construct_user_message(combined_prompt)
                        chat_history[agent.agent_name].append(formatted_combined_prompt)
                        print("INPUT TO GENERATE: ", chat_history[agent.agent_name], "\n")
                        response = agent.generate_answer(chat_history[agent.agent_name])
                        print("OUTPUT FROM GENERATE: ", response, "\n")

                        # Save Final Result
                        if is_last_round:
                            uses_list = self.extract_response(response)
                            print(f"uses_list = {uses_list}")
                            final_result = {"item": object, "uses": uses_list, "Agent": agent.agent_name}
                            final_results.append(final_result)

                    formatted_response = agent.construct_assistant_message(response)
                    chat_history[agent.agent_name].append(formatted_response)  # Update the agent's chat history
                    round_responses[agent.agent_name].append(formatted_response)
                most_recent_responses = round_responses
            all_responses[question] = chat_history

        self.save_debate_conversations(self.agents, all_responses, init_results, final_results, amount_of_data, task_type="AUT")

    def construct_response(self, question, most_recent_responses, current_agent, object, is_last_round):
        prefix_string = "These are the solutions to the problem from other agents:\n"
        for agent_name, responses in most_recent_responses.items():
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

        if is_last_round:
            prefix_string += f"This is the last round of the discussion. Please present only the most creative uses of {object} as your final answers. List your responses as: 1. ..., 2. ..., 3. ..., and so on.\n\n"
#         else:
#             discussion_prompt =  "You are an active and helpful member in this discussion. \
# You should persuade each other that your answers are creative by giving reasonable explanations, be critical to verify each answer to see if it is creative enough,\
# justify your own answers, integrate with others' replies, coming up with ideas inspired by others, \
# remove answers that is not creative enough, merge similar ideas, and ask questions for further understandings.\n\n"
#             prefix_string += discussion_prompt
        prefix_string += question
        print("Constructed Response", prefix_string)
        return prefix_string
    


class LLM_Debate_Scientific(Discussion):
    # def __init__(self, agents_config, dataset_file, rounds, additional_param):
    #     super().__init__(agents_config, dataset_file, rounds)
    #     self.additional_param = additional_param

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
                print("initial chat_history: ", chat_history, "\n")
                # --------------->>>> set the system content
                question = example
                prompt_9 = "You would be in a group discussion with other teammates as a result, you should answer as diverge and creative as you can."
                question_prompt_9 = question + "\n" + prompt_9
                initial_prompt = "Initiate a discussion with others to collectively complete the following task: " + question_prompt_9
                # ------------------------------------------
                most_recent_responses = {}
                for round in range(self.rounds):
                    is_last_round = (round == self.rounds - 1)
                    is_first_round = (round == 0)
                    round_responses = {agent.agent_name: [] for agent in self.agents}
                    print(f"Round {round + 1}: Discussion on {question}")
                    for agent in self.agents:
                        if is_first_round:
                            formatted_initial_prompt = agent.construct_user_message(initial_prompt)
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
                            combined_prompt = self.construct_response(question_prompt_9, most_recent_responses, agent, is_last_round)
                            formatted_combined_prompt = agent.construct_user_message(combined_prompt)
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

        self.save_debate_conversations(self.agents, all_responses, init_results, final_results, amount_of_data, task_type="Scientific")

    def construct_response(self, question, most_recent_responses, current_agent, is_last_round):
        prefix_string = "These are the solutions to the problem from other agents:\n"
        for agent_name, responses in most_recent_responses.items():
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

        if is_last_round:
            prefix_string += f"This is the last round of the discussion, please only present a list of your final answers. Please list the final response in 1. ... 2. ... 3. ... and so on. \n\n"
#         else:
#             discussion_prompt =  "You are an active and helpful member in this discussion. \
# You should persuade each other that your answers are creative by giving reasonable explanations, be critical to verify each answer to see if it is creative enough,\
# justify your own answers, integrate with others' replies, coming up with ideas inspired by others, \
# remove answers that is not creative enough, merge similar ideas, and ask questions for further understandings.\n\n"
#             prefix_string += discussion_prompt
        prefix_string += question
        print("Constructed Response", prefix_string)
        return prefix_string
    

class LLM_Debate_Instance_Similarities(Discussion):
    def __init__(self, agents_config, dataset_file, rounds, task):
        super().__init__(agents_config, dataset_file, rounds)
        self.task_type = task

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
            prompt_9 = "You would be in a group discussion with other teammates as a result, you should answer as diverge and creative as you can."
            question_prompt_9 = question + "\n" + prompt_9
            initial_prompt = "Initiate a discussion with others to collectively complete the following task: " + question_prompt_9
            # ------------------------------------------
            most_recent_responses = {}
            for round in range(self.rounds):
                is_last_round = (round == self.rounds - 1)
                is_first_round = (round == 0)
                round_responses = {agent.agent_name: [] for agent in self.agents}
                print(f"Round {round + 1}: Discussion on {question}")
                for agent in self.agents:
                    if is_first_round:
                        formatted_initial_prompt = agent.construct_user_message(initial_prompt)
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
                        combined_prompt = self.construct_response(question_prompt_9, most_recent_responses, agent, is_last_round)
                        formatted_combined_prompt = agent.construct_user_message(combined_prompt)
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
        self.save_debate_conversations(self.agents, all_responses, init_results, final_results, amount_of_data, task_type=self.task_type)


    def construct_response(self, question, most_recent_responses, current_agent, is_last_round):
        prefix_string = "These are the solutions to the problem from other agents:\n"
        for agent_name, responses in most_recent_responses.items():
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

        if is_last_round:
            prefix_string += f"This is the last round of the discussion, please only present a list of your final answers. Please list the final response in 1. ... 2. ... 3. ... and so on. \n\n"
#         else:
#             discussion_prompt =  "You are an active and helpful member in this discussion. \
# You should persuade each other that your answers are creative by giving reasonable explanations, be critical to verify each answer to see if it is creative enough,\
# justify your own answers, integrate with others' replies, coming up with ideas inspired by others, \
# remove answers that is not creative enough, merge similar ideas, and ask questions for further understandings.\n\n"
#             prefix_string += discussion_prompt
        prefix_string += question
        print("Constructed Response", prefix_string)
        return prefix_string
    