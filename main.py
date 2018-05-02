#!/usr/bin/env python

from hue import Hue

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QApplication,
                             QBoxLayout, QLabel,
                             QSlider, QDialog)


WHITELIST = ['lampe', 'fernseher']


class HueSlider(QSlider):
    def __init__(self, orientation, lamp):
        super(QSlider, self).__init__(orientation)

        self.hue = Hue(username='lUwwJ1eMFb59iG5pANwAAw0VhTaG9UJxWvHMekTv')
        self.lamp = lamp

    def setHueValue(self, value):
        self.hue.set_light_state(self.lamp, state=(value != 0), bri=value)


class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__()
        self.hue = Hue(username='lUwwJ1eMFb59iG5pANwAAw0VhTaG9UJxWvHMekTv')

        self.slidersLayout = QBoxLayout(QBoxLayout.LeftToRight)

        for key, val in self.hue.get_lights().items():
            if val['name'] not in WHITELIST:
                continue

            label = QLabel(val['name'])

            slider = HueSlider(Qt.Vertical, key)
            slider.setFocusPolicy(Qt.StrongFocus)
            slider.setTickPosition(QSlider.TicksBothSides)
            slider.setTickInterval(255)
            slider.setMaximum(255)
            slider.setSingleStep(1)
            if val['state']['on'] is False:
                slider.setValue(0)
            else:
                slider.setValue(val['state']['bri'])
            slider.valueChanged.connect(slider.setHueValue)

            vLayout = QBoxLayout(QBoxLayout.TopToBottom)
            vLayout.addWidget(label)
            vLayout.addWidget(slider)
            self.slidersLayout.addLayout(vLayout)

        self.setLayout(self.slidersLayout)
        self.setWindowTitle("HUE")


if __name__ == '__main__':
    import sys
    import os
    abspath = os.path.dirname(os.path.abspath(__file__))
    libpath = os.path.join(abspath, 'venv/lib/python3.6/site-packages')
    sys.path.append(libpath)

    app = QApplication(sys.argv)
    window = Window()
    cursor = QCursor()
    pos = QCursor.pos()
    window.move(pos.x(), pos.y()-150)
    window.show()
    sys.exit(app.exec_())
