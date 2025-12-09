from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
import os
from datetime import datetime
from functools import wraps

admin_bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static', static_url_path='/admin/static')
admin_bp.secret_key = 'your-secret-key-here'  # Needed for flash messages

# Admin credentials
ADMIN_USERNAME = 'admin@123'
ADMIN_PASSWORD = 'admin@123'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

# Sample data for the dashboard
sample_projects = [
    {"id": 1, "title": "Admin", "name": "qwe", "price": "asd", "domain": "hjk"},
    {"id": 2, "title": "Student", "name": "qwe", "price": "asd", "domain": "hjk"},
    {"id": 3, "title": "ABC", "name": "qwe", "price": "asd", "domain": "hjk"},
    {"id": 4, "title": "ABC", "name": "qwe", "price": "asd", "domain": "hjk"},
    {"id": 5, "title": "ABC", "name": "qwe", "price": "asd", "domain": "hjk"},
]

# In-memory storage for projects (in real app, use a database)
projects = sample_projects.copy()

# Sample data for different project types
admin_projects_data = [
    {
        'id': 1,
        'title': 'E-commerce Platform',
        'description': 'Full-stack e-commerce solution with admin panel',
        'price': 1500,
        'domain': 'Web Development',
        'status': 'Active',
        'created_date': '2024-01-15',
        'developer_name': 'Admin User',
        'difficulty_level': 'Intermediate',
        'project_type': 'Major Project',
        'phase': 'Completed',
        'technologies': 'Python, Django, React, PostgreSQL, Redis',
        'video_tutorial': 'https://www.youtube.com/watch?v=example',
        'screenshots': ['screenshot1.jpg', 'screenshot2.jpg'],
        'zip_file': 'project_files.zip',
        'requirements': 'Full-stack development with payment integration'
    },
    {
        'id': 2,
        'title': 'AI Research Tool',
        'description': 'Advanced AI tool for research purposes',
        'price': 2500,
        'domain': 'AI/ML',
        'status': 'Completed',
        'created_date': '2024-01-10',
        'developer_name': 'Admin User',
        'difficulty_level': 'Advanced',
        'project_type': 'Major Project',
        'phase': 'Completed',
        'technologies': 'Python, TensorFlow, PyTorch, Scikit-learn',
        'video_tutorial': 'https://www.youtube.com/watch?v=example2',
        'screenshots': ['screenshot3.jpg'],
        'zip_file': 'ai_tool.zip',
        'requirements': 'Machine learning implementation'
    }
]

student_projects_data = [
    {
        'id': 1,
        'title': 'E-commerce Website',
        'student_name': 'John Doe',
        'email': 'john.doe@student.edu',
        'price': 800,
        'domain': 'Web Development',
        'description': 'Student e-commerce project with basic features',
        'technologies': 'HTML, CSS, JavaScript, PHP, MySQL',
        'status': 'Active',
        'created_date': '2024-01-12',
        'project_type': 'Mini Project'
    },
    {
        'id': 2,
        'title': 'Mobile Fitness App',
        'student_name': 'Jane Smith',
        'email': 'jane.smith@student.edu',
        'price': 600,
        'domain': 'Mobile App',
        'description': 'Fitness tracking mobile application',
        'technologies': 'React Native, Firebase, Node.js',
        'status': 'In Progress',
        'created_date': '2024-01-08',
        'project_type': 'Major Project'
    },
    {
        'id': 3,
        'title': 'AI Chatbot',
        'student_name': 'Mike Johnson',
        'email': 'mike.johnson@student.edu',
        'price': 1200,
        'domain': 'AI/ML',
        'description': 'AI-powered chatbot for customer service',
        'technologies': 'Python, NLTK, TensorFlow, Flask',
        'status': 'Completed',
        'created_date': '2024-01-05',
        'project_type': 'Major Project'
    },
    {
        'id': 4,
        'title': 'Data Analysis Tool',
        'student_name': 'Sarah Wilson',
        'email': 'sarah.wilson@student.edu',
        'price': 900,
        'domain': 'Data Science',
        'description': 'Data analysis and visualization tool',
        'technologies': 'Python, Pandas, Matplotlib, Seaborn',
        'status': 'Under Review',
        'created_date': '2024-01-03',
        'project_type': 'Mini Project'
    }
]

