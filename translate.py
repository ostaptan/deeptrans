import argparse
import os
import dill

import torch
from torchtext.legacy import data

from options import translate_opts
from model import Seq2seqAttn


def load_field(path):
    with open(path, 'rb') as f:
        return dill.load(f)


def id2w(pred, field):
    sentence = [field.vocab.itos[i] for i in pred]
    if '<eos>' in sentence:
        return ' '.join(sentence[:sentence.index('<eos>')])
    return ' '.join(sentence)


def main(args):
    device = torch.device('cuda' if args.gpu  else 'cpu')

    load_vars = torch.load(args.model)
    train_args = load_vars['train_args']
    model_params = load_vars['state_dict']

    dirname = os.path.dirname(args.model)
    SRC = load_field(os.path.join(dirname, 'src.field'))
    TGT = load_field(os.path.join(dirname, 'tgt.field'))
    fields = [('src', SRC), ('tgt', TGT)]

    # with open(args.input, 'r') as f:
    #     examples = [data.Example.fromlist([line], [('src', SRC)]) for line in f]

    with open(args.input, 'r') as f:
        examples = []
        for line in f:
            inp = line.split('| |')[0]
            examples.append(data.Example.fromlist([inp], [('src', SRC)]))

    test_data = data.Dataset(examples, [('src', SRC)])
    test_iter = data.Iterator(test_data, batch_size=args.batch_size,
                    train=False, shuffle=False, sort=False, device=device)

    model = Seq2seqAttn(train_args, fields, device).to(device)
    model.load_state_dict(model_params)

    model.eval()
    for samples in test_iter:
        preds = model(samples.src, tgts=None, maxlen=args.maxlen, tf_ratio=0.0)
        preds = preds.max(2)[1].transpose(1, 0)
        outs = [id2w(pred, TGT) for pred in preds]
        outfile_path = './data/test_out2.csv'
        with open(outfile_path, 'a') as f:
            i = 0
            while i < len(outs):
                f.write(f'{outs[i]}\n')
                i += 1

        print(f'Translations written to file {outfile_path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    translate_opts(parser)
    args = parser.parse_args()
    main(args)


# '| sd3 | sdfsd |'
