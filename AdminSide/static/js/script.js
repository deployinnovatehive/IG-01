// Main dashboard functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('InnovateGuide Admin Dashboard loaded');
    
    // Initialize any dashboard-specific functionality
    initializeDashboard();
});

function initializeDashboard() {
    // Add any dashboard initialization code here
    console.log('Dashboard initialized');
    
    // Example: Update stats in real-time
    updateStatsPeriodically();
}

function updateStatsPeriodically() {
    // This would fetch updated stats from the server in a real application
    setInterval(() => {
        fetch('/api/stats')
            .then(response => response.json())
            .then(stats => {
                // Update stats on the page
                document.getElementById('total-projects').textContent = stats.total_projects;
                document.getElementById('requested-projects').textContent = stats.requested_projects;
                document.getElementById('admin-projects').textContent = stats.admin_projects;
                document.getElementById('student-projects').textContent = stats.student_projects;
            })
            .catch(error => console.error('Error fetching stats:', error));
    }, 30000); // Update every 30 seconds
}

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        z-index: 1001;
        animation: slideIn 0.3s ease-out;
        max-width: 400px;
    `;
    
    if (type === 'success') {
        notification.style.backgroundColor = 'var(--success)';
    } else if (type === 'error') {
        notification.style.backgroundColor = 'var(--danger)';
    } else if (type === 'warning') {
        notification.style.backgroundColor = 'var(--warning)';
        notification.style.color = 'var(--dark)';
    } else {
        notification.style.backgroundColor = 'var(--primary)';
    }
    
    document.body.appendChild(notification);
    
    // Remove notification after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }
    }, 5000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);