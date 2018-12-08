#coding=utf-8

import tushare as ts
import pandas as pd
import numpy as np
import os
import random
import time
import datetime


#
cwd=""
StockListPath=""
DataSavePathA=""
TodayDataPath=""

CurHour=1
CurMinute=2
SecretData_A=[]
#
def mkdir(path):
    # 引入模块
    import os
 
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
 
        print(path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')
        return False

def PathInit():
    '''
    初始化路径
    '''
    global cwd
    global StockListPath
    global DataSavePathA
    global TodayDataPath
    
    #文件夹路径初始化

    #获取当前目录
    cwd = os.getcwd()
    #定义初始化股票列表目录
    StockListPath=cwd+'\\StockList'
    #定义A数据输出目录
    DataSavePathA=cwd+'\\DataA'

    #文件名初始化
    TodayDataPath=StockListPath+'\\today_all_data.csv'

def PathCreate():
    '''
    根据初始化路径新建文件夹
    '''
    global cwd
    global StockListPath
    global DataSavePathA
  
    mkdir(StockListPath)
    mkdir(DataSavePathA)

def CurDatalistCreate(path):
    """
    初始化当前更新列表   
    
    """

    #TODO 加个错误处理
    buff_dr_result=ts.get_today_all()

    buff_dr_result.to_csv(path)

def SecretDataAInit():
    '''
    初始化数据A  

    '''
    global SecretData_A

    #code,otherinfo + time(minute),(time+b1p1~s5p5)
    SecretData_A=np.zeros((4000,270,21),dtype=float)

    #读取列表
    buff_dr_result=pd.read_csv(TodayDataPath,encoding= 'gbk')

    for z in range(len(buff_dr_result['code'])):
        try:
            
            SecretData_A[(z,0,0)]=buff_dr_result['code'][z]
            #index初始化
            SecretData_A[(z,0,1)]=1


        except Exception as ex:
            sleeptime=random.randint(50,99)
            time.sleep(sleeptime/100)
            print (Exception,":",ex)

    '''
    for scode in SecretData_A[:,0,0]:
        print(scode)
    '''

    return buff_dr_result

def CSZL_SecretData_A_Update(tushare_result,date_max,update_index=1):
    """
    重要数据更新
    """

    global CurHour
    global CurMinute

    global SecretData_A
    
    for i in range(date_max):

        #获取当前数据更新位置
        CurIndex=int(SecretData_A[(update_index+i,0,1)])

        #超范围检测
        if CurIndex>269:
            continue

        try:

            #更新时间记录
            SecretData_A[(update_index+i,CurIndex,0)]=str(CurHour*100+CurMinute)

            #更新常时数据
            SecretData_A[(update_index+i,CurIndex,1)]=Z_AvailableJudge(tushare_result['b1_v'][i])
            SecretData_A[(update_index+i,CurIndex,2)]=Z_AvailableJudge(tushare_result['b1_p'][i])
            SecretData_A[(update_index+i,CurIndex,3)]=Z_AvailableJudge(tushare_result['b2_v'][i])
            SecretData_A[(update_index+i,CurIndex,4)]=Z_AvailableJudge(tushare_result['b2_p'][i])
            SecretData_A[(update_index+i,CurIndex,5)]=Z_AvailableJudge(tushare_result['b3_v'][i])
            SecretData_A[(update_index+i,CurIndex,6)]=Z_AvailableJudge(tushare_result['b3_p'][i])
            SecretData_A[(update_index+i,CurIndex,7)]=Z_AvailableJudge(tushare_result['b4_v'][i])
            SecretData_A[(update_index+i,CurIndex,8)]=Z_AvailableJudge(tushare_result['b4_p'][i])
            SecretData_A[(update_index+i,CurIndex,9)]=Z_AvailableJudge(tushare_result['b5_v'][i])
            SecretData_A[(update_index+i,CurIndex,10)]=Z_AvailableJudge(tushare_result['b5_p'][i])

            SecretData_A[(update_index+i,CurIndex,11)]=Z_AvailableJudge(tushare_result['a1_v'][i])
            SecretData_A[(update_index+i,CurIndex,12)]=Z_AvailableJudge(tushare_result['a1_p'][i])
            SecretData_A[(update_index+i,CurIndex,13)]=Z_AvailableJudge(tushare_result['a2_v'][i])
            SecretData_A[(update_index+i,CurIndex,14)]=Z_AvailableJudge(tushare_result['a2_p'][i])
            SecretData_A[(update_index+i,CurIndex,15)]=Z_AvailableJudge(tushare_result['a3_v'][i])
            SecretData_A[(update_index+i,CurIndex,16)]=Z_AvailableJudge(tushare_result['a3_p'][i])
            SecretData_A[(update_index+i,CurIndex,17)]=Z_AvailableJudge(tushare_result['a4_v'][i])
            SecretData_A[(update_index+i,CurIndex,18)]=Z_AvailableJudge(tushare_result['a4_p'][i])
            SecretData_A[(update_index+i,CurIndex,19)]=Z_AvailableJudge(tushare_result['a5_v'][i])
            SecretData_A[(update_index+i,CurIndex,20)]=Z_AvailableJudge(tushare_result['a5_p'][i])

            #更新数据位置
            SecretData_A[(update_index+i,0,1)]=SecretData_A[(update_index+i,0,1)]+1

        except Exception as ex:

            wrongEx=str(ex)


def Z_AvailableJudge(zzz):
    """
    数据可靠性检测
    """

    if(zzz==""):
        return (-1)

    return zzz

def CSZL_GETA_Main(update_rate=30):
    '''
    循环获取数据
    '''

    global TodayDataPath

    
    #无限循环
    while True:

        #休息时间
        while CSZL_StartCheck():
            print("长等待")
            time.sleep(600)

        g_exit_flag=True
        #初始化线程计数
        List_update_index=1
        #初始化更新频率
        update_cur=update_rate
        #程序运行状态 #1代表线程正常 -1代表线程异常 0代表等待
        INFO_all_routine=0

        #读取列表
        buff_dr_result=SecretDataAInit()
        #列表总长度
        list_max=np.alen(buff_dr_result)

        #当日更新循环
        while g_exit_flag:

            #当日收盘检查
            if(CSZL_ExitCheck()):
                #保存重要数据
                CSZL_SecretDataSave()
                g_exit_flag=False
            if (CSZL_TimeCheck()):
                try:
                    #初始化代码串
                    update_buff_arr=[]
                    for i in range(update_cur):                   
                        temp=str(buff_dr_result['code'][List_update_index+i]).zfill(6)
                        update_buff_arr.append(temp)

                    #使用tushare接收数据
                    buff_result = ts.get_realtime_quotes(update_buff_arr)
                    #更新数据
                    CSZL_SecretData_A_Update(buff_result,update_cur,List_update_index)


                    #数据指针更新
                    List_update_index+=update_cur

                    #如果下次更新量将要超过总数
                    if (List_update_index+update_cur)>=list_max:
                        update_cur=list_max-List_update_index
                        #如果现在已经是最后一个数据
                        if List_update_index==list_max:
                            #index回到1，这里可以加入一些一次循环后的事件
                            List_update_index=1
                            update_cur=update_rate
                            

                    INFO_all_routine=1
                    print("正常运行")
                except Exception as ex:
                    INFO_all_routine=-1                
                    wrongmessage="Allroutine FAIL at : %s \n" % ( time.ctime(time.time()))
                    print("错误")

            else:
                INFO_all_routine=0
                print("短等待")

            print(List_update_index)
            sleeptime=random.randint(50,99)
            time.sleep(sleeptime/200)



         

def CSZL_SecretDataSave():
    """
    保存A数据
    """
    global SecretData_A
    global DataSavePathA
   

    now=datetime.datetime.now()
    now=now.strftime('%Y%m%d')

    txtFileA = DataSavePathA + '\\secretA'+now+'.npy'

    np.save(txtFileA, SecretData_A)

    fefe=2


def SecdateCheck(Data_A):

    for ii in range(Data_A.shape[0]):
        print(Data_A[ii,0,0], end='')           
        print(Data_A[ii,1,0], end='')
        print(Data_A[ii,1,1], end='')
        print(Data_A[ii,1,2], end='')
        print(Data_A[ii,2,3], end='')
        print(Data_A[ii,2,4], end='')
        print(Data_A[ii,2,5], end='')
        print(Data_A[ii,3,6], end='')
        print(Data_A[ii,3,7], end='')
        print(Data_A[ii,3,8])
        

#输入要显示的文字，返回输入的数字
def CMDInput(Info):

    return 0
    getinput=0
    getinput2=input(Info+"\n")
    if getinput2!="":
        getinput=int(getinput2)

    return getinput

def CSZL_TimeCheck():
    global CurHour
    global CurMinute



    CurHour=int(time.strftime("%H", time.localtime()))
    CurMinute=int(time.strftime("%M", time.localtime()))

    caltemp=CurHour*100+CurMinute


    if (caltemp>=915 and caltemp<=1132) or (caltemp>=1300 and caltemp<=1503) or CSZLsuper.G_mode['RoutineTestFlag']:
        return True
    else:
        return False  
def CSZL_ExitCheck():
    global CurHour
    global CurMinute


    CurHour=int(time.strftime("%H", time.localtime()))
    CurMinute=int(time.strftime("%M", time.localtime()))

    caltemp=CurHour*100+CurMinute


    if (caltemp>=1507 and caltemp<=1510):
        return True
    else:
        return False   
def CSZL_StartCheck():
    global CurHour
    global CurMinute


    CurHour=int(time.strftime("%H", time.localtime()))
    CurMinute=int(time.strftime("%M", time.localtime()))

    caltemp=CurHour*100+CurMinute


    if (caltemp>=830 and caltemp<=850):
        return False
    else:
        return True

if __name__ == '__main__':

    #初始化路径和新建路径文件夹
    PathInit()
    PathCreate()


    
    if(CMDInput("是否重新更新列表:输入1表示更新 回车取消")==1):
        #调用tushare接口初始化数据源
        CurDatalistCreate(TodayDataPath)
    
    '''
    now=datetime.datetime.now()
    now=now.strftime('%Y%m%d')
    txtFileA = DataSavePathA + '\\secretA'+now+'.npy'
    Data_A=np.load(txtFileA)
    SecdateCheck(Data_A)
    '''

    CSZL_GETA_Main(update_rate=30)

    a=1