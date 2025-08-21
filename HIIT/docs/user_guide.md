# 📖 HIIT Training Manager - User Guide

## Getting Started

1. **First Time Setup**
   - Run `python main.py`
   - Select option 1 to create your first weekly schedule
   - Choose your fitness level

2. **Daily Usage**
   - Run the program
   - Select option 3 to see today's workout
   - After completing, use option 5 to log your progress

## Menu Options Explained

### 1. Create New Weekly Schedule
- Generates a complete 7-day schedule
- Automatically varies workout focus
- Includes rest day on Sunday

### 2. View Current Schedule
- Shows your complete weekly plan
- Displays workout details for each day

### 3. Today's Workout
- Quick access to today's specific workout
- Shows detailed exercise list and timing

### 4. Generate Single Workout
- Create a custom workout for extra sessions
- Choose level and focus area

### 5. Log Workout Completion
- Track which workouts you've completed
- Add notes about your performance

### 6. View Progress
- See your completion statistics
- Review recent workout history

## Exercise Categories

### Cardio Focus
- High-energy exercises to boost heart rate
- Examples: Jumping Jacks, Burpees, High Knees

### Strength Focus
- Bodyweight exercises to build muscle
- Examples: Push-ups, Squats, Lunges

### Core Focus
- Exercises targeting abdominal muscles
- Examples: Crunches, Plank, Russian Twists

### Mixed Focus
- Combination of all exercise types
- Provides balanced full-body workout

## Data Files

Your data is stored in the `data/` folder:
- `hiit_schedule.json` - Your current weekly schedule
- `hiit_progress.json` - Your workout completion history

## Tips for Success

1. **Consistency is Key**: Aim to complete at least 4-5 workouts per week
2. **Progressive Overload**: Start with beginner level, advance when comfortable
3. **Proper Form**: Quality over quantity - focus on correct technique
4. **Recovery**: Don't skip rest days, they're crucial for improvement
5. **Hydration**: Keep water nearby during workouts
6. **Warm-up**: Do 2-3 minutes of light movement before starting

## Troubleshooting

**Program won't start?**
- Check Python installation: `python --version`
- Ensure you're in the HIIT folder

**Data not saving?**
- Check folder permissions
- Ensure data/ directory exists

**Want to reset progress?**
- Delete files in data/ folder
- Program will create fresh files on next run