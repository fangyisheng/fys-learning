from GPTHelper import GPTHelper
from SystemPrompt import question_classifier

async def question_classifier(prompt):
    system_prompt = question_classifier()
    return await GPTHelper.gptChat(system_prompt,prompt,0.7,True)