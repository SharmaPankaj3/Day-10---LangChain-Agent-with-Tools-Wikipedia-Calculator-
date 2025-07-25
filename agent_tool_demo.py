# Step 1 import library
import os
import wikipedia
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import AgentExecutor,create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate

# Step 2. Load API key
with open(r"D:\desktop\Key_GEN_AI.txt", "r") as f:
    os.environ["OPENAI_API_KEY"] = f.read().strip()

# Step 3. Define custom tools
def search_wikipedia(query:str) -> str:
    return wikipedia.summary(query, sentences=2)

tools = [
    Tool(
        name="Wikipedia_Search",
        func=search_wikipedia,
        description="Useful for answering questions about people,places, and things."
    ),
Tool(
    name="Calculator",
    func=lambda x: str(eval(x)),
    description="Useful for doing basic math calculation"
    )
]

#Step 4 load llm
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")


# Step 5 Create prompt
prompt= ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}"),
    ("ai","{agent_scratchpad}")
    ])

# Step 6 Create the agent
agent = create_openai_functions_agent(llm=llm,tools=tools,prompt=prompt)



# Step 7 : Wrap it in an executer

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Step 8  Run it

if __name__ == "__main__":
    query = input("Ask your question:")
    result = agent_executor.invoke({"input": query})
    print("\n Agent's Response: \n", result["output"])



# Ask your question:Who is Albert Einstein and what is 365 * 2?