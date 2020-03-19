import pandas as pd
df_18_01 = pd.read_csv('L:\\M_Media\\DataFriend\\DFW Department\\Grivtsov\\data\\processing\\Pochta\\NPS\\input\\LetoBank18-01.csv', sep=';', encoding='utf-8', low_memory=False)
df_19_11 = pd.read_csv('L:\\M_Media\\DataFriend\\DFW Department\\Grivtsov\\data\\processing\\Pochta\\NPS\\input\\LetoBank19-11.csv', sep=';', encoding='utf-8', low_memory=False)
a_column_18 = df_18_01.columns.tolist()#получение списка содержащего названия всех столбцов
a_column_19 = df_19_11.columns.tolist()#получение списка содержащего названия всех столбцов
q_18_01={}
for i in a_column_18:#берез значение из списка с именами переменных
    d = df_18_01[i].unique().tolist()#получение всех уникальных значений их столбцов
    q_18_01[i]=d
    
q_19_11={}
for i in a_column_19:#берез значение из списка с именами переменных
    d = df_19_11[i].unique().tolist()#получение всех уникальных значений их столбцов
    q_19_11[i]=d
q_18_01_up = {}
for i in q_18_01:
    if i in q_19_11:
        q_18_01_up[i]=q_18_01[i]
q_19_11_up = q_19_11
for i in q_18_01_up:
    for v_1 in q_18_01_up[i]:
        if v_1 in q_19_11_up[i]:
            q_18_01_up[i].remove(v_1)
            q_19_11_up[i].remove(v_1)
for i in q_18_01_up:
    print(i,"-в этом столбеце следующие значения из 18 и 19 года")
    print(q_18_01_up[i],'-18 год')
    print('_________________________')
    print(q_19_11_up[i],'-19 год')
    print('=====================================')