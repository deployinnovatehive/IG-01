from flask import Blueprint, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

user_bp = Blueprint('user', __name__, template_folder='templates', static_folder='static', static_url_path='/user/static')

# Sample data for projects
PROJECTS_DATA = [
    {
        "id": 1,
        "title": "AI-Powered Study Assistant",
        "description": "An intelligent assistant that helps students organize their study materials and schedule.",
        "technology": ["Python", "AI", "Web"],
        "price": 49.99,
        "difficulty": "High",
        "popularity": 95,
        "date_added": "2023-10-15",
        "seller": "TechStudent123",
        "image": "ai_assistant.jpg",
        "sales_count": 25
    },
    {
        "id": 2,
        "title": "Smart Campus Navigation",
        "description": "An app that helps students navigate campus with real-time updates.",
        "technology": ["Android", "IoT", "Maps"],
        "price": 29.99,
        "difficulty": "Medium",
        "popularity": 87,
        "date_added": "2023-11-02",
        "seller": "CampusDev",
        "image": "campus_nav.jpg",
        "sales_count": 18
    },
    {
        "id": 3,
        "title": "Eco-Friendly Shopping Platform",
        "description": "A web platform connecting consumers with sustainable products.",
        "technology": ["Web", "Python", "Data Science"],
        "price": 39.99,
        "difficulty": "Medium",
        "popularity": 78,
        "date_added": "2023-11-10",
        "seller": "GreenTech",
        "image": "eco_platform.jpg",
        "sales_count": 32
    },
    {
        "id": 4,
        "title": "Virtual Lab Simulator",
        "description": "A physics lab simulator for remote learning environments.",
        "technology": ["Web", "JavaScript", "Simulation"],
        "price": 59.99,
        "difficulty": "High",
        "popularity": 92,
        "date_added": "2023-10-28",
        "seller": "SciencePro",
        "image": "lab_simulator.jpg",
        "sales_count": 15
    },
    {
        "id": 5,
        "title": "Mental Health Tracker",
        "description": "An app to track mood and provide mental wellness resources.",
        "technology": ["Android", "AI", "Health"],
        "price": 24.99,
        "difficulty": "Medium",
        "popularity": 83,
        "date_added": "2023-11-05",
        "seller": "WellnessDev",
        "image": "health_tracker.jpg",
        "sales_count": 22
    },
    {
        "id": 6,
        "title": "Blockchain Voting System",
        "description": "A secure voting system using blockchain technology.",
        "technology": ["Blockchain", "Web", "Security"],
        "price": 79.99,
        "difficulty": "High",
        "popularity": 88,
        "date_added": "2023-10-20",
        "seller": "SecureVote",
        "image": "voting_system.jpg",
        "sales_count": 12
    }
]

# Sample data for top sellers
TOP_SELLERS = [
    {"name": "TechStudent123", "projects_sold": 15, "rating": 4.9},
    {"name": "CampusDev", "projects_sold": 12, "rating": 4.8},
    {"name": "GreenTech", "projects_sold": 10, "rating": 4.7},
    {"name": "SciencePro", "projects_sold": 8, "rating": 4.9},
    {"name": "WellnessDev", "projects_sold": 7, "rating": 4.6}
]

@user_bp.route('/')
def index():
    # Sort projects for different sections
    trending_projects = sorted(PROJECTS_DATA, key=lambda x: (-x['popularity'], -x['difficulty'].count('High')))
    new_projects = sorted(PROJECTS_DATA, key=lambda x: x['date_added'], reverse=True)
    mini_projects = sorted(PROJECTS_DATA, key=lambda x: x['price'])[:4]  # Mini projects by lowest price
    top_selling_projects = sorted(PROJECTS_DATA, key=lambda x: x['sales_count'], reverse=True)[:3]

    # Get categories - updated with specified list
    categories = [
        "Web Development",
        "App Development",
        "web Application",
        "Data Science",
        "AIML",
        "Blockchain",
        "Cybersecurity",
        "Cloud Computing"
    ]

    return render_template('index.html',
                           trending_projects=trending_projects[:4],
                           new_projects=new_projects[:4],
                           mini_projects=mini_projects,
                           top_selling_projects=top_selling_projects,
                           categories=categories,
                           top_sellers=TOP_SELLERS)

@user_bp.route('/sell_your_project', methods=['GET', 'POST'])
def sell_your_project():
    if request.method == 'POST':
        # Process form data
        title = request.form.get('title')
        description = request.form.get('description')
        technology = request.form.getlist('technology')
        price = request.form.get('price')
        difficulty = request.form.get('difficulty')
        
        # In a real app, you would save this to a database
        flash('Your project has been submitted successfully!', 'success')
        return redirect(url_for('user.index'))
    
    return render_template('sell_your_project.html')

@user_bp.route('/browse_all_projects')
def browse_all_projects():
    # Get filter parameters
    technology_filter = request.args.get('technology', '')
    price_filter = request.args.get('price', '')
    difficulty_filter = request.args.get('difficulty', '')

    # Filter projects
    filtered_projects = PROJECTS_DATA.copy()

    if technology_filter:
        filtered_projects = [p for p in filtered_projects if technology_filter in p['technology']]

    if price_filter:
        if price_filter == 'low':
            filtered_projects = [p for p in filtered_projects if p['price'] < 30]
        elif price_filter == 'medium':
            filtered_projects = [p for p in filtered_projects if 30 <= p['price'] <= 60]
        elif price_filter == 'high':
            filtered_projects = [p for p in filtered_projects if p['price'] > 60]

    if difficulty_filter:
        filtered_projects = [p for p in filtered_projects if p['difficulty'].lower() == difficulty_filter.lower()]

    return render_template('browse_all_projects.html', projects=filtered_projects)

@user_bp.route('/project/<int:project_id>')
def project_details(project_id):
    # Find the project by ID
    project = next((p for p in PROJECTS_DATA if p['id'] == project_id), None)
    if not project:
        flash('Project not found.', 'error')
        return redirect(url_for('user.index'))

    return render_template('project_details.html', project=project)

@user_bp.route('/get_guidance', methods=['POST'])
def get_guidance():
    email = request.form.get('email')
    project_type = request.form.get('project_type')
    description = request.form.get('description')

    # In a real app, you would send an email or save to database
    flash('Your guidance request has been submitted! We will contact you soon.', 'success')
    return redirect(url_for('user.index'))