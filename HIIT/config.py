# Configuration file for HIIT Training Manager

EXERCISE_DATABASE = {
    'cardio': [
        'Jumping Jacks', 'High Knees', 'Burpees', 'Mountain Climbers',
        'Jump Rope', 'Running in Place', 'Squat Jumps', 'Star Jumps',
        'Butt Kickers', 'Lateral Jumps', 'Speed Skaters', 'Tuck Jumps'
    ],
    'strength': [
        'Push-ups', 'Squats', 'Lunges', 'Plank', 'Tricep Dips',
        'Glute Bridges', 'Wall Sit', 'Pike Push-ups', 'Single Leg Glute Bridges',
        'Chair Step-ups', 'Incline Push-ups', 'Calf Raises', 'Bear Crawl'
    ],
    'core': [
        'Crunches', 'Russian Twists', 'Bicycle Crunches', 'Leg Raises',
        'Dead Bug', 'Bird Dog', 'Side Plank', 'Hollow Body Hold',
        'Mountain Climber Twists', 'Flutter Kicks', 'Scissor Kicks', 'V-ups'
    ]
}

WORKOUT_TEMPLATES = {
    'beginner': {
        'work_time': 20,
        'rest_time': 40,
        'rounds': 4,
        'exercises_per_round': 4
    },
    'intermediate': {
        'work_time': 30,
        'rest_time': 30,
        'rounds': 5,
        'exercises_per_round': 5
    },
    'advanced': {
        'work_time': 45,
        'rest_time': 15,
        'rounds': 6,
        'exercises_per_round': 6
    }
}

SETTINGS = {
    'data_directory': 'data',
    'default_level': 'intermediate',
    'auto_save': True,
    'rest_day': 'Sunday'
}