import darknet.python.darknet as dn  # available in the darknet/python folder
import cv2


class FaceDetector:
    def __init__(self):
        self.__net = dn.load_net(b"cfg/yolov3-openimages.cfg",
                                 b"yolov3-openimages.weights", 0)
        self.__meta = dn.load_meta(b"cfg/openimages.data")

    def detectFaces(self, sourceImagePath, destinationWritePath, startingIndex=0):  # takes image from source path, writes images of only faces to destination path. returns number of faces.
        '''
        :param sourceImagePath: absolute path
        :param destinationWritePath: absolute path
        :return: counter
        '''
        detected_classes = dn.detect(net=self.__net, meta=self.__meta, image=sourceImagePath.encode('utf-8'),
                                     thresh=0.1)
        image = cv2.imread(sourceImagePath)
        counter = startingIndex
        for (detected_class, confidence, (x, y, w, h)) in detected_classes:
            if detected_class != b'Human face':
                continue
            w_ = w / 2
            h_ = h / 2
            pt1 = (int(x - w_), int(y - h_))
            pt2 = (int(x + w_), int(y + h_))
            cv2.imwrite(destinationWritePath + str(counter) + '.jpg',
                        image[int(y - h_):int(y + h_), int(x - w_):int(x + w_)])  # startY:endY, startX:endX
            # cv2.rectangle(img=image, pt1=pt1, pt2=pt2, color=(255, 0, 255), thickness=3)
            counter = counter + 1
        return counter
        # cv2.imwrite(destinationWritePath + 'predictions.jpg', image)
