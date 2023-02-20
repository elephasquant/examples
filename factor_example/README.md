# Factor 基类

`Factor` 是实现factor的基类。所有要加入因子库的factor都要继承这个类，并实现其中的几个抽象方法。安装请运行下面程序

```bash
python -m pip install --index-url http://192.168.0.157:8081/simple/ factorbase -U --trusted-host 192.168.0.157
```

### 代码

```python
class SecurityType(Enum):
    DEFAULT = "default"
    FUTURE = "future"
    FUTURE_COMMODITY = "future_commodity"
    FUTURE_INDEX = "future_index"
    STOCK = "stock"


class Frequency(Enum):
    MONTHLY = 'monthly'
    DAILY = 'daily'
    HOURLY = 'hourly'
    MINUTE = 'minute'
    SECOND = 'second'


class Factor(ABC):
    @abstractmethod
    def factor_name(self) -> str:
        """
        return: 因子名称
        """
        pass

    @abstractmethod
    def author(self) -> str:
        """
        return: 作者
        """
        pass

    @abstractmethod
    def security_type(self) -> SecurityType:
        """
        return: 返回因子类型
        """
        pass

    @abstractmethod
    def frequency(self) -> Frequency:
        """
        return: 返回因子频率
        """
        pass

    @abstractmethod
    def trigger_time(self) -> str:
        """
        return: 返回触发时间
        语法为cron类似语法
        https://www.freeformatter.com/cron-expression-generator-quartz.html

        Second Minute Hour Day(Month) Month Day(Week) Year
        """
        pass

    @abstractmethod
    def run(self, start_time: datetime, end_time: datetime) -> Tuple[pd.DataFrame, Exception]:
        """
        param: start_time, 因子计算开始时间，自然时间
        param: end_time, 因子计算结束时间，自然时间。在计算因子时获取的数据不能晚于这个时间
        return: (因子的DataFrame, 异常)

        例如 每日收盘价格（close）作为因子
        这是一个daily的因子，因此需要返回所有在[start_time, end_time]之间的每个票在每个交易日的close
        DataFrame的格式为

        index为 [datetime]
        columns为 ['gen_time', 'A2201', 'A2205', ...]

                    gen_time            A2201  A2205  ....
        datetime              
        2022-01-04  2022-01-04 15:00:00 5877.0 5876.0   
        2022-01-05  2022-01-04 15:00:00 5912.0 5917.0
        2022-01-06  2022-01-04 15:00:00 5877.0 5879.0 
        2022-01-07  2022-01-04 15:00:00 5894.0 5895.0

        其中 'gen_time' 为这个因子理论上最早能算出来的时间。对于close而言，收盘后才能拿到，那么就是15：00

        如果在计算过程中有异常或者计算的不全，需要返回一个异常（如果有严重错误，可以直接抛出一个异常）
        """
        pass

```

## 说明

* 请用因子的名称作为类名

* 各个标的的 `code` 以米筐的 `order_book_id` 为统一标准

* 返回的因子数据是一个DataFrame，`index` 为因子时间`'datetime'`，数据为各个票的因子值，其中第一列为`gen_time`

* `index` 中的 `datetime` 和数据列中的 `gen_time` 格式都为 `np.datetime`。具体含义可以参考下面代码中的注释

* 在实现各个函数的时候，请加上 `@Factor.checker` 修饰，这个可以帮助检查返回的结果格式是否正确

* 每天收盘价作为一个因子，这里有个[例子](https://github.com/elephasquant/examples/tree/main/factor_example/StockClose.py)


