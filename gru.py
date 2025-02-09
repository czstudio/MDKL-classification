import torch.nn as nn

import torch
import torch.nn.functional as F

# num_classes = 11
class gru2(nn.Module):
    def __init__(self, dataset='128'):
        super(gru2, self).__init__()

        self.gru1 = nn.GRU(
            input_size=2,
            hidden_size=128,
            num_layers=1,
            bias=False,
            batch_first=True
        )
        self.gru2 = nn.GRU(
            input_size=128,
            hidden_size=64,
            num_layers=1,
            bias=False,
            batch_first=True
        )

        if dataset == '128':
            num_classes = 11
            self.fc1 = nn.Linear(128*64, 64)
            self.fc2 = nn.Linear(64, num_classes)
        elif dataset == '512':
            num_classes = 12
            self.fc1 = nn.Linear(512*64, 64)
            self.fc2 = nn.Linear(64, num_classes)
        elif dataset == '1024':
            num_classes = 24
            self.fc1 = nn.Linear(1024*64, 64)
            self.fc2 = nn.Linear(64, num_classes)
        elif dataset == '3040':
            num_classes = 106
            self.fc1 = nn.Linear(3040*64, 64)
            self.fc2 = nn.Linear(64, num_classes)


    def forward(self, x, return_features=False):
        x, _ = self.gru1(x.transpose(2,1))
        x = F.relu(x)
        x, _ = self.gru2(x)
        x = torch.reshape(x, [x.shape[0],-1])
        mid_features = self.fc1(x)  # 这里是中间特征
        x = self.fc2(mid_features)
        if return_features:
            return mid_features, x
        return x

# from torchinfo import summary
# model = gru2(dataset='128').cuda()
# summary(model, input_size=(128, 2, 128))
