from __future__ import annotations

import json
from typing import List, Optional

import pendulum as dt
from pydantic import BaseModel, Field, validator


class PolygonBase(BaseModel):
    @classmethod
    def loads(cls, s: str):
        return cls(**json.loads(s))

    def dumps(self):
        return json.dumps(self.dict())

    @staticmethod
    def timestamp_to_datetime(ts: int):
        return dt.from_timestamp(ts / 1000)

    def print(self):
        print(f"{self.__str__()}")


class WebsocketPolygonBase(PolygonBase):
    event: str = Field(alias="ev", description="Event Type")


class PolygonStatus(WebsocketPolygonBase):
    status: str
    message: str

    def __str__(self):
        return f"{self.__class__.__name__}({self.status}, {self.message})"


class PolygonStockBase(WebsocketPolygonBase):
    symbol: str = Field(alias="sym", description="Symbol Ticker")


class PolygonTrade(WebsocketPolygonBase):
    exchange_id: int = Field(alias="x", description="Exchange ID")
    trade_id: str = Field(alias="i", description="Trade ID")
    tape: int = Field(alias="z", description="Tape ( 1=A 2=B 3=C)")
    price: float = Field(alias="p", description="Price")
    size: int = Field(alias="s", description="Trade Size")
    conditions: List[int] = Field(alias="c", description="Trade Conditions")
    timestamp: int = Field(alias="t", description="Trade Timestamp ( Unix MS )")

    @property
    def dt(self):
        return self.timestamp_to_datetime(self.timestamp)


class PolygonQuote(PolygonStockBase):
    bid_exchange_id: int = Field(alias="bx", description="Bid Exchange ID")
    bid_price: float = Field(alias="bp", description="Bid Price")
    bid_size: int = Field(alias="bs", description="Bid Size")
    ask_exchange_id: int = Field(alias="ax", description="Ask Exchange ID")
    ask_price: float = Field(alias="ap", description="Ask Price")
    ask_size: int = Field(alias="as", description="Ask Size")
    condition: int = Field(alias="c", description="Quote Condition")
    timestamp: int = Field(alias="t", description="Quote Timestamp ( Unix MS )")

    @property
    def dt(self):
        return self.timestamp_to_datetime(self.timestamp)

    def dict(self, **kwargs):
        res = super().dict()
        res.update({"dt": self.dt.isoformat()})
        return res


class PolygonAggregate(PolygonStockBase):
    volume: int = Field(alias="v", description="Tick Volume")
    volume_accum: int = Field(alias="av", description="Accumulated Volume (today)")
    open_today: Optional[float] = Field(alias="op", description="Today's official opening price")
    volume_weighted_average: float = Field(
        alias="vw", description="VWAP (Volume Weighted Average Price)"
    )
    open: float = Field(alias="o", description="Tick Open Price")
    close: float = Field(alias="c", description="Tick Close Price")
    high: float = Field(alias="h", description="Tick High Price")
    low: float = Field(alias="l", description="Tick Low Price")
    average: float = Field(alias="a", description="Tick Average Price / VWAP Price")
    timestamp_start: int = Field(
        alias="s", description="Tick Start Timestamp (Unix MS)"
    )
    timestamp_end: int = Field(alias="e", description="Tick Start Timestamp (Unix MS)")

    @property
    def dt_start(self):
        return self.timestamp_to_datetime(self.timestamp_start)

    @property
    def dt_end(self):
        return self.timestamp_to_datetime(self.timestamp_end)

    def __str__(self):
        return f"{self.__class__.__name__}({self.symbol}, open={self.open}, close={self.close}, high={self.high}, low={self.low}, volume={self.volume}...)"

    @property
    def aggregation_type(self) -> str:
        types = {"AM": "1min", "A": "1sec"}
        return types[self.event]

    def dumps(self):
        return json.dumps(self.dict())

    def dict(self, **kwargs):
        res = super().dict()
        res.update(
            {"dt_start": self.dt_start.isoformat(), "dt_end": self.dt_end.isoformat()}
        )
        return res


class PolygonMessage(BaseModel):
    events: List[WebsocketPolygonBase]
    dt: str = dt.now().format("HH:mm:ss")

    @classmethod
    def loads(cls, message: str) -> PolygonMessage:
        mapping = {
            "A": PolygonAggregate,
            "AM": PolygonAggregate,
            "T": PolygonTrade,
            "Q": PolygonQuote,
            "status": PolygonStatus,
        }

        data = json.loads(message)
        return cls(events=[mapping[msg["ev"]](**msg) for msg in data])

    def __len__(self):
        return len(self.events)

    def __iter__(self):
        return self.events.__iter__()

    def print(self):
        print(f"{self.dt} - {len(self)} events:")
        for event in self.events:
            event.print()

    def get_events_by_type(self, /, t: str) -> List:
        return [e for e in self.events if e.event == t]

    def get_aggregation_events(self) -> List[PolygonAggregate]:
        return self.get_events_by_type("AM")

    def get_quote_events(self) -> List[PolygonQuote]:
        return self.get_events_by_type("Q")


class PolygonDailyData(PolygonBase):
    symbol: str = Field(alias="symbol", description="Symbol Ticker")
    open: float = Field(alias="o", description="Tick Open Price")
    close: float = Field(alias="c", description="Tick Close Price")
    high: float = Field(alias="h", description="Tick High Price")
    low: float = Field(alias="l", description="Tick Low Price")
    volume: int = Field(alias="v", description="Tick Volume")
    volume_weighted_average: float = Field(
        alias="vw", description="VWAP (Volume Weighted Average Price)"
    )
    timestamp_start: int = Field(
        alias="t", description="Unix Msec Timestamp ( Start of Aggregate window )"
    )
    items_number: int = Field(
        alias="n", description="Number of items in aggregate window"
    )

    @property
    def dt_start(self):
        return self.timestamp_to_datetime(self.timestamp_start)

    def dict(self, **kwargs):
        res = super().dict()
        res.update({"dt_start": self.dt_start.isoformat()})
        return res


class PolygonHistoricalAggregate(PolygonDailyData):
    @property
    def dt_end(self):
        return self.timestamp_to_datetime(self.timestamp_start).add(minutes=1)

    @property
    def timestamp_end(self):
        return self.dt_end.int_timestamp

    def dict(self, **kwargs):
        res = super().dict()
        res.update({"dt_end": self.dt_end.isoformat()})
        return res
