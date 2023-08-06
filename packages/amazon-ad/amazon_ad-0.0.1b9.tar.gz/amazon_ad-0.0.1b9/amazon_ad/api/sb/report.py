# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)

from amazon_ad.api.base import ZADOpenAPI

ALLOW_REPORT_TYPES = [
    "campaigns",
    "adGroups",
    "keywords",
]


DEFAULT_REPORT_METRICS = {
    "campaigns":  [
        "campaignName",
        "campaignId",
        "campaignStatus",
        "campaignBudget",
        "campaignBudgetType",
        "impressions",
        "clicks",
        "cost",
        "attributedDetailPageViewsClicks14d",
        "attributedSales14d",
        "attributedSales14dSameSKU",
        "attributedConversions14d",
        "attributedConversions14dSameSKU",
        "attributedOrdersNewToBrand14d",
        "attributedOrdersNewToBrandPercentage14d",
        "attributedOrderRateNewToBrand14d",
        "attributedSalesNewToBrand14d",
        "attributedSalesNewToBrandPercentage14d",
        "attributedUnitsOrderedNewToBrand14d",
        "attributedUnitsOrderedNewToBrandPercentage14d",
        "unitsSold14d",
        "dpv14d",
    ],
    "adGroups": [
        "campaignName",
        "campaignId",
        "campaignStatus",
        "campaignBudget",
        "campaignBudgetType",
        "adGroupName",
        "adGroupId",
        "impressions",
        "clicks",
        "cost",
        "attributedDetailPageViewsClicks14d",
        "attributedSales14d",
        "attributedSales14dSameSKU",
        "attributedConversions14d",
        "attributedConversions14dSameSKU",
        "attributedOrdersNewToBrand14d",
        "attributedOrdersNewToBrandPercentage14d",
        "attributedOrderRateNewToBrand14d",
        "attributedSalesNewToBrand14d",
        "attributedSalesNewToBrandPercentage14d",
        "attributedUnitsOrderedNewToBrand14d",
        "attributedUnitsOrderedNewToBrandPercentage14d",
        "unitsSold14d",
        "dpv14d",
    ],
    "keywords": [
        "campaignName",
        "campaignId",
        "campaignStatus",
        "campaignBudget",
        "campaignBudgetType",
        "adGroupName",
        "adGroupId",
        "keywordText",
        "keywordBid",
        "keywordStatus",
        "targetId",
        "targetingExpression",
        "targetingText",
        "targetingType",
        "matchType",
        "impressions",
        "clicks",
        "cost",
        "attributedDetailPageViewsClicks14d",
        "attributedSales14d",
        "attributedSales14dSameSKU",
        "attributedConversions14d",
        "attributedConversions14dSameSKU",
        "attributedOrdersNewToBrand14d",
        "attributedOrdersNewToBrandPercentage14d",
        "attributedOrderRateNewToBrand14d",
        "attributedSalesNewToBrand14d",
        "attributedSalesNewToBrandPercentage14d",
        "attributedUnitsOrderedNewToBrand14d",
        "attributedUnitsOrderedNewToBrandPercentage14d",
        "unitsSold14d",
        "dpv14d",
    ],
    # "all": [
    #     "campaignName",
    #     "campaignId",
    #     "campaignStatus",
    #     "campaignBudget",
    #     "campaignBudgetType",
    #     "adGroupName",
    #     "adGroupId",
    #     "keywordText",
    #     "keywordBid",
    #     "keywordStatus",
    #     "targetId",
    #     "targetingExpression",
    #     "targetingText",
    #     "targetingType",
    #     "matchType",
    #     "impressions",
    #     "clicks",
    #     "cost",
    #     "attributedDetailPageViewsClicks14d",
    #     "attributedSales14d",
    #     "attributedSales14dSameSKU",
    #     "attributedConversions14d",
    #     "attributedConversions14dSameSKU",
    #     "attributedOrdersNewToBrand14d",
    #     "attributedOrdersNewToBrandPercentage14d",
    #     "attributedOrderRateNewToBrand14d",
    #     "attributedSalesNewToBrand14d",
    #     "attributedSalesNewToBrandPercentage14d",
    #     "attributedUnitsOrderedNewToBrand14d",
    #     "attributedUnitsOrderedNewToBrandPercentage14d",
    #     "unitsSold14d",
    #     "dpv14d",
    # ],

}

