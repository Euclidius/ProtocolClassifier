import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

csv_file_name=input_file
abc = pd.read_csv(csv_file_name,sep=',')
resc=list(abc[abc['src_ip']=='172.17.240.131'].index)
abc=abc[abc['src_ip']!='172.17.240.131']
#resc=list(res_c.index)
useful=['pkt_len_'+str(i) for i in range(13)]
abc=abc[useful].dropna()
#model = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
model = joblib.load(open('tree_weights/tree1.sav', 'rb')) 
yabc = model.predict(abc)
abcr=abc
abcr['class']=yabc
resa=list(abcr[abcr['class']=='a'].index)
resb=list(abcr[abcr['class']=='b'].index)
ra=pd.DataFrame({'ind':resa})
ra['class']=['a' for _ in range(len(resa))]
rb=pd.DataFrame({'ind':resb})
rb['class']=['b' for _ in range(len(resb))]
rc=pd.DataFrame({'ind':resc})
rc['class']=['c' for _ in range(len(resc))]
r=pd.concat([ra,rb,rc],axis=0)
r=r.sort_values(by='ind')
r.to_csv(output_file,sep=';',index=False)
