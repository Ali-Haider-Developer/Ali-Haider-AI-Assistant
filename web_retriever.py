"""
Web search and content extraction functionality.
"""
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.tools.tavily_search import TavilySearchResults

from config import CHUNK_SIZE, CHUNK_OVERLAP, MAX_SEARCH_RESULTS


class WebRetriever:
    """
    Class for retrieving information from the web.
    """

    def __init__(self):
        """
        Initialize the web retriever.
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )

    def search_web(self, query: str) -> List[Dict[str, Any]]:
        """
        Search the web for information related to the query.

        Args:
            query: The search query.

        Returns:
            List of search results.
        """
        # Check if the query is about Badar Abbas or Lunar AI Studio
        badar_abbas_keywords = ["badar", "abbas", "badar abbas", "lunar", "lunar ai", "lunar studio", "lunar ai studio"]

        # If the query is about Badar Abbas or Lunar AI Studio, prioritize the specific websites
        if any(keyword.lower() in query.lower() for keyword in badar_abbas_keywords):
            # Return predefined results for Badar Abbas and Lunar AI Studio
            return [
                {
                    "title": "Lunar AI Studio",
                    "url": "https://www.lunarstudio.site/",
                    "content": "Lunar AI Studio is a technology company specializing in Agentic AI and Cyber Security solutions."
                },
                {
                    "title": "Badar Abbas - LinkedIn",
                    "url": "https://www.linkedin.com/in/badar-abbas/",
                    "content": "Badar Abbas is a 17-year-old entrepreneur with expertise in business development, Agentic AI, and more."
                }
            ]

        # For other queries, use the Tavily search tool from LangChain
        try:
            search_tool = TavilySearchResults(max_results=MAX_SEARCH_RESULTS)
            search_results = search_tool.invoke(query)
            return search_results
        except Exception as e:
            print(f"Error searching the web: {e}")
            # Return empty results if search fails
            return []

    def extract_content_from_url(self, url: str) -> List:
        """
        Extract content from a URL.

        Args:
            url: The URL to extract content from.

        Returns:
            List of document chunks.
        """
        # Check if the URL is one of the specific websites we have local data for
        if "lunarstudio.site" in url:
            # Use the local data for Lunar AI Studio
            from document_loader import load_document
            import os

            data_dir = os.path.join(os.path.dirname(__file__), "data")
            file_path = os.path.join(data_dir, "lunar_studio_website.txt")

            if os.path.exists(file_path):
                print(f"Using local data for {url}")
                return load_document(file_path)

        elif "linkedin.com/in/badar-abbas" in url:
            # Use the local data for Badar Abbas's LinkedIn
            from document_loader import load_document
            import os

            data_dir = os.path.join(os.path.dirname(__file__), "data")
            file_path = os.path.join(data_dir, "badar_abbas_linkedin.txt")

            if os.path.exists(file_path):
                print(f"Using local data for {url}")
                return load_document(file_path)

        # For other URLs, try to fetch the content
        try:
            # Use WebBaseLoader to load the content
            loader = WebBaseLoader(url)
            documents = loader.load()

            # Split the document into chunks
            return self.text_splitter.split_documents(documents)
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return []

    def retrieve_from_web(self, query: str) -> List:
        """
        Retrieve information from the web based on a query.

        Args:
            query: The search query.

        Returns:
            List of document chunks.
        """
        # Search the web
        search_results = self.search_web(query)

        # Extract content from each search result
        all_documents = []
        for result in search_results:
            url = result.get("url")
            if url:
                documents = self.extract_content_from_url(url)
                all_documents.extend(documents)

        return all_documents

    def extract_text_from_html(self, html_content: str) -> str:
        """
        Extract text from HTML content.

        Args:
            html_content: The HTML content.

        Returns:
            Extracted text.
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        # Get text
        text = soup.get_text()

        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())

        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text
