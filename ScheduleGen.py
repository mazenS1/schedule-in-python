import itertools
import tkinter as tk
from prettytable import PrettyTable 
from tkinter import ttk

class Schedule:
    def __init__(self, id, name, day1, start_time, end_time, day2=None, start_time2=None, end_time2=None, day3=None, start_time3=None, end_time3=None):
        self.id = id
        self.name = name
        self.day1 = day1
        self.start_time = start_time
        self.end_time = end_time
        self.day2 = day2
        self.start_time2 = start_time2
        self.end_time2 = end_time2
        self.day3 = day3
        self.start_time3 = start_time3
        self.end_time3 = end_time3

class ScheduleGenerator:
    def __init__(self, course_data):
        self.course_data = course_data

    def isValidSchedule(self, schedule):
        #check if there are any conflicts in the schedule by first checking if there are any courses that are scheduled at the same day, if yes then check if the times overlap, if yes then return false , if no then return true, make sure to handle the case where a course is scheduled on 3 days, but the other course is scheduled on 2 days since not all courses have the same number of days
        for course1, course2 in itertools.combinations(schedule, 2):
            if course1.day1 == course2.day1:
                if course1.start_time <= course2.end_time and course2.start_time <= course1.end_time:
                    return False
            if course1.day1 == course2.day2:
                if course1.start_time <= course2.end_time2 and course2.start_time2 <= course1.end_time:
                    return False
            if course1.day2 == course2.day1:
                if course1.start_time2 <= course2.end_time and course2.start_time <= course1.end_time2:
                    return False
            if course1.day2 == course2.day2:
                if course1.start_time2 <= course2.end_time2 and course2.start_time2 <= course1.end_time2:
                    return False
            if course1.day3 and course1.day3 == course2.day1:
                if course1.start_time3 <= course2.end_time and course2.start_time <= course1.end_time3:
                    return False
            if course1.day3 and course1.day3 == course2.day2:
                if course1.start_time3 <= course2.end_time2 and course2.start_time2 <= course1.end_time3:
                    return False
            if course1.day3 and course1.day3 == course2.day3:
                if course1.start_time3 <= course2.end_time3 and course2.start_time3 <= course1.end_time3:
                    return False
        return True 

    def generateSchedules(self):
        course_dict = self.groupCourses(self.course_data)
        courses = list(course_dict.values())
        schedules = list(itertools.product(*courses))
        valid_schedules = []
        for schedule in schedules:
            if self.isValidSchedule(schedule):
                valid_schedules.append(schedule)
        print(f"Generated {len(valid_schedules)} valid schedules.")
        return valid_schedules

    def printSchedule(self, schedule):
        table = PrettyTable()
        table.field_names = ["ID", "Course Name", "Day1", "Start Time", "End Time", "Days 2", "Start Time 2", "End Time 2", "Days 3", "Start Time 3", "End Time 3"]
        for course in schedule:
            row = [course.id, course.name, course.day1, course.start_time, course.end_time]
            if course.day2:
                row += [course.day2, course.start_time2, course.end_time2]
            else:
                row += ['', '', '']
            if course.day3:
                row += [course.day3, course.start_time3, course.end_time3]
            else:
                row += ['', '', '']
            table.add_row(row)
        print(table)

    def groupCourses(self, courseList):
        course_dict = {}
        for course in courseList:
            name = course.name
            if name not in course_dict:
                course_dict[name] = []
            course_dict[name].append(course)
        print(f"Successfully grouped {len(course_dict)} courses.")    
        return course_dict  

class ScheduleGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Schedule Generator")

        self.label = tk.Label(master, text="Enter course data:")
        self.label.pack()

        self.id_label = tk.Label(master, text="Course ID:")
        self.id_label.pack()
        self.id_entry = tk.Entry(master)
        self.id_entry.pack()

        self.name_label = tk.Label(master, text="Course Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(master)
        self.name_entry.pack()

        self.day1_label = tk.Label(master, text="Day 1:")
        self.day1_label.pack()
        self.day1_entry = tk.Entry(master)
        self.day1_entry.pack()

        self.start1_label = tk.Label(master, text="Start Time 1:")
        self.start1_label.pack()
        self.start1_entry = tk.Entry(master)
        self.start1_entry.pack()

        self.end1_label = tk.Label(master, text="End Time 1:")
        self.end1_label.pack()
        self.end1_entry = tk.Entry(master)
        self.end1_entry.pack()

        self.day2_label = tk.Label(master, text="Day 2:")
        self.day2_label.pack()
        self.day2_entry = tk.Entry(master)
        self.day2_entry.pack()

        self.start2_label = tk.Label(master, text="Start Time 2:")
        self.start2_label.pack()
        self.start2_entry = tk.Entry(master)
        self.start2_entry.pack()

        self.end2_label = tk.Label(master, text="End Time 2:")
        self.end2_label.pack()
        self.end2_entry = tk.Entry(master)
        self.end2_entry.pack()

        self.day3_label = tk.Label(master, text="Day 3 (optional):")
        self.day3_label.pack()
        self.day3_entry = tk.Entry(master)
        self.day3_entry.pack()

        self.start3_label = tk.Label(master, text="Start Time 3 (optional):")
        self.start3_label.pack()
        self.start3_entry = tk.Entry(master)
        self.start3_entry.pack()

        self.end3_label = tk.Label(master, text="End Time 3 (optional):")
        self.end3_label.pack()
        self.end3_entry = tk.Entry(master)
        self.end3_entry.pack()

        self.button = tk.Button(master, text="Add Course", command=self.add_course)
        self.button.pack()

        self.textbox = tk.Text(master, height=10, width=50)
        self.textbox.pack()

        self.generate_button = tk.Button(master, text="Generate Schedules", command=self.generate_schedules)
        self.generate_button.pack()

        self.course_list = []

    def add_course(self):
            course_id = self.id_entry.get()
            course_name = self.name_entry.get()
            day1 = self.day1_entry.get()
            start1 = self.start1_entry.get()
            end1 = self.end1_entry.get()
            day2 = self.day2_entry.get()
            start2 = self.start2_entry.get()
            end2 = self.end2_entry.get()
            day3 = self.day3_entry.get()
            start3 = self.start3_entry.get()
            end3 = self.end3_entry.get()

            # Validate input
            if not course_id.isdigit():
                self.textbox.insert(tk.END, "Error: Course ID must be a number.\n")
                return
            if not course_name:
                self.textbox.insert(tk.END, "Error: Course Name cannot be empty.\n")
                return
            if not day1.isalpha():
                self.textbox.insert(tk.END, "Error: Day 1 cannot be empty.\n")
                return
            if not start1.__contains__(":") or not start1.split(":")[0].isdigit or not start1.split(":")[1].isdigit or not end1.__contains__(":") or not end1.split(":")[0].isdigit() or not end1.split(":")[1].isdigit():
                self.textbox.insert(tk.END, "Error: Start Time and End Time for Day 1 must be numbers.\n")
                return
            if not day2.isalpha():
                self.textbox.insert(tk.END, "Error: Start Time and End Time for Day 2 must be numbers.\n")
                return
            if day2 and (not start2.__contains__(":") or not start2.split(":")[0].isdigit or not start2.split(":")[1].isdigit or not end2.__contains__(":") or not end2.split(":")[0].isdigit() or not end2.split(":")[1].isdigit()):
                self.textbox.insert(tk.END, "Error: Start Time and End Time for Day 2 must be numbers.\n")
                return 
            if day3 and not day3.isalpha():
                self.textbox.insert(tk.END, "Error: Day 3 must be a letter.\n")
                return
            if day3 and (not start3.__contains__(":") or not start3.split(":")[0].isdigit or not start3.split(":")[1].isdigit or not end3.__contains__(":") or not end3.split(":")[0].isdigit() or not end3.split(":")[1].isdigit()):
                self.textbox.insert(tk.END, "Error: Start Time and End Time for Day 3 must be numbers.\n")
                return
            # give a message if the course is added successfully
            self.textbox.delete(1.0, tk.END)
            self.textbox.insert(tk.END, "Course added successfully.\n")
            course = Schedule(int(course_id), course_name, day1, start1, end1, day2, start2, end2, day3, start3, end3)
            # show the course in the textbox in one line
            self.textbox.insert(tk.END, f"{course.id} {course.name} {course.day1} {course.start_time} {course.end_time} {course.day2} {course.start_time2} {course.end_time2} {course.day3} {course.start_time3} {course.end_time3}\n")
            # add the course to the list of courses
            self.course_list.append(course)
            # clear the entry boxes for new courses to be added
            self.id_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.day1_entry.delete(0, tk.END)
            self.start1_entry.delete(0, tk.END)
            self.end1_entry.delete(0, tk.END)
            self.day2_entry.delete(0, tk.END)
            self.start2_entry.delete(0, tk.END)
            self.end2_entry.delete(0, tk.END)
            self.day3_entry.delete(0, tk.END)
            self.start3_entry.delete(0, tk.END)
            self.end3_entry.delete(0, tk.END)
    # generate the schedules
    def generate_schedules(self):
        generator = ScheduleGenerator(self.course_list)
        schedules = generator.generateSchedules()
        for schedule in schedules:
            generator.printSchedule(schedule)
            
root = tk.Tk()
gui = ScheduleGeneratorGUI(root)
root.mainloop()