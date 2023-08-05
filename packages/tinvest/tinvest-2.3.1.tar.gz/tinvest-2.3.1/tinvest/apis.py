from typing import Any, Generic, Optional, TypeVar

from .schemas import (
    CandleResolution,
    CandlesResponse,
    Empty,
    LimitOrderRequest,
    LimitOrderResponse,
    MarketInstrumentListResponse,
    MarketOrderRequest,
    MarketOrderResponse,
    OperationsResponse,
    OrderbookResponse,
    OrdersResponse,
    PortfolioCurrenciesResponse,
    PortfolioResponse,
    SandboxRegisterRequest,
    SandboxRegisterResponse,
    SandboxSetCurrencyBalanceRequest,
    SandboxSetPositionBalanceRequest,
    SearchMarketInstrumentResponse,
    UserAccountsResponse,
)
from .typedefs import datetime_or_str
from .utils import isoformat

__all__ = (
    'OpenApi',
    'MarketApi',
    'OperationsApi',
    'OrdersApi',
    'PortfolioApi',
    'SandboxApi',
    'UserApi',
)

T = TypeVar('T')  # pragma: no mutate


class BaseApi(Generic[T]):
    def __init__(self, client: T) -> None:
        self._client = client

    @property
    def client(self) -> T:
        return self._client


class OpenApi(Generic[T]):
    def __init__(self, client: T) -> None:
        self.sandbox = SandboxApi(client)
        self.orders = OrdersApi(client)
        self.portfolio = PortfolioApi(client)
        self.market = MarketApi(client)
        self.operations = OperationsApi(client)
        self.user = UserApi(client)


class SandboxApi(BaseApi):
    def sandbox_register_post(self, body: SandboxRegisterRequest, **kwargs: Any) -> Any:
        """
        POST /sandbox/register
        """
        kwargs.setdefault('data', body.json(by_alias=True))
        return self.client.request(
            'POST',
            '/sandbox/register',
            response_model=SandboxRegisterResponse,
            **kwargs,
        )

    def sandbox_currencies_balance_post(
        self,
        body: SandboxSetCurrencyBalanceRequest,
        broker_account_id: Optional[str] = None,
        **kwargs: Any
    ) -> Any:
        """
        POST /sandbox/currencies/balance
        """
        kwargs.setdefault('params', {})
        params = kwargs['params']
        if broker_account_id:
            params.setdefault('brokerAccountId', broker_account_id)
        kwargs.setdefault('data', body.json())
        return self.client.request(
            'POST',
            '/sandbox/currencies/balance',
            response_model=Empty,
            **kwargs,
        )

    def sandbox_positions_balance_post(
        self,
        body: SandboxSetPositionBalanceRequest,
        broker_account_id: Optional[str] = None,
        **kwargs: Any
    ) -> Any:
        """
        POST /sandbox/positions/balance
        """
        kwargs.setdefault('params', {})
        params = kwargs['params']
        if broker_account_id:
            params.setdefault('brokerAccountId', broker_account_id)
        kwargs.setdefault('data', body.json())
        return self.client.request(
            'POST', '/sandbox/positions/balance', response_model=Empty, **kwargs
        )

    def sandbox_remove_post(
        self, broker_account_id: Optional[str] = None, **kwargs: Any
    ) -> Any:
        """POST /sandbox/remove"""
        kwargs.setdefault('params', {})
        params = kwargs['params']
        if broker_account_id:
            params.setdefault('brokerAccountId', broker_account_id)
        return self.client.request(
            'POST', '/sandbox/remove', response_model=Empty, **kwargs
        )

    def sandbox_clear_post(
        self, broker_account_id: Optional[str] = None, **kwargs: Any
    ) -> Any:
        """POST /sandbox/clear"""
        kwargs.setdefault('params', {})
        params = kwargs['params']
        if broker_account_id:
            params.setdefault('brokerAccountId', broker_account_id)
        return self.client.request(
            'POST', '/sandbox/clear', response_model=Empty, **kwargs
        )


class OrdersApi(BaseApi):
    def orders_get(self, broker_account_id: Optional[str] = None, **kwargs: Any) -> Any:
        """GET /orders"""
        kwargs.setdefault('params', {})
        params = kwargs['params']
        if broker_account_id:
            params.setdefault('brokerAccountId', broker_account_id)
        return self.client.request(
            'GET', '/orders', response_model=OrdersResponse, **kwargs
        )

    def orders_limit_order_post(
        self,
        figi: str,
        body: LimitOrderRequest,
        broker_account_id: Optional[str] = None,
        **kwargs: Any
    ) -> Any:
        """POST /orders/limit-order"""
        kwargs.setdefault('params', {})
        params = kwargs['params']
        params.setdefault('figi', figi)
        if broker_account_id:
            params.setdefault('brokerAccountId', broker_account_id)
        kwargs.setdefault('data', body.json())
        return self.client.request(
            'POST',
            '/orders/limit-order',
            response_model=LimitOrderResponse,
            **kwargs,
        )

    def orders_market_order_post(
        self,
        figi: str,
        body: MarketOrderRequest,
        broker_account_id: Optional[str] = None,
        **kwargs: Any
    ) -> Any:
        """POST /orders/market-order"""
        kwargs.setdefault('params', {})
        params = kwargs['params']
        params.setdefault('figi', figi)
        if broker_account_id:
            params.setdefault('brokerAccountId', broker_account_id)
        kwargs.setdefault('data', body.json())
        return self.client.request(
            'POST', '/orders/market-order', response_model=MarketOrderResponse, **kwargs
        )

    def orders_cancel_post(
        self, order_id: str, broker_account_id: Optional[str] = None, **kwargs: Any
    ) -> Any:
        """POST /orders/cancel"""
        kwargs.setdefault('params', {})
        params = kwargs['params']
        params.setdefault('orderId', order_id)
        if broker_account_id:
            params.setdefault('brokerAccountId', broker_account_id)
        return self.client.request(
            'POST', '/orders/cancel', response_model=Empty, **kwargs
        )


