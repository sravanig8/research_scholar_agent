"""
Search module for Research Scholar Agent
Fetches research papers from arXiv API
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime


def search_papers(query, max_results=5):
    """
    Search for research papers on arXiv
    
    Args:
        query (str): Search query topic
        max_results (int): Maximum number of papers to fetch (default: 5)
    
    Returns:
        list: List of paper dictionaries containing:
              - title
              - authors
              - year
              - abstract
              - link
    """
    try:
        # Construct arXiv API URL
        url = "http://export.arxiv.org/api/query"
        
        # Parameters for the API request
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        # Add timeout to avoid hanging requests
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        # Parse XML response
        papers = parse_arxiv_response(response.text)
        
        return papers
    
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return []
    except Exception as e:
        print(f"Error searching papers: {e}")
        return []


def parse_arxiv_response(xml_response):
    """
    Parse arXiv API XML response
    
    Args:
        xml_response (str): Raw XML response from arXiv API
    
    Returns:
        list: List of parsed paper dictionaries
    """
    papers = []
    
    try:
        root = ET.fromstring(xml_response)
        
        # arXiv uses namespaces in XML
        namespace = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        
        # Find all entries (papers)
        entries = root.findall('atom:entry', namespace)
        
        for entry in entries:
            try:
                # Extract title
                title_elem = entry.find('atom:title', namespace)
                title = title_elem.text.strip() if title_elem is not None else "N/A"
                
                # Extract authors
                authors_elem = entry.findall('atom:author', namespace)
                authors = ', '.join([a.find('atom:name', namespace).text 
                                   for a in authors_elem 
                                   if a.find('atom:name', namespace) is not None])
                
                # Extract published date (year)
                published_elem = entry.find('atom:published', namespace)
                year = 0
                if published_elem is not None:
                    try:
                        year = int(published_elem.text.split('-')[0])
                    except:
                        year = 0
                
                # Extract abstract
                summary_elem = entry.find('atom:summary', namespace)
                abstract = summary_elem.text.strip() if summary_elem is not None else "N/A"
                
                # Extract link
                link = "N/A"
                for link_elem in entry.findall('atom:link', namespace):
                    if link_elem.get('type') == 'text/html':
                        link = link_elem.get('href')
                        break
                
                # If no HTML link found, get the default link
                if link == "N/A":
                    link_elem = entry.find('atom:link', namespace)
                    if link_elem is not None:
                        link = link_elem.get('href', "N/A")
                
                # Create paper dictionary
                paper = {
                    'title': title,
                    'authors': authors,
                    'year': year,
                    'abstract': abstract,
                    'link': link
                }
                
                papers.append(paper)
            
            except Exception as e:
                print(f"Error parsing individual paper: {e}")
                continue
        
        return papers
    
    except ET.ParseError as e:
        print(f"Error parsing XML response: {e}")
        return []
    except Exception as e:
        print(f"Error in parse_arxiv_response: {e}")
        return []
