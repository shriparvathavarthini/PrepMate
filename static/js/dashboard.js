// Dashboard utilities
export class DashboardManager {
    constructor() {
        this.userData = null;
        this.studyPlan = null;
    }

    async loadUserData() {
        try {
            const response = await fetch('/api/user-data');
            if (!response.ok) {
                throw new Error('Failed to load user data');
            }
            
            this.userData = await response.json();
            this.updateDashboard();
            return this.userData;
        } catch (error) {
            console.error('Error loading user data:', error);
            throw error;
        }
    }

    updateDashboard() {
        if (!this.userData) return;

        this.displayTopicRatings(this.userData.topic_ratings || {});
        this.displayStudyPlanSummary(this.userData.study_plan);
        this.updateUserInfo(this.userData.user);
    }

    displayTopicRatings(ratings) {
        const container = document.getElementById('topicRatings');
        const countElement = document.getElementById('topicCount');
        
        if (!container) return;

        const topicCount = Object.keys(ratings).length;
        if (countElement) {
            countElement.textContent = `${topicCount} topic${topicCount !== 1 ? 's' : ''}`;
        }

        if (topicCount === 0) {
            container.innerHTML = this.getEmptyTopicsHTML();
            return;
        }

        container.innerHTML = '';
        Object.entries(ratings).forEach(([topic, rating]) => {
            const topicCard = this.createTopicRatingCard(topic, rating);
            container.appendChild(topicCard);
        });
    }

    createTopicRatingCard(topic, rating) {
        const col = document.createElement('div');
        col.className = 'col-md-4 col-sm-6 mb-3';
        
        const stars = '★'.repeat(rating) + '☆'.repeat(5 - rating);
        
        col.innerHTML = `
            <div class="card topic-rating-card h-100">
                <div class="card-body text-center">
                    <h6 class="card-title">${topic}</h6>
                    <div class="rating-stars text-warning" style="font-size: 1.2em;">
                        ${stars}
                    </div>
                    <small class="text-muted">Level ${rating}/5</small>
                </div>
            </div>
        `;
        
        return col;
    }

    displayStudyPlanSummary(studyPlan) {
        const container = document.getElementById('studyPlanSummary');
        if (!container) return;

        if (!studyPlan) {
            container.innerHTML = this.getEmptyPlanHTML();
            return;
        }

        const totalTopics = studyPlan.total_topics || 0;
        const generatedAt = new Date(studyPlan.generated_at).toLocaleDateString();
        
        container.innerHTML = `
            <div class="row">
                <div class="col-md-4 text-center mb-3">
                    <div class="stat-item">
                        <h3 class="text-primary">${totalTopics}</h3>
                        <p class="text-muted mb-0">Topics Covered</p>
                    </div>
                </div>
                <div class="col-md-4 text-center mb-3">
                    <div class="stat-item">
                        <h3 class="text-success">7</h3>
                        <p class="text-muted mb-0">Days Plan</p>
                    </div>
                </div>
                <div class="col-md-4 text-center mb-3">
                    <div class="stat-item">
                        <h3 class="text-info">${generatedAt}</h3>
                        <p class="text-muted mb-0">Generated</p>
                    </div>
                </div>
            </div>
            <div class="text-center mt-3">
                <a href="/study-plan" class="btn btn-primary">
                    <i class="fas fa-eye me-1"></i>View Detailed Plan
                </a>
            </div>
        `;
    }

    updateUserInfo(user) {
        const userNameElement = document.getElementById('userName');
        if (userNameElement && user) {
            userNameElement.textContent = user.display_name || user.email || 'User';
        }
    }

    getEmptyTopicsHTML() {
        return `
            <div class="col-12 text-center text-muted py-4">
                <i class="fas fa-info-circle fa-2x mb-3"></i>
                <p>No topics rated yet. <a href="/topics" class="text-decoration-none">Start by selecting topics</a> to get personalized recommendations.</p>
            </div>
        `;
    }

    getEmptyPlanHTML() {
        return `
            <div class="text-center text-muted py-4">
                <i class="fas fa-calendar-plus fa-2x mb-3"></i>
                <p>No active study plan. Generate one after rating your topics!</p>
            </div>
        `;
    }

    showProgress(show = true) {
        const loadingState = document.getElementById('loadingState');
        const mainContent = document.getElementById('mainContent');
        
        if (loadingState) {
            loadingState.classList.toggle('d-none', !show);
        }
        if (mainContent) {
            mainContent.classList.toggle('d-none', show);
        }
    }

    showError(message) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(alert, container.firstChild);
        }
        
        setTimeout(() => {
            alert.remove();
        }, 5000);
    }
}
