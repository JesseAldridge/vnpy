
class BacktestingEngine:
    """"""

    gateway_name = "BACKTESTING"

    def __init__(self):
        """"""
        self.vt_symbols: List[str] = []
        self.start: datetime = None
        self.end: datetime = None

        self.rates: Dict[str, float] = 0
        self.slippages: Dict[str, float] = 0
        self.sizes: Dict[str, float] = 1
        self.priceticks: Dict[str, float] = 0

        self.capital: float = 1_000_000

        self.strategy: StrategyTemplate = None
        self.bars: Dict[str, BarData] = {}
        self.datetime: datetime = None

        self.interval: Interval = None
        self.days: int = 0
        self.history_data: Dict[Tuple, BarData] = {}
        self.dts: Set[datetime] = set()

        self.limit_order_count = 0
        self.limit_orders = {}
        self.active_limit_orders = {}

        self.trade_count = 0
        self.trades = {}

        self.logs = []

        self.daily_results = {}
        self.daily_df = None

    def clear_data(self) -> None:
        """
        Clear all data of last backtesting.
        """
        self.strategy = None
        self.bars = {}
        self.datetime = None

        self.limit_order_count = 0
        self.limit_orders.clear()
        self.active_limit_orders.clear()

        self.trade_count = 0
        self.trades.clear()

        self.logs.clear()
        self.daily_results.clear()
        self.daily_df = None

    def set_parameters(
        self,
        vt_symbols: List[str],
        interval: Interval,
        start: datetime,
        rates: Dict[str, float],
        slippages: Dict[str, float],
        sizes: Dict[str, float],
        priceticks: Dict[str, float],
        capital: int = 0,
        end: datetime = None
    ) -> None:
        """"""
        self.vt_symbols = vt_symbols
        self.interval = interval

        self.rates = rates
        self.slippages = slippages
        self.sizes = sizes
        self.priceticks = priceticks

        self.start = start
        self.end = end
        self.capital = capital

    def add_strategy(self, strategy_class: type, setting: dict) -> None:
        """"""
        self.strategy = strategy_class(
            self, strategy_class.__name__, copy(self.vt_symbols), setting
        )

    def load_data(self) -> None:
        """"""
        self.output("Start loading historical data")

        if not self.end:
            self.end = datetime.now()

        if self.start >= self.end:
            self.output("The start date must be less than the end date")
            return

        # Clear previously loaded history data
        self.history_data.clear()
        self.dts.clear()

        # Load 30 days of data each time and allow for progress update
        progress_delta = timedelta(days=30)
        total_delta = self.end - self.start
        interval_delta = INTERVAL_DELTA_MAP[self.interval]

        for vt_symbol in self.vt_symbols:
            start = self.start
            end = self.start + progress_delta
            progress = 0

            data_count = 0
            while start < self.end:
                end = min(end, self.end)  # Make sure end time stays within set range

                data = load_bar_data(
                    vt_symbol,
                    self.interval,
                    start,
                    end
                )

                for bar in data:
                    self.dts.add(bar.datetime)
                    self.history_data[(bar.datetime, vt_symbol)] = bar
                    data_count += 1

                progress += progress_delta / total_delta
                progress = min(progress, 1)
                progress_bar = "#" * int(progress * 10)
                self.output(f"{vt_symbol}Loading progress: {progress_bar} [{progress:.0%}]")

                start = end + interval_delta
                end += (progress_delta + interval_delta)

            self.output(f"{vt_symbol}Historical data loading is complete, data volume: {data_count}")

        self.output("All historical data loaded")

    def run_backtesting(self) -> None:
        """"""
        self.strategy.on_init()

        # Generate sorted datetime list
        dts = list(self.dts)
        dts.sort()

        # Use the first [days] of history data for initializing strategy
        day_count = 0
        ix = 0

        for ix, dt in enumerate(dts):
            if self.datetime and dt.day != self.datetime.day:
                day_count += 1
                if day_count >= self.days:
                    break

            try:
                self.new_bars(dt)
            except Exception:
                self.output("Exception caught; backtest terminated")
                self.output(traceback.format_exc())
                return

        self.strategy.inited = True
        self.output("Strategy initialization completed")

        self.strategy.on_start()
        self.strategy.trading = True
        self.output("Start playback of historical data")

        # Use the rest of history data for running backtesting
        for dt in dts[ix:]:
            try:
                self.new_bars(dt)
            except Exception:
                self.output("Exception caught; backtest terminated")
                self.output(traceback.format_exc())
                return

        self.output("End of historical data playback")

    def calculate_result(self) -> None:
        """"""
        self.output("Start calculating mark-to-market profit and loss")

        if not self.trades:
            self.output("The transaction record is empty and cannot be calculated")
            return

        # Add trade data into daily reuslt.
        for trade in self.trades.values():
            d = trade.datetime.date()
            daily_result = self.daily_results[d]
            daily_result.add_trade(trade)

        # Calculate daily result by iteration.
        pre_closes = {}
        start_poses = {}

        for daily_result in self.daily_results.values():
            daily_result.calculate_pnl(
                pre_closes,
                start_poses,
                self.sizes,
                self.rates,
                self.slippages,
            )

            pre_closes = daily_result.close_prices
            start_poses = daily_result.end_poses

        # Generate dataframe
        results = defaultdict(list)

        for daily_result in self.daily_results.values():
            fields = [
                "date", "trade_count", "turnover",
                "commission", "slippage", "trading_pnl",
                "holding_pnl", "total_pnl", "net_pnl"
            ]
            for key in fields:
                value = getattr(daily_result, key)
                results[key].append(value)

        self.daily_df = DataFrame.from_dict(results).set_index("date")

        self.output("Mark-to-market profit and loss calculation completed")
        return self.daily_df

    def calculate_statistics(self, df: DataFrame = None, output=True) -> None:
        """"""
        self.output("Start calculating strategy statistics")

        # Check DataFrame input exterior
        if df is None:
            df = self.daily_df

        # Check for init DataFrame
        if df is None:
            # Set all statistics to 0 if no trade.
            start_date = ""
            end_date = ""
            total_days = 0
            profit_days = 0
            loss_days = 0
            end_balance = 0
            max_drawdown = 0
            max_ddpercent = 0
            max_drawdown_duration = 0
            total_net_pnl = 0
            daily_net_pnl = 0
            total_commission = 0
            daily_commission = 0
            total_slippage = 0
            daily_slippage = 0
            total_turnover = 0
            daily_turnover = 0
            total_trade_count = 0
            daily_trade_count = 0
            total_return = 0
            annual_return = 0
            daily_return = 0
            return_std = 0
            sharpe_ratio = 0
            return_drawdown_ratio = 0
        else:
            # Calculate balance related time series data
            df["balance"] = df["net_pnl"].cumsum() + self.capital
            df["return"] = np.log(df["balance"] / df["balance"].shift(1)).fillna(0)
            df["highlevel"] = (
                df["balance"].rolling(
                    min_periods=1, window=len(df), center=False).max()
            )
            df["drawdown"] = df["balance"] - df["highlevel"]
            df["ddpercent"] = df["drawdown"] / df["highlevel"] * 100

            # Calculate statistics value
            start_date = df.index[0]
            end_date = df.index[-1]

            total_days = len(df)
            profit_days = len(df[df["net_pnl"] > 0])
            loss_days = len(df[df["net_pnl"] < 0])

            end_balance = df["balance"].iloc[-1]
            max_drawdown = df["drawdown"].min()
            max_ddpercent = df["ddpercent"].min()
            max_drawdown_end = df["drawdown"].idxmin()

            if isinstance(max_drawdown_end, date):
                max_drawdown_start = df["balance"][:max_drawdown_end].idxmax()
                max_drawdown_duration = (max_drawdown_end - max_drawdown_start).days
            else:
                max_drawdown_duration = 0

            total_net_pnl = df["net_pnl"].sum()
            daily_net_pnl = total_net_pnl / total_days

            total_commission = df["commission"].sum()
            daily_commission = total_commission / total_days

            total_slippage = df["slippage"].sum()
            daily_slippage = total_slippage / total_days

            total_turnover = df["turnover"].sum()
            daily_turnover = total_turnover / total_days

            total_trade_count = df["trade_count"].sum()
            daily_trade_count = total_trade_count / total_days

            total_return = (end_balance / self.capital - 1) * 100
            annual_return = total_return / total_days * 240
            daily_return = df["return"].mean() * 100
            return_std = df["return"].std() * 100

            pnl_std = df["net_pnl"].std()

            if return_std:
                # sharpe_ratio = daily_return / return_std * np.sqrt(240)
                sharpe_ratio = daily_net_pnl / pnl_std * np.sqrt(240)
            else:
                sharpe_ratio = 0

            return_drawdown_ratio = -total_net_pnl / max_drawdown

        # Output
        if output:
            self.output("-" * 30)
            self.output(f"First trading day: \t{start_date}")
            self.output(f"Last trading day: \t{end_date}")

            self.output(f"Total trading days: \t{total_days}")
            self.output(f"Profitable days: \t{profit_days}")
            self.output(f"Loss Days: \t{loss_days}")

            self.output(f"Starting capital: \t{self.capital:,.2f}")
            self.output(f"Ending capital: \t{end_balance:,.2f}")

            self.output(f"Total return: \t{total_return:,.2f}%")
            self.output(f"Annualized return: \t{annual_return:,.2f}%")
            self.output(f"Max drawdown: \t{max_drawdown:,.2f}")
            self.output(f"Max drawdown percent: {max_ddpercent:,.2f}%")
            self.output(f"Maximum drawdown days: \t{max_drawdown_duration}")

            self.output(f"Total profit and loss: \t{total_net_pnl:,.2f}")
            self.output(f"Total commissions: \t{total_commission:,.2f}")
            self.output(f"Total slippage: \t{total_slippage:,.2f}")
            self.output(f"Total turnover: \t{total_turnover:,.2f}")
            self.output(f"Total trade count: \t{total_trade_count}")

            self.output(f"Average daily profit and loss: \t{daily_net_pnl:,.2f}")
            self.output(f"Average daily commission: \t{daily_commission:,.2f}")
            self.output(f"Average daily slippage: \t{daily_slippage:,.2f}")
            self.output(f"Average daily turnover: \t{daily_turnover:,.2f}")
            self.output(f"Average daily trade count: \t{daily_trade_count}")

            self.output(f"Average daily rate of return: \t{daily_return:,.2f}%")
            self.output(f"Return standard deviation: \t{return_std:,.2f}%")
            self.output(f"Sharpe Ratio: \t{sharpe_ratio:,.2f}")
            self.output(f"Earnings drawdown ratio: \t{return_drawdown_ratio:,.2f}")

        statistics = {
            "start_date": start_date,
            "end_date": end_date,
            "total_days": total_days,
            "profit_days": profit_days,
            "loss_days": loss_days,
            "capital": self.capital,
            "end_balance": end_balance,
            "max_drawdown": max_drawdown,
            "max_ddpercent": max_ddpercent,
            "max_drawdown_duration": max_drawdown_duration,
            "total_net_pnl": total_net_pnl,
            "daily_net_pnl": daily_net_pnl,
            "total_commission": total_commission,
            "daily_commission": daily_commission,
            "total_slippage": total_slippage,
            "daily_slippage": daily_slippage,
            "total_turnover": total_turnover,
            "daily_turnover": daily_turnover,
            "total_trade_count": total_trade_count,
            "daily_trade_count": daily_trade_count,
            "total_return": total_return,
            "annual_return": annual_return,
            "daily_return": daily_return,
            "return_std": return_std,
            "sharpe_ratio": sharpe_ratio,
            "return_drawdown_ratio": return_drawdown_ratio,
        }

        # Filter potential error infinite value
        for key, value in statistics.items():
            if value in (np.inf, -np.inf):
                value = 0
            statistics[key] = np.nan_to_num(value)

        self.output("Completion of calculation of strategy statistics indicators")
        return statistics

    def show_chart(self, df: DataFrame = None) -> None:
        """"""
        # Check DataFrame input exterior
        if df is None:
            df = self.daily_df

        # Check for init DataFrame
        if df is None:
            return

        fig = make_subplots(
            rows=4,
            cols=1,
            subplot_titles=["Balance", "Drawdown", "Daily Pnl", "Pnl Distribution"],
            vertical_spacing=0.06
        )

        balance_line = go.Scatter(
            x=df.index,
            y=df["balance"],
            mode="lines",
            name="Balance"
        )
        drawdown_scatter = go.Scatter(
            x=df.index,
            y=df["drawdown"],
            fillcolor="red",
            fill='tozeroy',
            mode="lines",
            name="Drawdown"
        )
        pnl_bar = go.Bar(y=df["net_pnl"], name="Daily Pnl")
        pnl_histogram = go.Histogram(x=df["net_pnl"], nbinsx=100, name="Days")

        fig.add_trace(balance_line, row=1, col=1)
        fig.add_trace(drawdown_scatter, row=2, col=1)
        fig.add_trace(pnl_bar, row=3, col=1)
        fig.add_trace(pnl_histogram, row=4, col=1)

        fig.update_layout(height=1000, width=1000)
        fig.show()

    def update_daily_close(self, bars: Dict[str, BarData], dt: datetime) -> None:
        """"""
        d = dt.date()

        close_prices = {}
        for bar in bars.values():
            close_prices[bar.vt_symbol] = bar.close_price

        daily_result = self.daily_results.get(d, None)

        if daily_result:
            daily_result.update_close_prices(close_prices)
        else:
            self.daily_results[d] = PortfolioDailyResult(d, close_prices)

    def new_bars(self, dt: datetime) -> None:
        """"""
        self.datetime = dt

        # self.bars.clear()
        for vt_symbol in self.vt_symbols:
            bar = self.history_data.get((dt, vt_symbol), None)

            # If bar data of vt_symbol at dt exists
            if bar:
                self.bars[vt_symbol] = bar
            # Otherwise, use previous data to backfill
            elif vt_symbol in self.bars:
                old_bar = self.bars[vt_symbol]

                bar = BarData(
                    symbol=old_bar.symbol,
                    exchange=old_bar.exchange,
                    datetime=dt,
                    open_price=old_bar.close_price,
                    high_price=old_bar.close_price,
                    low_price=old_bar.close_price,
                    close_price=old_bar.close_price,
                    gateway_name=old_bar.gateway_name
                )
                self.bars[vt_symbol] = bar

        self.cross_limit_order()
        self.strategy.on_bars(self.bars)

        self.update_daily_close(self.bars, dt)

    def cross_limit_order(self) -> None:
        """
        Cross limit order with last bar/tick data.
        """
        for order in list(self.active_limit_orders.values()):
            bar = self.bars[order.vt_symbol]

            long_cross_price = bar.low_price
            short_cross_price = bar.high_price
            long_best_price = bar.open_price
            short_best_price = bar.open_price

            # Push order update with status "not traded" (pending).
            if order.status == Status.SUBMITTING:
                order.status = Status.NOTTRADED
                self.strategy.update_order(order)

            # Check whether limit orders can be filled.
            long_cross = (
                order.direction == Direction.LONG
                and order.price >= long_cross_price
                and long_cross_price > 0
            )

            short_cross = (
                order.direction == Direction.SHORT
                and order.price <= short_cross_price
                and short_cross_price > 0
            )

            if not long_cross and not short_cross:
                continue

            # Push order update with status "all traded" (filled).
            order.traded = order.volume
            order.status = Status.ALLTRADED
            self.strategy.update_order(order)

            self.active_limit_orders.pop(order.vt_orderid)

            # Push trade update
            self.trade_count += 1

            if long_cross:
                trade_price = min(order.price, long_best_price)
            else:
                trade_price = max(order.price, short_best_price)

            trade = TradeData(
                symbol=order.symbol,
                exchange=order.exchange,
                orderid=order.orderid,
                tradeid=str(self.trade_count),
                direction=order.direction,
                offset=order.offset,
                price=trade_price,
                volume=order.volume,
                datetime=self.datetime,
                gateway_name=self.gateway_name,
            )

            self.strategy.update_trade(trade)
            self.trades[trade.vt_tradeid] = trade

    def load_bars(
        self,
        strategy: StrategyTemplate,
        days: int,
        interval: Interval
    ) -> None:
        """"""
        self.days = days

    def send_order(
        self,
        strategy: StrategyTemplate,
        vt_symbol: str,
        direction: Direction,
        offset: Offset,
        price: float,
        volume: float,
        lock: bool
    ) -> List[str]:
        """"""
        price = round_to(price, self.priceticks[vt_symbol])
        symbol, exchange = extract_vt_symbol(vt_symbol)

        self.limit_order_count += 1

        order = OrderData(
            symbol=symbol,
            exchange=exchange,
            orderid=str(self.limit_order_count),
            direction=direction,
            offset=offset,
            price=price,
            volume=volume,
            status=Status.SUBMITTING,
            datetime=self.datetime,
            gateway_name=self.gateway_name,
        )

        self.active_limit_orders[order.vt_orderid] = order
        self.limit_orders[order.vt_orderid] = order

        return [order.vt_orderid]

    def cancel_order(self, strategy: StrategyTemplate, vt_orderid: str) -> None:
        """
        Cancel order by vt_orderid.
        """
        if vt_orderid not in self.active_limit_orders:
            return
        order = self.active_limit_orders.pop(vt_orderid)

        order.status = Status.CANCELLED
        self.strategy.update_order(order)

    def write_log(self, msg: str, strategy: StrategyTemplate = None) -> None:
        """
        Write log message.
        """
        msg = f"{self.datetime}\t{msg}"
        self.logs.append(msg)

    def send_email(self, msg: str, strategy: StrategyTemplate = None) -> None:
        """
        Send email to default receiver.
        """
        pass

    def sync_strategy_data(self, strategy: StrategyTemplate) -> None:
        """
        Sync strategy data into json file.
        """
        pass

    def put_strategy_event(self, strategy: StrategyTemplate) -> None:
        """
        Put an event to update strategy status.
        """
        pass

    def output(self, msg) -> None:
        """
        Output message of backtesting engine.
        """
        print(f"{datetime.now()}\t{msg}")

    def get_all_trades(self) -> List[TradeData]:
        """
        Return all trade data of current backtesting result.
        """
        return list(self.trades.values())

    def get_all_orders(self) -> List[OrderData]:
        """
        Return all limit order data of current backtesting result.
        """
        return list(self.limit_orders.values())

    def get_all_daily_results(self) -> List["PortfolioDailyResult"]:
        """
        Return all daily result data.
        """
        return list(self.daily_results.values())

