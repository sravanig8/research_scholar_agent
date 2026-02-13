"""
Research Scholar Agent - AI-Powered Academic Assistant
Searches for research papers, summarizes them, and enables comparison

SETUP INSTRUCTIONS:
1. Install dependencies:
   pip install -r requirements.txt

2. Set OpenAI API key (optional but recommended):
   - Windows (PowerShell): $env:OPENAI_API_KEY = "your-api-key-here"
   - Windows (CMD): set OPENAI_API_KEY=your-api-key-here
   - Linux/Mac: export OPENAI_API_KEY="your-api-key-here"
   
   Note: If no API key is provided, the app will use simple text extraction
   for summaries instead of AI summarization.

3. Run the application:
   python app.py

4. Open your browser and navigate to:
   http://localhost:5000

FEATURES:
- Search research papers by topic from arXiv
- AI-powered abstract summarization (with fallback)
- Store search results in local database
- View search history
- Compare papers side-by-side
- Clean, academic-themed user interface
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
from dotenv import load_dotenv

# Import modules
from modules.search import search_papers
from modules.summarize import summarize_text, check_openai_api
from modules.compare import compare_papers, get_comparison_summary
from database import init_db, save_papers, get_history, get_papers_by_query, get_paper_by_id

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'research-scholar-secret-key-12345')

# Initialize database on startup
init_db()


@app.route('/')
def index():
    """Home page with search interface"""
    api_available = check_openai_api()
    return render_template('index.html', api_available=api_available)


@app.route('/search', methods=['POST'])
def search():
    """Search for papers and generate summaries"""
    try:
        query = request.form.get('query', '').strip()
        
        if not query or len(query) < 2:
            return render_template('index.html', error="Please enter a valid search query")
        
        # Fetch papers from arXiv
        papers = search_papers(query, max_results=5)
        
        if not papers:
            return render_template('index.html', 
                                 error="No papers found. Try a different search query.")
        
        # Generate summaries for each paper
        api_available = check_openai_api()
        for paper in papers:
            paper['summary'] = summarize_text(
                paper.get('abstract', ''), 
                use_ai=api_available
            )
        
        # Save to database
        save_papers(query, papers)
        
        # Store current search in session for comparison feature
        session['current_query'] = query
        session['current_papers'] = [
            {k: p[k] for k in ['title', 'authors', 'year', 'abstract', 'summary', 'link']}
            for p in papers
        ]
        
        return render_template('results.html', 
                             query=query, 
                             papers=papers,
                             api_available=api_available)
    
    except Exception as e:
        print(f"Error in search route: {e}")
        return render_template('index.html', 
                             error="An error occurred during search. Please try again.")


@app.route('/history')
def history():
    """View search history"""
    try:
        search_history = get_history()
        return render_template('history.html', history=search_history)
    except Exception as e:
        print(f"Error in history route: {e}")
        return render_template('history.html', 
                             error="Error loading history",
                             history=[])


@app.route('/history/<query>')
def view_query_results(query):
    """View previous search results"""
    try:
        papers = get_papers_by_query(query)
        api_available = check_openai_api()
        return render_template('results.html', 
                             query=query, 
                             papers=papers,
                             api_available=api_available,
                             from_history=True)
    except Exception as e:
        print(f"Error viewing query results: {e}")
        return redirect(url_for('history'))


@app.route('/compare', methods=['POST', 'GET'])
def compare():
    """Compare two papers side by side"""
    try:
        if request.method == 'POST':
            # Get selected paper IDs from form
            paper_id_1 = request.form.get('paper1')
            paper_id_2 = request.form.get('paper2')
            
            if not paper_id_1 or not paper_id_2:
                return render_template('index.html', 
                                     error="Please select two papers to compare")
            
            if paper_id_1 == paper_id_2:
                return render_template('index.html', 
                                     error="Please select two different papers")
            
            # Fetch papers from database
            paper1 = get_paper_by_id(paper_id_1)
            paper2 = get_paper_by_id(paper_id_2)
            
            if not paper1 or not paper2:
                return render_template('index.html', 
                                     error="One or both papers not found")
            
            # Generate comparison
            comparison = compare_papers(paper1, paper2)
            
            return render_template('compare.html', 
                                 comparison=comparison,
                                 paper1_id=paper_id_1,
                                 paper2_id=paper_id_2)
        
        else:
            # GET request - show comparison selection page
            return render_template('compare_select.html')
    
    except Exception as e:
        print(f"Error in compare route: {e}")
        return render_template('index.html', 
                             error="An error occurred during comparison.")


@app.route('/api/papers/<query>')
def api_get_papers(query):
    """API endpoint to get papers for comparison selection"""
    try:
        papers = get_papers_by_query(query)
        # Return as JSON
        return jsonify({
            'success': True,
            'papers': papers
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/recent-searches')
def api_recent_searches():
    """API endpoint to get recent searches for dropdown"""
    try:
        history = get_history()
        # Return only query names (limit to last 10)
        queries = [h['query'] for h in history[:10]]
        return jsonify({
            'success': True,
            'queries': queries
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/clear-db', methods=['POST'])
def clear_db():
    """Clear database (for development/testing)"""
    try:
        from database import clear_database
        clear_database()
        return jsonify({'success': True, 'message': 'Database cleared'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('index.html', error="Page not found"), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    print(f"Server error: {e}")
    return render_template('index.html', 
                         error="An internal server error occurred"), 500


if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║   Research Scholar Agent - AI Academic Assistant          ║
    ║   URL: http://localhost:5000                              ║
    ║   Press Ctrl+C to stop the server                         ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Check if OpenAI API is configured
    if not check_openai_api():
        print("⚠️  WARNING: OpenAI API key not configured.")
        print("   AI summaries will use fallback method (text extraction).")
        print("   To enable AI summaries, set the OPENAI_API_KEY environment variable.\n")
    else:
        print("✓ OpenAI API key found. AI summaries enabled.\n")
    
    # Run the Flask development server
    app.run(debug=True, host='127.0.0.1', port=5000)
