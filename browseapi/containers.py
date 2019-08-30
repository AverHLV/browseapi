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

        if 'warnings' in response:
            self.warnings = [ErrorDetailV3(warning) for warning in response['warnings']]

        # itemSummary methods

        if method in ('search', 'search_by_image'):
            self.href = response['href']
            self.limit = response['limit']
            self.offset = response['offset']
            self.total = response['total']

            for key in 'next', 'prev':
                setattr(self, key, response.get(key))

            if 'refinement' in response:
                self.refinement = Refinement(response['refinement'])

            if 'itemSummaries' in response:
                self.itemSummaries = [ItemSummary(item) for item in response['itemSummaries']]

        # item methods

        elif method in ('get_item', 'get_item_by_legacy_id'):
            self.adultOnly = response.get('adultOnly')
            self.categoryId = response.get('categoryId')
            self.categoryPath = response.get('categoryPath')
            self.condition = response.get('condition')
            self.conditionId = response.get('conditionId')
            self.description = response.get('description')
            self.enabledForGuestCheckout = response.get('enabledForGuestCheckout')
            self.itemWebUrl = response.get('itemWebUrl')
            self.title = response.get('title')

            for key in ('ageGroup',
                        'bidCount',
                        'brand',
                        'buyingOptions',
                        'color',
                        'energyEfficiencyClass',
                        'epid',
                        'gender',
                        'gtin',
                        'inferredEpid',
                        'itemAffiliateWebUrl',
                        'itemEndDate',
                        'itemId',
                        'material',
                        'mpn',
                        'pattern',
                        'priceDisplayCondition',
                        'productFicheWebUrl',
                        'quantityLimitPerBuyer',
                        'reservePriceMet',
                        'sellerItemRevision',
                        'shortDescription',
                        'size',
                        'sizeSystem',
                        'sizeType',
                        'subtitle',
                        'topRatedBuyingExperience',
                        'uniqueBidderCount',
                        'unitPricingMeasure'):
                setattr(self, key, response.get(key))

            if 'additionalImages' in response:
                self.additionalImages = [Image(image) for image in response['additionalImages']]

            if 'currentBidPrice' in response:
                self.currentBidPrice = ConvertedAmount(response['currentBidPrice'])

            if 'estimatedAvailabilities' in response:
                self.estimatedAvailabilities = [EstimatedAvailability(availability)
                                                for availability in response['estimatedAvailabilities']]

            if 'image' in response:
                self.image = Image(response['image'])

            if 'itemLocation' in response:
                self.itemLocation = Address(response['itemLocation'])

            if 'localizedAspects' in response:
                self.localizedAspects = [TypedNameValue(aspect) for aspect in response['localizedAspects']]

            if 'marketingPrice' in response:
                self.marketingPrice = MarketingPrice(response['marketingPrice'])

            if 'minimumPriceToBid' in response:
                self.minimumPriceToBid = ConvertedAmount(response['minimumPriceToBid'])

            if 'price' in response:
                self.price = ConvertedAmount(response['price'])

            if 'primaryItemGroup' in response:
                self.primaryItemGroup = ItemGroupSummary(response['primaryItemGroup'])

            if 'primaryProductReviewRating' in response:
                self.primaryProductReviewRating = ReviewRating(response['primaryProductReviewRating'])

            if 'product' in response:
                self.product = Product(response['product'])

            if 'returnTerms' in response:
                self.returnTerms = ItemReturnTerms(response['returnTerms'])

            if 'seller' in response:
                self.seller = SellerDetail(response['seller'])

            if 'shippingOptions' in response:
                self.shippingOptions = [ShippingOption(option) for option in response['shippingOptions']]

            if 'shipToLocations' in response:
                self.shipToLocations = ShipToLocations(response['shipToLocations'])

            if 'taxes' in response:
                self.taxes = [Taxes(taxes) for taxes in response['taxes']]

            if 'unitPrice' in response:
                self.unitPrice = ConvertedAmount(response['unitPrice'])

        elif method == 'get_items_by_item_group':
            if 'commonDescriptions' in response:
                self.commonDescriptions = [CommonDescriptions(description)
                                           for description in response['commonDescriptions']]

            if 'items' in response:
                self.items = [Item(item) for item in response['items']]

        else:
            self.compatibilityStatus = response.get('compatibilityStatus')

    @staticmethod
    def parse_errors(response: dict) -> None:
        """
        Handle all Browse API errors,
        for more information visit https://developer.ebay.com/api-docs/static/handling-error-messages.html
        """

        for error in response['errors']:
            if error['errorId'] in (11000, 12000):
                raise exceptions.BrowseAPIInternalError(error)

            if error['errorId'] in (1001, 1002, 1003, 1004, 1100):
                raise exceptions.BrowseAPIRequestOAuthError(error)

            if error['errorId'] in (2001, 2002, 2003, 2004):
                raise exceptions.BrowseAPIAccessError(error)

            if error['errorId'] in (3001, 3002, 3003, 3004, 3005):
                raise exceptions.BrowseAPIRoutingError(error)

            if 11001 <= error['errorId'] <= 11507 or 12001 <= error['errorId'] <= 12007 \
                    or 12023 <= error['errorId'] <= 12506:
                raise exceptions.BrowseAPIRequestParamError(error)

            if error['errorId'] in (12013, 12019):
                raise exceptions.BrowseAPIBusinessError(error)

            raise exceptions.BrowseAPIError('Unhandled error, code: {0}, message: {1}'.format(
                error['errorId'], error['message'])
            )


