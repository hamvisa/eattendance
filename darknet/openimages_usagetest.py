from darknet import openimages_face_extract
face_detector = openimages_face_extract.FaceDetector()


def extractFaces(source_path, destination_path):
    try:
        counter = face_detector.detectFaces(sourceImagePath=source_path, destinationWritePath=destination_path)
        return True, counter
    except:
        return False, 0

path = input("Enter absolute path of the image")
#extractFaces("images/1.jpg", "output/")
extractFaces(path, "output/")
