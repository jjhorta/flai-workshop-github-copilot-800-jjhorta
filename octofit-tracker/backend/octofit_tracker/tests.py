from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class TeamModelTest(TestCase):
    """Test Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team'
        )
    
    def test_team_creation(self):
        """Test that a team can be created"""
        self.assertIsNotNone(self.team._id)
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.description, 'A test team')


class UserModelTest(TestCase):
    """Test User model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team'
        )
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            team_id=str(self.team._id)
        )
    
    def test_user_creation(self):
        """Test that a user can be created"""
        self.assertIsNotNone(self.user._id)
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.team_id, str(self.team._id))


class TeamAPITest(APITestCase):
    """Test Team API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(
            name='Marvel Team',
            description='Heroes team'
        )
    
    def test_get_teams(self):
        """Test retrieving list of teams"""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_create_team(self):
        """Test creating a new team"""
        data = {
            'name': 'DC Team',
            'description': 'Justice League'
        }
        response = self.client.post('/api/teams/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'DC Team')


class UserAPITest(APITestCase):
    """Test User API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(
            name='Test Team',
            description='Test'
        )
        self.user = User.objects.create(
            name='Spider-Man',
            email='spiderman@marvel.com',
            team_id=str(self.team._id)
        )
    
    def test_get_users(self):
        """Test retrieving list of users"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_create_user(self):
        """Test creating a new user"""
        data = {
            'name': 'Iron Man',
            'email': 'ironman@marvel.com',
            'team_id': str(self.team._id)
        }
        response = self.client.post('/api/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Iron Man')


class ActivityAPITest(APITestCase):
    """Test Activity API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name='Team', description='Test')
        self.user = User.objects.create(
            name='Test User',
            email='test@test.com',
            team_id=str(self.team._id)
        )
        self.activity = Activity.objects.create(
            user_id=str(self.user._id),
            activity_type='Running',
            duration=30,
            distance=5.0,
            calories=300,
            date=datetime.now()
        )
    
    def test_get_activities(self):
        """Test retrieving list of activities"""
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_create_activity(self):
        """Test creating a new activity"""
        data = {
            'user_id': str(self.user._id),
            'activity_type': 'Cycling',
            'duration': 45,
            'distance': 10.0,
            'calories': 400,
            'date': datetime.now().isoformat()
        }
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['activity_type'], 'Cycling')


class WorkoutAPITest(APITestCase):
    """Test Workout API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.workout = Workout.objects.create(
            name='Super Strength',
            description='Build strength',
            difficulty_level='Advanced',
            duration=60,
            exercise_type='Strength'
        )
    
    def test_get_workouts(self):
        """Test retrieving list of workouts"""
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_create_workout(self):
        """Test creating a new workout"""
        data = {
            'name': 'Cardio Blast',
            'description': 'High intensity cardio',
            'difficulty_level': 'Intermediate',
            'duration': 30,
            'exercise_type': 'Cardio'
        }
        response = self.client.post('/api/workouts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Cardio Blast')


class LeaderboardAPITest(APITestCase):
    """Test Leaderboard API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name='Team', description='Test')
        self.user = User.objects.create(
            name='Champion',
            email='champion@test.com',
            team_id=str(self.team._id)
        )
        self.leaderboard = Leaderboard.objects.create(
            user_id=str(self.user._id),
            total_calories=5000,
            total_activities=20,
            rank=1
        )
    
    def test_get_leaderboard(self):
        """Test retrieving leaderboard"""
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_leaderboard_order(self):
        """Test leaderboard is ordered by rank"""
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if len(response.data) > 0:
            self.assertEqual(response.data[0]['rank'], 1)