class PortfolioApi(BaseApi):
    def portfolio_get(
        self, broker_account_id: Optional[str] = None, **kwargs: Any
    ) -> Any:
        """GET /portfolio"""
        kwargs.setdefault('params', {})
        params = kwargs['params']
        if broker_account_id:
            params.setdefault('brokerAccountId', broker_account_id)
        return self.client.request(
            'GET', '/portfolio', response_model=PortfolioResponse, **kwargs
        )

    def portfolio_currencies_get(
        self, broker_account_id: Optional[str] = None, **kwargs: Any
    ) -> Any:
        """GET /portfolio/currencies"""
        kwargs.setdefault('params', {})
        params = kwargs['params']
        if broker_account_id:
            params.setdefault('brokerAccountId', broker_account_id)
        return self.client.request(
            'GET',
            '/portfolio/currencies',
            response_model=PortfolioCurrenciesResponse,
            **kwargs,
        )


class MarketApi(BaseApi):
    def market_stocks_get(self, **kwargs: Any) -> Any:
        """GET /market/stocks"""
        return self.client.request(
            'GET',
            '/market/stocks',
            response_model=MarketInstrumentListResponse,
            **kwargs,
        )

    def market_bonds_get(self, **kwargs: Any) -> Any:
        """GET /market/bonds"""
        return self.client.request(
            'GET',
            '/market/bonds',
            response_model=MarketInstrumentListResponse,
            **kwargs,
        )

    def market_etfs_get(self, **kwargs: Any) -> Any:
        """GET /market/etfs"""
        return self.client.request(
            'GET',
            '/market/etfs',
            response_model=MarketInstrumentListResponse,
            **kwargs,
        )

    def market_currencies_get(self, **kwargs: Any) -> Any:
        """GET /market/currencies"""
        return self.client.request(
            'GET',
            '/market/currencies',
            response_model=MarketInstrumentListResponse,
            **kwargs,
        )

    def market_orderbook_get(self, figi: str, depth: int, **kwargs: Any) -> Any:
        """GET /market/orderbook"""
        kwargs.setdefault('params', {})
        params = kwargs['params']
        params.setdefault('figi', figi)
        params.setdefault('depth', depth)
        return self.client.request(
            'GET',
            '/market/orderbook',
            response_model=OrderbookResponse,
            **kwargs,
        )

    def market_candles_get(
        self,
        figi: str,
        from_: datetime_or_str,
        to: datetime_or_str,
        interval: CandleResolution,
        **kwargs: Any
    ) -> Any:
        """GET /market/candles"""
        kwargs.setdefault('params', {})
        params = kwargs['params']
        params.setdefault('figi', figi)
        params.setdefault('from', isoformat(from_))
        params.setdefault('to', isoformat(to))
        params.setdefault('interval', interval.value)
        return self.client.request(
            'GET', '/market/candles', response_model=CandlesResponse, **kwargs
        )

    def market_search_by_figi_get(self, figi: str, **kwargs: Any) -> Any:
        """GET /market/search/by-figi"""
        kwargs.setdefault('params', {})
        params = kwargs['params']
        params.setdefault('figi', figi)
        return self.client.request(
            'GET',
            '/market/search/by-figi',
            response_model=SearchMarketInstrumentResponse,
            **kwargs,
        )

    def market_search_by_ticker_get(self, ticker: str, **kwargs: Any) -> Any:
        """GET /market/search/by-ticker"""
        kwargs.setdefault('params', {})
        params = kwargs['params']
        params.setdefault('ticker', ticker)
        return self.client.request(
            'GET',
            '/market/search/by-ticker',
            response_model=MarketInstrumentListResponse,
            **kwargs,
        )


class OperationsApi(BaseApi):
    def operations_get(
        self,
        from_: datetime_or_str,
        to: datetime_or_str,
        figi: Optional[str] = None,
        broker_account_id: Optional[str] = None,
        **kwargs: Any
    ) -> Any:
        """GET /operations"""
        kwargs.setdefault('params', {})
        params = kwargs['params']
        params.setdefault('from', isoformat(from_))
        params.setdefault('to', isoformat(to))
        if figi:
            params.setdefault('figi', figi)
        if broker_account_id:
            params.setdefault('brokerAccountId', broker_account_id)
        return self.client.request(
            'GET', '/operations', response_model=OperationsResponse, **kwargs
        )


class UserApi(BaseApi):
    def accounts_get(self, **kwargs: Any) -> Any:
        """GET /user/accounts"""
        return self.client.request(
            'GET', '/user/accounts', response_model=UserAccountsResponse, **kwargs
        )
