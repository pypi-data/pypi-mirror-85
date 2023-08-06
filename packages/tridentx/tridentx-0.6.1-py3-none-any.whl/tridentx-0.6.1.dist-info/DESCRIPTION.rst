Multiverse for Deep Learning Developers without Pitfall



Release Note
0.6.0

New Features:

#. new TextSequenceDataset and TextSequenceDataProvider for prepare dense/ sparse text tensor.
#. rnn/ lstm/ gru is supporting now ( in pytorch backend).
#. reinforcement learning is supporting now ( in pytorch backend).
#. normalization in sequence supporting (automatic permute)
#. bounding box inplace operation. (no need to split first 4 element)
#. New optimizer: RangerLars, and gradient centralization is now supporting.
#. New method 'trigger_when' in Model class , make add new callbacks or new event-listening much more easy.


Bug fix:
#. min, max, reduce_min, reduce_max bad arguments issue.




0.5.9
#. fix the Model argments ordinal bug.
#. fix the deprecated  addcdiv\_ functions


0.5.8
#. fix the deprecated divide ops and add\_ functions

0.5.7
#. Support AMP (automatic mixed precision) with pytorch 1.6.
#. attach lots of functions in ops on the tensor and use @numpy_compatible to share same syntax within numpy array or tensor.
#. New attribute 'sequence_rank' comes to all conv_blocks familay, if sequence_rank='cna' means the order is  'Convolution-Normalization-Activation'.
#. Adding EvoNorm, SIREN ..

