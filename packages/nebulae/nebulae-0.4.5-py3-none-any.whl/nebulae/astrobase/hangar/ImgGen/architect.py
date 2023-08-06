#!/usr/bin/env python
'''
architect
Created by Seria at 2020/11/18 1:42 PM
Email: zzqsummerai@yeah.net

                    _ooOoo_
                  o888888888o
                 o88`_ . _`88o
                 (|  0   0  |)
                 O \   。   / O
              _____/`-----‘\_____
            .’   \||  _ _  ||/   `.
            |  _ |||   |   ||| _  |
            |  |  \\       //  |  |
            |  |    \-----/    |  |
             \ .\ ___/- -\___ /. /
         ,--- /   ___\<|>/___   \ ---,
         | |:    \    \ /    /    :| |
         `\--\_    -. ___ .-    _/--/‘
   ===========  \__  NOBUG  __/  ===========
   
'''
# -*- coding:utf-8 -*-
from ... import dock

from math import ceil



class MLPG(dock.Craft):
    def __init__(self, in_shape, latent_dim, scope='MLPG'):
        super(MLPG, self).__init__(scope)
        H, W, C = in_shape
        self.H = H
        self.W = W
        self.C = C

        self.lrelu = dock.LRelu()
        self.fc_1 = dock.Dense(latent_dim, latent_dim)
        self.fc_2 = dock.Dense(latent_dim, latent_dim * 2)
        self.bn_2 = dock.BN(latent_dim * 2, dim=1, mmnt=0.2)
        self.fc_3 = dock.Dense(latent_dim * 2, latent_dim * 4)
        self.bn_3 = dock.BN(latent_dim * 4, dim=1, mmnt=0.2)
        self.fc_4 = dock.Dense(latent_dim * 4, latent_dim * 8)
        self.bn_4 = dock.BN(latent_dim * 8, dim=1, mmnt=0.2)

        self.fc_pixel = dock.Dense(latent_dim * 8, H * W * C)
        self.tanh = dock.Tanh()
        self.rect = dock.Reshape()

    def run(self, z):
        self['latent_code'] = z
        z = self.fc_1(self['latent_code'])
        z = self.lrelu(z)

        z = self.fc_2(z)
        z = self.bn_2(z)
        z = self.lrelu(z)

        z = self.fc_3(z)
        z = self.bn_3(z)
        z = self.lrelu(z)

        z = self.fc_4(z)
        z = self.bn_4(z)
        z = self.lrelu(z)

        z = self.fc_pixel(z)
        z = self.tanh(z)
        self['fake'] = self.rect(z, (-1, self.C, self.H, self.W))

        return self['fake']


class MLPD(dock.Craft):
    def __init__(self, in_shape, latent_dim, scope='MLPD'):
        super(MLPD, self).__init__(scope)
        H, W, C = in_shape
        self.H = H
        self.W = W
        self.C = C

        self.lrelu = dock.LRelu()
        self.flat = dock.Reshape()
        self.fc_1 = dock.Dense(H * W * C, latent_dim * 2)
        self.fc_2 = dock.Dense(latent_dim * 2, latent_dim)

    def run(self, x):
        self['input'] = x
        x = self.flat(self['input'], (-1, self.C * self.H * self.W))
        x = self.fc_1(x)
        x = self.lrelu(x)
        x = self.fc_2(x)
        self['out'] = self.lrelu(x)

        return self['out']



