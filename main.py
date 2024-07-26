import json,math
import os,sys

from pathlib import Path

import numpy as np
import cvxpy as cp

class ConfigNotFoundError(FileNotFoundError):
    pass

def generateConfig(filedir:str=None)->bool:
    pass

if __name__=='__main__':
    try:
        with open('config.json','r',encoding='utf-8') as config_file:
            config=json.load(config_file)
    except FileNotFoundError:
        generateConfig(os.path.join((Path(sys.argv[0])).parent,'config.json'))
        raise ConfigNotFoundError("未找到配置文件,已自动生成，请重新运行")
    
    characters=config['角色']
    characterList=[]
    resourceList=[]
    unlockList=[]
    totalList=np.zeros(7)
    
    for character in characters:
        for armor in characters[character]:
            characterList.append([character,armor])
            resourceList.append(characters[character][armor]['资源'])
            unlockList.append(characters[character][armor]['解锁'])
            totalList+=np.array(resourceList[-1])
    


    resource=config['资源']
    requireList=[]
    for type in resource:
        requireList.append(resource[type][0]-resource[type][1])
    
    n=len(characterList)
    
    c=np.ones(n) # Max z = \sigma (-1) * x
    a=np.transpose(np.array(resourceList))
    b=np.array(requireList)
    eq=~np.array(unlockList)
    x=cp.Variable(n,integer=True)

    objective=cp.Minimize(cp.sum(c*x*1/3))
    constriants=[0<=x,a*x>=b,eq*x==0]
    prob=cp.Problem(objective,constriants)
    results=prob.solve(solver=cp.CPLEX)

    print('总计出战次数：',math.ceil(prob.value))
    ans=x.value

    for (armor,times) in zip(characterList,ans):
        if times!=0:
            print(armor,int(times))