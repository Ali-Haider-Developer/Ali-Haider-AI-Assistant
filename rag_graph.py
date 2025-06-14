"""
LangGraph workflow for the RAG application.
"""
from typing import Dict, List, Annotated, TypedDict, Sequence
from typing_extensions import TypedDict

from langchain.schema.document import Document
from langchain.schema.runnable import RunnableConfig
from langchain.schema.messages import HumanMessage
from langgraph.graph import StateGraph, END

from llm import get_llm
from vector_store import VectorStore
from web_retriever import WebRetriever
from prompt_templates import get_rag_prompt_template, get_query_transformation_prompt


# Define the state
class GraphState(TypedDict):
    """
    State for the RAG graph.
    """
    question: str
    search_query: str
    context: List[Document]
    answer: str
    web_search_enabled: bool


def create_rag_graph():
    """
    Create the RAG graph.

    Returns:
        The RAG graph.
    """
    # Initialize components
    llm = get_llm(model_name="gemini-1.5-flash")  # Explicitly use Gemini Flash 1.5
    print(f"RAG Graph using LLM model: {llm.model}")

    vector_store = VectorStore()
    web_retriever = WebRetriever()
    rag_prompt = get_rag_prompt_template()
    query_transformation_prompt = get_query_transformation_prompt()

    # Define the nodes

    def transform_query(state: GraphState) -> GraphState:
        """
        Transform the user question into an optimized search query.
        """
        # Get the question
        question = state["question"]

        # Transform the question into a search query
        chain = query_transformation_prompt | llm
        response = chain.invoke({"question": question})
        search_query = response.content

        # Update the state
        return {"search_query": search_query}

    def retrieve_from_vector_store(state: GraphState) -> GraphState:
        """
        Retrieve relevant documents from the vector store.
        """
        # Get the search query
        search_query = state["search_query"]

        # Retrieve documents from the vector store
        documents = vector_store.similarity_search(search_query)

        # Update the state
        return {"context": documents}

    def retrieve_from_web(state: GraphState) -> GraphState:
        """
        Retrieve relevant documents from the web.
        """
        # Check if web search is enabled
        if not state.get("web_search_enabled", False):
            return {"context": []}

        # Get the search query
        search_query = state["search_query"]

        # Retrieve documents from the web
        documents = web_retriever.retrieve_from_web(search_query)

        # Update the state
        return {"context": documents}

    def combine_context(state: GraphState) -> GraphState:
        """
        Combine context from different sources.
        """
        # Get the context from vector store and web
        vector_store_context = state.get("context", [])
        web_context = state.get("web_context", [])

        # Combine the context
        combined_context = vector_store_context + web_context

        # Update the state
        return {"context": combined_context}

    def generate_answer(state: GraphState) -> GraphState:
        """
        Generate an answer based on the context.
        """
        # Get the question and context
        question = state["question"]
        context = state.get("context", [])

        # Format the context
        context_text = "\n\n".join([doc.page_content for doc in context])

        # Generate the answer
        chain = rag_prompt | llm
        response = chain.invoke({
            "context": context_text,
            "question": question,
        })
        answer = response.content

        # Update the state
        return {"answer": answer}

    def should_search_web(state: GraphState) -> str:
        """
        Determine if web search should be performed.
        """
        return "search_web" if state.get("web_search_enabled", False) else "skip_web_search"

    # Create the graph
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("transform_query", transform_query)
    workflow.add_node("retrieve_from_vector_store", retrieve_from_vector_store)
    workflow.add_node("retrieve_from_web", retrieve_from_web)
    workflow.add_node("combine_context", combine_context)
    workflow.add_node("generate_answer", generate_answer)

    # Add edges
    workflow.add_edge("transform_query", "retrieve_from_vector_store")
    workflow.add_conditional_edges(
        "retrieve_from_vector_store",
        should_search_web,
        {
            "search_web": "retrieve_from_web",
            "skip_web_search": "generate_answer",
        }
    )
    workflow.add_edge("retrieve_from_web", "combine_context")
    workflow.add_edge("combine_context", "generate_answer")
    workflow.add_edge("generate_answer", END)

    # Set the entry point
    workflow.set_entry_point("transform_query")

    # Compile the graph
    return workflow.compile()


def run_rag_graph(question: str, web_search_enabled: bool = True) -> str:
    """
    Run the RAG graph.

    Args:
        question: The user's question.
        web_search_enabled: Whether to enable web search.

    Returns:
        The answer.
    """
    # Create the graph
    graph = create_rag_graph()

    # Run the graph
    result = graph.invoke({
        "question": question,
        "web_search_enabled": web_search_enabled,
    })

    return result["answer"]
