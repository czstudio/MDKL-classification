import torch.nn as nn
import torch
import torch.nn.functional as F
# from torch.fftpack import fft, rfft, ifft
from torch.fft import fft,ifft

# num_classes = 11
# ResNet {{{
class ResNet1D(nn.Module):
    def __init__(self, dataset='128'):
        super(ResNet1D, self).__init__()
        self.conv1 = ResidualStack(1, kernel_size=(2, 3),pool_size=(2, 2),first=True)
        self.conv2 = ResidualStack(32, kernel_size=3, pool_size=2)
        self.conv3 = ResidualStack(32, kernel_size=3, pool_size=2)
        self.conv4 = ResidualStack(32, kernel_size=3, pool_size=2)
        self.conv5 = ResidualStack(32, kernel_size=3, pool_size=2)
        self.conv6 = ResidualStack(32, kernel_size=3, pool_size=2)
        if dataset == '128':
            num_classes = 11
            self.dense = nn.Linear(64, 128)
        elif dataset == '512':
            num_classes = 12
            self.dense = nn.Linear(256, 128)
        elif dataset == '1024':
            num_classes = 24
            self.dense = nn.Linear(512, 128)
        elif dataset == '3040':
            num_classes = 106
            self.dense = nn.Linear(1504, 128)
        self.drop = nn.Dropout(p=0.3)
        self.classfier = nn.Linear(128, num_classes)

    def forward(self, x, return_features=False):

        x = self.conv1(x.unsqueeze(dim=1)).squeeze(dim=2)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.conv5(x)
        x = self.conv6(x).view(x.size(0),-1)
        mid_features = self.dense(x)  # mid_features 中间特征是经过所有卷积层和第一个全连接层（self.dense）处理后的特征。这些特征包含了输入信号的高级表示，但还没有被映射到最终的类别概率。
        x = self.classfier(self.drop(mid_features))
        if return_features:
            return mid_features, x
        return x
     # 中间特征通常指的是网络在最终分类层之前的深层表示。这些特征包含了输入数据的高级抽象信息，对于知识蒸馏特别有用。


class ResidualStack(nn.Module):
    def __init__(self, in_channel, kernel_size, pool_size, first=False):
        super(ResidualStack, self).__init__()
        mid_channel = 32
        padding = 1
        if first:
            conv = nn.Conv2d
            pool = nn.MaxPool2d
            self.conv1 = conv(in_channel, mid_channel, kernel_size=1, padding=0, bias=False)
            self.conv2 = conv(mid_channel, mid_channel, kernel_size=kernel_size, padding=(1, padding), bias=False)
            self.conv3 = conv(mid_channel, mid_channel, kernel_size=kernel_size, padding=(0, padding), bias=False)
            self.conv4 = conv(mid_channel, mid_channel, kernel_size=kernel_size, padding=(1, padding), bias=False)
            self.conv5 = conv(mid_channel, mid_channel, kernel_size=kernel_size, padding=(0, padding), bias=False)
            self.pool = pool(kernel_size=pool_size, stride=pool_size)
        else:
            conv = nn.Conv1d
            pool = nn.MaxPool1d
            self.conv1 = conv(in_channel, mid_channel, kernel_size=1, padding=0, bias=False)
            self.conv2 = conv(mid_channel, mid_channel, kernel_size=kernel_size, padding=padding, bias=False)
            self.conv3 = conv(mid_channel, mid_channel, kernel_size=kernel_size, padding=padding, bias=False)
            self.conv4 = conv(mid_channel, mid_channel, kernel_size=kernel_size, padding=padding, bias=False)
            self.conv5 = conv(mid_channel, mid_channel, kernel_size=kernel_size, padding=padding, bias=False)
            self.pool = pool(kernel_size=pool_size, stride=pool_size)
    def forward(self, x):
        # residual 1
        x = self.conv1(x)
        shortcut = x
        x = self.conv2(x)
        x = F.relu(x)
        x = self.conv3(x)
        x += shortcut
        x = F.relu(x)

        # residual 2
        shortcut = x
        x = self.conv4(x)
        x = F.relu(x)
        x = self.conv5(x)
        x += shortcut
        x = F.relu(x)
        x = self.pool(x)

        return x
        
# def resnet1d(**kwargs):
#     return ResNet1D(**kwargs)


# data = torch.randn(10,2,512)
# print(len(data))
# # model = resnet1d()
# # out = model(data)
# # print(out.shape)
# from torchsummary import summary
# model = resnet1d().cuda()
# summary(model, (2, 128))

# from torchinfo import summary
# model = resnet1d(dataset='128').cuda()
# summary(model, input_size=(128, 2, 128))
#
