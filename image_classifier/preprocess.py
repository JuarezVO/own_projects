# %%
import numpy as np, os, cv2, random, matplotlib.pyplot as plt

# %%
datadir = 'D:\machine_learning\image_classification\chapadao'
categories = ['sem_prp','com_prp']

training_data = []
for cat in categories:
  paths = os.path.join(datadir,cat)
  class_num = categories.index(cat)
  for img in os.listdir(paths):
    # belém = [743:1718,979:1982,:]
    # Chapadão1: [1190:1546,1632:1950,:]
    # chapadão2: [1290:1500,1632:1950,:]
    img_array = cv2.imread(os.path.join(paths,img))[1190:1546,1632:1950,:]
    training_data.append([img_array,class_num])

random.shuffle(training_data)

# %%
x = []
y = []
for fig, classe in training_data:
  x.append(fig)
  y.append(classe)
    
# belem = (-1,190,350,3)
# chapadao1 = (-1,356, 318,3)
x = np.array(x).reshape(-1,356,318,3)

# %%
import pickle
pickle_out = open('D:\machine_learning\image_classification\chapadao\X_chapadao.pickle','wb')
pickle.dump(x,pickle_out)
pickle_out.close()
pickle_out = open('D:\machine_learning\image_classification\chapadao\Y_chapadao.pickle','wb')
pickle.dump(y,pickle_out)
pickle_out.close()

# %%



