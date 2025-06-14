"""
Script to fetch data from specific websites and save it as documents.
"""
import os
import requests
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create data directory if it doesn't exist
data_dir = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(data_dir, exist_ok=True)


def fetch_and_save_website(url, filename):
    """
    Fetch content from a website and save it as a document.
    
    Args:
        url: URL of the website to fetch.
        filename: Name of the file to save the content to.
    """
    try:
        print(f"Fetching data from {url}...")
        
        # Add a user agent to avoid being blocked
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Fetch the website
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
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
        
        # Save the content to a file
        file_path = os.path.join(data_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"Successfully saved content to {file_path}")
        return True
    
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return False


def create_random_document():
    """
    Create a document with random information about Badar Abbas.
    """
    content = """
# Badar Abbas - Additional Information

## Projects and Achievements

### AI-Powered Voice Assistant
Badar led the development of an advanced voice assistant that uses natural language processing to understand and respond to user queries. The assistant can perform tasks such as setting reminders, answering questions, and controlling smart home devices.

### RAG Application Framework
Developed a comprehensive framework for building Retrieval-Augmented Generation applications that combine the power of large language models with custom knowledge bases. This framework has been used to create specialized assistants for various industries.

### Cyber Security Solutions
Designed and implemented robust cyber security solutions for businesses, focusing on threat detection, vulnerability assessment, and secure data management. These solutions have helped companies protect their sensitive information from cyber attacks.

## Technical Skills

### Programming Languages
- Python (Advanced)
- JavaScript (Intermediate)
- TypeScript (Intermediate)
- Java (Basic)
- C# (Basic)

### Frameworks and Libraries
- LangChain
- FastAPI
- React
- Node.js
- TensorFlow
- PyTorch

### Tools and Platforms
- Docker
- AWS
- Azure
- Git
- Kubernetes
- Jira

## Education and Certifications

### Education
- Currently pursuing intermediate education
- Self-taught in various aspects of AI and software development
- Participated in numerous online courses and workshops

### Certifications
- AI Engineering Fundamentals
- Web Development Bootcamp
- Cyber Security Essentials
- Cloud Computing Basics

## Personal Interests

### Technology
Passionate about emerging technologies, particularly in the fields of artificial intelligence, machine learning, and natural language processing.

### Entrepreneurship
Interested in business development and startup culture, with a focus on creating innovative solutions to real-world problems.

### Continuous Learning
Committed to lifelong learning and staying updated with the latest developments in technology and business.

## Contact Information

For professional inquiries, Badar can be reached through Lunar AI Studio's official channels or via his LinkedIn profile.
"""
    
    # Save the content to a file
    file_path = os.path.join(data_dir, "badar_abbas_additional_info.md")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Successfully created random document at {file_path}")
    return True


def main():
    """
    Main function to fetch data from websites and create random document.
    """
    # Websites to fetch
    websites = [
        {"url": "https://www.lunarstudio.site/", "filename": "lunar_studio_website.txt"},
        {"url": "https://www.linkedin.com/in/badar-abbas/", "filename": "badar_abbas_linkedin.txt"}
    ]
    
    # Fetch data from websites
    for website in websites:
        success = fetch_and_save_website(website["url"], website["filename"])
        if success:
            # Add a delay to avoid being rate-limited
            time.sleep(2)
    
    # Create random document
    create_random_document()
    
    print("Data fetching and document creation completed.")


if __name__ == "__main__":
    main()
