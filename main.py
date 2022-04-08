# *************************************************************************
#    > Author: Feng Bohan
#    > Mail: 1953356163@qq.com
#    > DateTime: 2022/4/8 19:53
# ************************************************************************/

"""
文件说明：main.py
"""
from email.policy import default
from enum import IntEnum
import json
from os import stat
from pathlib import Path
import logging
import time
import datetime
class App:
    def __init__(self) -> None:
        self.currentDir = Path.cwd()
        self.dataFileName = 'data.json'
        self.data = {}
        self.load_data(self.dataFileName)
        self.itemType = {'default':0, 'study':1, 'game':2}
        pass
    def load_data(self,name="data.json") -> None:
        """
            初始化载入 json 文件 
        """
        myPath = self.currentDir / name
        try:
            with open(str(myPath),"r") as f1:
                try:
                    self.data = json.load(f1)
                    logging.info("Load data from {}".format(str(myPath)))
                except:
                    logging.warning("Can't decode json data")
        except FileNotFoundError:
            logging.warning("{} is not exist, try to creat file;".format(str(myPath)))
            with open(str(myPath),"w") as f1:
                logging.info("Create file {}".format(str(myPath)))
    def add_item(self, itemName, itemType, startTime, endTime, times):
        """  
            增加 时间记录
        """
        currentDay = time.strftime("%Y-%m-%d", time.localtime())
        logging.debug('Current day is {}'.format(currentDay))
        if currentDay in self.data:
            index = len(self.data[currentDay])
        else:
            self.data[currentDay] = []
            index = 0
        try:
            self.data[currentDay].append({'name':itemName, 'type':itemType, 'startTime':startTime, 'endTime':endTime, 'times':times})
            logging.info('Add the {} item {}'.format(index, itemName))
        except:
            logging.error("Can't add item;") 

    def del_item(self, current_day, index=0):
        """  
            删除 时间记录
        """   
        if current_day is None:
            current_day=time.strftime("%Y-%m-%d", time.localtime())
            logging.info('Use the current day as the day index')
        
        if current_day in self.data:
            if index in self.data[current_day]:
                del self.data[current_day][index]
                logging.info('del the key: {}-{}'.format(current_day,index))
            else:
                logging.warning('The index is not valible')
        else:
            logging.warning('The day is not valible')
    
    def save_data(self):
        with open(self.dataFileName, 'w') as f1:
            try:
                data = json.dumps(self.data, indent=1)
                f1.write(data)
                logging.info('Save data')
            except:
                logging.error("Can't save data")
    
    def itemStart(self):
        itemName = input('请输入待办事项名称：')
        while True:
            index = input('请选择待办事项类型：\n\t0:default\t1:study\t2:game\n')
            if index == '0':
                itemType = self.itemType['default']
                break
            elif index == '1':
                itemType = self.itemType['study']
                break
            elif index == '2':
                itemType = self.itemType['game']
                break
            else:
                print('输入错误，请重新输入')

        startTime = datetime.datetime.now()
        while True:
            state = input('输入q结束计时:\t')
            if state == 'q':
                endTime = datetime.datetime.now()
                times = (endTime - startTime).total_seconds()/60
                break
        
        self.add_item(itemName=itemName, itemType=itemType, startTime=startTime.ctime(), endTime=endTime.ctime(), times=times)


if __name__ == '__main__':
    # config logging
    LOG_FORMAT = "%(asctime)s - %(levelname)s -  %(filename)s - %(funcName)s - %(lineno)d - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)
    
    # call main
    a = App()
    a.itemStart()
    a.save_data()