class Item(BrowseAPIBaseContainer):
    """
    Type that defines the fields for the item details for a specific item
    https://developer.ebay.com/api-docs/buy/browse/types/gct:Item
    """

    def __init__(self, item: dict):
        if 'warnings' in item:
            self.warnings = [ErrorDetailV3(warning) for warning in item['warnings']]

        self.adultOnly = item.get('adultOnly')
        self.categoryId = item.get('categoryId')
        self.categoryPath = item.get('categoryPath')
        self.condition = item.get('condition')
        self.conditionId = item.get('conditionId')
        self.description = item.get('description')
        self.enabledForGuestCheckout = item.get('enabledForGuestCheckout')
        self.itemWebUrl = item.get('itemWebUrl')
        self.title = item.get('title')

        for key in ('ageGroup',
                    'bidCount',
                    'brand',
                    'buyingOptions',
                    'color',
                    'energyEfficiencyClass',
                    'epid',
                    'gender',
                    'gtin',
                    'inferredEpid',
                    'itemAffiliateWebUrl',
                    'itemEndDate',
                    'itemId',
                    'material',
                    'mpn',
                    'pattern',
                    'priceDisplayCondition',
                    'productFicheWebUrl',
                    'quantityLimitPerBuyer',
                    'reservePriceMet',
                    'sellerItemRevision',
                    'shortDescription',
                    'size',
                    'sizeSystem',
                    'sizeType',
                    'subtitle',
                    'topRatedBuyingExperience',
                    'uniqueBidderCount',
                    'unitPricingMeasure'):
            setattr(self, key, item.get(key))

        if 'additionalImages' in item:
            self.additionalImages = [Image(image) for image in item['additionalImages']]

        if 'currentBidPrice' in item:
            self.currentBidPrice = ConvertedAmount(item['currentBidPrice'])

        if 'estimatedAvailabilities' in item:
            self.estimatedAvailabilities = [EstimatedAvailability(availability)
                                            for availability in item['estimatedAvailabilities']]

        if 'image' in item:
            self.image = Image(item['image'])

        if 'itemLocation' in item:
            self.itemLocation = Address(item['itemLocation'])

        if 'localizedAspects' in item:
            self.localizedAspects = [TypedNameValue(aspect) for aspect in item['localizedAspects']]

        if 'marketingPrice' in item:
            self.marketingPrice = MarketingPrice(item['marketingPrice'])

        if 'minimumPriceToBid' in item:
            self.minimumPriceToBid = ConvertedAmount(item['minimumPriceToBid'])

        if 'price' in item:
            self.price = ConvertedAmount(item['price'])

        if 'primaryItemGroup' in item:
            self.primaryItemGroup = ItemGroupSummary(item['primaryItemGroup'])

        if 'primaryProductReviewRating' in item:
            self.primaryProductReviewRating = ReviewRating(item['primaryProductReviewRating'])

        if 'product' in item:
            self.product = Product(item['product'])

        if 'returnTerms' in item:
            self.returnTerms = ItemReturnTerms(item['returnTerms'])

        if 'seller' in item:
            self.seller = SellerDetail(item['seller'])

        if 'shippingOptions' in item:
            self.shippingOptions = [ShippingOption(option) for option in item['shippingOptions']]

        if 'shipToLocations' in item:
            self.shipToLocations = ShipToLocations(item['shipToLocations'])

        if 'taxes' in item:
            self.taxes = [Taxes(taxes) for taxes in item['taxes']]

        if 'unitPrice' in item:
            self.unitPrice = ConvertedAmount(item['unitPrice'])


