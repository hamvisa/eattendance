from EventProcessor import *
from database.models import *
import datetime
import time as t
from darknet.openimages_face_extract import FaceDetector

class EventGenerator:
    event_processor = None

    def __init__(self):
        self.event_processor = EventProcessor()
        self.face_detector = FaceDetector()

    def startGeneratingEvents(self, time_between_event_cycles_in_seconds):
        while True:
            print("Event gererator running")
            scheduler_start_time = t.time()

            my_datetime = datetime.datetime.now()
            date = my_datetime.date()
            time = my_datetime.time()
            number_day = my_datetime.weekday()
            # weekday(...)
            #     Return the day of the week represented by the date.
            #     Monday == 0 ... Sunday == 6
            days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
            day = days[number_day]
            print("DAY:"+str(day)+" TIME:"+str(time))
            schedules_falling_in_current_time = Schedule.objects.filter(day=day, beginning_time__lte=time,
                                                                        ending_time__gte=time)
            print(str(schedules_falling_in_current_time))
            for schedule in schedules_falling_in_current_time:
                self.event_processor.startProcessing(schedule=schedule, face_detector=self.face_detector)

            scheduler_end_time = t.time()
            time_elapsed = scheduler_end_time - scheduler_start_time


            if time_elapsed < time_between_event_cycles_in_seconds:  # 5 minutes converted into seconds, keeping 5 mnutes as the interval between two consecutive scans
                t.sleep(time_between_event_cycles_in_seconds - time_elapsed)  # whatever time left from 5 minutes, sleep for that time before the scheduler runs again to create events
