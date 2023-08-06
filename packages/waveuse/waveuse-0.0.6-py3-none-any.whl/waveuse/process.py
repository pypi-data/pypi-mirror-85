import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import librosa

path='MACNN_mfcc.pth'
class FeatureExtractor(object):
    def __init__(self, rate):
        self.rate = rate
    # 定义函数获取特征提取的方法
    def get_features(self, features_to_use, X):
        X_features = None
        accepted_features_to_use = ("logfbank", 'mfcc', 'fbank', 'melspectrogram', 'spectrogram', 'pase')
        if features_to_use not in accepted_features_to_use:
            raise NotImplementedError("{} not in {}!".format(features_to_use, accepted_features_to_use))
        if features_to_use in ('logfbank'):
            X_features = self.get_logfbank(X)  # 调用下面的定义的方法
        if features_to_use in ('mfcc'):
            X_features = self.get_mfcc(X,26)
        if features_to_use in ('fbank'):
            X_features = self.get_fbank(X)
        if features_to_use in ('melspectrogram'):
            X_features = self.get_melspectrogram(X)
        if features_to_use in ('spectrogram'):
            # spectrogram是一个MATLAB函数，使用短时傅里叶变换得到信号的频谱图。当使用时无输出参数，会自动绘制频谱图；有输出参数，则会返回输入信号的短时傅里叶变换。
            X_features = self.get_spectrogram(X)
        if features_to_use in ('pase'):
            X_features = self.get_Pase(X)
        return X_features

    def get_logfbank(self, X):  # 用不同的方法来获取特征处理结果
        def _get_logfbank(x):
            out = logfbank(signal=x, samplerate=self.rate, winlen=0.040, winstep=0.010, nfft=1024, highfreq=4000,
                           nfilt=40)
            return out

        X_features = np.apply_along_axis(_get_logfbank, 1, X)
        return X_features
# 提取特征 用librosa提取mfcc特征
    def get_mfcc(self, X, n_mfcc=13):
        def _get_mfcc(x):
            mfcc_data = librosa.feature.mfcc(x, sr=self.rate, n_mfcc=n_mfcc)
            return mfcc_data

        X_features = np.apply_along_axis(_get_mfcc, 1, X)
        return X_features

    def get_fbank(self, X):
        def _get_fbank(x):
            out, _ = fbank(signal=x, samplerate=self.rate, winlen=0.040, winstep=0.010, nfft=1024)
            return out

        X_features = np.apply_along_axis(_get_fbank, 1, X)
        return X_features

    def get_melspectrogram(self, X):
        def _get_melspectrogram(x):
            mel = librosa.feature.melspectrogram(y=x, sr=self.rate)
            mel = np.log10(mel + 1e-10)
            return mel

        X_features = np.apply_along_axis(_get_melspectrogram, 1, X)
        return X_features

    def get_spectrogram(self, X):
        def _get_spectrogram(x):
            frames = sigproc.framesig(x, 640, 160)
            out = sigproc.logpowspec(frames, NFFT=3198)
            out = out.swapaxes(0, 1)
            return out[:][:400]

        X_features = np.apply_along_axis(_get_spectrogram, 1, X)
        return X_features


    def get_Pase(self,X):
        return X

