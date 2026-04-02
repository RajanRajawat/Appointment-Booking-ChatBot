
#Learnings

#! Langchain tools expect :
'''
def register_user(RegisterUser) -> str:
    This is incorrect:

RegisterUser here is treated as a variable, not your model
LangChain expects explicit arguments, not a Pydantic class like this

'''