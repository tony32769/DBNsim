import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from DBNlogic.util import plotImage



class WeightsPlotter:
    """Plotter for the weights of a neural network layer."""

    def __init__(self, net, shape = None):
        self.net = net
        self.shape = shape
        if shape != None:
            self.width, self.heigth = shape
            if (self.width * self.heigth) != len(self.net.v):
                raise Exception('Problems with the image shape.')

    def weights(self):
        return self.net.W

    def plot(self, index = None):
        fields = self.net.W
        if self.shape != None:
            fields = self.net.W.reshape(len(self.net.h), self.width, self.heigth)
        if index != None:
            plt.imshow(fields[index])
        else:
            plt.imshow(fields)
        plt.show()



class ErrorPlotter:
    """Plotter for the error of a training session."""

    def __init__(self, trainer, dataset):
        self.trainer = trainer
        self.dataset = dataset
        self.gen = None

    def plot(self):
        # fig, ax = plt.subplots()
        # xdata, ydata = [], []
        # ln, = plt.plot([], [], 'ro', animated = True)

        # def start():
        #     ax.set_xlim(0, self.trainer.max_epochs)
        #     ax.set_ylim(0, 1)
        #     self.trainer.run(self.dataset)
        #     return ln,

        # def update(frame):
        #     xdata.append(frame)
        #     ydata.append(0.5)
        #     # ydata.append(self.trainer.mean_squared_err)
        #     ln.set_data(xdata, ydata)
        #     return ln,

        # ani = FuncAnimation(fig, update, frames = np.linspace(0, self.trainer.max_epochs, 128), init_func = start, blit = True)
        # plt.show()

        fig, ax = plt.subplots()
        xdata, ydata = [], []
        ln, = plt.plot([], [], 'ro', animated=True)

        def start():
            ax.set_xlim(0, self.trainer.max_epochs)
            ax.set_ylim(0, 1)
            self.gen = self.trainer.run(self.dataset)
            return ln,

        def update(frame):
            xdata.append(frame)
            ydata.append(next(self.gen))
            ln.set_data(xdata, ydata)
            return ln,

        ani = FuncAnimation(fig, update, frames=np.linspace(0, self.trainer.max_epochs, 128), init_func=start, blit=True)
        plt.show()