class MACNN(nn.Module):    # 定义注意力卷积模型
    # 相当于输入的特征值的不同数量，详见ppt
    def __init__(self, attention_heads=8, attention_hidden=256, out_size=4):
        super(MACNN, self).__init__()  # 继承函数__init__()中的相关的参数
        self.attention_heads = attention_heads # 初始化参数 attention_heads # 这里的是需要额外赋值
        self.attention_hidden = attention_hidden # 初始化参数 attention_hidden
        # 接下来就是定义的各个卷积层
        # kernel_size和padding之间的关系：padding=int(kernel_size - 1)//2 （表示向下取整的意思）
        self.conv1a = nn.Conv2d(kernel_size=(10, 2), in_channels=1, out_channels=8, padding=(4, 0))
        self.conv1b = nn.Conv2d(kernel_size=(2, 8), in_channels=1, out_channels=8, padding=(0, 3))
        self.conv2 = nn.Conv2d(kernel_size=(3, 3), in_channels=16, out_channels=32, padding=1)
        self.conv3 = nn.Conv2d(kernel_size=(3, 3), in_channels=32, out_channels=48, padding=1)
        self.conv4 = nn.Conv2d(kernel_size=(3, 3), in_channels=48, out_channels=64, padding=1)
        self.conv5 = nn.Conv2d(kernel_size=(3, 3), in_channels=64, out_channels=attention_hidden, padding=1)
        #池化操作
        self.maxp = nn.MaxPool2d(kernel_size=(2, 2))
        # 参数为out_channels 进行数据的归一化处理
        self.bn1a = nn.BatchNorm2d(8)  # 参数为待处理数据通道数
        self.bn1b = nn.BatchNorm2d(8)  # 每一次卷积操作之后都会进行一次数据的标准化操作
        self.bn2 = nn.BatchNorm2d(32)
        self.bn3 = nn.BatchNorm2d(48)
        self.bn4 = nn.BatchNorm2d(64)
        self.bn5 = nn.BatchNorm2d(attention_hidden)
        # 自适应平均池化函数 参数是output_size
        self.gap = nn.AdaptiveAvgPool2d(1)
        # 是用来设置网络的全连接层的
        self.fc = nn.Linear(in_features=self.attention_hidden, out_features=out_size)
        # 以0.5的概率让神经元置0
        self.dropout = nn.Dropout(0.5)
        # 对于cnn前馈神经网络如果前馈一次写一个forward函数会有些麻烦
        self.attention_query = nn.ModuleList() # 这个是注意力self-attention的三个参数
        self.attention_key = nn.ModuleList()
        self.attention_value = nn.ModuleList()
        for i in range(self.attention_heads):
          self.attention_query.append(nn.Linear(90, 90))
          self.attention_key.append(nn.Linear(90, 90))
          self.attention_value.append(nn.Linear(90, 90))

# 定义前向传播函数 就是模型照着来

    def forward(self, *input):
        xa = self.conv1a(input[0])  # 这个input[0]
        xa = self.bn1a(xa)

        xa = F.relu(xa)
        xb = self.conv1b(input[0])
        xb = self.bn1b(xb)

        xb = F.relu(xb)
        # 将两个tensor连接起来，具体如何连接见下面例子
        x = torch.cat((xa, xb), 1)
        x = self.conv2(x)
        x = self.bn2(x)

        x = F.relu(x)
        x = self.maxp(x)
        x = self.conv3(x)
        x = self.bn3(x)

        x = F.relu(x)
        x = self.maxp(x)
        x = self.conv4(x)
        x = self.bn4(x)

        x = F.relu(x)

        x = self.conv5(x)
        x = self.bn5(x)

        x = F.relu(x)

        height = x.shape[2]
        width = x.shape[3]
        # 重新定义四维张量的形状
        x = x.reshape(x.shape[0], x.shape[1], 1, -1)
        # Head Fusion
        attn = None  # 用于计算self-attention
        for i in range(self.attention_heads):
            Q = self.attention_query[i](x)
            K = self.attention_key[i](x).transpose(2,3)
            V = self.attention_value[i](x)
            attention = F.softmax(torch.matmul(K,Q))
            attention = torch.matmul(V,attention)
            attention=attention.reshape(attention.shape[0],attention.shape[1],height,width)
            if (attn is None):
                attn = attention
            else:
                attn = torch.cat((attn, attention), 2)
        x = attn
        x = F.relu(x)
        x = self.gap(x)

        x = x.reshape(x.shape[0], x.shape[1] * x.shape[2] * x.shape[3])

        x = self.fc(x)
        return x

def WavPro(wav_data):
    model = MACNN(4, 32)  # 调用模型
    model.load_state_dict(torch.load('MACNN_mfcc.pth'))  # 加载模型
    model = model.cuda()  # u、cuda加速
    index = 0  # 索引从0开始
    X1 = []  # 设置列表，用来存储已经处理过的数据
    while (index + 2 * 16000 <= len(wav_data)):  # 主要是对wav文件进行后移裁剪的工作
        X1.append(wav_data[int(index):int(index + 2 * 16000)])
        index += int(0.4 * 16000)
    T_X1 = np.array(X1)
    featureExtractor = FeatureExtractor(16000)  # 将每次取样的16000个点进行提取特征值
    X = featureExtractor.get_features('mfcc', T_X1)  # 利用mfcc提取特征，数据是处理过的x1
    X = torch.tensor(X).unsqueeze(1).cuda()  # 在第二个位置上增加一个一维的数据
    with torch.no_grad():
        out = model(X)
        # 获取最大值以及最大值的索引
    max_value, max_idx = torch.max(out, dim=1)
    if max_idx[-1] == 0:
        temp_print = 'neutral'
    elif max_idx[-1] == 1:
        temp_print = 'sad'
    elif max_idx[-1] == 2:
        temp_print = 'angry'
    else:
        temp_print = 'happy'
    return temp_print
