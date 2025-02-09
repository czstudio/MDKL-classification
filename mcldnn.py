import torch.nn as nn
import torch
import torch.nn.functional as F
from torch.nn import Sequential

# num_classes = 11
# BasicBlock {{{
class MCLDNN(nn.Module):

    def __init__(self, dataset='128'):
        super(MCLDNN, self).__init__()
        if dataset == '128':
            num_classes = 11
        elif dataset == '512':
            num_classes = 12
        elif dataset == '1024':
            num_classes = 24
        elif dataset == '3040':
            num_classes = 106
        self.conv1 = nn.Conv1d(
            in_channels=2,
            out_channels=50,
            kernel_size=7,
            bias=False,
            padding=3,
        )
        self.conv2 = Sequential(
            nn.Conv1d(
            in_channels=2,
            out_channels=100,
            kernel_size=7,
            bias=False,
            padding=3,
            groups=2
        ),
            nn.ReLU(True),
            nn.Conv1d(
            in_channels=100,
            out_channels=50,
            kernel_size=7,
            bias=False,
            padding=3,
        ))
        self.conv3 = nn.Conv1d(
            in_channels=100,
            out_channels=100,
            kernel_size=5,
            bias=False
        )
        self.lstm1 = nn.LSTM(
            input_size=100,
            hidden_size=128,
            num_layers=1,
            bias=False,
        )
        self.lstm2 = nn.LSTM(
            input_size=128,
            hidden_size=128,
            num_layers=1,
            bias=False,
            batch_first=True
        )
        self.fc = Sequential(
            nn.Linear(128, 128),
            nn.SELU(True),
            nn.Dropout(0.5),
            nn.Linear(128, 128),
            nn.SELU(True),
            nn.Dropout(0.5),
            nn.Linear(128, num_classes)
        )
        
    def forward(self, x, return_features=False):
        assert len(x.shape)==3 and x.shape[1]==2
        x1 = self.conv1(x)
        x2 = self.conv2(x)
        x3 = F.relu(torch.cat([x1,x2],dim=1))
        x3 = F.relu(self.conv3(x3))
        x3, _ = self.lstm1(x3.transpose(2,1))
        _, (x3, __) = self.lstm2(x3)
        
        # 我们选择LSTM2的输出作为中间特征
        mid_features = x3.squeeze()
        
        x3 = self.fc(mid_features)

        if return_features:
            return mid_features, x3
        else:
            return x3


# model = MCLDNN(11)
# data = torch.randn(10,2,512)
# out = model(data)
# print(out.shape)

# from torchinfo import summary
# model = MCLDNN(11).cuda()
# summary(model, input_size=(128, 2, 3040))




