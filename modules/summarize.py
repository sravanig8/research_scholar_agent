"""
Summarization module for Research Scholar Agent
Generates AI-based summaries using OpenAI or fallback methods
"""

import os
import openai


def summarize_text(text, use_ai=True):
    """
    Summarize text using OpenAI API or fallback method
    
    Args:
        text (str): Text to summarize
        use_ai (bool): Whether to try using OpenAI API
    
    Returns:
        str: Summary of the text
    """
    if not text or len(text.strip()) == 0:
        return "No abstract available."
    
    # Try AI summarization if enabled and API key exists
    if use_ai:
        summary = summarize_with_openai(text)
        if summary:
            return summary
    
    # Fallback to simple extraction
    return summarize_fallback(text)


def summarize_with_openai(text):
    """
    Summarize using OpenAI API
    
    Args:
        text (str): Text to summarize
    
    Returns:
        str: Summary or None if API unavailable
    """
    try:
        # Check if API key is available
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return None
        
        # Set API key
        openai.api_key = api_key
        
        # Create summarization prompt
        prompt = f"""Please provide a concise 3-4 sentence summary of the following abstract:

{text}

Summary:"""
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a skilled academic researcher who creates concise, clear summaries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.5,
            timeout=10
        )
        
        # Extract summary from response
        summary = response['choices'][0]['message']['content'].strip()
        return summary
    
    except openai.error.AuthenticationError:
        print("OpenAI API authentication failed. Check your API key.")
        return None
    except openai.error.APIError as e:
        print(f"OpenAI API error: {e}")
        return None
    except Exception as e:
        print(f"Error during AI summarization: {e}")
        return None


def summarize_fallback(text):
    """
    Fallback summarization method
    Extracts first 2-3 sentences from text
    
    Args:
        text (str): Text to summarize
    
    Returns:
        str: Summary (first few sentences)
    """
    # Clean text
    text = text.replace('\n', ' ').strip()
    
    # Split by sentences (simple method)
    sentences = text.split('. ')
    
    # Get first 2-3 sentences
    num_sentences = min(2, len(sentences))
    summary = '. '.join(sentences[:num_sentences])
    
    # Add period if missing
    if summary and not summary.endswith('.'):
        summary += '.'
    
    # Limit length to reasonable size
    if len(summary) > 500:
        summary = summary[:500] + '...'
    
    return summary if summary else "Abstract not available."


def check_openai_api():
    """
    Check if OpenAI API is available and configured
    
    Returns:
        bool: True if API key is set, False otherwise
    """
    api_key = os.getenv('OPENAI_API_KEY')
    return bool(api_key)
