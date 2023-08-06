import maglev
import englishauction
import persistence

from typing import Any, List, Callable

class EnglishAuction:
	"""
	An Auction Library
	Timed auction starting at a low price and increasing until no more bids are made.
	Also supports reserve price and automatic bidding.
	"""
	def __init__(self):
		bus = maglev.maglev_MagLev.getInstance("englishauction")
		lib = englishauction.englishauction_EnglishAuction(bus)
		persistence.persistence_Persistence(bus)

	def Create(self, start: str, end: str, startingPrice: float, reservePrice: float, priceIncrement: float) -> str:
		"""		Create a new auction
		Args:
			start (str):start time of auction
			end (str):end time of auction
			startingPrice (float):starting price of auction
			reservePrice (float):reserve price for the auction (0 = none)
			priceIncrement (float):price increments for bids in the auction
		Returns:
			auctionId
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [start, end, startingPrice, reservePrice, priceIncrement]
		ret = pybus.call('EnglishAuction.Create', args);
		return ret;

	def GetStart(self, auctionId: str) -> float:
		"""		Get the start of an auction
		Will return a timestamp in milliseconds
		Args:
			auctionId (str):auction id
		Returns:
			start of auction
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [auctionId]
		ret = pybus.call('EnglishAuction.GetStart', args);
		return ret;

	def GetEnd(self, auctionId: str) -> bool:
		"""		Check if auction has ended
		Args:
			auctionId (str):auction id
		Returns:
			true if auction has ended, false otherwise
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [auctionId]
		ret = pybus.call('EnglishAuction.GetEnd', args);
		return ret;

	def HasStarted(self, auctionId: str) -> bool:
		"""		Check if an auction has started yet
		Args:
			auctionId (str):auction id
		Returns:
			true if auction started, false otherwise
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [auctionId]
		ret = pybus.call('EnglishAuction.HasStarted', args);
		return ret;

	def Bid(self, auctionId: str, userId: str, price: float):
		"""		Create a bid in an auction
		Args:
			auctionId (str):auction id
			userId (str):user id
			price (float):price bud
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [auctionId, userId, price]
		pybus.call('EnglishAuction.Bid', args);

	def GetHighestBidder(self, auctionId: str) -> Any:
		"""		Get the highest bidder in an auction
		Args:
			auctionId (str):auction id
		Returns:
			
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [auctionId]
		ret = pybus.call('EnglishAuction.GetHighestBidder', args);
		return ret;

	def GetHighestBids(self, auctionId: str, numBids: float) -> List[Any]:
		"""		Get the highest bids in an auction
		Args:
			auctionId (str):auction id
			numBids (float):max number of highest bids to return
		Returns:
			Highest bids for the specified auction
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [auctionId, numBids]
		ret = pybus.call('EnglishAuction.GetHighestBids', args);
		return ret;

	def GetNumberOfBids(self, auctionId: str) -> float:
		"""		Get the number of bids in an auction
		Args:
			auctionId (str):auction id
		Returns:
			Number of bids placed in the specified auction
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [auctionId]
		ret = pybus.call('EnglishAuction.GetNumberOfBids', args);
		return ret;

	def GetPriceIncrement(self, auctionId: str) -> float:
		"""		Get the price increment for the specified auction
		Args:
			auctionId (str):auction id
		Returns:
			Price increment
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [auctionId]
		ret = pybus.call('EnglishAuction.GetPriceIncrement', args);
		return ret;

	def GetReservePrice(self, auctionId: str) -> float:
		"""		Get the reserve price for the specified auction
		Args:
			auctionId (str):auction id
		Returns:
			Reserve price
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [auctionId]
		ret = pybus.call('EnglishAuction.GetReservePrice', args);
		return ret;

	def GetStartingPrice(self, auctionId: str) -> float:
		"""		Get the starting price for the specified auction
		Args:
			auctionId (str):auction id
		Returns:
			Starting price
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [auctionId]
		ret = pybus.call('EnglishAuction.GetStartingPrice', args);
		return ret;

	def CalcTimeRemaining(self, auctionId: str, now: float) -> float:
		"""		Get the time remaining for the specified auction
		Args:
			auctionId (str):auction id
			now (float):current unix timestamp
		Returns:
			Time remaining in seconds
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [auctionId, now]
		ret = pybus.call('EnglishAuction.CalcTimeRemaining', args);
		return ret;

	def CalcMinimumBid(self, auctionId: str) -> float:
		"""		Get the minimum next bid for the specified auction
		Args:
			auctionId (str):auction id
		Returns:
			Minimum bid price
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [auctionId]
		ret = pybus.call('EnglishAuction.CalcMinimumBid', args);
		return ret;

	def GetAuctionsEnding(self, endfrom: float, endto: float, page: float, perpage: float, sort: str, asc: bool) -> List[Any]:
		"""		Get a list of auctions based on their end time
		Args:
			endfrom (float):end from
			endto (float):end to
			page (float):
			perpage (float):number of auctions per page
			sort (str):field to sort by
			asc (bool):ascending (true) or descending (false)
		Returns:
			List of auctions ending in the specified period
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [endfrom, endto, page, perpage, sort, asc]
		ret = pybus.call('EnglishAuction.GetAuctionsEnding', args);
		return ret;

	def GetAuctionsStarting(self, startfrom: float, startto: float, page: float, perpage: float, sort: str, asc: bool) -> List[Any]:
		"""		Get a list of auctions based on their start time
		Args:
			startfrom (float):start from
			startto (float):start to
			page (float):
			perpage (float):number of auctions per page
			sort (str):field to sort by
			asc (bool):ascending (true) or descending (false)
		Returns:
			List of auctions starting in the specified period
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [startfrom, startto, page, perpage, sort, asc]
		ret = pybus.call('EnglishAuction.GetAuctionsStarting', args);
		return ret;

	def GetOpenAuctions(self, page: float, perpage: float, sort: str, asc: bool) -> List[Any]:
		"""		Get a list of currently running auctions
		Args:
			page (float):
			perpage (float):number of auctions per page
			sort (str):field to sort by
			asc (bool):ascending (true) or descending (false)
		Returns:
			List of open auctions
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [page, perpage, sort, asc]
		ret = pybus.call('EnglishAuction.GetOpenAuctions', args);
		return ret;

	def SetupNewAuctionQueryCallback(self, strategyMethod: Callable[[List[Any]], Any]) -> str:
		"""		Provide a callback used to store new auctions (eg. in a database) and return the ID of the new auction.
		Args:
			strategyMethod (Callable[[List[Any]], Any]):
		Returns:
			new auction id
		"""
		recordType = "EnglishAuction.Auction"
		operationName = "CreateNew"
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [recordType, operationName, strategyMethod]
		ret = pybus.call('Persistence.AddMutator', args);
		return ret;

	def SetupFindAuctionByIdQueryCallback(self, strategyMethod: Callable[[List[Any]], Any]) -> object:
		"""		Provide a callback used to retrieve auctions (eg. from a database) by ID
		Args:
			strategyMethod (Callable[[List[Any]], Any]):
		Returns:
			The auction or null
		"""
		recordType = "EnglishAuction.Auction"
		operationName = "FindById"
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [recordType, operationName, strategyMethod]
		ret = pybus.call('Persistence.AddGetter', args);
		return ret;

	def SetupFindAuctionsStartingQueryCallback(self, strategyMethod: Callable[[List[Any]], Any]) -> List[Any]:
		"""		Provide a callback used to retrieve auctions (eg. from a database) by their start date/time
		Args:
			strategyMethod (Callable[[List[Any]], Any]):
		Returns:
			A list of auctions
		"""
		recordType = "EnglishAuction.Auction"
		operationName = "FindStarting"
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [recordType, operationName, strategyMethod]
		ret = pybus.call('Persistence.AddGetter', args);
		return ret;

	def SetupFindAuctionsEndingQueryCallback(self, strategyMethod: Callable[[List[Any]], Any]) -> List[Any]:
		"""		Provide a callback used to retrieve auctions (eg. from a database) by their end data/time
		Args:
			strategyMethod (Callable[[List[Any]], Any]):
		Returns:
			A list of auctions
		"""
		recordType = "EnglishAuction.Auction"
		operationName = "FindEnding"
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [recordType, operationName, strategyMethod]
		ret = pybus.call('Persistence.AddGetter', args);
		return ret;

	def SetupFindOpenAuctionsQueryCallback(self, strategyMethod: Callable[[List[Any]], Any]) -> List[Any]:
		"""		Provide a callback used to retrieve open auctions (eg. from a database)
		Args:
			strategyMethod (Callable[[List[Any]], Any]):
		Returns:
			A list of auctions
		"""
		recordType = "EnglishAuction.Auction"
		operationName = "FindOpen"
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [recordType, operationName, strategyMethod]
		ret = pybus.call('Persistence.AddGetter', args);
		return ret;

	def SetupCountBidsQueryCallback(self, strategyMethod: Callable[[List[Any]], Any]) -> float:
		"""		Provide a callback used to count the number of bids for an auction (eg. in a database)
		Args:
			strategyMethod (Callable[[List[Any]], Any]):
		Returns:
			Number of bids
		"""
		recordType = "EnglishAuction.Bid"
		operationName = "CountForAuction"
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [recordType, operationName, strategyMethod]
		ret = pybus.call('Persistence.AddGetter', args);
		return ret;

	def SetupHighestBidsQueryCallback(self, strategyMethod: Callable[[List[Any]], Any]) -> List[Any]:
		"""		Provide a callback used to retrieve (eg. from a database) the highest bids for an auction
		Args:
			strategyMethod (Callable[[List[Any]], Any]):
		Returns:
			A list of highest bids
		"""
		recordType = "EnglishAuction.Bid"
		operationName = "FindByHighestPriceForAuction"
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [recordType, operationName, strategyMethod]
		ret = pybus.call('Persistence.AddGetter', args);
		return ret;

	def SetupNewBidQueryCallback(self, strategyMethod: Callable[[List[Any]], Any]) -> str:
		"""		Provide a callback used to store new bids (eg. in a database) and return the ID of the new bid.
		Args:
			strategyMethod (Callable[[List[Any]], Any]):
		Returns:
			New bid id
		"""
		recordType = "EnglishAuction.Bid"
		operationName = "New"
		pybus = maglev.maglev_MagLevPy.getInstance("englishauction")
		args = [recordType, operationName, strategyMethod]
		ret = pybus.call('Persistence.AddGetter', args);
		return ret;



