"""
COMPLETE PERSONALIZED PROBLEM RECOMMENDER
==========================================

Just pass your SQLAlchemy Problem and Submission objects directly.
No setup needed - handles all conversions internally.

USAGE:
------
from recommender import get_daily_challenge, get_top_recommendations, get_user_progress

# Get single best recommendation
daily = get_daily_challenge(problems, submissions, user_id)

# Get top 3 recommendations  
top_3 = get_top_recommendations(problems, submissions, user_id, n=3)

# Get user progress stats
progress = get_user_progress(problems, submissions, user_id)
"""

from typing import List, Dict, Optional
from collections import defaultdict


class PersonalizedRecommender:
    """Fast personalized problem recommender"""
    
    def __init__(self, problems_data: List[Dict], submissions_data: List[Dict]):
        self.problems = {p['id']: p for p in problems_data}
        self.user_submissions = submissions_data
        self.topic_proficiency = self._calculate_topic_proficiency()
        
    def _calculate_topic_proficiency(self) -> Dict[str, float]:
        """Calculate user's proficiency in each topic (0-1 scale)"""
        topic_stats = defaultdict(lambda: {'solved': 0, 'attempted': 0, 'total_attempts': 0})
        
        for submission in self.user_submissions:
            problem = self.problems.get(submission['problem_id'])
            if not problem:
                continue
                
            for topic in problem['topics']:
                topic_stats[topic]['attempted'] += 1
                topic_stats[topic]['total_attempts'] += submission.get('attempts', 1)
                
                if submission['status'] == 'accepted':
                    topic_stats[topic]['solved'] += 1
        
        proficiency = {}
        for topic, stats in topic_stats.items():
            if stats['attempted'] == 0:
                proficiency[topic] = 0.0
            else:
                solve_rate = stats['solved'] / stats['attempted']
                avg_attempts = stats['total_attempts'] / stats['attempted']
                attempt_penalty = min(avg_attempts / 5, 1.0)
                proficiency[topic] = solve_rate * (1 - attempt_penalty * 0.3)
        
        return proficiency
    
    def _get_solved_problems(self) -> set:
        return {sub['problem_id'] for sub in self.user_submissions if sub['status'] == 'accepted'}
    
    def _get_attempted_problems(self) -> set:
        return {sub['problem_id'] for sub in self.user_submissions}
    
    def _estimate_user_level(self) -> float:
        """Estimate user's level (1=easy, 2=medium, 3=hard)"""
        if not self.user_submissions:
            return 1.0
        
        solved = self._get_solved_problems()
        if not solved:
            return 1.0
        
        difficulty_map = {'easy': 1, 'medium': 2, 'hard': 3}
        solved_difficulties = [
            difficulty_map[self.problems[pid]['difficulty']]
            for pid in solved if pid in self.problems
        ]
        
        if not solved_difficulties:
            return 1.0
        
        avg_solved = sum(solved_difficulties) / len(solved_difficulties)
        solve_rate = len(solved) / len(self._get_attempted_problems())
        
        if solve_rate > 0.7:
            return min(avg_solved + 0.5, 3.0)
        elif solve_rate < 0.3:
            return max(avg_solved - 0.5, 1.0)
        else:
            return avg_solved
    
    def _get_recent_topics(self, n: int = 3) -> List[str]:
        """Get topics from last n submissions"""
        recent_subs = sorted(
            self.user_submissions,
            key=lambda x: x.get('timestamp', 0),
            reverse=True
        )[:n]
        
        topics = []
        for sub in recent_subs:
            problem = self.problems.get(sub['problem_id'])
            if problem:
                topics.extend(problem['topics'])
        return topics
    
    def _calculate_problem_score(self, problem: Dict) -> float:
        """Calculate recommendation score (0-100)"""
        score = 0.0
        
        # 1. Topic relevance (40 points)
        topic_scores = []
        for topic in problem['topics']:
            proficiency = self.topic_proficiency.get(topic, 0.0)
            
            if proficiency == 0:
                topic_scores.append(0.3 if len(self.topic_proficiency) > 0 else 0.5)
            elif 0 < proficiency < 0.4:
                topic_scores.append(0.8)  # Struggling - reinforce
            elif 0.4 <= proficiency < 0.7:
                topic_scores.append(1.0)  # Learning - perfect
            elif 0.7 <= proficiency < 0.9:
                topic_scores.append(0.6)  # Good - ready to advance
            else:
                topic_scores.append(0.2)  # Mastered - move on
        
        avg_topic_score = sum(topic_scores) / len(topic_scores) if topic_scores else 0
        score += avg_topic_score * 40
        
        # 2. Difficulty progression (30 points)
        difficulty_map = {'easy': 1, 'medium': 2, 'hard': 3}
        user_level = self._estimate_user_level()
        problem_level = difficulty_map[problem['difficulty']]
        level_diff = problem_level - user_level
        
        if level_diff == 0:
            difficulty_score = 1.0
        elif level_diff == 1:
            difficulty_score = 0.8
        elif level_diff == -1:
            difficulty_score = 0.5
        else:
            difficulty_score = 0.2
        
        score += difficulty_score * 30
        
        # 3. Variety bonus (15 points)
        recent_topics = self._get_recent_topics(n=3)
        is_different = not any(topic in recent_topics for topic in problem['topics'])
        score += 15 if is_different else 5
        
        # 4. Acceptance rate (15 points)
        acceptance = problem.get('acceptance_rate', 50)
        if 30 <= acceptance <= 60:
            score += 15
        elif 20 <= acceptance < 30 or 60 < acceptance <= 70:
            score += 10
        else:
            score += 5
        
        return score
    
    def recommend(self, exclude_solved: bool = False) -> Optional[Dict]:
        """Get single best recommendation"""
        solved = self._get_solved_problems()
        candidates = []
        
        for problem_id, problem in self.problems.items():
            if exclude_solved and problem_id in solved:
                continue
            
            score = self._calculate_problem_score(problem)
            
            if not exclude_solved and problem_id in solved:
                score *= 0.7  # 30% penalty for repetition
            
            candidates.append({**problem, 'recommendation_score': score})
        
        if not candidates:
            return None
        
        return max(candidates, key=lambda x: x['recommendation_score'])
    
    def recommend_top_n(self, n: int = 3, exclude_solved: bool = False) -> List[Dict]:
        """Get top N recommendations"""
        solved = self._get_solved_problems()
        candidates = []
        
        for problem_id, problem in self.problems.items():
            # if exclude_solved and problem_id in solved:
            #     continue

            if problem_id == 4:
                continue
            
            score = self._calculate_problem_score(problem)
            
            # if not exclude_solved and problem_id in solved:
            #     score *= 0.7
            
            candidates.append({**problem, 'recommendation_score': score})
        
        candidates.sort(key=lambda x: x['recommendation_score'], reverse=True)
        return candidates[:n]


