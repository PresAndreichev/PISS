from PIL import Image, ImageDraw, ImageFont

class WeeklySchedule:
    def __init__(self, timetable, subjects, overlaps_can_appear, hours, days):
        self.timetable = timetable  
        self.subjects = subjects  
        self.overlaps_can_appear = overlaps_can_appear
        self.hours = hours  
        self.days = days  

class ImageGenerator:
    @staticmethod
    def generateWeeklySchedule(schedule: WeeklySchedule, output_file="weekly_schedule.png"):
        # Set image dimensions
        img_width, img_height = 1000, 900
        margin_left, margin_top = 100, 50  # For labels
        img = Image.new('RGB', (img_width, img_height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Grid dimensions
        grid_width = img_width - margin_left
        grid_height = img_height - margin_top
        cell_width = grid_width // len(schedule.days)
        cell_height = grid_height // len(schedule.hours)
        
        # Draw days as column headers
        for i, day in enumerate(schedule.days):
            x = margin_left + i * cell_width
            draw.text((x + cell_width // 2 - 20, 10), day, fill='black')  # Adjust for centering
        
        # Draw hours as row headers
        for i, hour in enumerate(schedule.hours):
            y = margin_top + i * cell_height
            draw.text((10, y + cell_height // 2 - 10), hour, fill='black')  # Adjust for centering
        
        # Draw grid
        for day in range(len(schedule.days)):
            for hour in range(len(schedule.hours)):
                x0 = margin_left + day * cell_width
                y0 = margin_top + hour * cell_height
                x1 = x0 + cell_width
                y1 = y0 + cell_height
                draw.rectangle([x0, y0, x1, y1], outline='gray')
        
        for day, hours in enumerate(schedule.timetable):
            for hour, subject_index in enumerate(hours):
                if subject_index != -1:  # Assume -1 means no class
                    x0 = margin_left + day * cell_width
                    y0 = margin_top + hour * cell_height
                    x1 = x0 + cell_width
                    y1 = y0 + cell_height
                    draw.rectangle([x0, y0, x1, y1], fill='lightblue')
                    subject = schedule.subjects[subject_index]
                    draw.text((x0 + 5, y0 + 5), subject, fill='black')
        
        img.save(output_file)
        print(f"Weekly schedule saved as {output_file}")

# Example Usage
timetable = [
    [0, 1, -1, -1, -1, -1, -1],  # Monday
    [2, -1, 3, -1, -1, -1, -1],  # Tuesday
    [1, 0, -1, -1, -1, -1, -1],  # Wednesday
    [3, -1, 2, -1, -1, -1, -1],  # Thursday
    [0, 2, -1, 1, -1, -1, -1],  # Friday
    [1, 3, 0, -1, -1, -1, -1],  # Saturday
    [2, -1, -1, 3, -1, -1, -1],  # Sunday
]
subjects = ["Math", "Science", "History", "Art"]
overlaps_can_appear = False
hours = [f"{hour}:00" for hour in range(7, 23)]  # 07:00 to 22:00
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

schedule = WeeklySchedule(timetable, subjects, overlaps_can_appear, hours, days)
ImageGenerator.generateWeeklySchedule(schedule)
