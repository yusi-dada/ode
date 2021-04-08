# -*- coding: utf-8 -*-

import os, sys, time
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import csv
import copy

"""
データロガークラス

 [ method ]
 * append(key, val)
 * appendClass(cls, keys=None, ukeys=None)
 * log(keys=None, ukeys=None)
 * info()
 * merge(index=None, keys=None)
 * to_csv(folder, index=None, keys=None):

 [使用方法]
 * 親クラスから本クラスを継承して使用
 * 親クラスからlogメソッドで、親クラス内のインスタンス変数のログ取得(keys, ukeysでログを取得する変数を指定可)

"""
class logger(dict):
  def __init__(self):
    pass

  """
  append 追記
  * key : データラベル
  * val : データ本体(スカラ、リスト、np.array)
  """
  def append(self, key, val):
    val = np.atleast_2d(val)
    if key in self.keys():
      self[key] = np.r_[self[key], val]
    else:
      self[key] = val

  """
  appendClass 追記
  * cls  : クラスデータ
           インスタンス変数を保存
  * keys : 保存するラベルリスト
  * ukeys: 保存しないラベルリスト（keysの指定が優勢）
  """
  def appendClass(self, cls, keys=None, ukeys=None):
    keys_ = cls.__dict__.keys()
    vals_ = cls.__dict__.values()

    if keys is None:
      if ukeys is not None:
        ukeys = ukeys if isinstance(ukeys, list) else [ukeys]
        for key, val in zip(keys_, vals_):
          if not (key in ukeys):
            self.append(key,val)
      else:
        for key, val in zip(keys_, vals_):
          self.append(key,val)
    else:
      keys = keys if isinstance(keys, list) else [keys]
      for key, val in zip(keys_, vals_):    
        if key in keys:
          self.append(key,val)

  """
  log 継承先クラスのインスタンス変数を保存
      loggerクラス自信からの呼び出しは無効
  * keys : 保存するラベルリスト
  * ukeys: 保存しないラベルリスト（keysの指定が優勢）
  """
  def log(self, keys=None, ukeys=None):
    if self.__class__.__name__ != 'logger':
      self.appendClass(self, keys, ukeys)
    else:
      print("[log] method is invalid in this instance.")

  """
  info 登録データ一覧表示
  """
  def info(self):
    for key in self.keys():
      row , col = self[key].shape
      print("+ {0} : row={1}, col={2}".format(key, row, col))

  """
  disp ログデータを表示
  * idx  : 表示するログインデックス（0:一番最初にログしたデータ）
  * keys : ログデータの中で表示するデータ
  """
  def disp(self, idx=0, keys=None):
    if keys is None:
      keys = self.keys()
    else:
      keys = keys if isinstance(keys, list) else [keys]
    for key in keys:
      if (key in self.keys()):
        print(key,self[key][idx])
    
  """
  merge データ結合
  * index : データの行インデックスに使うデータ(None:インデックスなし)
  * keys  : 保存するデータラベル(None:全データ)
  """
  def merge(self, index=None, keys=None):
    if keys is None:
      keys = self.keys()
    else:
      keys = keys if isinstance(keys, list) else [keys]

    """ index から保存する初期データを作成 """
    merge_dat = None
    header = []    
    if index in self.keys():
      merge_dat = self[index]
      _, col = self[index].shape
      if col==1:
        header.append(index)
      else:
        for i in range(col):
          header.append(index+"_"+str(i))
    
    """ keys で指定したデータを順番に結合 """
    for key in keys:
      if (key in self.keys()) and (key != index) and (key is not None):
        if merge_dat is None:
          merge_dat = self[key]
        else:
          merge_dat = np.c_[merge_dat, self[key]]

        _, col = self[key].shape
        if col==1:
          header.append(key)
        else:
          for i in range(col):
            header.append(key+"_"+str(i))

    return header, merge_dat

  """
  get_time_str 日時を文字列で取得
  """
  def get_time_str(self):
    return datetime.now().strftime('%Y-%m-%d_%H_%M_%S')

  """
  to_csv ファイルへ保存
  * folder: 保存フォルダパス（デフォルト：現在ディレクトリ）
  * fname : 保存ファイル名
  * index : データの行インデックスに使うデータ(None:インデックスなし)
  * keys  : 保存するデータラベル(None:全データ)
  """
  def to_csv(self, folder=".", fname=None, index=None, keys=None):
    fname = self.get_time_str() if fname is None else fname
    header, save_dat = self.merge(index, keys)
    
    if save_dat is not None:
      fpath = folder + '/' + fname + ".csv"
      with open(fpath,'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for line in save_dat:
          writer.writerow(line)
      print("Save file: "+fpath)
