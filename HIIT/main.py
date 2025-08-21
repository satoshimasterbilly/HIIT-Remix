import random
import datetime
import json
import os
from config import EXERCISE_DATABASE, WORKOUT_TEMPLATES, SETTINGS

class HIITScheduleManager:
    def __init__(self):
        self.exercises = EXERCISE_DATABASE
        self.workout_templates = WORKOUT_TEMPLATES
        self.data_dir = SETTINGS['data_directory']
        self.schedule_file = os.path.join(self.data_dir, 'hiit_schedule.json')
        self.progress_file = os.path.join(self.data_dir, 'hiit_progress.json')

        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)

    def generate_workout(self, level='intermediate', focus='mixed'):
        """Generate a HIIT workout based on level and focus area"""
        template = self.workout_templates[level]
        workout = {
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'level': level,
            'focus': focus,
            'work_time': template['work_time'],
            'rest_time': template['rest_time'],
            'rounds': template['rounds'],
            'exercises': []
        }

        # Select exercises based on focus
        if focus == 'cardio':
            exercise_pool = self.exercises['cardio'] * 2
        elif focus == 'strength':
            exercise_pool = self.exercises['strength'] * 2
        elif focus == 'core':
            exercise_pool = self.exercises['core'] * 2
        else:  # mixed
            exercise_pool = (self.exercises['cardio'] +
                           self.exercises['strength'] +
                           self.exercises['core'])

        # Generate exercises for each round
        for round_num in range(template['rounds']):
            round_exercises = random.sample(exercise_pool, template['exercises_per_round'])
            workout['exercises'].append({
                'round': round_num + 1,
                'exercises': round_exercises
            })
            # Remove selected exercises to avoid immediate repetition
            for ex in round_exercises:
                if ex in exercise_pool:
                    exercise_pool.remove(ex)

            # Replenish pool if getting low
            if len(exercise_pool) < template['exercises_per_round']:
                if focus == 'mixed':
                    exercise_pool.extend(self.exercises['cardio'] +
                                       self.exercises['strength'] +
                                       self.exercises['core'])
                else:
                    exercise_pool.extend(self.exercises[focus])

        return workout

    def create_weekly_schedule(self, level='intermediate'):
        """Create a weekly HIIT schedule with varied focus areas"""
        weekly_focus = ['cardio', 'strength', 'mixed', 'core', 'cardio', 'strength', 'mixed']
        schedule = {}

        today = datetime.datetime.now()

        for i in range(7):
            day = today + datetime.timedelta(days=i)
            day_name = day.strftime('%A')
            day_date = day.strftime('%Y-%m-%d')

            # Rest day on Sunday
            if day_name == 'Sunday':
                schedule[day_name] = {
                    'date': day_date,
                    'type': 'rest',
                    'activity': 'Rest Day - Light stretching or yoga recommended'
                }
            else:
                focus = weekly_focus[i]
                workout = self.generate_workout(level, focus)
                schedule[day_name] = workout

        return schedule

    def save_schedule(self, schedule):
        """Save the schedule to a JSON file"""
        with open(self.schedule_file, 'w') as f:
            json.dump(schedule, f, indent=2)
        print(f"✅ Schedule saved to {self.schedule_file}")

    def load_schedule(self):
        """Load schedule from JSON file"""
        if os.path.exists(self.schedule_file):
            with open(self.schedule_file, 'r') as f:
                return json.load(f)
        return None

    def log_workout_completion(self, day, completed=True, notes=""):
        """Log workout completion and progress"""
        progress_data = self.load_progress()

        entry = {
            'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            'day': day,
            'completed': completed,
            'notes': notes
        }

        progress_data.append(entry)

        with open(self.progress_file, 'w') as f:
            json.dump(progress_data, f, indent=2)

        print(f"✅ Workout logged for {day}!")

    def load_progress(self):
        """Load progress from JSON file"""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return []

    def display_workout(self, workout):
        """Display a formatted workout"""
        if workout.get('type') == 'rest':
            print(f"\n🛌 {workout['activity']}")
            return

        print(f"\n💪 HIIT Workout - {workout['level'].title()} Level")
        print(f"📅 Date: {workout['date']}")
        print(f"🎯 Focus: {workout['focus'].title()}")
        print(f"⏱️  Work: {workout['work_time']}s | Rest: {workout['rest_time']}s")
        print(f"🔄 Rounds: {workout['rounds']}")
        print("-" * 50)

        for round_data in workout['exercises']:
            print(f"\nRound {round_data['round']}:")
            for i, exercise in enumerate(round_data['exercises'], 1):
                print(f"  {i}. {exercise}")

        total_time = (workout['work_time'] + workout['rest_time']) * len(workout['exercises'][0]['exercises']) * workout['rounds']
        print(f"\n⏰ Estimated total time: {total_time // 60} minutes {total_time % 60} seconds")

    def display_schedule(self, schedule):
        """Display the weekly schedule"""
        print("\n📋 YOUR WEEKLY HIIT SCHEDULE")
        print("=" * 50)

        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        for day in days_order:
            if day in schedule:
                print(f"\n🗓️  {day.upper()}:")
                workout = schedule[day]

                if workout.get('type') == 'rest':
                    print(f"   🛌 {workout['activity']}")
                else:
                    print(f"   💪 {workout['level'].title()} {workout['focus'].title()} HIIT")
                    print(f"   ⏱️  {workout['work_time']}s work / {workout['rest_time']}s rest")
                    print(f"   🔄 {workout['rounds']} rounds")

    def get_today_workout(self, schedule):
        """Get today's workout from the schedule"""
        today = datetime.datetime.now().strftime('%A')
        return schedule.get(today)

    def show_progress_summary(self):
        """Show workout completion summary"""
        progress_data = self.load_progress()

        if not progress_data:
            print("No workout history found.")
            return

        completed_count = sum(1 for entry in progress_data if entry['completed'])
        total_logged = len(progress_data)
        completion_rate = (completed_count / total_logged) * 100 if total_logged > 0 else 0

        print(f"\n📊 PROGRESS SUMMARY")
        print("=" * 30)
        print(f"Total workouts logged: {total_logged}")
        print(f"Completed workouts: {completed_count}")
        print(f"Completion rate: {completion_rate:.1f}%")

        # Show recent workouts
        print(f"\nRecent workouts:")
        for entry in progress_data[-5:]:
            status = "✅" if entry['completed'] else "❌"
            print(f"  {status} {entry['day']} - {entry['date']}")

