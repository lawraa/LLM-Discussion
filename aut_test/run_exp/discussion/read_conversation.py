import json
import argparse

def main(filename: str):
    with open(filename, 'r') as file:
        chat_data = json.load(file)

    # Generating HTML content for the chat
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Chat History</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">
    <style>
    body { font-family: 'Roboto', sans-serif; margin: 20px; }
    .chat-container { background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin-bottom: 20px; }
    .message { border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 55%; line-height: 1.5;}
    .user, .model { color: white; float: left; clear: both; }
    .user { background-color: #007bff; float: left; clear: both; }
    .model { background-color: #28a745; float: right; clear: both; }
    h2, h3 { font-weight: 1000; }
    .clearfix { clear: both; }
    </style>
    </head>
    <body>
    """

    for question, agents_responses in chat_data.items():
        html_content += f"<h2>Discussion Topic: {question}</h2>\n"
        
        for agent, responses in agents_responses.items():
            html_content += f"<div class='chat-container'>\n<h3>{agent}</h3>\n"
            
            for response in responses:
                role = response["role"]
                css_class = "user" if role == "user" else "model"
                if "content" in response:
                    message = response["content"]
                elif "parts" in response:
                    message = " ".join(response["parts"])
                html_content += f"<div class='{css_class} message'>{message}</div>\n"
            
            html_content += "<div class='clearfix'></div></div>\n"

    html_content += """
    </body>
    </html>
    """

    # Save the HTML content to a file
    file_path = 'chat_history_ui_2.html'
    with open(file_path, 'w') as file:
        file.write(html_content)

    print(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make HTML to show chat.")
    parser.add_argument("-i", "--input", required=True, help="Path to the conversation log file.")
    args = parser.parse_args()
    main(args.input)
