# Credits: Mervin Praison
# https://mer.vin/2024/01/langgraph-agents/

import functools
import operator
from typing import TypedDict, Annotated, Sequence

from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END

from mars.agents.utils import llm
from mars.agents.internet_agents import search_agent, insights_research_agent


# Set environment variables
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_PROJECT"] = "LangGraph Research Agents"


# Define agent nodes
def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}


# Create Agent Supervisor
members = ["Web_Searcher", "Insight_Researcher"]
system_prompt = (
    "As a supervisor, your role is to oversee a dialogue between these"
    " workers: {members}. Based on the user's request,"
    " determine which worker should take the next action. Each worker is responsible for"
    " executing a specific task and reporting back their findings and progress. Once all tasks are complete,"
    " indicate with 'FINISH'."
)

options = ["FINISH"] + members
function_def = {
    "name": "route",
    "description": "Select the next role.",
    "parameters": {
        "title": "routeSchema",
        "type": "object",
        "properties": {"next": {"title": "Next", "anyOf": [{"enum": options}]}},
        "required": ["next"],
    },
}

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="messages"),
    ("system", "Given the conversation above, who should act next? Or should we FINISH? Select one of: {options}"),
]).partial(options=str(options), members=", ".join(members))

search_node = functools.partial(agent_node, agent=search_agent, name="Web_Searcher")

supervisor_node = (
        prompt | llm.bind_functions(functions=[function_def], function_call="route") | JsonOutputFunctionsParser())

insights_research_node = functools.partial(agent_node, agent=insights_research_agent, name="Insight_Researcher")


# Define the Agent State, Edges and Graph

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str


workflow = StateGraph(AgentState)
workflow.add_node("Web_Searcher", search_node)
workflow.add_node("Insight_Researcher", insights_research_node)
workflow.add_node("supervisor", supervisor_node)

# Define edges
for member in members:
    workflow.add_edge(member, "supervisor")

conditional_map = {k: k for k in members}
conditional_map["FINISH"] = END
workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)
workflow.set_entry_point("supervisor")

graph = workflow.compile()

# Run the graph
for s in graph.stream({
    "messages": [HumanMessage(content="""Search for the latest AI technology trends in 2024,
            summarize the content. After summarise pass it on to insight researcher
            to provide insights for each topic""")]
}):
    if "__end__" not in s:
        print(s)
        print("----")
