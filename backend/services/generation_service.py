from typing import List, Dict, Any, Optional
import cohere
from config.settings import settings
from utils import logger
import json

# Import for local LLM fallback
LOCAL_LLM_AVAILABLE = False
try:
    # Try to import and initialize to check if everything works
    import torch  # Check if torch can be imported first
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    # Try to initialize a basic model to check if everything works
    model_name = "microsoft/DialoGPT-small"
    test_tokenizer = AutoTokenizer.from_pretrained(model_name)
    test_model = AutoModelForCausalLM.from_pretrained(model_name)
    test_generator = pipeline('text-generation', model=test_model, tokenizer=test_tokenizer)
    LOCAL_LLM_AVAILABLE = True
    del test_tokenizer, test_model, test_generator  # Clean up
except Exception as e:
    logger.warning(f"Transformers not available or not working properly: {str(e)}. Local LLM will not work.")
    logger.warning("This is often due to PyTorch compatibility issues on Windows.")


class GenerationService:
    def __init__(self):
        # Check if we should use local LLM
        if settings.LANGUAGE_MODEL_PROVIDER == 'local' and LOCAL_LLM_AVAILABLE:
            self.use_local = True
            # Use a lightweight model for local generation
            model_name = "microsoft/DialoGPT-small"  # Using a smaller, faster model
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForCausalLM.from_pretrained(model_name)
                # Create a text generation pipeline
                self.generator = pipeline('text-generation', model=self.model, tokenizer=self.tokenizer)
                logger.info("Using local LLM model")
            except Exception as e:
                logger.error(f"Failed to load local model: {e}")
                raise ValueError("Failed to initialize local LLM. Please check your installation.")
        elif settings.COHERE_API_KEY and settings.COHERE_API_KEY.strip():
            self.use_local = False
            self.client = cohere.Client(settings.COHERE_API_KEY)
            self.model = None

            # Try the most current Cohere models
            # Based on the error message, older models were removed on September 15, 2025
            # Current models might be different - let's try the newer ones
            # According to Cohere docs, current models might include "command", "command-light", etc.
            # But since those were also removed, let's try the embed models as a test
            available_models_to_try = ["command", "command-light", "c4ai-aya-expanse-8b", "c4ai-aya-expanse-32b"]

            for model_name in available_models_to_try:
                try:
                    # Test if the model is available by making a simple call
                    response = self.client.chat(
                        message="test",
                        model=model_name,
                        max_tokens=1,
                        temperature=0.0
                    )
                    self.model = model_name
                    logger.info(f"Successfully verified Cohere model: {self.model}")
                    break  # Exit the loop if a model works
                except Exception as e:
                    logger.warning(f"Model {model_name} not available: {str(e)}")
                    continue  # Try the next model

            if self.model is None:
                logger.warning("No preferred Cohere models available, falling back to local model")
                self.use_local = True
                model_name = "microsoft/DialoGPT-small"
                try:
                    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
                    self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                    self.model = AutoModelForCausalLM.from_pretrained(model_name)
                    self.generator = pipeline('text-generation', model=self.model, tokenizer=self.tokenizer)
                    logger.info("Using local LLM model as fallback")
                except Exception as e:
                    logger.error(f"Failed to load local model: {e}")
                    # If local model fails, use basic fallback
                    logger.warning("No generation service available. Using basic fallback response.")
                    self.use_local = False  # Not actually using local, but flagging for fallback
                    self.fallback_mode = True  # Flag to indicate fallback mode
                    self.model = "fallback-model"  # For logging purposes
            else:
                logger.info(f"Using Cohere model: {self.model}")
        else:
            # Default to local if available, otherwise use fallback
            if LOCAL_LLM_AVAILABLE:
                self.use_local = True
                model_name = "microsoft/DialoGPT-small"
                try:
                    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
                    self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                    self.model = AutoModelForCausalLM.from_pretrained(model_name)
                    self.generator = pipeline('text-generation', model=self.model, tokenizer=self.tokenizer)
                    logger.info("Using local LLM model as fallback")
                except Exception as e:
                    logger.error(f"Failed to load local model: {e}")
                    # If local model fails, use basic fallback
                    logger.warning("No generation service available. Using basic fallback response.")
                    self.use_local = False  # Not actually using local, but flagging for fallback
                    self.fallback_mode = True  # Flag to indicate fallback mode
                    self.model = "fallback-model"  # For logging purposes
            else:
                # If no services are available, provide a basic fallback that returns a message
                logger.warning("No generation service available. Using basic fallback response.")
                self.use_local = False  # Not actually using local, but flagging for fallback
                self.fallback_mode = True  # Flag to indicate fallback mode
                self.model = "fallback-model"  # For logging purposes
    
    def generate_answer(
        self,
        query: str,
        context: List[Dict[str, Any]],
        mode: str = "full_book",
        temperature: float = 0.1  # Lower temperature for more factual responses
    ) -> Dict[str, Any]:
        """
        Generate an answer based on the query and context

        Args:
            query: The user's question
            context: List of relevant context chunks
            mode: Either "full_book" or "selected_text_only"
            temperature: Controls randomness in the response (0.0 to 1.0)

        Returns:
            Dictionary with answer and citations
        """
        try:
            # Check if we're in fallback mode
            if hasattr(self, 'fallback_mode') and self.fallback_mode:
                # Return a basic response indicating the system is not fully functional
                answer = (
                    "The system is currently running in fallback mode because no generation service is available. "
                    "Please configure either a Cohere API key or install the required dependencies for local models. "
                    f"Query received: '{query}'"
                )
                citations = []
                for chunk in context:
                    citations.append({
                        "text": chunk['text'][:100] + "..." if len(chunk['text']) > 100 else chunk['text'],
                        "chapter": chunk.get('metadata', {}).get('chapter', 'Unknown'),
                        "page": chunk.get('metadata', {}).get('page', 'Unknown'),
                        "paragraph": chunk.get('metadata', {}).get('paragraph', 'Unknown'),
                        "relevance_score": chunk.get('relevance_score', 0.0),
                        "validated": True
                    })

                result = {
                    "answer": answer,
                    "citations": citations,
                    "context_used": len(context),
                    "model": "fallback-model"
                }

                logger.info("Generated fallback response")
                return result

            # Build the context text from the retrieved chunks
            context_texts = []
            citations = []

            for i, chunk in enumerate(context):
                text = chunk['text']
                context_texts.append(f"Context {i+1}: {text}")

                # Add citation info
                citation = {
                    "text": text,
                    "chapter": chunk.get('metadata', {}).get('chapter', 'Unknown'),
                    "page": chunk.get('metadata', {}).get('page', 'Unknown'),
                    "paragraph": chunk.get('metadata', {}).get('paragraph', 'Unknown'),
                    "relevance_score": chunk.get('relevance_score', 0.0)
                }
                citations.append(citation)

            context_str = "\n\n".join(context_texts)

            if self.use_local:
                # Use local model for generation
                # For local models, we'll format the prompt differently
                if context_str:
                    prompt = f"Based on the following context, answer the question:\n\n{context_str}\n\nQuestion: {query}\n\nAnswer:"
                else:
                    prompt = f"Answer the following question: {query}\n\nAnswer:"

                # Generate response using local model
                response = self.generator(
                    prompt,
                    max_length=300,  # Limit response length
                    num_return_sequences=1,
                    temperature=temperature,
                    pad_token_id=self.tokenizer.eos_token_id
                )

                # Extract the answer from the response
                full_text = response[0]['generated_text']
                # Extract just the answer part (after the prompt)
                if 'Answer:' in full_text:
                    answer = full_text.split('Answer:')[1].strip()
                else:
                    answer = full_text[len(prompt):].strip()
            else:
                # Use Cohere API
                # Create the system prompt based on the mode
                if mode == "selected_text_only":
                    preamble = (
                        "You are a helpful assistant that answers questions based ONLY on the provided selected text. "
                        "Do not use any external knowledge or make assumptions beyond what is explicitly stated in the selected text. "
                        "If the answer is not available in the provided selected text, respond with: "
                        "\"The answer is not available in the provided text.\""
                    )
                else:  # full_book mode
                    preamble = (
                        "You are a helpful assistant that answers questions based ONLY on the provided book content. "
                        "Do not use any external knowledge or make assumptions beyond what is explicitly stated in the provided content. "
                        "Always cite the specific passages you use to answer the question."
                    )

                # Create the full message for Cohere
                if context_str:
                    message = f"Context:\n{context_str}\n\nQuestion: {query}"
                else:
                    message = f"Question: {query}"

                # Make the API call to Cohere
                response = self.client.chat(
                    message=message,
                    preamble=preamble,
                    model=self.model,
                    temperature=temperature,
                    max_tokens=500,  # Adjust based on expected answer length
                )

                # Extract the answer
                answer = response.text.strip()

            # Check if the answer indicates insufficient context
            if "answer is not available in the provided text" in answer.lower():
                logger.info("Response indicates insufficient context")

            # Validate citations to ensure accuracy
            validated_citations = self._validate_citations(answer, citations)

            # Prepare the result
            result = {
                "answer": answer,
                "citations": validated_citations,
                "context_used": len(context),
                "model": self.model if not self.use_local else "local-dialogpt"
            }

            logger.info(f"Generated answer with {'local' if self.use_local else 'Cohere'} model")
            return result
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            # Return a default response when model is unavailable
            if "model" in str(e) and "not found" in str(e):
                return {
                    "answer": "Model not available with your current Cohere plan. Please check your Cohere dashboard for available models.",
                    "citations": [],
                    "context_used": 0,
                    "model": self.model if not self.use_local else "local-dialogpt"
                }
            raise
    
    def validate_answer_based_on_context(
        self,
        answer: str,
        context: List[Dict[str, Any]]
    ) -> bool:
        """
        Validate that the answer is based on the provided context
        
        Args:
            answer: The generated answer
            context: List of context chunks that should support the answer
        
        Returns:
            True if the answer is consistent with the context
        """
        try:
            # This is a simple validation - in a more sophisticated implementation,
            # we might use semantic similarity, NLI models, or other techniques
            
            answer_lower = answer.lower()
            
            # Check if key terms from context appear in the answer
            context_terms = set()
            for chunk in context:
                text = chunk['text'].lower()
                # Extract some key terms (simplified approach)
                words = text.split()
                # Take some significant words (not stop words)
                for word in words[:20]:  # Check first 20 words for relevant terms
                    if len(word) > 4:  # Only consider words with more than 4 characters
                        context_terms.add(word)
            
            # Check if any of the context terms appear in the answer
            term_found = any(term in answer_lower for term in list(context_terms)[:5])  # Check first 5 terms

            logger.info(f"Answer validation result: {term_found}")
            return term_found
        except Exception as e:
            logger.error(f"Error validating answer: {str(e)}")
            return False

    def _validate_citations(self, answer: str, citations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate that citations accurately reflect the information in the answer

        Args:
            answer: The generated answer
            citations: List of citations to validate

        Returns:
            List of validated citations
        """
        try:
            validated_citations = []
            answer_lower = answer.lower()

            for citation in citations:
                citation_text = citation["text"].lower()

                # Check if the content of the citation appears in the answer
                # This is a simplified validation - in practice, you'd want more sophisticated NLP
                citation_content_in_answer = any(
                    sentence.strip() in answer_lower
                    for sentence in citation_text.split('. ')
                    if len(sentence.strip()) > 10  # Only check sentences with meaning
                )

                # Add validation flag to the citation
                validated_citation = citation.copy()
                validated_citation["validated"] = citation_content_in_answer
                validated_citations.append(validated_citation)

            logger.info(f"Validated {len(validated_citations)} citations")
            return validated_citations
        except Exception as e:
            logger.error(f"Error validating citations: {str(e)}")
            # Return original citations with validation flag if validation fails
            for citation in citations:
                citation["validated"] = False
            return citations