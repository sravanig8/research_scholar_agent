"""
Database module for Research Scholar Agent
Handles SQLite database initialization and operations
"""

import sqlite3
import os
from datetime import datetime

# Database file path
DB_PATH = 'research_papers.db'


def init_db():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create papers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            title TEXT NOT NULL,
            authors TEXT,
            year INTEGER,
            abstract TEXT,
            summary TEXT,
            link TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create searches table to track unique searches
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT UNIQUE NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            paper_count INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()


def save_papers(query, papers):
    """
    Save search papers to database
    
    Args:
        query (str): Search query
        papers (list): List of paper dictionaries
    
    Returns:
        bool: True if successful
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Insert into searches table
        cursor.execute('''
            INSERT OR REPLACE INTO searches (query, paper_count)
            VALUES (?, ?)
        ''', (query, len(papers)))
        
        # Insert papers
        for paper in papers:
            cursor.execute('''
                INSERT INTO papers 
                (query, title, authors, year, abstract, summary, link)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                query,
                paper.get('title', ''),
                paper.get('authors', ''),
                paper.get('year', 0),
                paper.get('abstract', ''),
                paper.get('summary', ''),
                paper.get('link', '')
            ))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving papers: {e}")
        return False
    finally:
        conn.close()


def get_history():
    """
    Get search history from database
    
    Returns:
        list: List of search records with paper counts
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT query, timestamp, paper_count 
        FROM searches 
        ORDER BY timestamp DESC
    ''')
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_papers_by_query(query):
    """
    Get all papers for a specific query
    
    Args:
        query (str): Search query
    
    Returns:
        list: List of paper records
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, title, authors, year, abstract, summary, link 
        FROM papers 
        WHERE query = ? 
        ORDER BY timestamp DESC
    ''', (query,))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_paper_by_id(paper_id):
    """
    Get a single paper by ID
    
    Args:
        paper_id (int): Paper ID
    
    Returns:
        dict: Paper record
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM papers WHERE id = ?
    ''', (paper_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    return dict(result) if result else None


def clear_database():
    """Clear all data from database (for testing/reset)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM papers')
    cursor.execute('DELETE FROM searches')
    
    conn.commit()
    conn.close()
