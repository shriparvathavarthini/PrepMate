import logging
from datetime import datetime, timedelta

class StudyPlanGenerator:
    """
    Generates personalized 7-day DSA study plans using greedy algorithms.
    Prioritizes topics with lower skill ratings for more focused learning.
    """
    
    def __init__(self):
        # DSA topics with estimated study time (in hours) and prerequisites
        self.topics_info = {
            'Arrays': {'time': 2, 'difficulty': 1, 'prerequisites': []},
            'Strings': {'time': 2, 'difficulty': 1, 'prerequisites': []},
            'Linked Lists': {'time': 3, 'difficulty': 2, 'prerequisites': []},
            'Stacks': {'time': 2, 'difficulty': 2, 'prerequisites': ['Arrays']},
            'Queues': {'time': 2, 'difficulty': 2, 'prerequisites': ['Arrays']},
            'Hash Tables': {'time': 3, 'difficulty': 2, 'prerequisites': ['Arrays']},
            'Binary Trees': {'time': 4, 'difficulty': 3, 'prerequisites': ['Linked Lists']},
            'Binary Search Trees': {'time': 3, 'difficulty': 3, 'prerequisites': ['Binary Trees']},
            'Heaps': {'time': 3, 'difficulty': 3, 'prerequisites': ['Binary Trees']},
            'Graphs': {'time': 5, 'difficulty': 4, 'prerequisites': ['Hash Tables']},
            'Dynamic Programming': {'time': 6, 'difficulty': 5, 'prerequisites': ['Arrays', 'Strings']},
            'Greedy Algorithms': {'time': 4, 'difficulty': 4, 'prerequisites': ['Arrays']},
            'Backtracking': {'time': 4, 'difficulty': 4, 'prerequisites': ['Arrays', 'Strings']},
            'Sorting Algorithms': {'time': 3, 'difficulty': 2, 'prerequisites': ['Arrays']},
            'Searching Algorithms': {'time': 2, 'difficulty': 2, 'prerequisites': ['Arrays']},
            'Two Pointers': {'time': 2, 'difficulty': 2, 'prerequisites': ['Arrays']},
            'Sliding Window': {'time': 3, 'difficulty': 3, 'prerequisites': ['Arrays', 'Two Pointers']},
            'Bit Manipulation': {'time': 2, 'difficulty': 3, 'prerequisites': []},
            'Trie': {'time': 3, 'difficulty': 3, 'prerequisites': ['Strings', 'Binary Trees']},
            'Union Find': {'time': 3, 'difficulty': 3, 'prerequisites': ['Arrays']},
        }
        
        # Practice problems for each topic
        self.practice_problems = {
            'Arrays': [
                'Two Sum', 'Best Time to Buy and Sell Stock', 'Contains Duplicate',
                'Product of Array Except Self', 'Maximum Subarray'
            ],
            'Strings': [
                'Valid Anagram', 'Valid Palindrome', 'Longest Common Prefix',
                'String to Integer (atoi)', 'Implement strStr()'
            ],
            'Linked Lists': [
                'Reverse Linked List', 'Merge Two Sorted Lists', 'Linked List Cycle',
                'Remove Nth Node From End', 'Intersection of Two Linked Lists'
            ],
            'Stacks': [
                'Valid Parentheses', 'Min Stack', 'Evaluate Reverse Polish Notation',
                'Daily Temperatures', 'Next Greater Element'
            ],
            'Queues': [
                'Implement Queue using Stacks', 'Moving Average from Data Stream',
                'Design Circular Queue', 'Number of Islands (BFS)', 'Perfect Squares'
            ],
            'Hash Tables': [
                'Two Sum', 'Group Anagrams', 'Top K Frequent Elements',
                'Subarray Sum Equals K', 'Longest Substring Without Repeating Characters'
            ],
            'Binary Trees': [
                'Maximum Depth of Binary Tree', 'Same Tree', 'Invert Binary Tree',
                'Binary Tree Level Order Traversal', 'Path Sum'
            ],
            'Binary Search Trees': [
                'Validate Binary Search Tree', 'Lowest Common Ancestor of BST',
                'Convert Sorted Array to BST', 'Kth Smallest Element in BST', 'Range Sum of BST'
            ],
            'Heaps': [
                'Kth Largest Element in Array', 'Merge k Sorted Lists', 'Top K Frequent Elements',
                'Find Median from Data Stream', 'Last Stone Weight'
            ],
            'Graphs': [
                'Number of Islands', 'Clone Graph', 'Course Schedule',
                'Pacific Atlantic Water Flow', 'Alien Dictionary'
            ],
            'Dynamic Programming': [
                'Climbing Stairs', 'House Robber', 'Coin Change',
                'Longest Increasing Subsequence', 'Edit Distance'
            ],
            'Greedy Algorithms': [
                'Jump Game', 'Gas Station', 'Partition Labels',
                'Non-overlapping Intervals', 'Minimum Number of Arrows'
            ],
            'Backtracking': [
                'Permutations', 'Subsets', 'Combination Sum',
                'N-Queens', 'Word Search'
            ],
            'Sorting Algorithms': [
                'Sort Colors', 'Merge Intervals', 'Largest Number',
                'Meeting Rooms II', 'Kth Largest Element'
            ],
            'Searching Algorithms': [
                'Binary Search', 'Search in Rotated Sorted Array', 'Find First and Last Position',
                'Search a 2D Matrix', 'Find Peak Element'
            ],
            'Two Pointers': [
                'Two Sum II', 'Three Sum', 'Container With Most Water',
                'Remove Duplicates from Sorted Array', 'Trapping Rain Water'
            ],
            'Sliding Window': [
                'Maximum Subarray', 'Minimum Window Substring', 'Longest Substring Without Repeating',
                'Permutation in String', 'Sliding Window Maximum'
            ],
            'Bit Manipulation': [
                'Single Number', 'Number of 1 Bits', 'Counting Bits',
                'Missing Number', 'Reverse Bits'
            ],
            'Trie': [
                'Implement Trie', 'Word Search II', 'Add and Search Word',
                'Replace Words', 'Map Sum Pairs'
            ],
            'Union Find': [
                'Number of Islands', 'Friend Circles', 'Redundant Connection',
                'Accounts Merge', 'Most Stones Removed'
            ]
        }
    
    def generate_plan(self, user_ratings):
        """
        Generate a 7-day study plan using greedy algorithm.
        Prioritizes topics with lower skill ratings.
        
        Args:
            user_ratings: dict mapping topic names to skill levels (1-5)
        
        Returns:
            dict: 7-day study plan with daily recommendations
        """
        logging.info(f"Generating study plan for ratings: {user_ratings}")
        
        # Calculate priority scores using greedy approach
        topic_priorities = self._calculate_priorities(user_ratings)
        
        # Distribute topics across 7 days
        daily_plan = self._distribute_topics(topic_priorities)
        
        # Generate detailed study plan
        study_plan = self._create_detailed_plan(daily_plan, user_ratings)
        
        return study_plan
    
    def _calculate_priorities(self, user_ratings):
        """
        Calculate priority scores for topics using greedy algorithm.
        Lower skill rating = higher priority.
        """
        priorities = []
        
        for topic, skill_level in user_ratings.items():
            if topic in self.topics_info:
                # Greedy priority: inverse of skill level + difficulty factor
                base_priority = (6 - skill_level)  # Higher score for lower skill
                difficulty_bonus = self.topics_info[topic]['difficulty'] * 0.5
                time_factor = self.topics_info[topic]['time'] / 10  # Normalize time
                
                # Check if prerequisites are met
                prereq_penalty = self._calculate_prereq_penalty(topic, user_ratings)
                
                final_priority = base_priority + difficulty_bonus + time_factor - prereq_penalty
                
                priorities.append({
                    'topic': topic,
                    'priority': final_priority,
                    'skill_level': skill_level,
                    'estimated_time': self.topics_info[topic]['time']
                })
        
        # Sort by priority (descending - highest priority first)
        priorities.sort(key=lambda x: x['priority'], reverse=True)
        logging.info(f"Topic priorities calculated: {[(p['topic'], p['priority']) for p in priorities]}")
        
        return priorities
    
    def _calculate_prereq_penalty(self, topic, user_ratings):
        """Calculate penalty if prerequisites are not well understood"""
        prereqs = self.topics_info[topic]['prerequisites']
        penalty = 0
        
        for prereq in prereqs:
            if prereq in user_ratings:
                # Penalty if prerequisite skill is low
                if user_ratings[prereq] < 3:
                    penalty += (3 - user_ratings[prereq]) * 0.5
            else:
                # Higher penalty if prerequisite not rated (unknown)
                penalty += 2
        
        return penalty
    
    def _distribute_topics(self, topic_priorities):
        """Distribute topics across 7 days with time constraints"""
        daily_plan = {f'day_{i+1}': [] for i in range(7)}
        daily_time_limits = [3, 3, 4, 4, 4, 3, 2]  # Hours per day
        daily_time_used = [0] * 7
        
        for topic_info in topic_priorities:
            # Find the best day for this topic (greedy approach)
            best_day = -1
            for day in range(7):
                if daily_time_used[day] + topic_info['estimated_time'] <= daily_time_limits[day]:
                    best_day = day
                    break
            
            if best_day != -1:
                daily_plan[f'day_{best_day + 1}'].append(topic_info)
                daily_time_used[best_day] += topic_info['estimated_time']
            else:
                # If no day has enough time, add to day with most available time
                best_day = daily_time_used.index(min(daily_time_used))
                daily_plan[f'day_{best_day + 1}'].append(topic_info)
                daily_time_used[best_day] += topic_info['estimated_time']
        
        return daily_plan
    
    def _create_detailed_plan(self, daily_plan, user_ratings):
        """Create detailed study plan with problems and time estimates"""
        detailed_plan = {
            'generated_at': datetime.now().isoformat(),
            'total_topics': len(user_ratings),
            'plan_duration': '7 days',
            'daily_schedule': {}
        }
        
        start_date = datetime.now()
        
        for day_key, topics in daily_plan.items():
            day_num = int(day_key.split('_')[1])
            current_date = start_date + timedelta(days=day_num - 1)
            
            day_details = {
                'date': current_date.strftime('%Y-%m-%d'),
                'day_name': current_date.strftime('%A'),
                'topics': [],
                'total_time': 0,
                'focus_areas': []
            }
            
            for topic_info in topics:
                topic_name = topic_info['topic']
                skill_level = topic_info['skill_level']
                
                # Select appropriate problems based on skill level
                problems = self._select_problems(topic_name, skill_level)
                
                topic_details = {
                    'name': topic_name,
                    'current_skill_level': skill_level,
                    'estimated_time': topic_info['estimated_time'],
                    'priority_score': round(topic_info['priority'], 2),
                    'recommended_problems': problems,
                    'study_approach': self._get_study_approach(topic_name, skill_level),
                    'resources': self._get_study_resources(topic_name)
                }
                
                day_details['topics'].append(topic_details)
                day_details['total_time'] += topic_info['estimated_time']
                
                # Add to focus areas if low skill level
                if skill_level <= 2:
                    day_details['focus_areas'].append(topic_name)
            
            detailed_plan['daily_schedule'][day_key] = day_details
        
        return detailed_plan
    
    def _select_problems(self, topic, skill_level):
        """Select appropriate problems based on skill level"""
        if topic not in self.practice_problems:
            return []
        
        all_problems = self.practice_problems[topic]
        
        # Select problems based on skill level
        if skill_level <= 2:  # Beginner
            return all_problems[:3]  # Easy problems
        elif skill_level <= 3:  # Intermediate
            return all_problems[:4]  # Mix of easy and medium
        else:  # Advanced
            return all_problems  # All problems including hard ones
    
    def _get_study_approach(self, topic, skill_level):
        """Get recommended study approach based on skill level"""
        approaches = {
            1: "Start with basic concepts and simple examples. Focus on understanding fundamentals.",
            2: "Review theory briefly, then practice basic problems. Build confidence with easy exercises.",
            3: "Quick theory review, then focus on medium-difficulty problems. Work on pattern recognition.",
            4: "Minimal theory review. Focus on challenging problems and optimization techniques.",
            5: "Practice advanced problems and edge cases. Focus on interview-level questions."
        }
        return approaches.get(skill_level, approaches[3])
    
    def _get_study_resources(self, topic):
        """Get recommended study resources for the topic"""
        return {
            'theory': f"Review {topic} concepts and time complexity",
            'practice': f"LeetCode {topic} problems",
            'reference': f"GeeksforGeeks {topic} articles"
        }
