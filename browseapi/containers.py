from . import exceptions


class BrowseAPIBaseContainer(object):
    """ Base class for all custom types from response """

    def __str__(self):
        return str(self.__dict__)


class BrowseAPIResponse(BrowseAPIBaseContainer):
    """ Browse API parsed response data container """

    def __init__(self, response: dict, method: str):
        if 'errors' in response:
            self.parse_errors(response)

        if method in ('search', 'search_by_image'):
            self.href = response['href']
            self.limit = response['limit']
            self.offset = response['offset']
            self.total = response['total']
            self.itemSummaries = [ItemSummary(item) for item in response['itemSummaries']]

            for key in 'next', 'prev':
                setattr(self, key, response.get(key))

            if 'refinement' in response:
                self.refinement = Refinement(response['refinement'])

        if 'warnings' in response:
            self.warnings = [ErrorDetailV3(warning) for warning in response['warnings']]

    @staticmethod
    def parse_errors(response: dict) -> None:
        """
        Handle all Browse API errors,
        for more information visit https://developer.ebay.com/api-docs/static/handling-error-messages.html
        """

        for error in response['errors']:
            if error['errorId'] == 12000:
                raise exceptions.BrowseAPIInternalError(error)

            if error['errorId'] in (1001, 1002, 1003, 1004, 1100):
                raise exceptions.BrowseAPIRequestOAuthError(error)

            if error['errorId'] in (2001, 2002, 2003, 2004):
                raise exceptions.BrowseAPIAccessError(error)

            if error['errorId'] in (3001, 3002, 3003, 3004, 3005):
                raise exceptions.BrowseAPIRoutingError(error)

            if 12001 <= error['errorId'] <= 12007 or 12023 <= error['errorId'] <= 12506:
                raise exceptions.BrowseAPIRequestParamError(error)

            if error['errorId'] in (12013, 12019):
                raise exceptions.BrowseAPIBusinessError(error)

            raise exceptions.BrowseAPIError('Unhandled error, code: {0}, message: {1}'.format(
                error['errorId'], error['message'])
            )


