# -*- coding: utf-8 -*-

"""
ダウンサンプラー
  N : 指定回数Nの呼出しでTrueを出力
      (0の時、常にFalseを出力)
"""
class downSampler:
  def __init__(self, N=0):
    self.cnt0 = int(N)
    self.cnt = 0
  def __call__(self):
    if self.cnt0 == 0:
      return False

    self.cnt -= 1
    if self.cnt <= 0:
      self.cnt = self.cnt0
      return True
    else:
      return False