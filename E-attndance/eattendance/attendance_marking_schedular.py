from database.models import *
import datetime
import time as t
import urllib.request as urlreq
import os
from darknet.openimages_face_extract import FaceDetector
from FaceRecog.FaceRecognitionClass import FaceRecognition
from django.shortcuts import get_object_or_404

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
            days = ['MON', 'TUES', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
            day = days[number_day]

            schedules_falling_in_current_time = Schedule.objects.filter(day=day, beginning_time__lte=time,
                                                                        ending_time__gte=time)

            for schedule in schedules_falling_in_current_time:
                self.event_processor.startProcessing(schedule=schedule, face_detector=self.face_detector)

            scheduler_end_time = t.time()
            time_elapsed = scheduler_end_time - scheduler_start_time


            if time_elapsed < time_between_event_cycles_in_seconds:  # 5 minutes converted into seconds, keeping 5 mnutes as the interval between two consecutive scans
                t.sleep(time_between_event_cycles_in_seconds - time_elapsed)  # whatever time left from 5 minutes, sleep for that time before the scheduler runs again to create events


class EventProcessor:
    temp_storage_root = None
    pickle_data_root = None
    def __init__(self):
        self.temp_storage_root = "temp/"
        self.pickle_data_root = "database_pickle_files/"

    def startProcessing(self, schedule, face_detector):
        department = schedule.department #Getting required data
        year = schedule.year
        division = schedule.division
        batch = schedule.batch


        lecture_class = schedule.lecture_class #Getting urls of the images (IpWebcam)
        cameras = Camera.objects.filter(lecture_class=lecture_class) #Camera object in db has picture links (IpWebcam) for each lecture-class
        image_urls = []
        for camera in cameras:
            image_urls.append(camera.url)

        os.system("rm -r -f "+self.temp_storage_root+"/captures/*") #Clearing all previous files in the captures folder
        os.system("rm -r -f "+self.temp_storage_root+"/faces/*") #Clearing all previous files in the faces folder



        counter = 0 # links to capturing images that are being stored at temp_storage_path ie temp/capture ie a folder
        for image_url in image_urls:
            urlreq.urlretrieve(image_url, self.temp_storage_root+"captures/capture_"+str(counter)+".jpg")
            counter = counter + 1

        #Face Detection Begins
        counter = 0 #counts number of images in directory, helps in making one folder per picture for storing faces
        directory_contents = os.listdir(self.temp_storage_root+"captures/")
        for directory_content in directory_contents:
            item_path = os.path.join(self.temp_storage_root+"captures/", directory_content)
            if(os.path.isfile(item_path)):
                counter = face_detector.detectFaces(sourceImagePath=item_path, destinationWritePath=self.temp_storage_root+"faces/", starting_index=counter)
            else:
                print("A non-file content found in: "+self.temp_storage_root+"captures/ . The non-file is named: "+ directory_content)
        #Face Detection Ends, Faces written at temp_storage_root/faces/


        #Determine which .pickle file to use for face recognition.
        root_path = self.pickle_data_root
        department_subpath = department.acronym().lower()
        year_subpath = year.acronym().lower()
        division_subpath = division.lower()

        if(batch=='FC'):
            batch_subpath=''
        else:
            batch_subpath = batch.lower()+"/"


        #Putting all together
        pickle_path = root_path+department_subpath+"/"+year_subpath+"/"+division_subpath+"/"+batch_subpath #this is the folder path in which the appropriate .pickle file will be found

        #Face Recognition
        identified_students = set()
        face_recognizer = FaceRecognition(absolute_database_path=pickle_path)

        #For each face stored in the folder by face_detector
        directory_contents = os.listdir(self.temp_storage_root + "faces/")
        for directory_content in directory_contents:
            item_path = os.path.join(self.temp_storage_root + "faces/", directory_content)
            if (os.path.isfile(item_path)):
                recognized, identity = face_recognizer.recognizeFace(image_path=item_path, threshold=0.6)
                if recognized:
                    identified_students.add(identity)
                else:
                    print("Student Unrecognized.")
            else:
                print(
                    "A non-file content found in: " + self.temp_storage_root + "faces/ . The non-file is named: " + directory_content)
        #all the identified students ID (primary key of Student) is now stored in identified_students set.

        #Add attendance for students who were detected as present
        for student_identity in identified_students:
            person = get_object_or_404(Person, id=student_identity)
            student = get_object_or_404(Student, person=person)
            present=True
            #schedule already provided in function call

            attendance = Attendance(schedule=schedule, student=student, present=True)
            attendance.save()
        #Marked all detected students as present

        #get remaining students and mark them as absent

        #whether or not to apply batch filter
        if batch=='FC':
            unidentified_students = Student.objects.filter(department=department, year=year, division=division, )
        else:
            unidentified_students = Student.objects.filter(department=department, year=year, division=division, batch=batch)
        #got the remaining students

        #now mark them absent
        for unidentified_student in unidentified_students:
            attendance = Attendance(schedule=schedule, student=student, present=False)
            attendance.save()

        #all students are marked as per the face recognition






