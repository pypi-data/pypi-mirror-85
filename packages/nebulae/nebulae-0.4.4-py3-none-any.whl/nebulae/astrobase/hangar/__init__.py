#!/usr/bin/env python
'''
__init__
Created by Seria at 23/11/2018 10:30 AM
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
from .vgg import VGG_16
from .resnet import Resnet_V2_50, Resnet_V2_101, Resnet_V2_152
# from .senet import SE_RESNET_V2_50, SE_RESNET_V2_101, SE_RESNET_V2_152
from .gan import GAN
from .dcgan import DCGAN
from .fcgan import FCGAN
from .wgan import WGAN
from .wgan_div import WGANDiv
from .infogan import InfoGAN