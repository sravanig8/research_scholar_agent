"""
Comparison module for Research Scholar Agent
Compares two research papers side by side
"""


def compare_papers(paper1, paper2):
    """
    Compare two research papers
    
    Args:
        paper1 (dict): First paper with keys: title, authors, year, abstract, summary
        paper2 (dict): Second paper with keys: title, authors, year, abstract, summary
    
    Returns:
        dict: Comparison data with:
              - title1, title2: Paper titles
              - authors1, authors2: Authors
              - year1, year2: Publication years
              - summary1, summary2: Summaries
              - abstract1, abstract2: Full abstracts
              - method_analysis1, method_analysis2: Method analysis
              - conclusion_key_terms1, conclusion_key_terms2: Key conclusion terms
    """
    
    comparison = {
        # Basic information
        'title1': paper1.get('title', 'N/A'),
        'title2': paper2.get('title', 'N/A'),
        'authors1': paper1.get('authors', 'N/A'),
        'authors2': paper2.get('authors', 'N/A'),
        'year1': paper1.get('year', 'N/A'),
        'year2': paper2.get('year', 'N/A'),
        
        # Summaries and abstracts
        'summary1': paper1.get('summary', 'N/A'),
        'summary2': paper2.get('summary', 'N/A'),
        'abstract1': paper1.get('abstract', 'N/A'),
        'abstract2': paper2.get('abstract', 'N/A'),
        
        # Extracted analysis
        'method_analysis1': extract_methods(paper1.get('abstract', '')),
        'method_analysis2': extract_methods(paper2.get('abstract', '')),
        'conclusion_key_terms1': extract_key_terms(paper1.get('abstract', ''), 'conclusion'),
        'conclusion_key_terms2': extract_key_terms(paper2.get('abstract', ''), 'conclusion'),
    }
    
    return comparison


def extract_methods(abstract):
    """
    Extract methodology-related keywords from abstract
    
    Args:
        abstract (str): Paper abstract
    
    Returns:
        str: Extracted method description or keywords
    """
    if not abstract:
        return "No methods described"
    
    # Keywords that often indicate methodology
    method_keywords = [
        'propose', 'present', 'introduce', 'novel',
        'method', 'approach', 'algorithm', 'framework',
        'model', 'technique', 'using', 'based on',
        'we use', 'we develop', 'we introduce'
    ]
    
    abstract_lower = abstract.lower()
    
    # Find sentences containing method keywords
    sentences = abstract.split('. ')
    relevant_sentences = [s for s in sentences 
                         if any(keyword in s.lower() for keyword in method_keywords)]
    
    if relevant_sentences:
        # Return first relevant sentence (limit to 150 chars)
        method_text = relevant_sentences[0].strip()
        if len(method_text) > 150:
            method_text = method_text[:150] + '...'
        return method_text
    
    # If no specific methods found, extract first sentence
    if sentences:
        first_sent = sentences[0].strip()
        if len(first_sent) > 200:
            first_sent = first_sent[:200] + '...'
        return first_sent
    
    return "Methods not clearly described"


def extract_key_terms(abstract, section='conclusion'):
    """
    Extract key terms from a specific section of abstract
    
    Args:
        abstract (str): Paper abstract
        section (str): Section to analyze ('conclusion', 'results', etc.)
    
    Returns:
        str: Key terms or sentences from that section
    """
    if not abstract:
        return "No conclusions stated"
    
    abstract_lower = abstract.lower()
    
    # Keywords that indicate conclusion section
    if section == 'conclusion':
        conclusion_keywords = ['conclude', 'conclude that', 'conclude that the', 'result',
                             'demonstrate', 'show', 'find', 'found', 'achieve', 'achieved',
                             'outperform', 'surpass', 'improvement']
        
        sentences = abstract.split('. ')
        # Look for conclusion in last 2-3 sentences
        relevant_sentences = []
        for sentence in sentences[-3:]:
            if any(keyword in sentence.lower() for keyword in conclusion_keywords):
                relevant_sentences.append(sentence)
        
        if relevant_sentences:
            conclusion_text = relevant_sentences[-1].strip()
            if len(conclusion_text) > 200:
                conclusion_text = conclusion_text[:200] + '...'
            return conclusion_text
    
    # Fallback: return last sentence
    sentences = abstract.split('. ')
    if sentences:
        last_sent = sentences[-1].strip()
        if not last_sent:
            last_sent = sentences[-2].strip() if len(sentences) > 1 else "See abstract"
        if len(last_sent) > 200:
            last_sent = last_sent[:200] + '...'
        return last_sent
    
    return "See full abstract"


def get_comparison_summary(comparison):
    """
    Generate a text summary of the comparison
    
    Args:
        comparison (dict): Comparison dictionary from compare_papers()
    
    Returns:
        str: Human-readable comparison summary
    """
    summary = f"""
PAPER 1: {comparison['title1']}
- Authors: {comparison['authors1']}
- Year: {comparison['year1']}
- Methods: {comparison['method_analysis1']}
- Key Finding: {comparison['conclusion_key_terms1']}

PAPER 2: {comparison['title2']}
- Authors: {comparison['authors2']}
- Year: {comparison['year2']}
- Methods: {comparison['method_analysis2']}
- Key Finding: {comparison['conclusion_key_terms2']}
"""
    return summary.strip()
