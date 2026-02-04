from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
from pymongo import MongoClient
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing data...')
        
        # Delete existing data using Django ORM
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write('Creating teams...')
        
        # Create teams
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Mightiest Heroes of Earth',
            created_at=datetime.now()
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League Defenders',
            created_at=datetime.now()
        )
        
        self.stdout.write('Creating users...')
        
        # Create Marvel superheroes
        marvel_heroes = [
            {'name': 'Iron Man', 'email': 'tony.stark@marvel.com'},
            {'name': 'Captain America', 'email': 'steve.rogers@marvel.com'},
            {'name': 'Thor', 'email': 'thor.odinson@marvel.com'},
            {'name': 'Black Widow', 'email': 'natasha.romanoff@marvel.com'},
            {'name': 'Hulk', 'email': 'bruce.banner@marvel.com'},
            {'name': 'Spider-Man', 'email': 'peter.parker@marvel.com'},
            {'name': 'Black Panther', 'email': 'tchalla@marvel.com'},
            {'name': 'Doctor Strange', 'email': 'stephen.strange@marvel.com'},
        ]
        
        # Create DC superheroes
        dc_heroes = [
            {'name': 'Superman', 'email': 'clark.kent@dc.com'},
            {'name': 'Batman', 'email': 'bruce.wayne@dc.com'},
            {'name': 'Wonder Woman', 'email': 'diana.prince@dc.com'},
            {'name': 'The Flash', 'email': 'barry.allen@dc.com'},
            {'name': 'Aquaman', 'email': 'arthur.curry@dc.com'},
            {'name': 'Green Lantern', 'email': 'hal.jordan@dc.com'},
            {'name': 'Cyborg', 'email': 'victor.stone@dc.com'},
            {'name': 'Shazam', 'email': 'billy.batson@dc.com'},
        ]
        
        marvel_users = []
        for hero in marvel_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team_id=str(team_marvel._id),
                created_at=datetime.now()
            )
            marvel_users.append(user)
        
        dc_users = []
        for hero in dc_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team_id=str(team_dc._id),
                created_at=datetime.now()
            )
            dc_users.append(user)
        
        all_users = marvel_users + dc_users
        
        self.stdout.write('Creating activities...')
        
        # Activity types
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weight Training', 'Yoga', 'Boxing']
        
        # Create activities for all users
        for user in all_users:
            num_activities = random.randint(5, 15)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                distance = random.uniform(2.0, 15.0) if activity_type in ['Running', 'Cycling', 'Swimming'] else None
                calories = duration * random.randint(5, 12)
                
                Activity.objects.create(
                    user_id=str(user._id),
                    activity_type=activity_type,
                    duration=duration,
                    distance=distance,
                    calories=calories,
                    date=datetime.now() - timedelta(days=random.randint(0, 30)),
                    created_at=datetime.now()
                )
        
        self.stdout.write('Creating leaderboard...')
        
        # Calculate leaderboard data
        leaderboard_data = []
        for user in all_users:
            user_activities = Activity.objects.filter(user_id=str(user._id))
            total_calories = sum(activity.calories for activity in user_activities)
            total_activities = user_activities.count()
            
            leaderboard_data.append({
                'user': user,
                'total_calories': total_calories,
                'total_activities': total_activities
            })
        
        # Sort by total calories
        leaderboard_data.sort(key=lambda x: x['total_calories'], reverse=True)
        
        # Create leaderboard entries with ranks
        for rank, data in enumerate(leaderboard_data, start=1):
            Leaderboard.objects.create(
                user_id=str(data['user']._id),
                total_calories=data['total_calories'],
                total_activities=data['total_activities'],
                rank=rank,
                updated_at=datetime.now()
            )
        
        self.stdout.write('Creating workouts...')
        
        # Create superhero-themed workouts
        workouts = [
            {
                'name': 'Super Soldier Strength Training',
                'description': 'Build strength like Captain America with this intense workout',
                'difficulty_level': 'Advanced',
                'duration': 60,
                'exercise_type': 'Strength'
            },
            {
                'name': 'Stark Industries Cardio Blast',
                'description': 'High-intensity cardio session inspired by Iron Man',
                'difficulty_level': 'Intermediate',
                'duration': 45,
                'exercise_type': 'Cardio'
            },
            {
                'name': 'Asgardian Warrior Training',
                'description': 'Train like Thor with this comprehensive full-body workout',
                'difficulty_level': 'Advanced',
                'duration': 90,
                'exercise_type': 'Full Body'
            },
            {
                'name': 'Web-Slinger Agility Drills',
                'description': 'Improve agility and flexibility like Spider-Man',
                'difficulty_level': 'Beginner',
                'duration': 30,
                'exercise_type': 'Agility'
            },
            {
                'name': 'Bat Cave Core Crusher',
                'description': 'Batman-inspired core strengthening routine',
                'difficulty_level': 'Intermediate',
                'duration': 40,
                'exercise_type': 'Core'
            },
            {
                'name': 'Kryptonian Power Session',
                'description': 'Build superhuman power with this Superman-themed workout',
                'difficulty_level': 'Advanced',
                'duration': 75,
                'exercise_type': 'Power'
            },
            {
                'name': 'Amazonian Combat Training',
                'description': 'Warrior training inspired by Wonder Woman',
                'difficulty_level': 'Intermediate',
                'duration': 50,
                'exercise_type': 'Combat'
            },
            {
                'name': 'Speed Force Sprint Session',
                'description': 'Flash-inspired high-speed interval training',
                'difficulty_level': 'Advanced',
                'duration': 35,
                'exercise_type': 'Sprints'
            },
            {
                'name': 'Wakandan Mobility Flow',
                'description': 'Black Panther-inspired mobility and flexibility training',
                'difficulty_level': 'Beginner',
                'duration': 25,
                'exercise_type': 'Mobility'
            },
            {
                'name': 'Mystic Arts Meditation',
                'description': 'Doctor Strange-inspired mindfulness and meditation session',
                'difficulty_level': 'Beginner',
                'duration': 20,
                'exercise_type': 'Meditation'
            }
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data, created_at=datetime.now())
        
        # Create unique index on email field using PyMongo
        self.stdout.write('Creating unique index on email field...')
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.users.create_index([('email', 1)], unique=True)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with superhero test data!'))
        self.stdout.write(f'Created {len(all_users)} users')
        self.stdout.write(f'Created {Activity.objects.count()} activities')
        self.stdout.write(f'Created {Leaderboard.objects.count()} leaderboard entries')
        self.stdout.write(f'Created {Workout.objects.count()} workouts')
        self.stdout.write(f'Created 2 teams: Team Marvel and Team DC')
