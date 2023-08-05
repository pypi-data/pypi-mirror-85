Encapsulated interface：

1）getKline(symbol, klinePeriod, size) ->dict

2）getDepth(symbol) -> dict
   
3）getJumpPrice(symbol) -> float
   
4）buy(symbol, price, amount) -> str // orderId 
     
5）sell(symbol, price, amount) -> str // orderId 

6）short(symbol, price, amount) -> str // orderId 

7）cover(symbol, price, amount) -> str // orderId 
 
8）cancelOrder(symbol, orderId) -> str // true:撤销成功 false:失败
  
9）getOrderInfoState(symbol, orderId) -> str // -2:"其他",-1:"不存在",0:"全部成交" 1: "部分成交",2:"未成交" 3:"撤销中" 4:"已撤销" 5:"部分成交撤销"
                                                                               6:"拒绝请求" 7:"过期" 8:"失败" 9:"下单中

10）getPosition(symbol) -> float
 
11）getUsdt() -> float

12）getLastPrice(symbol) -> float
 
13）getPositionSt(symbol) -> float
 
PS：交易所类型 1：huobi 2:binance 3:okex
 