requested_projects_data = [
    {
        "id": 1,
        "title": "E-commerce Website",
        "name": "John Doe",
        "email": "john@example.com",
        "price": "299",
        "domain": "Web Development",
        "description": "A fully functional e-commerce website with user authentication, product catalog, shopping cart, and payment integration.",
        "difficulty": "Intermediate",
        "project_type": "Major Project",
        "technologies": "HTML, CSS, JavaScript, React, Node.js, MongoDB"
    },
    {
        "id": 2,
        "title": "Mobile App",
        "name": "Jane Smith",
        "email": "jane@example.com",
        "price": "499",
        "domain": "Mobile Development",
        "description": "Cross-platform mobile application for task management with cloud synchronization.",
        "difficulty": "Advanced",
        "project_type": "Major Project",
        "technologies": "React Native, Firebase, Redux"
    }
]

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@login_required
def dashboard():
    stats = {
        "total_projects": len(projects) + len(admin_projects_data) + len(student_projects_data),
        "requested_projects": len(requested_projects_data),
        "admin_projects": len(admin_projects_data),
        "student_projects": len(student_projects_data)
    }
    return render_template('dashboard.html', projects=projects, stats=stats)

@admin_bp.route('/add-new-project')
@login_required
def add_new_project_page():
    return render_template('add_new_project.html')

@admin_bp.route('/add_project', methods=['POST'])
@login_required
def add_project():
    if request.method == 'POST':
        # Get form data
        title = request.form.get('project-title')
        difficulty = request.form.get('difficulty-level')
        price = request.form.get('price')
        domain = request.form.get('domain')
        project_type = request.form.get('project-type')
        description = request.form.get('description')
        technologies = request.form.get('technologies')
        video_url = request.form.get('video-url')
        
        # Handle file uploads
        screenshots = request.files.getlist('screenshots')
        zip_file = request.files.get('zip-file')
        
        # Process the form data (in real app, save to database)
        new_project = {
            "id": len(projects) + 1,
            "title": title,
            "name": "Admin",  # Default name
            "price": price,
            "domain": domain,
            "project_type": project_type,
            "difficulty": difficulty,
            "description": description,
            "technologies": technologies.split(',') if technologies else [],
            "video_url": video_url,
            "screenshots_count": len(screenshots),
            "has_zip": bool(zip_file and zip_file.filename)
        }
        
        # Add to projects list
        projects.append(new_project)
        
        flash('Project added successfully!', 'success')
        return redirect(url_for('dashboard'))

