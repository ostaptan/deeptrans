# -*- coding: utf-8 -*-
from xml.etree import ElementTree
import csv
import random

def main():
  file = 'data/slowar.xml'

  tree = ElementTree.parse(file)
  root = tree.getroot()
  data = []

  for collection in root.iter('PhrasesToSerialize'):
    for keyval in collection.iter('KeyValueObject'):
      data.append([keyval.find('Key').text, keyval.find('Value').text])

  random.shuffle(data)
  ind = int(len(data) * .85)
  trainList = data[0:ind]
  validList = data[ind:]

  print(f'all data len: {len(data)}')
  print(f'train data len: {len(trainList)}')
  print(f'valid data len: {len(validList)}')

  with open('data/train.tsv', 'wt') as tr_file:
    tsv_writer = csv.writer(tr_file, delimiter='\t')
    tsv_writer.writerows(trainList)

  with open('data/valid.tsv', 'wt') as tr_file:
    tsv_writer = csv.writer(tr_file, delimiter='\t')
    tsv_writer.writerows(validList)

if __name__ == '__main__':
  main()
