import logging
from typing import Dict, Any, List
from openai import OpenAI
from config.settings import settings
import json
import time

logger = logging.getLogger(__name__)

class AssistantGenerationService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.LLM_MODEL
        self.temperature = settings.LLM_TEMPERATURE
        
        # Create or retrieve the assistant
        self.assistant = self._get_or_create_assistant()
        
    def _get_or_create_assistant(self):
        """Create or retrieve the assistant based on the book content"""
        try:
            # Check if we already have an assistant for this purpose
            assistants = self.client.beta.assistants.list(limit=20)
            
            # Look for an existing assistant with our specific name
            assistant_name = "AI Textbook RAG Assistant"
            existing_assistant = None
            
            for assistant in assistants.data:
                if assistant.name == assistant_name:
                    existing_assistant = assistant
                    break
            
            if existing_assistant:
                logger.info(f"Using existing assistant: {existing_assistant.id}")
                return existing_assistant
            else:
                # Create a new assistant
                assistant = self.client.beta.assistants.create(
                    name=assistant_name,
                    description="An AI assistant that answers questions based on textbook content using RAG",
                    instructions=f"""You are an AI assistant helping users understand content from textbooks.
                    Answer questions based strictly on the provided context from the book.
                    If the information isn't available in the context, say so directly.
                    Always be concise, accurate, and helpful.
                    Your responses should include citations to the specific parts of the text that support your answers.
                    Current mode: {settings.DEFAULT_RAG_MODE or 'full_book'}""",
                    model=self.model,
                    temperature=self.temperature,
                )
                
                logger.info(f"Created new assistant: {assistant.id}")
                return assistant
        except Exception as e:
            logger.error(f"Error creating or retrieving assistant: {str(e)}")
            raise

    def generate_answer(self, query: str, context: List[Dict[str, Any]], mode: str) -> Dict[str, Any]:
        """
        Generate an answer using the OpenAI Assistant API
        """
        try:
            if not context:
                # No relevant context found, return a generic response
                return {
                    'answer': "I couldn't find relevant information in the book to answer your question. Please try rephrasing or ask about a different topic.",
                    'citations': []
                }

            # Construct the context string
            context_str = "\n\n".join([
                f"Source: {chunk['source']}\nContent: {chunk['text']}" 
                for chunk in context
            ])

            # Create a thread for this conversation
            thread = self.client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Context: {context_str}\n\nQuestion: {query}\n\nAnswer:"
                    }
                ]
            )

            # Run the assistant on the thread
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.assistant.id,
                # Additional instructions specific to this run
                instructions=f"Answer the user's question based on the provided context. Mode: {mode}. If the answer is not in the context, clearly state that."
            )

            # Wait for the run to complete
            run = self._wait_for_run_completion(thread.id, run.id)

            if run.status == "completed":
                # Retrieve the messages from the thread
                messages = self.client.beta.threads.messages.list(
                    thread_id=thread.id,
                    order="desc"  # Most recent first
                )

                # Get the latest assistant message
                answer = ""
                for message in messages.data:
                    if message.role == "assistant":
                        # Extract the content from the message
                        for content_block in message.content:
                            if content_block.type == "text":
                                answer = content_block.text.value
                                break
                        break

                # Extract citations from context (sources of information)
                citations = []
                for chunk in context:
                    citation_info = {
                        'source': chunk.get('source', 'unknown'),
                        'content_snippet': chunk.get('text', '')[:200] + "..." if len(chunk.get('text', '')) > 200 else chunk.get('text', '')
                    }
                    if citation_info not in citations:  # Avoid duplicate citations
                        citations.append(citation_info)

                logger.info(f"Generated answer for query: {query[:50]}...")
                return {
                    'answer': answer,
                    'citations': citations
                }
            else:
                logger.error(f"Assistant run failed with status: {run.status}")
                return {
                    'answer': "Sorry, I encountered an error while generating a response. Please try again later.",
                    'citations': []
                }

        except Exception as e:
            logger.error(f"Error generating answer with assistant: {str(e)}")
            return {
                'answer': "Sorry, I encountered an error while generating a response. Please try again later.",
                'citations': []
            }

    def _wait_for_run_completion(self, thread_id: str, run_id: str, timeout: int = 60):
        """
        Wait for a run to complete with a timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )
            
            if run.status in ["completed", "failed", "cancelled", "expired"]:
                return run
                
            time.sleep(1)  # Wait 1 second before checking again
        
        # If we've reached the timeout, cancel the run and return
        self.client.beta.threads.runs.cancel(
            thread_id=thread_id,
            run_id=run_id
        )
        
        # Return a run object with a timeout status
        class TimeoutRun:
            status = "timeout"
        
        return TimeoutRun()