import pickle
import pandas as pd
from mksc.feature_engineering import seletction
from mksc.feature_engineering import values
from mksc.feature_engineering import binning
from imblearn.over_sampling import SMOTE


class FeatureEngineering(object):

    def __init__(self, feature, label, missing_threshold=(0.9, 0.05), distinct_threshold=0.9, unique_threshold=0.9,
                 abnormal_threshold=0.05, correlation_threshold=0.7):
        self.feature = feature
        self.label = label
        self.missing_threshold = missing_threshold
        self.distinct_threshold = distinct_threshold
        self.unique_threshold = unique_threshold
        self.abnormal_threshold = abnormal_threshold
        self.correlation_threshold = correlation_threshold
        self.threshold = {"missing_threshold": self.missing_threshold,
                          "distinct_threshold": self.distinct_threshold,
                          "unique_threshold": self.unique_threshold,
                          "abnormal_threshold": self.abnormal_threshold,
                          "correlation_threshold": self.correlation_threshold}

    def run(self):
        """
        特征工程过程函数,阈值参数可以自定义修改
        1. 特征组合
        2. 基于统计特性特征选择：缺失率、唯一率、众数比例
        3. 缺失值处理
        TODO 异常值处理
        4. 极端值处理
        5. 正态化处理
        6. 归一化处理
        7. 最优分箱
        8. IV筛选
        TODO PSI筛选
        9. 相关性筛选
        10. woe转化
        11. One-Hot
        12. XXX 降维：逐步回归筛选
        13. XXX 采样

        Returns:
            feature: 已完成特征工程的数据框
            label: 已完成特征工程的标签列
        """
        feature = self.feature
        label = self.label

        # One-Hot编码
        category_var = feature.select_dtypes(include=['object']).columns
        if not category_var.empty:
            feature[category_var].fillna("NA", inplace=True)
            feature = pd.concat([feature, pd.get_dummies(feature[category_var])], axis=1)
            feature.drop(category_var, axis=1, inplace=True)

        # 基于缺失率、唯一率、众数比例统计特征筛选
        missing_value = seletction.get_missing_value(feature, self.missing_threshold[0])
        distinct_value = seletction.get_distinct_value(feature, self.distinct_threshold)
        unique_value = seletction.get_unique_value(feature, self.unique_threshold)
        feature.drop(set(missing_value['drop'] + distinct_value['drop'] + unique_value['drop']), axis=1, inplace=True)

        # 缺失值处理
        feature, missing_filling = values.fix_missing_value(feature, self.missing_threshold[1])

        # 极端值处理
        feature, abnormal_value = values.fix_abnormal_value(feature, self.abnormal_threshold)

        # 正态化处理
        feature, standard_lambda = values.fix_standard(feature)

        # 归一化处理
        feature, scale_result = values.fix_scaling(feature)

        # 数值特征最优分箱，未处理的变量，暂时退出模型
        bin_result, iv_result, woe_result, woe_adjust_result = binning.tree_binning(label, feature)
        bin_error_drop = bin_result['error'] + woe_adjust_result

        # IV筛选
        iv_drop = list(filter(lambda x: iv_result[x] < 0.02, iv_result))
        feature.drop(iv_drop + bin_error_drop, inplace=True, axis=1)

        # 相关性筛选
        cor_drop = seletction.get_cor_drop(feature, iv_result, self.correlation_threshold)
        feature.drop(cor_drop, inplace=True, axis=1)

        # woe转化
        feature = binning.woe_transform(feature, woe_result, bin_result)

        # 重采样
        if label.sum()/len(label) < 0.1 or label.sum()/len(label) > 0.9:
            feature, label = SMOTE().fit_sample(feature, label)

        # 逐步回归筛选
        feature_selected = seletction.stepwise_selection(feature, label)
        feature = feature[feature_selected]

        # 中间结果保存
        result = {"missing_value": missing_value,
                  "distinct_value": distinct_value,
                  "unique_value": unique_value,
                  "abnormal_value": abnormal_value,
                  "missing_filling": missing_filling,
                  'standard_lambda': standard_lambda,
                  'scale_result': scale_result,
                  "bin_result": bin_result,
                  "iv_result": iv_result,
                  "woe_result": woe_result,
                  "woe_adjust_result": woe_adjust_result,
                  "bin_error_drop": bin_error_drop,
                  "iv_drop": iv_drop,
                  "cor_drop": cor_drop,
                  "feature_selected": feature_selected
                  }
        with open('result/feature_engineering.pickle', 'wb') as f:
            f.write(pickle.dumps(result))

        with open('result/apply_sql.txt', 'wb') as f:
            sql = ",".join(result["feature_selected"])
            f.write(f"select {sql} from ")