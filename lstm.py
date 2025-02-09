import torch.nn as nn

import torch

# num_classes = 11
class lstm2(nn.Module):
    def __init__(self, dataset='128'):
        super(lstm2, self).__init__()

        self.lstm1 = nn.LSTM(
            input_size=2,
            hidden_size=128,
            num_layers=1,
            bias=False,
            batch_first=True
        )
        self.lstm2 = nn.LSTM(
            input_size=128,
            hidden_size=64,
            num_layers=1,
            bias=False,
            batch_first=True
        )

        if dataset == '128':
            num_classes = 11
            self.fc = nn.Linear(128*64, num_classes)
        elif dataset == '512':
            num_classes = 12
            self.fc = nn.Linear(512*64, num_classes)
        elif dataset == '1024':
            num_classes = 24
            self.fc = nn.Linear(1024*64, num_classes)
        elif dataset == '3040':
            num_classes = 106
            self.fc = nn.Linear(3040*64, num_classes)

        # if num_classes == 10:
        #     self.fc = nn.Linear(128*64, num_classes)
        # if num_classes == 11:
        #     self.fc = nn.Linear(128*64, num_classes)
        # if num_classes == 12:
        #     self.fc = nn.Linear(512*64, num_classes)

    def forward(self, x, return_features=False):
        x, _ = self.lstm1(x.transpose(2,1))
        x, (h_n, _) = self.lstm2(x)
        
        # 使用最后一个时间步的隐藏状态作为中间层特征
        mid_features = h_n[-1]  # 形状为 [batch_size, hidden_size]
        
        x = torch.reshape(x, [x.shape[0], -1])
        output = self.fc(x)
        if return_features:
            return mid_features, output
        return output

# data = torch.randn(20,2,512)
# model = lstm2()
# print(model(data).shape)

# from torchinfo import summary
# model = lstm2(dataset='3040').cuda()
# summary(model, input_size=(128, 2, 3040))