def print_welcome():
    """Print welcome message"""
    print("🔥" * 50)
    print("🏋️‍♀️  WELCOME TO YOUR HIIT TRAINING MANAGER  🏋️‍♂️")
    print("🔥" * 50)
    print("Ready to crush your fitness goals? Let's go!")
    print()

def main():
    hiit_manager = HIITScheduleManager()
    print_welcome()

    while True:
        print("\n🏋️‍♀️ HIIT TRAINING MANAGER")
        print("=" * 30)
        print("1. 📅 Create new weekly schedule")
        print("2. 👀 View current schedule")
        print("3. 🔥 Today's workout")
        print("4. 💪 Generate single workout")
        print("5. ✅ Log workout completion")
        print("6. 📊 View progress")
        print("7. ❌ Exit")

        choice = input("\nSelect an option (1-7): ").strip()

        if choice == '1':
            print("\nSelect difficulty level:")
            print("1. 🟢 Beginner (20s work/40s rest)")
            print("2. 🟡 Intermediate (30s work/30s rest)")
            print("3. 🔴 Advanced (45s work/15s rest)")

            level_choice = input("Choose level (1-3): ").strip()
            level_map = {'1': 'beginner', '2': 'intermediate', '3': 'advanced'}
            level = level_map.get(level_choice, 'intermediate')

            schedule = hiit_manager.create_weekly_schedule(level)
            hiit_manager.save_schedule(schedule)
            hiit_manager.display_schedule(schedule)

        elif choice == '2':
            schedule = hiit_manager.load_schedule()
            if schedule:
                hiit_manager.display_schedule(schedule)
            else:
                print("❌ No schedule found. Create a new schedule first.")

        elif choice == '3':
            schedule = hiit_manager.load_schedule()
            if schedule:
                today_workout = hiit_manager.get_today_workout(schedule)
                if today_workout:
                    print(f"\n🔥 TODAY'S WORKOUT:")
                    hiit_manager.display_workout(today_workout)
                else:
                    print("❌ No workout scheduled for today.")
            else:
                print("❌ No schedule found. Create a new schedule first.")

        elif choice == '4':
            print("\nSelect level:")
            print("1. 🟢 Beginner  2. 🟡 Intermediate  3. 🔴 Advanced")
            level_choice = input("Choose (1-3): ").strip()
            level_map = {'1': 'beginner', '2': 'intermediate', '3': 'advanced'}
            level = level_map.get(level_choice, 'intermediate')

            print("\nSelect focus:")
            print("1. 🎯 Mixed  2. ❤️ Cardio  3. 💪 Strength  4. 🎯 Core")
            focus_choice = input("Choose (1-4): ").strip()
            focus_map = {'1': 'mixed', '2': 'cardio', '3': 'strength', '4': 'core'}
            focus = focus_map.get(focus_choice, 'mixed')

            workout = hiit_manager.generate_workout(level, focus)
            hiit_manager.display_workout(workout)

        elif choice == '5':
            schedule = hiit_manager.load_schedule()
            if schedule:
                print("\nWhich day's workout did you complete?")
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
                for i, day in enumerate(days, 1):
                    print(f"{i}. {day}")

                day_choice = input("Choose day (1-6): ").strip()
                if day_choice in '123456':
                    day = days[int(day_choice) - 1]
                    completed = input("Did you complete the workout? (y/n): ").lower().startswith('y')
                    notes = input("Any notes (optional): ").strip()
                    hiit_manager.log_workout_completion(day, completed, notes)
                else:
                    print("❌ Invalid choice.")
            else:
                print("❌ No schedule found. Create a schedule first.")

        elif choice == '6':
            hiit_manager.show_progress_summary()

        elif choice == '7':
            print("\n🎉 Keep up the great work! See you next time! 💪")
            print("🔥" * 50)
            break

        else:
            print("❌ Invalid choice. Please select 1-7.")

if __name__ == "__main__":
    main()