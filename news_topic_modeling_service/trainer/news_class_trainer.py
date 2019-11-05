from tensorflow.contrib import learn

import news_cnn_model
import numpy as np
import os
import pandas as pd
import pickle
import shutil
import tensorflow as tf

from sklearn import metrics


MODEL_OUTPUT_DIR = '../model'
DATA_FILE = '../data/labeled_news.csv'
VARS_FILE = '../model/vars'
VOCAB_PROCESSOR_FILE = '../model/vocab_processor_save_file'
MAX_DOC_LENGTH = 100
N_CLASSES = 17

STEPS = 200
REMOVE_PREVIOUS_MODEL = True

# tf.app.run function expects the main function to have a positional argument
def main(unused_argv):
    if REMOVE_PREVIOUS_MODEL:
        shutil.rmtree(MODEL_OUTPUT_DIR)
        os.mkdir(MODEL_OUTPUT_DIR)

    df = pd.read_csv(DATA_FILE, header=None)
    train_df = df[0:400]
    test_df = df.drop(train_df.index)

    x_train = train_df[1]
    y_train = train_df[0]
    x_test = test_df[1]
    y_test = test_df[0]

    vocab_processor = learn.preprocessing.VocabularyProcessor(MAX_DOC_LENGTH)
    x_train = np.array(list(vocab_processor.fit_transform(x_train))) # return indexes
    x_test = np.array(list(vocab_processor.transform(x_test))) # return word-id matrix

    n_words = len(vocab_processor.vocabulary_)
    print('Total words: %d' % n_words)

    with open(VARS_FILE, 'wb') as f:
        pickle.dump(n_words, f)
    vocab_processor.save(VOCAB_PROCESSOR_FILE)

    classifier = learn.Estimator(
        model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_OUTPUT_DIR
    )

    classifier.fit(x_train, y_train, steps=STEPS)

    y_predicted = [
        p['class'] for p in classifier.predict(x_test, as_iterable=True)
        # as_iterable: If True, return an iterable which keeps yielding predictions for each example until inputs are exhausted.
    ]

    score = metrics.accuracy_score(y_test, y_predicted)
    print('Accuracy: {0:f}'.format(score))

if __name__ == '__main__':
    tf.app.ran(main=main)