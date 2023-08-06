# -*- coding:utf-8 -*-
"""
Author:Jy
2020/11/12 12:32:00
shanghai
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'\\common')
import ast
import time
import grpc
import common_pb2_grpc
import common_pb2
import re
import numpy as np

class JyInterface(object):
    period = '10s'
    def __init__(self, **kwargs):
        """定义参数"""
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.grpcConfig(self.grpcAddress)
        
    def grpcConfig(self, grpcAddress:str="18.136.163.117:9309"):
        self.channel = grpc.insecure_channel(grpcAddress)
        self.stub = common_pb2_grpc.CommonServiceStub(self.channel)
    
    def sleep(self, n):
        time.sleep(n)
    
    def logPrint(self, *args):
        try:
            print(*args)
            msg = ''
            for v in args:
                msg = msg + str(v)
            self.stub.addTradeLog(common_pb2.LogRequest(transferId=self.transferId,
                                                        msg=msg))
        except:
            pass
 
    def stopStrategy(self):
        try:
            output = self.stub.stopStrategy(common_pb2.StopRequest(transferId=self.transferId)) 
            if output.message == 'false':
                sys.exit(0)
            return output.message
        except:
            self.logPrint('------stopStrategy------')
            sys.exit(0)
 
    
    def getCapital(self, symbol:str, choice:int=0):
        if self.futureOrSpot == 1:
            response = self.stub.getCapital(common_pb2.CapitalRequest(type=self.type_,
                                                                 appKey=self.appKey,
                                                                 secret=self.secret,
                                                                 passphrase=self.passphrase,
                                                                 futureOrSpot=self.futureOrSpot,
                                                                 symbols=symbol))   
        else:
            symstr = symbol.split('/', 1)[choice]
            response = self.stub.getCapital(common_pb2.CapitalRequest(type=self.type_,
                                                                 appKey=self.appKey,
                                                                 secret=self.secret,
                                                                 passphrase=self.passphrase,
                                                                 futureOrSpot=self.futureOrSpot,
                                                                 symbols=symstr))              
        
        return ast.literal_eval(response.message.replace('null','"null"'))
    
    def getKline(self, symbol, klinePeriod, size):
        pType = "" # fixed return all 
        response = self.stub.getKline(common_pb2.KlineRequest(type=self.type_,
                                                              symbols=symbol,
                                                              futureOrSpot=self.futureOrSpot,
                                                              cols=pType,
                                                              klinePeriod=klinePeriod,
                                                              size=size))
        response = ast.literal_eval(response.message)
        response['closes'] = np.array(response['closes'], dtype = float)
        response['highs'] = np.array(response['highs'], dtype = float)
        response['lows'] = np.array(response['lows'], dtype = float)
        response['opens'] = np.array(response['opens'], dtype = float)
        response['amounts'] = np.array(response['amounts'], dtype = float)
        response['timeStr'] = np.array(response['timeStr'])
        response['time'] = np.array(response['time'])
        return response
    
    def getDepth(self, symbol):
        response = self.stub.getDepth(common_pb2.DepthRequest(type=self.type_,
                                                              symbols=symbol,
                                                              futureOrSpot=self.futureOrSpot))
        return ast.literal_eval(response.message.replace('null','"null"'))
    
    def getJumpPrice(self, symbol):
        response = self.stub.getJumpPrice(common_pb2.JumpPriceRequest(type=self.type_,
                                                                      symbols=symbol,
                                                                      futureOrSpot=self.futureOrSpot))
        temp = response.message
        return float(temp)
    
    def buy(self, symbol, price, amount):
        if self.futureOrSpot  == 0:
            orderId = self.spotOrder(symbol, 0, price, amount)
        else:
            orderId = self.futureOrder(symbol, 1, price, amount) # 期货则买入做多当现货
        return orderId
    
    def sell(self, symbol, price, amount):
        if self.futureOrSpot  == 0:
            orderId = self.spotOrder(symbol, 1, price, amount)
        else:
            orderId = self.futureOrder(symbol, 3, price, amount) # 期货则卖出平空当现货
        return orderId
    
    def short(self, symbol, price, amount):
        orderId = self.futureOrder(symbol, 2, price, amount)
        return orderId
    
    def cover(self, symbol, price, amount):
        orderId = self.futureOrder(symbol, 4, price, amount)
        return orderId
    
    def spotOrder(self, symbol, buyOrSell, price, amount):
        response = self.stub.spotOrder(common_pb2.SpotOrderRequest(type=self.type_,
                                                                   symbols=symbol, 
                                                                   buyOrSell=buyOrSell,
                                                                   price=str(price), 
                                                                   amount=str(amount),
                                                                   appKey=self.appKey,
                                                                   secret=self.secret,
                                                                   passphrase=self.passphrase,
                                                                   transferId=self.transferId))
        return response.message
    
    def futureOrder(self, symbol, directOffset, price, amount):
        response = self.stub.futureOrder(common_pb2.FuturesOrderRequest(type=self.type_,
                                                                       symbols=symbol,
                                                                       price=str(price),
                                                                       amount=str(amount),
                                                                       appKey=self.appKey,
                                                                       secret=self.secret,
                                                                       passphrase=self.passphrase,
                                                                       directOffset=directOffset,
                                                                       transferId=self.transferId,
                                                                       futureOrSpot=self.futureOrSpot))
        return response.message
    
    def cancelOrder(self, symbol, orderId):
        response = self.stub.cancelOrder(common_pb2.CancelOrderRequest(type=self.type_,
                                                                       symbols=symbol,
                                                                       orderId=orderId,
                                                                       appKey=self.appKey,
                                                                       secret=self.secret,
                                                                       passphrase=self.passphrase,
                                                                       futureOrSpot=self.futureOrSpot))
        return response.message
    
    def getOrderInfoState(self, symbol, orderId):
        response = self.stub.getOrderInfoState(common_pb2.OrderInfoStateRequest (type=self.type_,
                                                                            symbols=symbol,
                                                                            orderId=str(orderId),
                                                                            appKey=self.appKey,
                                                                            secret=self.secret,
                                                                            passphrase=self.passphrase,
                                                                            futureOrSpot=self.futureOrSpot))
        return int(response.message)
    
    def getPosition(self, symbol:str, x:str='buy'):
        if self.futureOrSpot == 0:
            symstr = symbol.split('/', 1)
            response = self.stub.getPosition(common_pb2.BalanceRequest(type=self.type_,
                                                                 appKey=self.appKey,
                                                                 secret=self.secret,
                                                                 passphrase=self.passphrase,
                                                                 futureOrSpot=self.futureOrSpot,
                                                                 mark=symstr[0]))
            output = eval(response.message)
            return output[0]
        else:
            response = self.stub.getPosition(common_pb2.BalanceRequest(type=self.type_,
                                                                         appKey=self.appKey,
                                                                         secret=self.secret,
                                                                         passphrase=self.passphrase,
                                                                         futureOrSpot=self.futureOrSpot,
                                                                         mark=symbol))
            output = eval(response.message)
            if x == 'buy':
                return output[1]
            elif x == 'short': 
                return output[2]
            elif x == 'Margin':
                return output[0]
     
    def getMargin(self, symbol:str):
        response = self.stub.getPosition(common_pb2.BalanceRequest(type=self.type_,
                                                                appKey=self.appKey,
                                                                secret=self.secret,
                                                                passphrase=self.passphrase,
                                                                futureOrSpot=self.futureOrSpot,
                                                                mark=symbol))
        output = eval(response.message)
        return output[0]
     
    def getSecondary(self, symbol:str):
        symstr = symbol.split('/', 1)
        response = self.stub.getPosition(common_pb2.BalanceRequest(type=self.type_,
                                                            appKey=self.appKey,
                                                            secret=self.secret,
                                                            passphrase=self.passphrase,
                                                            futureOrSpot=self.futureOrSpot,
                                                            mark=symstr[1])) 
        output = eval(response.message)
        return output[0]
    
    def getUsdt(self):
        response = self.stub.getPosition(common_pb2.BalanceRequest(type=self.type_,
                                                            appKey=self.appKey,
                                                            secret=self.secret,
                                                            passphrase=self.passphrase,
                                                            futureOrSpot=self.futureOrSpot,
                                                            mark="USDT")) 
        output = eval(response.message)
        return output[0]
    
    def getLastPrice(self, symbol):
        response = self.stub.getLastPrice(common_pb2.LastPriceRequest(type=self.type_, 
                                                                      symbols=symbol, 
                                                                      futureOrSpot=self.futureOrSpot))
        return float(response.message)
    
    def getPositionSt(self, symbol:str, x:str='buy'):
        response = self.stub.getPositionByTransferId(common_pb2.TransferPositionRequest(type=self.type_, 
                                                                                       symbols=symbol, 
                                                                                       futureOrSpot=self.futureOrSpot,
                                                                                       transferId=self.transferId))
        output = eval(response.message)
        if self.futureOrSpot == 0:
            return output[0]
        elif self.futureOrSpot == 1:
            if x == 'buy':
                return output[1]
            elif x == 'short':
                return output[2]
    
    def transfer(self, symbol, amount, transferType:int=2, direction:int=1):
        response = self.stub.transfer(common_pb2.TransferRequest(type=self.type_, 
                                                                 transferType=transferType,  # 1:币币-交割; 2:币币-永续(币本位); 3-币币-永续(USDT本位)
                                                                 appKey=self.appKey,
                                                                 secret=self.secret,
                                                                 passphrase=self.passphrase,
                                                                 symbols=symbol, 
                                                                 direction=direction,
                                                                 amount=str(amount)))
        if response.message == "true":
            output = 0
        else:
            output = 1
        return output # 是否成功; 0:成功,1:失败

    def run_(self):
        """let subclass inherit"""
        try:
            tmnum = int(re.sub("\D", "", self.period))   
            tmstr = re.sub("[0-9]", "", self.period)
            tm = time.localtime(time.time())
            if tmstr[0] == 's' and tm.tm_sec % tmnum != 0:
                return
            elif tmstr[0] == 'h' and (tm.tm_hour % tmnum != 0 or tm.tm_min != 0 or tm.tm_sec != 0):
                return
            elif tmstr[0] == 'm' and (tm.tm_min % tmnum != 0 or tm.tm_sec != 0):
                return
            elif tmstr[0] == 'd' and (tm.tm_hour != 0 or tm.tm_min != 0 or tm.tm_sec != 0):
                return            
            self.loop()
        except Exception:
            if Exception == 'SystemExit':
                sys.exit(0)
            else:
                pass
    
    def run2_(self, *args):
        """let subclass inherit"""
        try:         
            self.loop2(*args)
        except Exception:
            if Exception == 'SystemExit':
                sys.exit(0)
            else:
                pass

    def run(self, func):
        while True:
            time.sleep(1)
            try:
                tmnum = int(re.sub("\D", "", self.period))   
                tmstr = re.sub("[0-9]", "", self.period)
                tm = time.localtime(time.time())
                if tmstr[0] == 's' and tm.tm_sec % tmnum != 0:
                    continue
                elif tmstr[0] == 'h' and (tm.tm_hour % tmnum != 0 or tm.tm_min != 0 or tm.tm_sec != 0):
                    continue
                elif tmstr[0] == 'm' and (tm.tm_min % tmnum != 0 or tm.tm_sec != 0):
                    continue
                elif tmstr[0] == 'd' and (tm.tm_hour != 0 or tm.tm_min != 0 or tm.tm_sec != 0):
                    continue
                func()
            except Exception:
                if Exception == 'SystemExit':
                    sys.exit(0)
                else:
                    pass                
            