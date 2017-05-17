import numpy as np

from DBNlogic.plot import WeightsPlotter
from DBNlogic.util import Configuration
from DBNlogic.util import sigmoid, activation, squared_error



class CDTrainer:
    """Contrastive Divergence trainer for RBMs."""

    def __init__(self, net, config = Configuration()):
        """Constructor for a RBM."""
        self.net = net               # the learner
        self.mean_squared_err = None # current training error
        self.epoch = 0               # current training epoch
        self.config = config         # hyper-parameters for training    

    def run(self, trainset):
        """Learn from a particular dataset."""
        net        = self.net
        max_epochs = self.config.max_epochs
        threshold  = self.config.threshold
        batch_sz   = self.config.batch_size
        learn_rate = self.config.learn_rate
        momentum   = self.config.momentum
        w_decay    = self.config.w_decay

        W_update = np.zeros(net.W.shape)
        a_update = np.zeros(net.a.shape)
        b_update = np.zeros(net.b.shape)
        pos_hid_probs = None

        self.mean_squared_err = threshold + 1 # (for entering the while loop)
        while (self.mean_squared_err > threshold) and (self.epoch < max_epochs):
            self.epoch += 1
            errors = np.array([])
            for batch_n in range(int(len(trainset) / batch_sz)):
                start = batch_sz * batch_n
                examples = np.array(trainset[start : start + batch_sz]).T
                data = examples

                # positive phase:
                hid_probs   = sigmoid(np.dot(net.W, data) + net.b.repeat(batch_sz, axis = 1))
                hid_states  = activation(hid_probs)
                pos_corr    = np.dot(hid_probs, data.T) / batch_sz # vis-hid correlations (+)
                pos_vis_act = data.sum(axis = 1, keepdims = True) / batch_sz
                pos_hid_act = hid_probs.sum(axis = 1, keepdims = True) / batch_sz

                pos_hid_probs = hid_probs

                # negative phase:
                vis_probs   = sigmoid(np.dot(net.W.T, hid_states) + net.a.repeat(batch_sz, axis = 1))
                data        = activation(vis_probs)
                hid_probs   = sigmoid(np.dot(net.W, data) + net.b.repeat(batch_sz, axis = 1))
                neg_corr    = np.dot(hid_probs, data.T) / batch_sz # vis-hid correlations (-)
                neg_vis_act = data.sum(axis = 1, keepdims = True)  / batch_sz
                neg_hid_act = hid_probs.sum(axis = 1, keepdims = True)  / batch_sz

                # updates:
                W_update = momentum * W_update + learn_rate * ((pos_corr - neg_corr) - w_decay * net.W)
                a_update = momentum * a_update + learn_rate * (pos_vis_act - neg_vis_act)
                b_update = momentum * b_update + learn_rate * (pos_hid_act - neg_hid_act)
                net.W += W_update
                net.a += a_update
                net.b += b_update
                errors = np.append(errors, squared_error(examples, data))

            # error update:
            self.mean_squared_err = errors.mean()

            yield pos_hid_probs