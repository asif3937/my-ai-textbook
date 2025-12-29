#!/usr/bin/env python
"""
Script to help ingest the actual textbook content into the RAG system
"""
import os
import json
import requests
from pathlib import Path


def create_textbook_ingestion_script():
    """
    Creates a script that will help ingest the actual textbook content
    """
    script_content = '''
import os
import json
import requests

def ingest_textbook_content():
    """
    Function to ingest the actual textbook content into the RAG system
    """
    # Read the actual textbook content - you'll need to provide this
    # For now, I'll show you how to structure it
    
    # Example of how to read content from your textbook files:
    # textbook_content = ""
    # with open("path_to_your_textbook_file.md", "r", encoding="utf-8") as f:
    #     textbook_content = f.read()
    
    # Or if you have multiple files, concatenate them:
    # textbook_content = ""
    # for file_path in ["file1.md", "file2.md", "file3.md"]:
    #     with open(file_path, "r", encoding="utf-8") as f:
    #         textbook_content += f.read() + "\\n\\n"
    
    # For demonstration, I'll use placeholder content
    textbook_content = """# Introduction to AI Textbook

This is the content of your actual textbook. 
You should replace this with the real content from your textbook files.

## Chapter 1: Introduction to Artificial Intelligence

Artificial Intelligence (AI) is intelligence demonstrated by machines...

## Chapter 2: Machine Learning Fundamentals

Machine learning is a method of data analysis that automates analytical model building...

[Include the rest of your textbook content here]
"""
    
    # Prepare the payload for the API
    payload = {
        "title": "AI Textbook",
        "author": "Textbook Author",  # Replace with actual author
        "content": textbook_content,
        "metadata": {
            "source": "AI Textbook Project",
            "year": 2023,
            "subject": "Artificial Intelligence"
        }
    }
    
    # Send the request to your API
    api_url = "http://localhost:8000/api/v1/books/ingest"
    
    try:
        response = requests.post(
            api_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Textbook successfully ingested!")
            print(f"Book ID: {result['book_id']}")
            return result
        else:
            print(f"❌ Failed to ingest textbook: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the API server. Make sure your FastAPI server is running on http://localhost:8000")
        return None
    except Exception as e:
        print(f"❌ Error during textbook ingestion: {str(e)}")
        return None


if __name__ == "__main__":
    print("Starting textbook ingestion...")
    result = ingest_textbook_content()
    
    if result:
        print(f"\\n🎉 Your textbook is now ready for RAG-based question answering!")
        print(f"   You can reference it using Book ID: {result['book_id']}")
    else:
        print("\\n❌ Textbook ingestion failed. Please check the errors above.")
'''
    
    with open("ingest_textbook.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("[SUCCESS] Created 'ingest_textbook.py' script")
    print("[INFO] Please modify this script with your actual textbook content before running it")


def instructions_for_user():
    """
    Provide instructions to the user on how to proceed
    """
    instructions = """
    [BOOK] INSTRUCTIONS TO INTEGRATE YOUR ACTUAL TEXTBOOK:

    1. Navigate to your textbook directory: C:\\Users\\AA\\desktop\\my-ai-textbook\\textbook\\docs

    2. The textbook appears to be organized with multiple markdown files across different directories:
       - capstone/
       - digital-twin/
       - humanoid-robotics/
       - physical-ai/
       - ros2/
       - vla/
       - And other topic-specific directories

    3. To ingest your actual textbook:
       a) Copy the content from your textbook files
       b) Update the 'ingest_textbook.py' script with the actual content
       c) Run the script: python ingest_textbook.py

    4. Alternative approach - Create a combined file:
       - Combine all your textbook markdown files into a single text file
       - Then use our existing ingest_book.py script:
         python ingest_book.py your_combined_textbook.txt "Your Textbook Title" "Author Name"

    5. Once ingested, you'll get a Book ID that you can use with your RAG chatbot
    """
    
    print(instructions)


if __name__ == "__main__":
    create_textbook_ingestion_script()
    instructions_for_user()