@admin_bp.route('/delete_project/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    global projects
    projects = [p for p in projects if p['id'] != project_id]
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/requested-projects')
@login_required
def requested_projects():
    return render_template('requested_projects.html', projects=requested_projects_data)

@admin_bp.route('/requested-project-details/<int:project_id>')
@login_required
def requested_project_details(project_id):
    # Find the requested project
    project = next((p for p in requested_projects_data if p['id'] == project_id), None)
    
    if project:
        project_details = {
            "id": project_id,
            "student": {
                "name": project['name'],
                "email": project['email'],
                "phone": "+1 (555) 123-4567",
                "message_no": f"MSG-{project_id:03d}",
                "college": "Stanford University",
                "course": "Computer Science",
                "year": "3rd Year"
            },
            "project": {
                "title": project['title'],
                "difficulty": project.get('difficulty', 'Intermediate'),
                "project_type": project.get('project_type', 'Mini Project'),
                "description": project['description'],
                "developer": project['name'],
                "price": f"${project['price']}",
                "domain": project['domain'],
                "technologies": project.get('technologies', 'Not specified'),
                "video_url": "https://youtube.com/watch?v=example123"
            },
            "screenshots": ["screenshot1.jpg", "screenshot2.jpg", "screenshot3.jpg"]
        }
        
        return render_template('requested_projects_details.html', project=project_details)
    else:
        flash('Project not found!', 'error')
        return redirect(url_for('admin.requested_projects'))

@admin_bp.route('/admin-projects')
@login_required
def admin_projects():
    return render_template('admin_project.html', admin_projects=admin_projects_data)

@admin_bp.route('/admin-projects/<int:project_id>')
@login_required
def admin_project_details(project_id):
    # Find the admin project
    project = next((p for p in admin_projects_data if p['id'] == project_id), None)
    
    if project:
        return render_template('admin_project_details.html', project=project)
    else:
        flash('Project not found!', 'error')
        return redirect(url_for('admin.admin_projects'))

@admin_bp.route('/add-admin-project', methods=['POST'])
@login_required
def add_admin_project():
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        price = float(request.form.get('price'))
        domain = request.form.get('domain')
        status = request.form.get('status')
        description = request.form.get('description')
        developer_name = request.form.get('developer_name')
        difficulty_level = request.form.get('difficulty_level')
        technologies = request.form.get('technologies')
        requirements = request.form.get('requirements', '')
        
        # Create new project
        new_project = {
            'id': len(admin_projects_data) + 1,
            'title': title,
            'description': description,
            'price': price,
            'domain': domain,
            'status': status,
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'developer_name': developer_name,
            'difficulty_level': difficulty_level,
            'technologies': technologies,
            'requirements': requirements,
            'phase': 'Planning',
            'video_tutorial': '',
            'screenshots': [],
            'zip_file': ''
        }
        
        # Add to admin projects
        admin_projects_data.append(new_project)
        
        flash('Admin project added successfully!', 'success')
        return redirect(url_for('admin.admin_projects'))

@admin_bp.route('/update-admin-project/<int:project_id>', methods=['POST'])
@login_required
def update_admin_project(project_id):
    if request.method == 'POST':
        # Find the project
        project = next((p for p in admin_projects_data if p['id'] == project_id), None)

        if project:
            # Update project data
            project['title'] = request.form.get('title')
            project['price'] = float(request.form.get('price'))
            project['domain'] = request.form.get('domain')
            project['project_type'] = request.form.get('project_type')
            project['status'] = request.form.get('status')
            project['description'] = request.form.get('description')
            project['developer_name'] = request.form.get('developer_name')
            project['difficulty_level'] = request.form.get('difficulty_level')
            project['technologies'] = request.form.get('technologies')
            project['phase'] = request.form.get('phase')
            project['video_tutorial'] = request.form.get('video_tutorial', '')

            # Handle file removals
            remove_images = request.form.getlist('remove_images')
            for image in remove_images:
                if image in project['screenshots']:
                    project['screenshots'].remove(image)

            flash('Project updated successfully!', 'success')
            return redirect(url_for('admin.admin_project_details', project_id=project_id))
        else:
            flash('Project not found!', 'error')
            return redirect(url_for('admin.admin_projects'))

@admin_bp.route('/delete-admin-project/<int:project_id>', methods=['DELETE'])
@login_required
def delete_admin_project(project_id):
    global admin_projects_data
    admin_projects_data = [p for p in admin_projects_data if p['id'] != project_id]
    return jsonify({'success': True, 'message': 'Project deleted successfully'})

@admin_bp.route('/student-projects')
@login_required
def student_projects():
    return render_template('student_project.html', student_projects=student_projects_data)

@admin_bp.route('/student-project-details/<int:project_id>')
@login_required
def student_project_details(project_id):
    # Find the student project
    project = next((p for p in student_projects_data if p['id'] == project_id), None)
    
    if project:
        # Add additional student information
        project_full = {
            **project,
            'mobile': '+1 (555) 123-4567',
            'college': 'Stanford University',
            'course': 'Computer Science',
            'year': '3rd Year',
            'difficulty_level': project.get('difficulty_level', 'Intermediate'),
            'project_type': project.get('project_type', 'Mini Project'),
            'video_tutorial': project.get('video_tutorial', 'https://www.youtube.com/watch?v=example'),
            'screenshots': project.get('screenshots', ['screenshot1.jpg', 'screenshot2.jpg']),
            'zip_file': project.get('zip_file', 'student_project_files.zip'),
            'technologies': project.get('technologies', 'HTML, CSS, JavaScript, React, Node.js'),
            'description': project.get('description', 'A detailed student project description.')
        }
        return render_template('student_project_details.html', project=project_full)
    else:
        flash('Project not found!', 'error')
        return redirect(url_for('admin.student_projects'))

@admin_bp.route('/delete-student-project/<int:project_id>', methods=['DELETE'])
@login_required
def delete_student_project(project_id):
    global student_projects_data
    student_projects_data = [p for p in student_projects_data if p['id'] != project_id]
    return jsonify({'success': True, 'message': 'Student project deleted successfully'})

@admin_bp.route('/total-projects')
@login_required
def total_projects():
    # Combine all projects
    total_projects_list = []
    
    # Add admin projects
    for project in admin_projects_data:
        total_projects_list.append({
            'id': project['id'],
            'type': 'admin',
            'title': project['title'],
            'name': project['developer_name'],
            'email': 'admin@innovateguide.com',
            'price': project['price'],
            'domain': project['domain'],
            'status': project['status'],
            'description': project['description']
        })
    
    # Add student projects
    for project in student_projects_data:
        total_projects_list.append({
            'id': project['id'],
            'type': 'student',
            'title': project['title'],
            'name': project['student_name'],
            'email': project['email'],
            'price': project['price'],
            'domain': project['domain'],
            'status': project.get('status', 'Active'),
            'description': project['description']
        })
    
    # Add requested projects (if approved)
    for project in requested_projects_data:
        total_projects_list.append({
            'id': project['id'],
            'type': 'requested',
            'title': project['title'],
            'name': project['name'],
            'email': project['email'],
            'price': float(project['price']),
            'domain': project['domain'],
            'status': 'Pending',
            'description': project['description']
        })
    
    return render_template('total_project.html', 
                         total_projects=total_projects_list,
                         total_projects_count=len(total_projects_list),
                         admin_projects_count=len(admin_projects_data),
                         student_projects_count=len(student_projects_data))

@admin_bp.route('/search')
@login_required
def search_projects():
    query = request.args.get('q', '')
    if query:
        filtered_projects = [p for p in projects if query.lower() in p['title'].lower()]
    else:
        filtered_projects = projects
    
    stats = {
        "total_projects": len(projects) + len(admin_projects_data) + len(student_projects_data),
        "requested_projects": len(requested_projects_data),
        "admin_projects": len(admin_projects_data),
        "student_projects": len(student_projects_data)
    }
    
    return render_template('dashboard.html', 
                         projects=filtered_projects, 
                         stats=stats, 
                         search_query=query)

# Additional utility routes
@admin_bp.route('/approve-project/<int:project_id>')
@login_required
def approve_project(project_id):
    # Find and approve requested project
    project = next((p for p in requested_projects_data if p['id'] == project_id), None)
    if project:
        # Move to student projects or update status
        flash(f'Project "{project["title"]}" approved successfully!', 'success')
    else:
        flash('Project not found!', 'error')
    return redirect(url_for('admin.requested_projects'))

@admin_bp.route('/update-student-project/<int:project_id>', methods=['POST'])
@login_required
def update_student_project(project_id):
    if request.method == 'POST':
        # Find the student project
        project = next((p for p in student_projects_data if p['id'] == project_id), None)

        if project:
            # Update project data
            project['title'] = request.form.get('title')
            project['price'] = float(request.form.get('price'))
            project['domain'] = request.form.get('domain')
            project['project_type'] = request.form.get('project_type')
            project['status'] = request.form.get('status')
            project['description'] = request.form.get('description')
            project['difficulty_level'] = request.form.get('difficulty_level')
            project['technologies'] = request.form.get('technologies')
            project['video_tutorial'] = request.form.get('video_tutorial', '')

            flash('Student project updated successfully!', 'success')
            return redirect(url_for('admin.student_project_details', project_id=project_id))
        else:
            flash('Student project not found!', 'error')
            return redirect(url_for('admin.student_projects'))

@admin_bp.route('/reject-project/<int:project_id>')
@login_required
def reject_project(project_id):
    # Find and reject requested project
    project = next((p for p in requested_projects_data if p['id'] == project_id), None)
    if project:
        # Remove from requested projects or update status
        requested_projects_data.remove(project)
        flash(f'Project "{project["title"]}" rejected!', 'success')
    else:
        flash('Project not found!', 'error')
    return redirect(url_for('admin.requested_projects'))
