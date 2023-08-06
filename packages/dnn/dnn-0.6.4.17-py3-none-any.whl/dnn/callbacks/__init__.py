import tensorflow as tf
from .confusion_matrix import ConfusionMatrixCallback
from .best_metrics import BestMetricsCallback
from .numpy_metric import NumpyMetricCallback
import math
import os
import shutil
from rs4 import pathtool

def monitor_options (monitor):
    if isinstance (monitor, (list, tuple)):
        monitor, mode = monitor
        if monitor == 'val_loss':
            assert mode == 'min', 'val_loss monitoring shoul be min'
    else:
        mode = 'min' if monitor == 'val_loss' else 'max'
    return monitor, mode


# decays ---------------------------------------
def step_decay (initial_lrate, decay_rate, per_epochs):
    def step_decay (epoch):
        lrate = initial_lrate * math.pow (decay_rate, math.floor((1+epoch)/per_epochs))
        return lrate
    return step_decay

def LREpochDecay (initial_lrate, decay_rate = 0.99, per_epochs = 1):
    return tf.keras.callbacks.LearningRateScheduler (step_decay (initial_lrate, decay_rate, per_epochs))

def LRPlateauDecay (decay_rate=0.5, patience=5, monitor='val_loss', min_lr=1e-8):
    return tf.keras.callbacks.ReduceLROnPlateau (monitor = monitor, factor=decay_rate, patience=patience, min_lr=1e-8)


# compsing -------------------------------------
def compose (
        train_dir,
        datasets,
        monitor = None, # monitor or (monitor, mode)
        custom_metric = None, # function
        decay_rate = None, # decay_rate, (decay_rate, decay_patience)
        early_stop = None, # patience or (patience, monitor, mode)
        enable_logging = True, # enable tensor board logging
        reset_train_dir = False
):
    reset_train_dir and os.path.isdir (train_dir) and shutil.rmtree (train_dir)

    CHECKPOINT_FORMAT = os.path.join (train_dir, 'checkpoint', '{epoch:04d}.ckpt')
    ASSETS_DIR = os.path.join (train_dir, 'assets')
    LOG_DIR = os.path.join (train_dir, 'log')
    pathtool.mkdir (ASSETS_DIR)

    datasets.save (ASSETS_DIR)
    composed_callbacks, intels = [], []

    if custom_metric:
        custom_metric = NumpyMetricCallback (custom_metric, datasets.validset)
        composed_callbacks.append (custom_metric)
        intels.append (custom_metric)

    if datasets.labels:
        confusion_matrix = ConfusionMatrixCallback (datasets.labels, datasets.validset)
        composed_callbacks.append (confusion_matrix)
        intels.append (confusion_matrix)

    if monitor:
        monitor, mode = monitor_options (monitor)
        composed_callbacks.append (BestMetricsCallback (monitor = monitor, mode = mode, intels = intels, log_path = ASSETS_DIR))
        composed_callbacks.append (tf.keras.callbacks.ModelCheckpoint (
            filepath = CHECKPOINT_FORMAT, save_weights_only = True,
            monitor = monitor, mode = mode, save_best_only = True
        ))

    if decay_rate:
        decay_patience = 0
        if not isinstance (decay_rate, tuple):
            raise TypeError ("decay_rate format is (initial lr, decay_rate, [devat_patience])")
        try:
            learning_rate, decay_rate, decay_patience = decay_rate
        except ValueError:
            learning_rate, decay_rate = decay_rate
        if decay_patience:
            composed_callbacks.append (LRPlateauDecay (decay_rate = decay_rate, patience = decay_patience))
        elif decay_rate:
            composed_callbacks.append (LREpochDecay (learning_rate, decay_rate))

    if enable_logging:
        if os.path.isdir (LOG_DIR):
            shutil.rmtree (LOG_DIR)
            pathtool.mkdir (LOG_DIR)
        composed_callbacks.append (tf.keras.callbacks.TensorBoard (log_dir = LOG_DIR))

    if early_stop:
        early_stop, monitor_, mode_ = early_stop, 'val_loss', "min"
        if isinstance (early_stop, tuple):
            if len (early_stop) == 3:
                patience, *mo = early_stop
            elif len (early_stop) == 2:
                patience, mo = early_stop
            else:
                raise ValueError ('unknown early_stop format')
            monitor_, mode_ = monitor_options (mo)
        else:
            patience = early_stop
        composed_callbacks.append (tf.keras.callbacks.EarlyStopping (monitor = monitor_, mode = mode_, patience = patience, verbose = True, restore_best_weights = True))
    return composed_callbacks
