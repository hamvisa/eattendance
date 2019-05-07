import darknet.openimages_face_extract as ofe
face_detector = ofe.FaceDetector()


def extractFaces(source_path, destination_path):
    try:
        counter = face_detector.detectFaces(sourceImagePath=source_path, destinationWritePath=destination_path)
        return True, counter
    except:
        return False, 0

extractFaces("images/sample.jpg", "output/")