class ItemSummary(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the details of a specific item
    https://developer.ebay.com/api-docs/buy/browse/types/gct:ItemSummary
    """

    def __init__(self, item_summary: dict):
        self.adultOnly = item_summary.get('adultOnly')
        self.buyingOptions = item_summary.get('buyingOptions')
        self.conditionId = item_summary.get('conditionId')
        self.itemHref = item_summary.get('itemHref')
        self.itemId = item_summary.get('itemId')
        self.itemWebUrl = item_summary.get('itemWebUrl')
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

        if 'price' in item_summary:
            self.price = ConvertedAmount(item_summary['price'])

        if 'image' in item_summary:
            self.image = Image(item_summary['image'])

        if 'itemLocation' in item_summary:
            self.itemLocation = ItemLocationImpl(item_summary['itemLocation'])

        if 'seller' in item_summary:
            self.seller = Seller(item_summary['seller'])

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


class CommonDescriptions(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the item IDs that all use a common description
    https://developer.ebay.com/api-docs/buy/browse/types/gct:CommonDescriptions
    """

    def __init__(self, description: dict):
        self.description = description.get('description')
        self.itemIds = description.get('itemIds')


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


class SellerDetail(Seller):
    """
    The type that defines the fields for the contact information for a seller
    https://developer.ebay.com/api-docs/buy/browse/types/gct:SellerLegalInfo
    """

    def __init__(self, detail: dict):
        super().__init__(detail)

        if 'sellerLegalInfo' in detail:
            self.sellerLegalInfo = SellerLegalInfo(detail['sellerLegalInfo'])


class SellerLegalInfo(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the contact information for a seller
    https://developer.ebay.com/api-docs/buy/browse/types/gct:SellerLegalInfo
    """

    def __init__(self, info: dict):
        for key in ('email',
                    'fax',
                    'imprint',
                    'legalContactFirstName',
                    'legalContactLastName',
                    'name',
                    'phone',
                    'registrationNumber',
                    'termsOfService'):
            setattr(self, key, info.get(key))

        if 'sellerProvidedLegalAddress' in info:
            self.sellerProvidedLegalAddress = Address(info['sellerProvidedLegalAddress'])

        if 'vatDetails' in info:
            self.vatDetails = [VatDetail(detail) for detail in info['vatDetails']]


class VatDetail(BrowseAPIBaseContainer):
    """
    The type the defines the fields for the VAT (value add tax) information
    https://developer.ebay.com/api-docs/buy/browse/types/gct:VatDetail
    """

    def __init__(self, detail: dict):
        for key in 'issuingCountry', 'vatId':
            setattr(self, key, detail.get(key))


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


class ShippingOption(ShippingOptionSummary):
    """
    The type that defines the fields for the details of a shipping provider
    https://developer.ebay.com/api-docs/buy/browse/types/gct:ShippingOption
    """

    def __init__(self, option: dict):
        super().__init__(option)

        for key in ('cutOffDateUsedForEstimate',
                    'fulfilledThrough',
                    'quantityUsedForEstimate',
                    'shippingCarrierCode',
                    'shippingServiceCode',
                    'trademarkSymbol',
                    'type'):
            setattr(self, key, option.get(key))

        if 'additionalShippingCostPerUnit' in option:
            self.additionalShippingCostPerUnit = ConvertedAmount(option['additionalShippingCostPerUnit'])

        if 'importCharges' in option:
            self.importCharges = ConvertedAmount(option['importCharges'])

        if 'shipToLocationUsedForEstimate' in option:
            self.shipToLocationUsedForEstimate = ShipToLocation(option['shipToLocationUsedForEstimate'])


class ShipToLocation(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the country and postal code of where an item is to be shipped
    https://developer.ebay.com/api-docs/buy/browse/types/gct:ShipToLocation
    """

    def __init__(self, location: dict):
        for key in 'country', 'postalCode':
            setattr(self, key, location.get(key))


class ShipToLocations(BrowseAPIBaseContainer):
    """
    The type that defines the fields that include and exclude geographic regions affecting where the item can be shipped
    https://developer.ebay.com/api-docs/buy/browse/types/gct:ShipToLocations
    """

    def __init__(self, locations: dict):
        if 'regionExcluded' in locations:
            self.regionExcluded = [Region(region) for region in locations['regionExcluded']]

        if 'regionIncluded' in locations:
            self.regionIncluded = [Region(region) for region in locations['regionIncluded']]


class Region(BrowseAPIBaseContainer):
    """
    The type that defines information for a region
    https://developer.ebay.com/api-docs/buy/browse/types/gct:Region
    """

    def __init__(self, region: dict):
        for key in 'regionName', 'regionType':
            setattr(self, key, region.get(key))


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


class EstimatedAvailability(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the estimated item availability information
    https://developer.ebay.com/api-docs/buy/browse/types/gct:EstimatedAvailability
    """

    def __init__(self, availability: dict):
        self.deliveryOptions = availability.get('deliveryOptions')

        for key in ('availabilityThreshold',
                    'availabilityThresholdType',
                    'estimatedAvailabilityStatus',
                    'estimatedAvailableQuantity',
                    'estimatedSoldQuantity'):
            setattr(self, key, availability.get(key))


class Address(BrowseAPIBaseContainer):
    """
    The type that defines the fields for an address
    https://developer.ebay.com/api-docs/buy/browse/types/gct:Address
    """

    def __init__(self, address: dict):
        self.addressLine1 = address.get('addressLine1')
        self.city = address.get('city')
        self.country = address.get('country')
        self.stateOrProvince = address.get('stateOrProvince')

        for key in 'addressLine2', 'county', 'postalCode':
            setattr(self, key, address.get(key))


class TypedNameValue(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the name/value pairs for item aspects
    https://developer.ebay.com/api-docs/buy/browse/types/gct:TypedNameValue
    """

    def __init__(self, typed_name: dict):
        for key in 'name', 'type', 'value':
            setattr(self, key, typed_name.get(key))


class ItemGroupSummary(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the details of each item in an item group
    https://developer.ebay.com/api-docs/buy/browse/types/gct:ItemGroupSummary
    """

    def __init__(self, summary: dict):
        for key in 'itemGroupHref', 'itemGroupId', 'itemGroupTitle', 'itemGroupType':
            setattr(self, key, summary.get(key))

        if 'itemGroupAdditionalImages' in summary:
            self.itemGroupAdditionalImages = [Image(image) for image in summary['itemGroupAdditionalImages']]

        if 'itemGroupImage' in summary:
            self.itemGroupImage = Image(summary['itemGroupImage'])


class ReviewRating(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the rating of a product review
    https://developer.ebay.com/api-docs/buy/browse/types/gct:ReviewRating
    """

    def __init__(self, review: dict):
        for key in 'averageRating', 'reviewCount':
            setattr(self, key, review.get(key))

        if 'ratingHistograms' in review:
            self.ratingHistograms = [RatingHistogram(histogram) for histogram in review['ratingHistograms']]


class RatingHistogram(BrowseAPIBaseContainer):
    """
    The type that defines the fields for product ratings
    https://developer.ebay.com/api-docs/buy/browse/types/gct:RatingHistogram
    """

    def __init__(self, histogram: dict):
        for key in 'count', 'rating':
            setattr(self, key, histogram.get(key))


class Product(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the product information of the item
    https://developer.ebay.com/api-docs/buy/browse/types/gct:Product
    """

    def __init__(self, product: dict):
        for key in 'brand', 'description', 'gtins', 'mpns', 'title':
            setattr(self, key, product.get(key))

        if 'additionalImages' in product:
            self.additionalImages = [Image(image) for image in product['additionalImages']]

        if 'additionalProductIdentities' in product:
            self.additionalProductIdentities = [AdditionalProductIdentity(identity)
                                                for identity in product['additionalProductIdentities']]

        if 'aspectGroups' in product:
            self.aspectGroups = [AspectGroup(aspect_group) for aspect_group in product['aspectGroups']]

        if 'image' in product:
            self.image = Image(product['image'])


class AdditionalProductIdentity(BrowseAPIBaseContainer):
    """
    The type that defines the array of product identifiers associated with the item
    https://developer.ebay.com/api-docs/buy/browse/types/gct:AdditionalProductIdentity
    """

    def __init__(self, identity: dict):
        if 'additionalProductIdentities' in identity:
            self.additionalProductIdentities = [ProductIdentity(identity)
                                                for identity in identity['additionalProductIdentities']]


class ProductIdentity(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the product identifier type/value pairs of product associated with an item
    https://developer.ebay.com/api-docs/buy/browse/types/gct:ProductIdentity
    """

    def __init__(self, identity: dict):
        for key in 'identifierType', 'identifierValue':
            setattr(self, key, identity.get(key))


class AspectGroup(BrowseAPIBaseContainer):
    """
    AspectGroup type
    https://developer.ebay.com/api-docs/buy/browse/types/gct:AspectGroup
    """

    def __init__(self, aspect_group: dict):
        self.localizedGroupName = aspect_group.get('localizedGroupName')

        if 'aspects' in aspect_group:
            self.aspects = [Aspect(aspect) for aspect in aspect_group['aspects']]


class Aspect(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the name/value pairs for the aspects of the product
    https://developer.ebay.com/api-docs/buy/browse/types/gct:Aspect
    """

    def __init__(self, aspect: dict):
        for key in 'localizedName', 'localizedValues':
            setattr(self, key, aspect.get(key))


class ItemReturnTerms(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the seller's return policy
    https://developer.ebay.com/api-docs/buy/browse/types/gct:ItemReturnTerms
    """

    def __init__(self, terms: dict):
        for key in ('extendedHolidayReturnsOffered',
                    'refundMethod',
                    'restockingFeePercentage',
                    'returnInstructions',
                    'returnMethod',
                    'returnsAccepted',
                    'returnShippingCostPayer'):
            setattr(self, key, terms.get(key))

        if 'returnPeriod' in terms:
            self.returnPeriod = TimeDuration(terms['returnPeriod'])


class TimeDuration(BrowseAPIBaseContainer):
    """
    The type that defines the fields for a period of time in the time-measurement units supplied
    https://developer.ebay.com/api-docs/buy/browse/types/ba:TimeDuration
    """

    def __init__(self, duration: dict):
        for key in 'unit', 'value':
            setattr(self, key, duration.get(key))


class Taxes(BrowseAPIBaseContainer):
    """
    The type that defines the tax fields
    https://developer.ebay.com/api-docs/buy/browse/types/gct:Taxes
    """

    def __init__(self, taxes: dict):
        for key in 'ebayCollectAndRemitTax', 'includedInPrice', 'shippingAndHandlingTaxed', 'taxPercentage', 'taxType':
            setattr(self, key, taxes.get(key))

        if 'taxJurisdiction' in taxes:
            self.taxJurisdiction = TaxJurisdiction(taxes['taxJurisdiction'])


class TaxJurisdiction(BrowseAPIBaseContainer):
    """
    The type that defines the fields for the tax jurisdiction details
    https://developer.ebay.com/api-docs/buy/browse/types/gct:TaxJurisdiction
    """

    def __init__(self, tax_info: dict):
        self.taxJurisdictionId = tax_info.get('taxJurisdictionId')

        if 'region' in tax_info:
            self.region = Region(tax_info['region'])


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
