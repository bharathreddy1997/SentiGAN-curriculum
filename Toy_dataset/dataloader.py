import numpy as np


class Gen_Data_loader():
    def __init__(self, batch_size, sequence_length):
        self.batch_size = batch_size
        self.token_stream = []
        self.sequence_length = sequence_length

    def create_batches(self, data_file, seq_len):
        """make self.token_stream into a integer stream."""
        self.token_stream = []
        with open(data_file, 'r') as f:
            for line in f:
                line = line.strip()
                line = line.split()
                parse_line = [int(x) for x in line]
                #print(len(parse_line))
                if len(parse_line) == self.sequence_length:
                    self.token_stream.append(parse_line[:seq_len] + [0] * (self.sequence_length - seq_len))
        self.num_batch = int(len(self.token_stream) / self.batch_size)
        # cut the taken_stream's length exactly equal to num_batch * batch_size
        self.token_stream = self.token_stream[:self.num_batch * self.batch_size]
        #import pdb
        #pdb.set_trace()
        self.sequence_batch = np.split(np.array(self.token_stream), self.num_batch, 0)
        self.pointer = 0

    def next_batch(self):
        """take next batch by self.pointer"""
        ret = self.sequence_batch[self.pointer]
        self.pointer = (self.pointer + 1) % self.num_batch
        return ret

    def reset_pointer(self):
        self.pointer = 0


class Dis_Data_loader():
    def __init__(self, batch_size, sequence_length):
        self.batch_size = batch_size
        self.sentences = np.array([])
        self.labels = np.array([])
        self.sequence_length = sequence_length


    def load_train_data(self, positive_file, negative_file, seq_len):
        # Load data
        positive_examples = []
        negative_examples = []
        with open(positive_file)as fin:
            for line in fin:
                line = line.strip()
                line = line.split()
                parse_line = [int(x) for x in line]
                positive_examples.append(parse_line[:seq_len] + [0] * (self.sequence_length - seq_len))
        with open(negative_file)as fin:
            for line in fin:
                line = line.strip()
                line = line.split()
                parse_line = [int(x) for x in line]
                # ???: why parse_line == 20
                if len(parse_line) == self.sequence_length:
                    negative_examples.append(parse_line[:seq_len] + [0] * (self.sequence_length - seq_len))
        self.sentences = np.array(positive_examples + negative_examples)

        # Generate labels
        positive_labels = [[0, 1] for _ in positive_examples]
        negative_labels = [[1, 0] for _ in negative_examples]
        self.labels = np.concatenate([positive_labels, negative_labels], 0)

        # Shuffle the data
        shuffle_indices = np.random.permutation(np.arange(len(self.labels)))
        self.sentences = self.sentences[shuffle_indices]
        self.labels = self.labels[shuffle_indices]

        # Split batches
        self.num_batch = int(len(self.labels) / self.batch_size)
        self.sentences = self.sentences[:self.num_batch * self.batch_size]
        self.labels = self.labels[:self.num_batch * self.batch_size]
        self.sentences_batches = np.split(self.sentences, self.num_batch, 0)
        self.labels_batches = np.split(self.labels, self.num_batch, 0)

        self.pointer = 0


    def next_batch(self):
        """take next batch (sentence, label) by self.pointer"""
        ret = self.sentences_batches[self.pointer], self.labels_batches[self.pointer]
        self.pointer = (self.pointer + 1) % self.num_batch
        return ret

    def reset_pointer(self):
        self.pointer = 0
