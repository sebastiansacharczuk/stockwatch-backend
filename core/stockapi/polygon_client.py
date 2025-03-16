import requests
from django.conf import settings
from typing import Dict, Any, Optional


class PolygonClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PolygonClient, cls).__new__(cls)
            cls._instance.api_key = settings.STOCK_API_KEY
            cls._instance.base_url = settings.STOCK_API_BASE_URL
        return cls._instance


    def get_aggregate_data(
            self,
            ticker: str,
            multiplier: int,
            timespan: str,
            from_date: str,
            to_date: str,
            adjusted: bool = True,
            sort: str = "asc",
            limit: int = 5000
    ) -> Dict[str, Any]:
        valid_timespans = ["second", "minute", "hour", "day", "week", "month", "quarter", "year"]
        if timespan not in valid_timespans:
            raise ValueError(f"Invalid parameter \"timespan\". Valid options: {', '.join(valid_timespans)}")

        if not ticker or not isinstance(multiplier, int) or not timespan or not from_date or not to_date:
            raise ValueError("Invalid query parameters.")

        url = f"{self.base_url}/v2/aggs/ticker/{ticker.upper()}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
        params = {
            "adjusted": str(adjusted).lower(),
            "sort": sort,
            "limit": limit,
            "apiKey": self.api_key
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()


    def get_tickers_snapshot(
            self,
            tickers = None,
            include_otc: bool = False
    ) -> Dict[str, Any]:

        url = f"{self.base_url}/v2/snapshot/locale/us/markets/stocks/tickers"
        params = {
            "apiKey": self.api_key,
            "include_otc": str(include_otc).lower()
        }

        # Handle tickers parameter if provided
        if tickers is not None:
            if not isinstance(tickers, list) or not all(isinstance(t, str) and t for t in tickers):
                raise ValueError("Tickers must be a list of non-empty strings")
            params["tickers"] = ",".join(tickers)

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Failed to retrieve tickers snapshot: {str(e)}")


    def get_search_tickers(
            self,
            search: str,
            date: Optional[str] = None,
            ticker: Optional[str] = None,
            ticker_type: Optional[str] = None,
            market: Optional[str] = "stocks",
            exchange: Optional[str] = None,
            active: bool = True,
            limit: int = 100,
            order: str = None,
            sort: str = None
    ) -> Dict[str, Any]:

        if not search:
            raise ValueError("Search parameter is required.")

        url = f"{self.base_url}/v3/reference/tickers"
        params = {
            "apiKey": self.api_key,
            "search": search,
            "active": str(active).lower(),
            "order": order,
            "limit": (max(1, min(limit, 1000))),  # Ensure limit doesn't exceed API max
            "sort": sort
        }

        # Add optional parameters if provided
        if date:
            params["date"] = date
        if ticker:
            params["ticker"] = ticker
        if ticker_type:
            params["type"] = ticker_type
        if market:
            params["market"] = market
        if exchange:
            params["exchange"] = exchange

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"API request failed: {str(e)}")


    def get_ticker_details(
            self,
            ticker: str,
            date: Optional[str] = None
    ) -> Dict[str, Any]:

        if not ticker or not isinstance(ticker, str):
            raise ValueError("Ticker parameter is required and must be a non-empty string.")

        url = f"{self.base_url}/v3/reference/tickers/{ticker}"
        params = {
            "apiKey": self.api_key,
            "date": date
        }

        # Add date parameter if provided
        if date:
            params["date"] = date

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Failed to retrieve ticker details: {str(e)}")


    def get_news(
            self,
            ticker: str = None,
            published_utc: str = None,
            order: str = "asc",
            limit: int = 15,
            sort: str = "published_utc"
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/v2/reference/news"
        params = {
            "apiKey": self.api_key,
            "ticker": ticker,
            "published_utc": published_utc,
            "order": order,
            "limit": limit,
            "sort": sort,
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Failed to retrieve news: {str(e)}")
        pass

