import os

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from torch.utils import data

from ..libs.resnet.resnet_crnn import Dataset_CRNN, CNNEncoder, RNNDecoder


class Recognizer:
    def __init__(self, model_dir="models", class_names=[], ctx_id=-1):
        self.model_dir = model_dir
        self.class_names = class_names
        self.device = torch.device("cuda:" + str(ctx_id)) if ctx_id > -1 else torch.device("cpu")
        self.cnn_encoder, self.rnn_decoder = self.load_model(model_dir, len(class_names))
        self.selected_frames = np.arange(1, 29, 1).tolist()

    @staticmethod
    def transform_data():
        transform = transforms.Compose([transforms.Resize([224, 224]),
                                        transforms.ToTensor(),
                                        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

        return transform

    @staticmethod
    def preprocess_data(data_dir, class_names: list):
        actions = []
        all_names = []
        filenames = os.listdir(data_dir)
        if ".DS_Store" in filenames:
            filenames.remove(".DS_Store")
        for f in filenames:
            if len(f.split('_')) < 2:
                continue
            actions.append(f.split('_')[0])
            all_names.append(f)
        le = LabelEncoder()
        le.fit(class_names)
        print(list(le.classes_))
        X_list = all_names  # all video file names
        y_list = le.transform(actions)  # all video labels
        return X_list, y_list

    def load_data(self, data_dir, batch_size=40):
        X_list, y_list = self.preprocess_data(data_dir, self.class_names)
        train_list, test_list, train_label, test_label = train_test_split(X_list, y_list, test_size=0.25,
                                                                          random_state=42)
        transform = self.transform_data()
        train_set = Dataset_CRNN(data_dir, train_list, train_label, self.selected_frames, transform=transform)
        valid_set = Dataset_CRNN(data_dir, test_list, test_label, self.selected_frames, transform=transform)

        params = {'batch_size': batch_size, 'shuffle': True, 'num_workers': 4, 'pin_memory': True}
        train_loader = data.DataLoader(train_set, **params)
        valid_loader = data.DataLoader(valid_set, **params)

        return train_loader, valid_loader

    def load_model(self, model_dir, num_classes=4):
        cnn_encoder = CNNEncoder(fc_hidden1=1024, fc_hidden2=768, drop_p=0.0, CNN_embed_dim=512).to(self.device)
        rnn_decoder = RNNDecoder(CNN_embed_dim=512, h_RNN_layers=3, h_RNN=512, h_FC_dim=256, drop_p=0.0,
                                 num_classes=num_classes).to(self.device)
        # cnn_encoder.load_state_dict(torch.load(os.path.join(model_dir, 'cnn_encoder_epoch63.pth'),
        #                                        map_location=None if torch.cuda.is_available() else 'cpu'))
        # rnn_decoder.load_state_dict(torch.load(os.path.join(model_dir, 'rnn_decoder_epoch63.pth'),
        #                                        map_location=None if torch.cuda.is_available() else 'cpu'))
        return cnn_encoder, rnn_decoder

    def get_optimizer(self, learning_rate=1e-3):
        if torch.cuda.device_count() > 1:
            print("Using", torch.cuda.device_count(), "GPUs!")
            self.cnn_encoder = nn.DataParallel(self.cnn_encoder)
            self.rnn_decoder = nn.DataParallel(self.rnn_decoder)
            crnn_params = list(self.cnn_encoder.module.fc1.parameters()) + list(
                self.cnn_encoder.module.bn1.parameters()) + list(self.cnn_encoder.module.fc2.parameters()) + list(
                self.cnn_encoder.module.bn2.parameters()) + list(self.cnn_encoder.module.fc3.parameters()) + list(
                self.rnn_decoder.parameters())
        else:
            print("Using", torch.cuda.device_count(), "GPU!")
            crnn_params = list(self.cnn_encoder.fc1.parameters()) + list(self.cnn_encoder.bn1.parameters()) + list(
                self.cnn_encoder.fc2.parameters()) + list(self.cnn_encoder.bn2.parameters()) + list(
                self.cnn_encoder.fc3.parameters()) + list(self.rnn_decoder.parameters())

        optimizer = torch.optim.Adam(crnn_params, lr=learning_rate)
        return optimizer

    def validation(self, test_loader):
        self.cnn_encoder.eval()
        self.rnn_decoder.eval()
        test_loss = 0
        all_y = []
        all_y_pred = []
        with torch.no_grad():
            for X, y in test_loader:
                X, y = X.to(self.device), y.to(self.device).view(-1, )
                output = self.rnn_decoder(self.cnn_encoder(X))
                loss = F.cross_entropy(output, y, reduction='sum')
                test_loss += loss.item()  # sum up batch loss
                y_pred = output.max(1, keepdim=True)[1]  # get the index of the max log-probability
                all_y.extend(y)
                all_y_pred.extend(y_pred)
        test_loss /= len(test_loader.dataset)
        # compute accuracy
        all_y = torch.stack(all_y, dim=0)
        all_y_pred = torch.stack(all_y_pred, dim=0)
        test_score = accuracy_score(all_y.cpu().data.squeeze().numpy(), all_y_pred.cpu().data.squeeze().numpy())
        print('\nTest set ({:d} samples): Average loss: {:.4f}, Accuracy: {:.2f}%\n'.format(len(all_y), test_loss,
                                                                                            100 * test_score))
        return test_loss, test_score

    def predict(self, data_dir):
        self.cnn_encoder.eval()
        self.rnn_decoder.eval()
        transform = self.transform_data()
        X = []
        for i in self.selected_frames:
            image = Image.open(os.path.join(data_dir, 'frame{:06d}.jpg'.format(i)))
            if transform is not None:
                image = transform(image)
            X.append(image)
        X = torch.stack(X, dim=0).unsqueeze(0)
        with torch.no_grad():
            X = X.to(self.device)
            output = self.rnn_decoder(self.cnn_encoder(X))
            pred = output.max(1, keepdim=True)[1]
            pred = int(pred.cpu().data.numpy())
        return pred

    def train(self, data_dir, batch_size=40, epochs=120):
        train_loader, test_loader = self.load_data(data_dir, batch_size)
        optimizer = self.get_optimizer()
        train_losses = []
        train_scores = []
        test_losses = []
        test_scores = []
        for epoch in range(epochs):
            self.cnn_encoder.train()
            self.rnn_decoder.train()
            losses = []
            scores = []
            N_count = 0  # counting total trained sample in one epoch
            for batch_idx, (X, y) in enumerate(train_loader):
                X, y = X.to(self.device), y.to(self.device).view(-1, )
                N_count += X.size(0)
                optimizer.zero_grad()
                output = self.rnn_decoder(self.cnn_encoder(X))  # output has dim = (batch, number of classes)
                loss = F.cross_entropy(output, y)
                losses.append(loss.item())
                # compute accuracy
                y_pred = torch.max(output, 1)[1]
                step_score = accuracy_score(y.cpu().data.squeeze().numpy(), y_pred.cpu().data.squeeze().numpy())
                scores.append(step_score)  # computed on CPU
                loss.backward()
                optimizer.step()
                if (batch_idx + 1) % 1 == 0:
                    print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}, Accu: {:.2f}%'.format(
                        epoch + 1, N_count, len(train_loader.dataset), 100. * (batch_idx + 1) / len(train_loader),
                        loss.item(),
                        100 * step_score))
            test_loss, test_score = self.validation(test_loader)
            train_losses.append(losses)
            train_scores.append(scores)
            test_losses.append(test_loss)
            test_scores.append(test_score)
            torch.save(self.cnn_encoder.state_dict(),
                       os.path.join(self.model_dir, 'cnn_encoder_epoch{}.pth'.format(epoch + 1)))
            torch.save(self.rnn_decoder.state_dict(),
                       os.path.join(self.model_dir, 'rnn_decoder_epoch{}.pth'.format(epoch + 1)))
        # plot
        fig = plt.figure(figsize=(10, 4))
        plt.subplot(121)
        plt.plot(np.arange(1, epochs + 1), np.array(train_losses)[:, -1])  # train loss (on epoch end)
        plt.plot(np.arange(1, epochs + 1), np.array(test_losses))  # test loss (on epoch end)
        plt.title("model loss")
        plt.xlabel('epochs')
        plt.ylabel('loss')
        plt.legend(['train', 'test'], loc="upper left")
        # 2nd figure
        plt.subplot(122)
        plt.plot(np.arange(1, epochs + 1), np.array(train_scores)[:, -1])  # train accuracy (on epoch end)
        plt.plot(np.arange(1, epochs + 1), np.array(test_scores))  # test accuracy (on epoch end)
        plt.title("training scores")
        plt.xlabel('epochs')
        plt.ylabel('accuracy')
        plt.legend(['train', 'test'], loc="upper left")
        title = "fig_ResNetCRNN.png"
        plt.savefig(title, dpi=600)
        plt.close(fig)
        pass


if __name__ == '__main__':
    # load actions names
    action_names = ['1D',
                    '2D',
                    '3D',
                    'CG']
    re = Recognizer(class_names=action_names)
    re.train(data_dir="jpgs_4")
