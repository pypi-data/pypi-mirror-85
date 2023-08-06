from tensorflow.keras.callbacks import Callback
import numpy as np
from rs4.termcolor import tc, stty_size
from . import base

def confusion_matrix (labels, predictions, num_labels):
    rows = []
    for i in range (num_labels):
        row = np.bincount (predictions[labels == i], minlength=num_labels)
        rows.append (row)
    return np.vstack (rows)


class ConfusionMatrixCallback (base.Display, base.ValiadtionSet, Callback):
    def __init__(self, labels, validation_data, display_list = None):
        Callback.__init__(self)
        base.ValiadtionSet.__init__ (self, validation_data)
        if not isinstance (labels, (list, tuple)):
            labels = [labels]
        self.labels = labels
        self.display_list = display_list
        self.buffer = []

    def _get_confusion_matrix (self, logits, ys):
        if logits is None:
            logits = self.logits
        if ys is None:
            ys = self.ys
        mat_ = confusion_matrix (
            np.argmax (logits, 1),
            np.argmax (ys, 1),
            logits.shape [1]
        )
        return mat_.T

    def _confusion_matrix (self, label_index = 0, indent = 4, show_label = True):
        cur_label = self.labels [label_index]
        if isinstance (self.ys, dict):
            ys = self.ys [self.model.outputs [label_index].name.split (":") [0].split ("/") [0]]
            logits = self.logits [label_index]
        else:
            ys = self.ys
            logits = self.logits
        mat_ = self._get_confusion_matrix (logits, ys)
        mat = str (mat_) [1:-1]

        try:
            self.buffer.append ("confusion matrix{}\n".format (tc.info (cur_label.name and (" of " + cur_label.name) or "")))
        except IndexError:
            return

        labels = []
        if show_label:
            first_row_length = len (mat.split ("\n", 1) [0]) - 2
            label_width = (first_row_length - 1) // mat_.shape [-1]
            labels = [str (each) [:label_width].rjust (label_width) for each in cur_label.class_names ()]
            self.buffer.append (tc.fail ((" " * (indent + label_width + 1)) + " ".join (labels)))

        lines = []
        for idx, line in enumerate (mat.split ("\n")):
            if idx > 0:
                line = line [1:]
            line = line [1:-1]
            if labels:
                line = tc.info (labels [idx]) + " " + line
            if indent:
                line = (" " * indent) + line
            self.buffer.append (line)

    def on_epoch_begin(self, epoch, logs):
        self.buffer = []

    def on_epoch_end(self, epoch, logs):
        self.make_predictions ()
        for label_index, label in enumerate (self.labels):
            if self.display_list and label.name not in self.display_list:
                continue
            self._confusion_matrix (label_index)
        print ('\n  - ' + '\n'.join (self.buffer))
        self.draw_line ()

    def get_info (self):
        return self.buffer
