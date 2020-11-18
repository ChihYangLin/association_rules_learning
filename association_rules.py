import pandas as pd
from apyori import apriori

def import_data_from_csv(filename):
    data = pd.read_csv(filename, encoding='utf-8')
    return data

def make_user_item_list(df,userID_col_name,itemName_col_name):
    user_item_df = df.groupby(userID_col_name).agg({itemName_col_name: lambda x : ','.join(x).split(',')})
    user_item_list = user_item_df[itemName_col_name].tolist()
    return user_item_list

def make_rules_df(double_list, min_sup, min_conf, min_lif):
    association_rules = apriori(double_list, min_support=min_sup, min_confidence = min_conf, min_lift=min_lif,max_length = 2)
    association_DF = pd.DataFrame(list(association_rules))
    association_DF = association_DF.explode('ordered_statistics')
    association_DF = association_DF.explode('ordered_statistics')
    association_DF.reset_index(drop=True,inplace=True)
    return association_DF

def make_support_df(df):
    df_copy = df.copy()
    for i in range(len(df)):
        if i%4 != 0:
            df_copy.drop(index=i,inplace=True)
    df_copy.reset_index(drop=True,inplace=True)
    return df_copy

def make_association_rule_df(df, sup_df):
    rule_list = []
    association_list = df['ordered_statistics'].tolist()
    n = 0
    while True:
        if n < len(df)-3:
            tmp_list = association_list[n:n+4]
            rule_list.append(tmp_list)
            n +=4
        else:
            break
    associate_df = pd.DataFrame(data = rule_list, columns=['item1','item2','confidence','lift'])
    association_rule_df = pd.concat([associate_df,sup_df['support']],axis=1)
    association_rule_df.drop(association_rule_df[association_rule_df['confidence']==1].index,axis=0, inplace=True)
    association_rule_df['item2_original_buy_rate'] = association_rule_df['confidence'] / association_rule_df['lift']
    return association_rule_df

def save_df_to_cvs(df,filename):
    df.to_csv(filename,encoding='utf_8_sig',index=False)


def main():
    # 參數設定
    open_file_name = 'transaction_records.csv'
    save_file_name_lift = 'association_rules_lift.csv'
    save_file_name_confidence = 'association_rules_confidence.csv'
    column_of_user_ID = 'CustomerID'
    column_of_item_name = 'ProductName'
    min_sup = 0.03  # 最小支持度  N(A,B)/N(All)
    min_conf = 0.6  # 最小信賴度   A 的信賴度 = N(A,B)/N(B)
    min_lif = 5  # 最小提升度   A 的提升度 = A 的信賴度/A 的購買率 (大於 1 才有意義，不然單買就好)

    # 從csv載入資料 --> Dataframe
    data_df = import_data_from_csv(open_file_name)

    # Dataframe --> 將購物籃變成雙重list ex:[[A,B],[A,C,D],[B,F]...]
    user_item_list = make_user_item_list(data_df, column_of_user_ID, column_of_item_name)

    # 購物籃list --> 關聯規則Dataframe
    rule_df = make_rules_df(user_item_list, min_sup=min_sup, min_conf=min_conf, min_lif=min_lif)

    # 創造每條規則的支持度(Support) Dataframe
    support_df = make_support_df(rule_df)

    # 將規則與支持度兩個Dataframe合併
    association_rule_df = make_association_rule_df(rule_df, support_df)

    # 依照提升度(Lift)做排序, 輸出成CSV檔
    association_rule_df.sort_values(by='lift', ascending=False, inplace=True)
    save_df_to_cvs(association_rule_df, save_file_name_lift)

    # 依照信賴度(confidence)做排序, 輸出成CSV檔
    association_rule_df.sort_values(by='confidence', ascending=False, inplace=True)
    save_df_to_cvs(association_rule_df, save_file_name_confidence)

if __name__ == '__main__':
    main()