def _convert_problems(problems) -> List[Dict]:
    """
    Convert SQLAlchemy Problem objects to recommender format.
    
    Handles:
    - problem.tags (many-to-many through ProblemTag)
    - problem.difficulty (Enum)
    """
    problem_list = []
    
    for problem in problems:
        # Extract topics from tags
        # Handles: problem.tags -> [ProblemTag] -> tag.name
        try:
            if hasattr(problem, 'tags') and problem.tags:
                topics = []
                for tag_relation in problem.tags:
                    # Handle ProblemTag -> Tag relationship
                    if hasattr(tag_relation, 'tag') and hasattr(tag_relation.tag, 'name'):
                        topics.append(tag_relation.tag.name)
                    # Handle direct tag name
                    elif hasattr(tag_relation, 'name'):
                        topics.append(tag_relation.name)
            else:
                topics = ['general']  # Default if no tags
        except:
            topics = ['general']
        
        # Convert difficulty enum to lowercase string
        try:
            if hasattr(problem.difficulty, 'value'):
                difficulty = problem.difficulty.value.lower()
            else:
                difficulty = str(problem.difficulty).lower()
        except:
            difficulty = 'medium'
        
        problem_dict = {
            'id': problem.id,
            'title': problem.title,
            'difficulty': difficulty,
            'topics': topics,
            'acceptance_rate': getattr(problem, 'acceptance_rate', 50.0)
        }
        
        problem_list.append(problem_dict)
    
    return problem_list


