# By Traders, For Traders.

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-2.1.5-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.7-blue.svg" />
    <img src ="https://img.shields.io/github/workflow/status/vnpy/vnpy/Python%20application/master"/>
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

vn.py is a Python-based open source quantitative trading system development framework. It was officially released in January 2015. It has been continuously contributing to the open source community for 6 years. The next step is to grow into a full-featured quantitative trading platform. Current users include financial institutions in China and abroad -- the software is used by more than 600 companies, including: private equity funds, proprietary securities and asset management, futures asset management and subsidiaries, university research institutions, proprietary trading companies, exchanges, Token Fund, etc.

The new series of online courses "vn.py advanced combat" has been launched on the official WeChat account [ vnpy-community ], covering CTA strategy (completed), option volatility trading (updated), etc. To purchase, please scan the QR code below to follow, and then click the [Advanced Course] button in the menu bar:

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy_qr.jpg"/>
</p>

If you have any questions in the process of using vn.py for secondary development (strategies, modules, etc.), please check the vn.py [project documentation](https://www.vnpy.com/docs/cn/index.html) . If you can’t solve it, please go to the [Questions and Help](https://www.vnpy.com/forum/) section of the official community forum for help. [Experience Sharing] Share your experience in the section!

For vn.py financial institution users, a special [vn.py institutional user group] (QQ group number: 676499931) was created to share issues related to institutional applications, such as: inter-bank market access, asset management O32 System, distributed deployment, etc. Please note that this group is only open to users of financial institutions. When adding a group, please indicate: name-institution-department.


## Features

1. The full-featured quantitative trading platform (vnpy.trader) integrates multiple trading interfaces, and provides a simple and easy-to-use API for specific strategy algorithms and function development, which is used to quickly build the quantitative trading applications needed by traders.

2. Trading interface (vnpy.gateway) covering all trading varieties at home and abroad:

    * Domestic market

        * CTP (ctp): domestic futures, options

        * CTP Mini (mini): domestic futures, options

        * CTP Securities (sopt): ETF options

        * Femas: Domestic futures

        * Hang Seng UFT (uft): domestic futures, ETF options

        * Feichuang Securities (sec): ETF options

        * Broad Rui (oes): Domestic securities (A shares)

        * Zhongtai XTP (xtp): domestic securities (A shares), ETF options

        * Hang Seng Options (hsoption): ETF options

        * Huaxin Singularity (tora): Domestic Securities (A shares)

        * Flying Mouse (sgit): Gold TD, domestic futures

        * Ksgold: Gold TD

        * Xin Guanjia (xgj): Futures Asset Management

        * Rohon: Futures Asset Management

        * Comstar: Inter-bank market

    * overseas market

        * Futu Securities (futu): Hong Kong stocks, US stocks

        * Tiger Securities (tiger): global securities, futures, options, foreign exchange, etc.

        * Interactive Brokers (ib): global securities, futures, options, foreign exchange, etc.

        * Yisheng 9.0 external disk (tap): global futures

        * Direct Futures (da): Global Futures

        * MetaTrader 5 (mt5): foreign exchange, CFD, futures, stocks

        * Alpaca (alpaca): US stocks (zero commission)

        * Kaisa Investment (kasia): Hong Kong stocks

    * Digital currency

        * BitMEX (bitmex): digital currency futures, options, perpetual contracts

        * Bybit (bybit): Digital currency perpetual contract

        * Binance: Digital currency spot

        * Binances: Digital currency perpetual contract

        * OKEX (okex): digital currency spot

        * OKEX Perpetual (okexs): Digital Currency Perpetual Contract

        * OKEX Futures (okexf): Digital Currency Futures

        * OKEX options (okexo): digital currency options

        * Huobi: Digital currency spot

        * Huobi Futures (huobif): Digital Currency Futures

        * Huobis: Digital currency is sustainable

        * Gate.io Perpetual (gateios): Digital Currency Perpetual Contract

        * Deribit (deribit), digital currency options, perpetual contracts

        * Bitfinex (bitfinex): digital currency spot

        * Coinbase (coinbase): digital currency spot

        * Bitstamp (bitstamp): digital currency spot

        * 1Token (onetoken): digital currency brokers (spot, futures)

    * Special application

        * RPC service (rpc): cross-process communication interface for distributed architecture

3. Various quantitative strategy trading applications out of the box (vnpy.app):

    * cta_strategy: The CTA strategy engine module, while maintaining ease of use, allows users to perform fine-grained control over the commissioned withdrawal behavior during the operation of CTA strategies (reducing transaction slippage and implementing high-frequency strategies)

    * cta_backtester: CTA strategy backtesting module, without using Jupyter Notebook, directly using the graphical interface to directly perform strategy backtesting analysis, parameter optimization and other related work

    * spread_trading: Spread trading module, supports custom spreads, real-time calculation of spreads and positions, supports semi-automatic spread algorithm trading and fully automatic spread strategy trading modes

    * option_master: Option trading module, designed for the domestic option market, supporting multiple option pricing models, implicit volatility surface calculation, Greek value risk tracking and other functions

    * portfolio_strategy: Portfolio strategy module, for quantitative strategies for simultaneous trading of multiple contracts (Alpha, option arbitrage, etc.), providing historical data back-testing and real-time automatic trading functions

    * algo_trading: Algorithmic trading module, providing a variety of commonly used intelligent trading algorithms: TWAP, Sniper, Iceberg, BestLimit, etc., supporting external intelligent algorithmic trading services (such as Kinner's algorithm)

    * script_trader: Script strategy module, designed for multi-standard combination trading strategies. At the same time, it can also directly implement REPL instruction trading in the command line, and does not support backtesting.

    * chart_wizard: K-line chart module, based on RQData data service (futures) or trading interface (digital currency) to obtain historical data, and combined with Tick push to display real-time market changes

    * portfolio_manager: Portfolio module, oriented to various fundamental trading strategies, based on independent strategy sub-accounts, providing automatic tracking of trading positions and real-time statistics of profit and loss

    * rpc_service: RPC service module, allowing a certain VN Trader process to be started as a server, as a unified market and transaction routing channel, allowing multiple clients to connect at the same time, realizing a multi-process distributed system

    * data_manager: historical data management module, view the existing data overview in the database through the tree directory, select any time period data to view the field details, support the data import and export of CSV files

    * data_recorder: market quotation recording module, configured based on the graphical interface, real-time recording of Tick or K-line quotations to the database according to requirements, for strategy backtesting or real disk initialization

    * excel_rtd: Excel RTD (Real Time Data) real-time data service, based on the pyxll module to achieve real-time push updates of various data (quotations, contracts, positions, etc.) obtained in Excel

    * risk_manager: Risk management module, which provides statistics and restrictions on rules including transaction flow control, number of orders placed, activity entrustment, total number of cancelled orders, etc., effectively realizing front-end risk control functions

4. Python transaction API interface package (vnpy.api), which provides the underlying docking implementation of the above transaction interface.

5. Simple and easy-to-use event-driven engine (vnpy.event), as the core of event-driven trading programs.

6. Cross-process communication standard component (vnpy.rpc), used to implement distributed deployment of complex trading systems.

7. Python high-performance K-line chart (vnpy.chart), supports large data volume chart display and real-time data update function.

8. [Community forums](http://www.vnpy.com) and [Zhihu columns]((http://zhuanlan.zhihu.com/vn-py)), including the development tutorial of the vn.py project and the application research of Python in the field of quantitative trading.

9. The official exchange group 262656087 (QQ) is strictly managed (regularly remove long-term diving members), and the group admission fee will be donated to the vn.py community fund.

## Environmental preparation

* It is recommended to use the Python release version VNStudio-2.1.5 specially created by the vn.py team for quantitative trading , which has the latest version of the vn.py framework and the VN Station quantitative management platform built-in, without manual installation
* Supported system version: Windows 7 or higher/Windows Server 2008 or higher/Ubuntu 18.04 LTS
* Supported Python version: Python 3.7 64-bit ( note that it must be Python 3.7 64-bit version )

## installation steps

In [this](https://github.com/vnpy/vnpy/releases) latest version, after decompression run the following command to install:

**Windows**

    install.bat

**Ubuntu**

    bash install.sh

## user's guidance

1. Register a CTP simulation account at [SimNow](http://www.simnow.com.cn/), and get the broker code and transaction server address on [this page](http://www.simnow.com.cn/product.action).

2. Register in the [vn.py community forum](https://www.vnpy.com/forum/) to get the VN Station account password (the forum account password is that)

3. Start VN Station (after installing VN Studio, a shortcut will be automatically created on the desktop), enter the account password from the previous step to log in

4. Click the **VN Trader Lite** button at the bottom to start your trading!!!

note:

* Do not close VN Station during the operation of VN Trader (it will automatically exit)
* For flexible configuration of quantitative trading application components, please use **VN Trader Pro**

## Script run

In addition to the graphical startup method based on VN Station, you can also create run.py in any directory and write the following sample code:


```Python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp
from vnpy.gateway.ctp import CtpGateway
from vnpy.app.cta_strategy import CtaStrategyApp
from vnpy.app.cta_backtester import CtaBacktesterApp

def main():
    """Start VN Trader"""
    qapp = create_qapp()

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)

    main_engine.add_gateway(CtpGateway)
    main_engine.add_app(CtaStrategyApp)
    main_engine.add_app(CtaBacktesterApp)

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()

if __name__ == "__main__":
    main()
```

Open CMD in this directory (hold Shift->click the right mouse button->open command window/PowerShell here) and run the following command to start VN Trader:

    python run.py

## Contribute code

vn.py uses Github to host its source code. If you want to contribute code, please use the github PR (Pull Request) process:

1. [Create Issue](https://github.com/vnpy/vnpy/issues/new) -For larger changes (such as new features, large refactorings, etc.), it is best to open an issue to discuss it first, and for smaller improvements (such as document improvements, bugfixes, etc.) directly send PR

2. Fork [vn.py](https://github.com/vnpy/vnpy) -Click the Fork button in the upper right corner

3. Clone your own fork: ```git clone https://github.com/$userid/vnpy.git```
    * If your fork is out of date, you need to sync manually: [synchronization method](https://help.github.com/articles/syncing-a-fork/)

4. Create your own feature branch from dev: ```git checkout -b $my_feature_branch dev```

5. Modify on $my_feature_branch and push the modification to your fork

6. 创建从你的fork的$my_feature_branch分支到主项目的**dev**分支的[Pull Request] -  [在此](https://github.com/vnpy/vnpy/compare?expand=1)点击**compare across forks**，选择需要的fork和branch创建PR

7. 等待review, 需要继续改进，或者被Merge!

在提交代码的时候，请遵守以下规则，以提高代码质量：

  * 使用[autopep8](https://github.com/hhatto/autopep8)格式化你的代码。运行```autopep8 --in-place --recursive . ```即可。
  * 使用[flake8](https://pypi.org/project/flake8/)检查你的代码，确保没有error和warning。在项目根目录下运行```flake8```即可。



## 项目捐赠

过去6年中收到过许多社区用户的捐赠，在此深表感谢！所有的捐赠资金都投入到了vn.py社区基金中，用于支持vn.py项目的运作。

先强调一下：**vn.py是开源项目，可以永久免费使用，并没有强制捐赠的要求！！！**

捐赠方式：支付宝3216630132@qq.com（*晓优）

长期维护捐赠清单，请在留言中注明是项目捐赠以及捐赠人的名字。

## 其他内容

* [获取帮助](https://github.com/vnpy/vnpy/blob/dev/.github/SUPPORT.md)
* [社区行为准侧](https://github.com/vnpy/vnpy/blob/dev/.github/CODE_OF_CONDUCT.md)
* [Issue模板](https://github.com/vnpy/vnpy/blob/dev/.github/ISSUE_TEMPLATE.md)
* [PR模板](https://github.com/vnpy/vnpy/blob/dev/.github/PULL_REQUEST_TEMPLATE.md)

## License

MIT
