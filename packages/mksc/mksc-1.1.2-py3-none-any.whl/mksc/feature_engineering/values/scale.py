
def fix_scaling(feature):
    """
    对数据框中的数据进行中性化处理

    Args:
        feature: 待处理的数据框

    Returns:
        feature: 已处理数据框
    """
    numeric_var = feature.select_dtypes(exclude=['object', 'datetime']).columns
    scale_result = {}
    for c in numeric_var:
        sm = feature[c].describe()
        scale_result[c] = {'mean': sm['mean'], 'std': sm['std']}
        feature[c] = feature[c].apply(lambda x: (x - sm['mean'])/sm['std'] if x else x)
    return feature, scale_result
