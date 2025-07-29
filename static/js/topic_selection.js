// Topic selection utilities
export class TopicManager {
    constructor() {
        this.selectedTopics = new Map();
        this.searchTerm = '';
        this.currentFilter = 'all';
    }

    initialize(existingRatings = {}) {
        this.selectedTopics.clear();
        Object.entries(existingRatings).forEach(([topic, rating]) => {
            this.selectedTopics.set(topic, rating);
        });
        this.updateUI();
    }

    addTopic(topicName, rating) {
        this.selectedTopics.set(topicName, rating);
        this.updateUI();
    }

    removeTopic(topicName) {
        this.selectedTopics.delete(topicName);
        this.updateUI();
    }

    updateTopicRating(topicName, rating) {
        if (this.selectedTopics.has(topicName)) {
            this.selectedTopics.set(topicName, rating);
            this.updateUI();
        }
    }

    getSelectedTopics() {
        return Object.fromEntries(this.selectedTopics);
    }

    getTopicCount() {
        return this.selectedTopics.size;
    }

    setSearchTerm(term) {
        this.searchTerm = term.toLowerCase();
        this.filterTopics();
    }

    setFilter(filter) {
        this.currentFilter = filter;
        this.filterTopics();
    }

    filterTopics() {
        const topicCards = document.querySelectorAll('.topic-card');
        topicCards.forEach(card => {
            const topicName = card.dataset.topic.toLowerCase();
            const difficulty = card.dataset.difficulty;
            
            const matchesSearch = topicName.includes(this.searchTerm);
            const matchesFilter = this.currentFilter === 'all' || difficulty === this.currentFilter;
            
            card.closest('.topic-item').style.display = 
                matchesSearch && matchesFilter ? 'block' : 'none';
        });
    }

    updateUI() {
        // Update selected count
        const countElement = document.getElementById('selectedCount');
        if (countElement) {
            countElement.textContent = `${this.getTopicCount()} selected`;
        }

        // Update button states
        const saveBtn = document.getElementById('saveRatingsBtn');
        const generateBtn = document.getElementById('generatePlanBtn');
        const hasTopics = this.getTopicCount() > 0;
        
        if (saveBtn) saveBtn.disabled = !hasTopics;
        if (generateBtn) generateBtn.disabled = !hasTopics;
    }

    validateSelection() {
        return this.getTopicCount() > 0;
    }
}

// Rating utilities
export class RatingManager {
    static createRatingStars(topicName, currentRating = 0) {
        const starsContainer = document.createElement('div');
        starsContainer.className = 'rating-stars';
        starsContainer.dataset.topic = topicName;

        for (let i = 1; i <= 5; i++) {
            const star = document.createElement('span');
            star.className = `star ${i <= currentRating ? 'active' : ''}`;
            star.dataset.rating = i;
            star.textContent = '★';
            star.addEventListener('click', (e) => this.handleStarClick(e));
            starsContainer.appendChild(star);
        }

        return starsContainer;
    }

    static handleStarClick(event) {
        const rating = parseInt(event.target.dataset.rating);
        const topicName = event.target.closest('.rating-stars').dataset.topic;
        const stars = event.target.closest('.rating-stars').querySelectorAll('.star');
        
        // Update visual state
        stars.forEach((star, index) => {
            star.classList.toggle('active', index < rating);
        });

        // Dispatch custom event
        const ratingEvent = new CustomEvent('ratingChanged', {
            detail: { topic: topicName, rating: rating }
        });
        document.dispatchEvent(ratingEvent);
    }

    static getRatingText(rating) {
        const texts = {
            1: 'Beginner',
            2: 'Novice', 
            3: 'Intermediate',
            4: 'Advanced',
            5: 'Expert'
        };
        return texts[rating] || 'Not rated';
    }
}
