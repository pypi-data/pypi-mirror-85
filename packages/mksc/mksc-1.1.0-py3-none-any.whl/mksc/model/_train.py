import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import auc, roc_curve, accuracy_score, recall_score
from mksc.model import model_choose

def training(x_train, y_train, x_test, y_test, x_valid, y_valid, model_name='lr'):
    """
    模型训练过程函数
    1. 训练
    2. 预测
    3. 评估
    4. 模型可选

    Args:
        x_train: 训练集特征
        y_train: 训练集标签
        x_test: 测试集特征
        y_test: 测试集标签
        x_valid: 验证集特征
        y_valid: 验证集标签
        model_name: 使用模型类型
    """
    model = model_choose(model_name)
    model.fit(x_train, y_train)

    # 预测结果
    predict_train = model.predict(x_train)
    predict_valid = model.predict(x_valid)
    predict_test = model.predict(x_test)

    # 模型评估
    acu_train = accuracy_score(y_train, predict_train)
    acu_valid = accuracy_score(y_valid, predict_valid)
    acu_test = accuracy_score(y_test, predict_test)

    sen_train = recall_score(y_train, predict_train, pos_label=1)
    sen_valid = recall_score(y_valid, predict_valid, pos_label=1)
    sen_test = recall_score(y_test, predict_test, pos_label=1)

    spe_train = recall_score(y_train, predict_train, pos_label=0)
    spe_valid = recall_score(y_valid, predict_valid, pos_label=0)
    spe_test = recall_score(y_test, predict_test, pos_label=0)
    print(f'模型准确率：验证 {acu_valid * 100:.2f}%	训练 {acu_train * 100:.2f}%	测试 {acu_test * 100:.2f}%')
    print(f'正例覆盖率：验证 {sen_valid * 100:.2f}%	训练 {sen_train * 100:.2f}%	测试 {sen_test * 100:.2f}%')
    print(f'负例覆盖率：验证 {spe_valid * 100:.2f}%	训练 {spe_train * 100:.2f}%	测试 {spe_test * 100:.2f}%')

    # K-s & roc
    predict_train_prob = np.array([i[1] for i in model.predict_proba(x_train)])
    fpr, tpr, thresholds = roc_curve(y_train.values, predict_train_prob, pos_label=1)
    auc_score = auc(fpr, tpr)
    w = tpr - fpr
    ks_score = w.max()
    ks_x = fpr[w.argmax()]
    ks_y = tpr[w.argmax()]
    fig, ax = plt.subplots()
    ax.plot(fpr, tpr, label='AUC=%.5f' % auc_score)
    ax.set_title('Receiver Operating Characteristic')
    ax.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6))
    ax.plot([ks_x, ks_x], [ks_x, ks_y], '--', color='red')
    ax.text(ks_x, (ks_x + ks_y) / 2, '  KS=%.5f' % ks_score)
    ax.legend()
    fig.savefig("result/ks_roc.png")

    # 模型保存
    coefs = dict(list(zip(x_train.columns, list(model.coef_[0]))) + [("intercept_", model.intercept_[0])])
    with open(f'result/{model_name}.pickle', 'wb') as f:
        f.write(pickle.dumps(model))
    if model_name == 'lr':
        with open('result/coefs.pickle', 'wb') as f:
            f.write(pickle.dumps(coefs))