class ItemSummary(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the details of a specific item
    https://developer.ebay.com/api-docs/buy/browse/types/gct:ItemSummary
    """

    def __init__(self, item_summary: dict):
        self.adultOnly = item_summary.get('adultOnly')
        self.buyingOptions = item_summary.get('buyingOptions')
        self.conditionId = item_summary.get('conditionId')
        self.image = Image(item_summary['image'])
        self.itemHref = item_summary.get('itemHref')
        self.itemId = item_summary.get('itemId')
        self.itemLocation = ItemLocationImpl(item_summary['itemLocation'])
        self.itemWebUrl = item_summary.get('itemWebUrl')
        self.price = ConvertedAmount(item_summary['price'])
        self.seller = Seller(item_summary['seller'])
        self.shortDescription = item_summary.get('shortDescription')
        self.title = item_summary.get('title')
        self.unitPricingMeasure = item_summary.get('unitPricingMeasure')

        for key in ('bidCount',
                    'compatibilityMatch',
                    'condition',
                    'energyEfficiencyClass',
                    'epid',
                    'itemAffiliateWebUrl',
                    'itemGroupHref',
                    'itemGroupType'):
            setattr(self, key, item_summary.get(key))

        if 'additionalImages' in item_summary:
            self.additionalImages = [Image(image) for image in item_summary['additionalImages']]

        if 'categories' in item_summary:
            self.categories = [Category(category) for category in item_summary['categories']]

        if 'compatibilityProperties' in item_summary:
            self.categories = [CompatibilityProperty(compatibility_property)
                               for compatibility_property in item_summary['compatibilityProperties']]

        if 'currentBidPrice' in item_summary:
            self.currentBidPrice = ConvertedAmount(item_summary['currentBidPrice'])

        if 'distanceFromPickupLocation' in item_summary:
            self.distanceFromPickupLocation = TargetLocation(item_summary['distanceFromPickupLocation'])

        if 'marketingPrice' in item_summary:
            self.marketingPrice = MarketingPrice(item_summary['marketingPrice'])

        if 'pickupOptions' in item_summary:
            self.pickupOptions = [PickupOptionSummary(option) for option in item_summary['pickupOptions']]

        if 'shippingOptions' in item_summary:
            self.shippingOptions = [ShippingOptionSummary(option) for option in item_summary['shippingOptions']]

        if 'thumbnailImages' in item_summary:
            self.thumbnailImages = [Image(image) for image in item_summary['thumbnailImages']]

        if 'unitPrice' in item_summary:
            self.unitPrice = ConvertedAmount(item_summary['unitPrice'])


class Image(BrowseAPIBaseContainer):
    """
    Type the defines the details of an image, such as size and image URL
    https://developer.ebay.com/api-docs/buy/browse/types/gct:Image
    """

    def __init__(self, image: dict):
        for key in 'height', 'imageUrl', 'width':
            setattr(self, key, image.get(key))


class Category(BrowseAPIBaseContainer):
    """
    This type is used by the categories container in the response of the search method
    https://developer.ebay.com/api-docs/buy/browse/types/gct:Category
    """

    def __init__(self, category: dict):
        self.categoryId = category.get('categoryId')


class CompatibilityProperty(BrowseAPIBaseContainer):
    """
    This container returns the product attribute name/value pairs that are compatible with the keyword
    https://developer.ebay.com/api-docs/buy/browse/types/gct:CompatibilityProperty
    """

    def __init__(self, compatibility_property: dict):
        for key in 'localizedName', 'name', 'value':
            setattr(self, key, compatibility_property.get(key))


class ConvertedAmount(BrowseAPIBaseContainer):
    """
    This type defines the monetary value of an amount
    https://developer.ebay.com/api-docs/buy/browse/types/gct:ConvertedAmount
    """

    def __init__(self, current_price: dict):
        self.currency = current_price.get('currency')
        self.value = current_price.get('value')

        for key in 'convertedFromCurrency', 'convertedFromValue':
            setattr(self, key, current_price.get(key))


class TargetLocation(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the distance between the item location and the buyer's location
    https://developer.ebay.com/api-docs/buy/browse/types/gct:TargetLocation
    """

    def __init__(self, location: dict):
        for key in 'unitOfMeasure', 'value':
            setattr(self, key, location.get(key))


class ItemLocationImpl(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the location of an item
    https://developer.ebay.com/api-docs/buy/browse/types/gct:ItemLocationImpl
    """

    def __init__(self, location: dict):
        for key in 'addressLine1', 'addressLine2', 'city', 'country', 'county', 'stateOrProvince', 'postalCode':
            setattr(self, key, location.get(key))


class MarketingPrice(BrowseAPIBaseContainer):
    """
    The type that defines the fields that describe a seller discount
    https://developer.ebay.com/api-docs/buy/browse/types/gct:MarketingPrice
    """

    def __init__(self, price: dict):
        for key in 'discountPercentage', 'currency', 'value':
            setattr(self, key, price.get(key))

        if 'discountAmount' in price:
            self.discountAmount = ConvertedAmount(price['discountAmount'])

        if 'originalPrice' in price:
            self.originalPrice = ConvertedAmount(price['originalPrice'])


class PickupOptionSummary(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the local pickup options that are available for the item
    https://developer.ebay.com/api-docs/buy/browse/types/gct:PickupOptionSummary
    """

    def __init__(self, option: dict):
        self.pickupLocationType = option.get('pickupLocationType')


class Seller(BrowseAPIBaseContainer):
    """
    The type that defines the fields for basic information about the seller of the item
    https://developer.ebay.com/api-docs/buy/browse/types/gct:Seller
    """

    def __init__(self, seller: dict):
        self.feedbackPercentage = seller.get('feedbackPercentage')
        self.feedbackScore = seller.get('feedbackScore')
        self.username = seller.get('username')
        self.sellerAccountType = seller.get('sellerAccountType')


class ShippingOptionSummary(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the shipping information
    https://developer.ebay.com/api-docs/buy/browse/types/gct:ShippingOptionSummary
    """

    def __init__(self, option: dict):
        self.maxEstimatedDeliveryDate = option.get('maxEstimatedDeliveryDate')
        self.minEstimatedDeliveryDate = option.get('minEstimatedDeliveryDate')
        self.shippingCostType = option.get('shippingCostType')

        if 'shippingCost' in option:
            self.shippingCost = ConvertedAmount(option['shippingCost'])


class Refinement(BrowseAPIBaseContainer):
    """
    This type defines the fields for the various refinements of an item
    https://developer.ebay.com/api-docs/buy/browse/types/gct:Refinement
    """

    def __init__(self, refinement: dict):
        self.dominantCategoryId = refinement.get('dominantCategoryId')

        if 'aspectDistributions' in refinement:
            self.aspectDistributions = [AspectDistribution(distribution)
                                        for distribution in refinement['aspectDistributions']]

        if 'buyingOptionDistributions' in refinement:
            self.buyingOptionDistributions = [BuyingOptionDistribution(distribution)
                                              for distribution in refinement['buyingOptionDistributions']]

        if 'categoryDistributions' in refinement:
            self.categoryDistributions = [CategoryDistribution(distribution)
                                          for distribution in refinement['categoryDistributions']]

        if 'conditionDistributions' in refinement:
            self.conditionDistributions = [ConditionDistribution(distribution)
                                           for distribution in refinement['conditionDistributions']]


class AspectDistribution(BrowseAPIBaseContainer):
    """
    The type that define the fields for the aspect information
    https://developer.ebay.com/api-docs/buy/browse/types/gct:AspectDistribution
    """

    def __init__(self, distribution):
        self.localizedAspectName = distribution.get('localizedAspectName')

        if 'aspectValueDistributions' in distribution:
            self.aspectValueDistributions = [AspectValueDistribution(value_distribution)
                                             for value_distribution in distribution['aspectValueDistributions']]


class AspectValueDistribution(BrowseAPIBaseContainer):
    """
    The container that defines the fields for the conditions refinements
    https://developer.ebay.com/api-docs/buy/browse/types/gct:AspectValueDistribution
    """

    def __init__(self, value_distribution: dict):
        self.localizedAspectValue = value_distribution.get('localizedAspectValue')
        self.matchCount = value_distribution.get('matchCount')
        self.refinementHref = value_distribution.get('refinementHref')


class BuyingOptionDistribution(BrowseAPIBaseContainer):
    """
    The container that defines the fields for the buying options refinements
    https://developer.ebay.com/api-docs/buy/browse/types/gct:BuyingOptionDistribution
    """

    def __init__(self, distribution: dict):
        self.buyingOption = distribution.get('buyingOption')
        self.matchCount = distribution.get('matchCount')
        self.refinementHref = distribution.get('refinementHref')


class CategoryDistribution(BrowseAPIBaseContainer):
    """
    The container that defines the fields for the category refinements
    https://developer.ebay.com/api-docs/buy/browse/types/gct:CategoryDistribution
    """

    def __init__(self, distribution: dict):
        self.categoryId = distribution.get('categoryId')
        self.categoryName = distribution.get('categoryName')
        self.matchCount = distribution.get('matchCount')
        self.refinementHref = distribution.get('refinementHref')


class ConditionDistribution(BrowseAPIBaseContainer):
    """
    The container that defines the fields for the conditions refinements
    https://developer.ebay.com/api-docs/buy/browse/types/gct:ConditionDistribution
    """

    def __init__(self, distribution: dict):
        self.conditionId = distribution.get('conditionId')
        self.matchCount = distribution.get('matchCount')
        self.refinementHref = distribution.get('refinementHref')
        self.condition = distribution.get('condition')


class ErrorDetailV3(BrowseAPIBaseContainer):
    """
    The type that defines the fields that can be returned in an error
    https://developer.ebay.com/api-docs/buy/browse/types/cos:ErrorDetailV3
    """

    def __init__(self, warning: dict):
        for key in ('category',
                    'domain',
                    'errorId',
                    'message',
                    'inputRefIds',
                    'longMessage',
                    'outputRefIds',
                    'subdomain'):
            setattr(self, key, warning.get(key))

        if 'parameters' in warning:
            self.parameters = [ErrorParameterV3(parameter) for parameter in warning['parameters']]


class ErrorParameterV3(BrowseAPIBaseContainer):
    """
    An array of name/value pairs that provide details regarding the error
    https://developer.ebay.com/api-docs/buy/browse/types/cos:ErrorParameterV3
    """

    def __init__(self, parameter: dict):
        for key in 'name', 'value':
            setattr(self, key, parameter.get(key))