class ConvG(dock.Craft):
    def __init__(self, in_shape, latent_dim, scope='CONVG'):
        super(ConvG, self).__init__(scope)
        H, W, C = in_shape
        assert H % 4 == 0 and W % 4 == 0
        self.H = H
        self.W = W
        self.C = C

        self.lrelu = dock.LRelu()
        self.up = dock.Upscale(2)

        self.fc_1 = dock.Dense(latent_dim, 128 * (H // 4) * (W // 4))
        self.bn_1 = dock.BN(128, dim=2)
        pad = dock.autoPad((H // 2, W // 2), (3, 3))
        self.conv_1 = dock.Conv(128, 128, (3, 3), padding=pad)
        self.bn_2 = dock.BN(128, dim=2, mmnt=0.2)
        pad = dock.autoPad((H, W), (3, 3))
        self.conv_2 = dock.Conv(128, 64, (3, 3), padding=pad)
        self.bn_3 = dock.BN(64, dim=2, mmnt=0.2)
        pad = dock.autoPad((H, W), (3, 3))
        self.conv_3 = dock.Conv(64, C, (3, 3), padding=pad)

        self.tanh = dock.Tanh()
        self.reshape = dock.Reshape()

    def run(self, z):
        self['latent_code'] = z
        z = self.fc_1(self['latent_code'])
        z = self.reshape(z, (-1, 128, self.H // 4, self.W // 4))

        z = self.bn_1(z)
        z = self.up(z)
        z = self.conv_1(z)

        z = self.bn_2(z)
        z = self.lrelu(z)
        z = self.up(z)
        z = self.conv_2(z)

        z = self.bn_3(z)
        z = self.lrelu(z)
        z = self.conv_3(z)

        self['fake'] = self.tanh(z)

        return self['fake']

class DeconvG(dock.Craft):
    def __init__(self, in_shape, latent_dim, scope='DECONVG'):
        super(DeconvG, self).__init__(scope)
        H, W, C = in_shape
        assert H%4==0 and W%4==0
        self.H = H
        self.W = W
        self.C = C

        self.lrelu = dock.LRelu()

        self.fc_1 = dock.Dense(latent_dim, 128 * (H // 4) * (W // 4))
        self.bn_1 = dock.BN(128, dim=2)
        pad = dock.autoPad((H // 2, W // 2), (3, 3), stride=2)
        self.conv_1 = dock.TransConv(128, 128, (H // 2, W // 2), kernel=(3, 3), stride=2, padding=pad)
        self.bn_2 = dock.BN(128, dim=2, mmnt=0.2)
        pad = dock.autoPad((H, W), (3, 3), stride=2)
        self.conv_2 = dock.TransConv(128, 64, (H, W), kernel=(3, 3), stride=2, padding=pad)
        self.bn_3 = dock.BN(64, dim=2, mmnt=0.2)
        pad = dock.autoPad((H, W), (3, 3))
        self.conv_3 = dock.Conv(64, C, (3, 3), padding=pad)

        self.tanh = dock.Tanh()
        self.reshape = dock.Reshape()

    def run(self, z):
        self['latent_code'] = z
        z = self.fc_1(self['latent_code'])
        z = self.reshape(z, (-1, 128, self.H//4, self.W//4))

        z = self.bn_1(z)
        z = self.conv_1(z)

        z = self.bn_2(z)
        z = self.lrelu(z)
        z = self.conv_2(z)

        z = self.bn_3(z)
        z = self.lrelu(z)
        z = self.conv_3(z)

        self['fake'] = self.tanh(z)

        return self['fake']

class ConvD(dock.Craft):
    def __init__(self, in_shape, scope='CONVD'):
        super(ConvD, self).__init__(scope)
        H, W, C = in_shape
        self.H = H
        self.W = W
        self.C = C

        self.lrelu = dock.LRelu()
        self.flat = dock.Reshape()
        pad = dock.autoPad((H, W), (3, 3), stride=2)
        self.conv_1 = dock.Conv(C, 16, (3, 3), stride=2, padding=pad)
        pad = dock.autoPad((ceil(H / 2), ceil(W / 2)), (3, 3), stride=2)
        self.conv_2 = dock.Conv(16, 32, (3, 3), stride=2, padding=pad)
        self.bn_2 = dock.BN(32, dim=2, mmnt=0.2)
        pad = dock.autoPad((ceil(H / 4), ceil(W / 4)), (3, 3), stride=2)
        self.conv_3 = dock.Conv(32, 64, (3, 3), stride=2, padding=pad)
        self.bn_3 = dock.BN(64, dim=2, mmnt=0.2)
        pad = dock.autoPad((ceil(H / 8), ceil(W / 8)), (3, 3), stride=2)
        self.conv_4 = dock.Conv(64, 128, (3, 3), stride=2, padding=pad)
        self.bn_4 = dock.BN(128, dim=2, mmnt=0.2)

    def run(self, x):
        bs = x.shape[0]
        self['input'] = x
        x = self.conv_1(x)
        x = self.lrelu(x)

        x = self.conv_2(x)
        x = self.lrelu(x)
        x = self.bn_2(x)

        x = self.conv_3(x)
        x = self.lrelu(x)
        x = self.bn_3(x)

        x = self.conv_4(x)
        x = self.lrelu(x)
        x = self.bn_4(x)

        self['out'] = self.flat(x, (bs, -1))

        return self['out']



class SimpleRes(dock.Craft):
    def __init__(self, in_shape, neck_chs, stride=1, width_multp=4., scope='SIMRES'):
        super(SimpleRes, self).__init__(scope)
        H, W, C = in_shape
        self.body_chs = int(neck_chs * width_multp)
        self.bn_1 = dock.BN(C, dim=2)
        pad = dock.autoPad((H, W), (3, 3), stride=stride)
        self.conv_1 = dock.Conv(C, neck_chs, (3, 3), stride=stride, padding=pad)
        self.bn_2 = dock.BN(neck_chs, dim=2)
        self.conv_2 = dock.Conv(neck_chs, self.body_chs, (1, 1))
        self.relu = dock.Relu()

        self.ds_conv = dock.Conv(C, self.body_chs, (1, 1), stride)
        self.ds_bn = dock.BN(self.body_chs, dim=2)

    def run(self, x):
        self['input'] = x

        y = self.bn_1(x)
        y = self.relu(y)
        y = self.conv_1(y)

        y = self.bn_2(y)
        y = self.relu(y)
        y = self.conv_2(y)

        self['identity'] = self.ds_bn(self.ds_conv(x))

        y += self['identity']
        y = self.relu(y)

        return y


class ResG(dock.Craft):
    def __init__(self, in_shape, latent_dim, scope='RESG'):
        super(ResG, self).__init__(scope)
        H, W, C = in_shape
        assert H % 4 == 0 and W % 4 == 0
        self.H = H
        self.W = W
        self.C = C

        self.up = dock.Upscale(2)

        self.fc_1 = dock.Dense(latent_dim, 128 * (H // 4) * (W // 4))
        self.res_1 = SimpleRes(((H // 4), (W // 4), 128), 128, width_multp=0.5)
        self.res_2 = SimpleRes(((H // 2), (W // 2), 64), 64, width_multp=0.5)
        self.res_3 = SimpleRes((H, W, 32), 32, width_multp=C/32)
        self.tanh = dock.Tanh()
        self.reshape = dock.Reshape()

    def run(self, z):
        self['latent_code'] = z
        z = self.fc_1(self['latent_code'])
        z = self.reshape(z, (-1, 128, self.H // 4, self.W // 4))

        z = self.res_1(z)
        z = self.up(z)
        z = self.res_2(z)
        z = self.up(z)
        z = self.res_3(z)

        self['fake'] = self.tanh(z)

        return self['fake']

class ResD(dock.Craft):
    def __init__(self, in_shape, scope='RESD'):
        super(ResD, self).__init__(scope)
        H, W, C = in_shape

        self.relu = dock.Relu()
        self.flat = dock.Reshape()
        pad = dock.autoPad((H, W), (3, 3))
        self.conv_0 = dock.Conv(C, 32, (3, 3), padding=pad)
        self.res_1 = SimpleRes((H, W, 32), 16, stride=2)
        self.res_2 = SimpleRes(((H // 2), (W // 2), 64), 32, stride=2)
        self.bn = dock.BN(128, dim=2)

    def run(self, x):
        bs = x.shape[0]
        self['input'] = x
        x = self.conv_0(x)

        x = self.res_1(x)
        x = self.res_2(x)
        x = self.bn(x)
        x = self.relu(x)

        self['out'] = self.flat(x, (bs, -1))

        return self['out']