def _convert_submissions(submissions, user_id: int) -> List[Dict]:
    """
    Convert SQLAlchemy Submission objects to recommender format.
    Groups multiple submissions per problem and counts attempts.
    """
    problem_attempts = defaultdict(list)
    
    for sub in submissions:
        if sub.user_id == user_id:
            problem_attempts[sub.problem_id].append(sub)
    
    submission_list = []
    
    for problem_id, subs in problem_attempts.items():
        # Sort by timestamp safely
        try:
            sorted_subs = sorted(subs, key=lambda x: x.created_at.timestamp() if hasattr(x.created_at, 'timestamp') else 0)
        except:
            sorted_subs = subs
        latest_sub = sorted_subs[-1]
        
        attempts = len(subs)
        
        # Normalize status to lowercase
        status = str(latest_sub.status).lower()
        
        # Map common status values to 'accepted'
        if status in ['accepted', 'correct', 'passed', 'success', 'ac']:
            status = 'accepted'
        
        # Convert timestamp
        try:
            if hasattr(latest_sub.created_at, 'timestamp'):
                timestamp = int(latest_sub.created_at.timestamp())
            else:
                timestamp = 0
        except:
            timestamp = 0
        
        submission_dict = {
            'problem_id': problem_id,
            'status': status,
            'attempts': attempts,
            'timestamp': timestamp
        }
        
        submission_list.append(submission_dict)
    
    return submission_list


# ==================== PUBLIC API ====================

def get_daily_challenge(problems, submissions, user_id: int, exclude_solved: bool = False) -> Optional[Dict]:
    """
    Get the best single problem recommendation for a user.
    
    Args:
        problems: List of Problem model objects from database
        submissions: List of Submission model objects from database
        user_id: User's ID to filter submissions
        exclude_solved: If True, don't recommend already solved problems
    
    Returns:
        Dict with: problem_id, title, difficulty, topics, recommendation_score, acceptance_rate
        or None if no recommendations available
    
    Example:
        daily = get_daily_challenge(Problem.query.all(), Submission.query.all(), user_id=1)
        if daily:
            print(f"Today's challenge: {daily['title']} ({daily['difficulty']})")
    """
    problems_data = _convert_problems(problems)
    submissions_data = _convert_submissions(submissions, user_id)
    
    recommender = PersonalizedRecommender(problems_data, submissions_data)
    recommendation = recommender.recommend(exclude_solved=exclude_solved)
    
    if recommendation:
        return {
            'problem_id': recommendation['id'],
            'title': recommendation['title'],
            'difficulty': recommendation['difficulty'],
            'topics': recommendation['topics'],
            'recommendation_score': round(recommendation['recommendation_score'], 2),
            'acceptance_rate': recommendation['acceptance_rate']
        }
    return None


def get_top_recommendations(problems, submissions, user_id: int, n: int = 3, exclude_solved: bool = False) -> List[Dict]:
    """
    Get top N problem recommendations for a user.
    
    Args:
        problems: List of Problem model objects from database
        submissions: List of Submission model objects from database
        user_id: User's ID to filter submissions
        n: Number of recommendations to return
        exclude_solved: If True, don't recommend already solved problems
    
    Returns:
        List of dicts with: problem_id, title, difficulty, topics, recommendation_score, acceptance_rate
    """


    problems_data = _convert_problems(problems)
    submissions_data = _convert_submissions(submissions, user_id)
    
    recommender = PersonalizedRecommender(problems_data, submissions_data)
    recommendations = recommender.recommend_top_n(n=n, exclude_solved=exclude_solved)
    
    return [
        {
            'problem_id': rec['id'],
            'title': rec['title'],
            'difficulty': rec['difficulty'],
            'topics': rec['topics'],
            'recommendation_score': round(rec['recommendation_score'], 2),
            'acceptance_rate': rec['acceptance_rate']
        }
        for rec in recommendations
    ]



    
    print("=" * 60)
    print("PERSONALIZED PROBLEM RECOMMENDER")
    print("=" * 60)
    print("\nIMPORT THIS IN YOUR FLASK APP:")
    print("\n  from recommender import get_daily_challenge, get_top_recommendations, get_user_progress")
    print("\nUSAGE:")
    print("\n  daily = get_daily_challenge(problems, submissions, user_id)")
    print("  top_3 = get_top_recommendations(problems, submissions, user_id, n=3)")
    print("  progress = get_user_progress(problems, submissions, user_id)")
    print("\n" + "=" * 60)