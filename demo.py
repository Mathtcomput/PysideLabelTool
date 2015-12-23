# ****************************************************************
# Copyright: Guangyu Zhong all rights reserved
# Author: Guangyu Zhong
# Date: 12/23/2015
# Description:
# - A Label tool.
# - This tool is for a private project.
# - If you want to reference the codes please contact me first.
# - Any problem, feel free to contact guangyuzhonghikari@gmail.com
# ****************************************************************
import sys
from PySide.QtGui import *
from PySide.QtCore import *

import LabelTool
import os
import copy

class Label(QMainWindow, LabelTool.Ui_MainWindow):
    def __init__(self):
        super(Label, self).__init__()
        self.cropQPixmap = [0]
        self.cur_img_path = ''
        self.label_img_size = [0, 0]
        self.gt_img_size = [0, 0]
        self.load_path = ''
        self.save_path = ''
        self.obj_num = 0
        self.sig_draw = 0
        self.stop = 0
        self.polygon = []
        self.allpolygon = []
        self.breakstate = -1
        self.turnstate = -1
        self.setupUi(self)
        self.connect(self.pushButton, SIGNAL("clicked()"), self.path_define)
        self.connect(self.select, SIGNAL("clicked()"), self.load_img_current)
        self.connect(self.pushButton_viewLeft, SIGNAL("clicked()"), self.load_img_left)
        self.connect(self.pushButton_viewRight, SIGNAL("clicked()"), self.load_img_right)
        self.connect(self.pushButton_2, SIGNAL("clicked()"), self.poly_save)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.radioButton_BreakOn.toggled.connect(self.breakon)
        self.radioButton_BreakOff.toggled.connect(self.breakoff)
        self.radioButton_TurnOff.toggled.connect(self.turnoff)
        self.radioButton_TurnLeft.toggled.connect(self.turnleft)
        self.radioButton_TurnRight.toggled.connect(self.turnright)

    def breakon(self):
        self.breakstate = 1

    def breakoff(self):
        self.breakstate = 0

    def turnoff(self):
        self.turnstate = 0

    def turnleft(self):
        self.turnstate = 1

    def turnright(self):
        self.turnstate = 2

    def detectOverlap(self, point, rect):
        flag = 0
        if (rect[0] <= point.x() <= (rect[0] + rect[2]) ):
            if (rect[1] <= point.y() <= (rect[1] + rect[3]) ):
                flag = 1
        return flag

    def path_define(self):
        self.listWidget.clear()
        paths = self.lineEdit.text()
        if os.path.isdir(paths):
            pass
        else:
            paths = '../toyota_test/'
        self.browse_folder(paths)
        self.load_path = paths
        self.save_path = self.load_path + 'save/'
        if os.path.exists(self.save_path):
            pass
        else:
            print('make save path')
            os.mkdir(self.save_path)

    def browse_folder(self, paths):
        directory = [i for i in os.listdir(paths) if i[-4:] in ('.png', '.jpg', '.bmp')]
        if directory:
            for file_name in directory:
                self.listWidget.addItem(paths + file_name)

    def load_img_current(self):
        img_name = self.listWidget.currentItem()
        self.load_img(img_name)

    def load_img_left(self):
        itenum = (self.listWidget.row(self.listWidget.currentItem()) - 1) % self.listWidget.count()
        self.listWidget.setCurrentItem(self.listWidget.item(itenum))
        img_name = self.listWidget.currentItem()
        self.load_img(img_name)

    def load_img_right(self):
            itenum = (self.listWidget.row(self.listWidget.currentItem()) + 1) % self.listWidget.count()
            self.listWidget.setCurrentItem(self.listWidget.item(itenum))
            img_name = self.listWidget.currentItem()
            self.load_img(img_name)

    def load_img(self, img_name):
        self.label_3.resize(380, 380)
        img_name_text = img_name.text()
        pixmap = QPixmap(img_name_text)
        self.gt_img_size = [pixmap.width(), pixmap.height()]
        size = min(self.label_3.width(), self.label_3.height())
        pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatio)
        self.label_img_size = [pixmap.width(), pixmap.height()]
        print('label_img_size:', self.label_img_size)
        self.label_3.setPixmap(pixmap)
        self.label_3.adjustSize()
        self.label_title.setText(img_name_text)
        self.cur_img_path = img_name_text
        self.obj_num = 0
        print('load image')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Z:
            self.allpolygon.append(self.polygon)
            self.polygon = []
            print('save polygon')
            print(self.allpolygon)
        if event.key() == Qt.Key_X:
            self.polygon = []
            self.allpolygon.pop()
            self.copy_crop = copy.copy(self.cropQImage)
            cur = QPoint()
            color = qRgb(0, 0, 255)
            if len(self.allpolygon) >= 1:
                for ipoly in self.allpolygon:
                    for j in range(0, len(ipoly) - 1):
                        point1 = ipoly[j]
                        point2 = ipoly[j+1]
                        if point1.x() == point2.x():
                            for i in range(point1.y(), point2.y(), self.gene_step(point1.y(), point2.y())):
                                cur.x = point1.x() - self.label_4.pos().x()
                                cur.y = i - self.label_4.pos().y()
                                self.copy_crop.setPixel(cur.x, cur.y, color)
                        elif abs(point1.x() - point2.x()) > abs(point1.y() - point2.y()):
                            k = float(point2.y() - point1.y())/float(point2.x() - point1.x())
                            for i in range(point1.x(), point2.x(), self.gene_step(point1.x(), point2.x())):
                                cur.x = i - self.label_4.pos().x()
                                cur.y = point2.y() - int(k*(point2.x() - i)) - self.label_4.pos().y()
                                self.copy_crop.setPixel(cur.x, cur.y, color)
                        else:
                            k = float(point2.y() - point1.y())/float(point2.x() - point1.x())
                            for i in range(point1.y(), point2.y(), self.gene_step(point1.y(), point2.y())):
                                cur.y = i - self.label_4.pos().y()
                                cur.x = point2.x() - int(float(point2.y() - i)/k) - self.label_4.pos().x()
                                self.copy_crop.setPixel(cur.x, cur.y, color)

            tmp_crop_polyline = QPixmap()
            tmp_crop_polyline.convertFromImage(self.copy_crop)
            self.label_4.setPixmap(tmp_crop_polyline)
            print('delete polygon')
            # print(self.polygon)


    def mousePressEvent(self, event):
        gt_loc = [self.label_3.pos().x(), self.label_3.pos().y(), self.label_3.width(), self.label_3.height()]
        crop_loc = [self.label_4.pos().x(), self.label_4.pos().y(), self.label_4.width(), self.label_4.height()]
        if (event.button() == Qt.LeftButton) and (self.detectOverlap(event.pos(), gt_loc)):
           self.origin = QPoint(event.pos())
           self.rubberBand.setGeometry(QRect(self.origin, QSize()))
           self.rubberBand.show()
        elif (event.button() == Qt.LeftButton) and (self.detectOverlap(event.pos(), crop_loc)):
            self.polygon.append(QPoint(event.pos().x(), event.pos().y()))
            if len(self.polygon) >= 2:
                print('draw_poly')
                self.draw_poly()
                temp1 = self.polygon[len(self.polygon) - 1]
                temp2 = self.polygon[0]
                print(self.distance(temp1, temp2))

        else:
            event.ignore()
            print(0)

    def mouseMoveEvent(self, event):
        gt_loc = [self.label_3.pos().x(), self.label_3.pos().y(), self.label_3.width(), self.label_3.height()]
        if not self.origin.isNull() and (self.detectOverlap(event.pos(), gt_loc)):
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        gt_loc = [self.label_3.pos().x(), self.label_3.pos().y(), self.label_3.width(), self.label_3.height()]
        crop_loc = [self.label_4.pos().x(), self.label_4.pos().y(), self.label_4.width(), self.label_4.height()]
        if (event.button() == Qt.LeftButton) and (self.detectOverlap(event.pos(), gt_loc)):
            self.rubberBand.hide()
            self.crop_img()
        else:
            event.ignore()

    def distance(self, point1, point2):
        dist = float((point1.x() - point2.x())**2 + (point1.y() - point2.y())**2)**0.5
        return dist

    def draw_poly(self):
        point1 = self.polygon[len(self.polygon) - 1]
        point2 = self.polygon[len(self.polygon) - 2]
        print('point1: ', point1.x(), point1.y())
        print('point2: ', point2.x(), point2.y())
        cur = QPoint()
        color = qRgb(0, 0, 255)
        if point1.x() == point2.x():
                for i in range(point1.y(), point2.y(), self.gene_step(point1.y(), point2.y())):
                    cur.x = point1.x() - self.label_4.pos().x()
                    cur.y = i - self.label_4.pos().y()
                    self.copy_crop.setPixel(cur.x, cur.y, color)
        elif abs(point1.x() - point2.x()) > abs(point1.y() - point2.y()):
            k = float(point2.y() - point1.y())/float(point2.x() - point1.x())
            for i in range(point1.x(), point2.x(), self.gene_step(point1.x(), point2.x())):
                cur.x = i - self.label_4.pos().x()
                cur.y = point2.y() - int(k*(point2.x() - i)) - self.label_4.pos().y()
                self.copy_crop.setPixel(cur.x, cur.y, color)
        else:
            k = float(point2.y() - point1.y())/float(point2.x() - point1.x())
            for i in range(point1.y(), point2.y(), self.gene_step(point1.y(), point2.y())):
                cur.y = i - self.label_4.pos().y()
                cur.x = point2.x() - int(float(point2.y() - i)/k) - self.label_4.pos().x()
                self.copy_crop.setPixel(cur.x, cur.y, color)

        tmp_crop_polyline = QPixmap()
        tmp_crop_polyline.convertFromImage(self.copy_crop)
        self.label_4.setPixmap(tmp_crop_polyline)

    def gene_step(self, a, b):
        if a <= b:
            return 1
        else:
            return -1

    def crop_img(self):
        self.label_4.resize(380, 380)
        self.polygon = []
        rect_x = self.rubberBand.pos().x() - self.label_3.pos().x()
        rect_y = self.rubberBand.pos().y() - self.label_3.pos().y()
        rect_width = self.rubberBand.width()
        rect_height = self.rubberBand.height()
        # cropQPixmap = self.label_3.pixmap().copy(rect_x, rect_y, rect_width, rect_height)
        gt_img = QPixmap(self.cur_img_path)
        gt_img_Qim = QImage(self.cur_img_path)
        ratio = float(self.gt_img_size[0])/float(self.label_img_size[0])
        print('ratio :', ratio)
        cropQPixmap = gt_img.copy(int(rect_x*ratio), int(rect_y*ratio), int(rect_width*ratio), int(rect_height*ratio))
        cropQImage = gt_img_Qim.copy(int(rect_x*ratio), int(rect_y*ratio), int(rect_width*ratio), int(rect_height*ratio))
        size = min(self.label_4.width(), self.label_4.height())
        cropQPixmap = cropQPixmap.scaled(size, size, Qt.KeepAspectRatio)
        cropQImage = cropQImage.scaled(size, size, Qt.KeepAspectRatio)
        self.label_4.setPixmap(cropQPixmap)
        self.label_4.adjustSize()
        self.cropQPixmap = copy.copy(cropQPixmap)
        self.cropQImage = copy.copy(cropQImage)
        self.copy_crop = copy.copy(cropQImage)

    def poly_save(self):
        self.obj_num += 1
        save_name = str(self.cur_img_path)[len(self.load_path):len(self.cur_img_path) - 4] + '_' + str(self.obj_num) + '.png'
        print(self.save_path + save_name)
        self.cropQPixmap.save(self.save_path + save_name)
        save_txt_name = str(self.cur_img_path)[len(self.load_path):len(self.cur_img_path) - 4] + '_' + str(self.obj_num) + '.txt'
        file_object = open(self.save_path + save_txt_name, 'w')
        file_object.write(str(self.tidy_polygon()))
        file_object.write('\n')
        file_object.write('Break Light: ')
        file_object.write(str(self.breakstate))
        file_object.write('\n')
        file_object.write('Turn Light: ')
        file_object.write(str(self.turnstate))
        file_object.close()
        print(self.allpolygon)

    def tidy_polygon(self):
        tmp_all = []
        for i in self.allpolygon:
            tmp = []
            for j in i:
                x = j.x() - self.label_4.pos().x()
                y = j.y() - self.label_4.pos().y()
                tmp.append([x, y])
            tmp_all.append(tmp)
        print (tmp_all)
        return tmp_all

def main():
    app = QApplication(sys.argv)
    form = Label()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()