AVAILABLE_VIDEO_REPORT_METRICS = [
    "campaignName",
    "campaignId",
    "campaignStatus",
    "campaignBudget",
    "campaignBudgetType",
    "adGroupName",
    "adGroupId",
    "keywordText",
    "keywordBid",
    "keywordStatus",
    "targetId",
    "targetingExpression",
    "targetingText",
    "targetingType",
    "matchType",
    "impressions",
    "clicks",
    "cost",
    "attributedSales14d",
    "attributedSales14dSameSKU",
    "attributedConversions14d",
    "attributedConversions14dSameSKU",
]


DEFAULT_REPORT_DIMENSIONAL = {
    "keywords": "query",
    "campaigns": "placement"
}

DEFAULT_CREATIVE_TYPE = [
    "video"
]

class SbReport(ZADOpenAPI):
    def request(self, record_type, report_date, metrics, segment=None, creative_type=None):
        path = '/v2/hsa/{record_type}/report'.format(record_type=record_type)

        if creative_type:
            metrics = list(set(metrics).intersection(set(AVAILABLE_VIDEO_REPORT_METRICS)))

        if isinstance(metrics, (list, tuple)):
            metrics = ','.join(metrics)


        data = {
           'reportDate': report_date,
           'metrics': metrics
        }

        if segment:
            data['segment'] = segment

        if creative_type:
            data['creativeType'] = creative_type

        return self.post(path, data)


    def _get_metrics(self, metrics, default):
        if not metrics:
            metrics = default

        return metrics

    def campaigns(self, report_date, metrics=None, creative_type=None):

        metrics = self._get_metrics(metrics, DEFAULT_REPORT_METRICS.get('campaigns'))

        return self.request('campaigns', report_date, metrics, creative_type=creative_type)

    def placements(self, report_date, metrics=None, creative_type=None):

        segment = DEFAULT_REPORT_DIMENSIONAL.get('campaigns')

        metrics = self._get_metrics(metrics, DEFAULT_REPORT_METRICS.get('campaigns'))

        return self.request('campaigns', report_date, metrics, segment, creative_type)

    def ad_groups(self, report_date, metrics=None, creative_type=None):

        metrics = self._get_metrics(metrics, DEFAULT_REPORT_METRICS.get('adGroups'))

        return self.request('adGroups', report_date, metrics, creative_type=creative_type)

    def keywords(self, report_date, metrics=None, creative_type=None):

        metrics = self._get_metrics(metrics, DEFAULT_REPORT_METRICS.get('keywords'))

        return self.request('keywords', report_date, metrics, creative_type=creative_type)

    def queries(self, report_date, metrics=None, creative_type=None):

        segment = DEFAULT_REPORT_DIMENSIONAL.get('keywords')

        metrics = self._get_metrics(metrics, DEFAULT_REPORT_METRICS.get('keywords'))

        not_allow_metrics = [
            "targetingType",
            "targetingExpression",
            "targetId",
            "targetingText",
            "attributedSales14dSameSKU",
            "attributedUnitsOrderedNewToBrand14d",
            "attributedOrdersNewToBrand14d",
            "attributedOrdersNewToBrandPercentage14d",
            "attributedSalesNewToBrand14d",
            "attributedUnitsOrderedNewToBrandPercentage14d",
            "unitsSold14d",
            "attributedOrderRateNewToBrand14d",
            "attributedSalesNewToBrandPercentage14d",
            "dpv14d",
            "attributedConversions14dSameSKU",
            "attributedDetailPageViewsClicks14d",
        ]

        metrics = list(set(metrics).difference(set(not_allow_metrics)))

        return self.request('keywords', report_date, metrics, segment, creative_type)
