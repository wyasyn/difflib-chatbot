import json
from difflib import get_close_matches
import os

class ChatBot:
    def __init__(self, knowledge_base_file='knowledge_base.json'):
        self.knowledge_base_file = knowledge_base_file
        self.knowledge_base = self.load_knowledge_base()

    def load_knowledge_base(self) -> dict:
        if os.path.exists(self.knowledge_base_file):
            with open(self.knowledge_base_file, 'r') as file:
                data: dict = json.load(file)
            return data
        else:
            # If the file doesn't exist, create an empty knowledge base
            return {"interactions": []}

    def save_knowledge_base(self):
        with open(self.knowledge_base_file, 'w') as file:
            json.dump(self.knowledge_base, file, indent=2)

    def find_best_match(self, user_question: str) -> str | None:
        questions = [q["question"].lower() for q in self.knowledge_base["interactions"]]
        matches = get_close_matches(user_question.lower(), questions, n=1, cutoff=0.6)
        return matches[0] if matches else None

    def get_answer_for_question(self, question: str) -> str | None:
        for q in self.knowledge_base["interactions"]:
            if q["question"].lower() == question.lower():
                return q["answer"]

    def get_response(self, text: str) -> str:
        best_match = self.find_best_match(text)

        if best_match:
            answer = self.get_answer_for_question(best_match)
            return answer
        else:
            return "I'm not sure how to respond to that. Can you provide more details?"

    def learn_response(self, text: str):
        print(f"I don't know the answer. Can you teach me?")
        new_answer = input('Type the answer or "skip" to skip: ')

        if new_answer.lower() != "skip":
            self.knowledge_base["interactions"].append({"question": text, "answer": new_answer})
            self.save_knowledge_base()
            print("Thank you! I learned a new response!")

# Instantiate the chat bot
chat_bot = ChatBot()

if __name__ == '__main__':
    print("Lets's chat! (type 'quit) to exit")
    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break

        response = chat_bot.get_response(user_input)
        print(f"BOT: {response}")

