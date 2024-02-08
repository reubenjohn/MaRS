from mars.agents.utils import create_agent, llm, tools

search_agent = create_agent(llm, tools, "You are a web searcher. Search the internet for information.")
insights_research_agent = create_agent(llm, tools,
                                       """You are a Insight Researcher. Do step by step. 
                                       Based on the provided content first identify the list of topics,
                                       then search internet for each topic one by one
                                       and finally find insights for each topic one by one.
                                       Include the insights and sources in the final response
                                       """)
