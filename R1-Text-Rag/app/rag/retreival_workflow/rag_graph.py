from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from app.rag.retreival_workflow.rag_state import RagState
from app.rag.vector_db import vector_db
from app.core.config import settings



# LLM
rag_llm = init_chat_model(
    model="deepseek-chat",
    model_provider="openai",
    api_key=settings.DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)



# RETRIEVER
retriever = vector_db.as_retriever(search_kwargs={"k" : 2})


# NODES
async def retrieve_docs(state: RagState) -> RagState:
    user_message = state["messages"][-1].content  # Get the last message from the list

    docs = await retriever.ainvoke(user_message)

    return {
        "retrieved_docs" : docs
    }


async def response_node(state : RagState) -> RagState:
    messages = state["messages"]  
    retrieve_docs = state["retrieved_docs"]

    text_list = []
    for doc in retrieve_docs:
        text_list.append(doc.page_content)

    context = "\n".join(text_list)
    

    system_message = SystemMessage(
        content = f"""
        You are a helpful assistant that answers questions based on the provided context. 
        If the context does not contain the answer, respond with "I don't know.".
        Here is your context : 
        {context}
        """
    )


    response = await rag_llm.ainvoke([system_message] + messages)

    return {
        "messages" : [response]
    }




# GRAPH
rag_graph = StateGraph(state_schema=RagState)
rag_graph.add_node("retrieve_docs", retrieve_docs)
rag_graph.add_node("response_node", response_node)

rag_graph.add_edge(START, "retrieve_docs")
rag_graph.add_edge("retrieve_docs", "response_node")
rag_graph.add_edge("response_node", END)

rag_workflow = rag_graph.compile()