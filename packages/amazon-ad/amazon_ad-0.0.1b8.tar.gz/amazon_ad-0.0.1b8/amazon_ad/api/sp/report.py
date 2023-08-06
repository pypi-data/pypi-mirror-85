# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)

from amazon_ad.api.base import ZADOpenAPI

ALLOW_REPORT_TYPES = [
    "campaigns",
    "adGroups",
    "keywords",
    "productAds",
    "targets"
]


DEFAULT_REPORT_METRICS = {
    "campaigns":  [
        # "bidPlus",
        "campaignName",
        "campaignId",
        "campaignStatus",
        "campaignBudget",
        "impressions",
        "clicks",
        "cost",
        "attributedConversions1d",
        "attributedConversions7d",
        "attributedConversions14d",
        "attributedConversions30d",
        "attributedConversions1dSameSKU",
        "attributedConversions7dSameSKU",
        "attributedConversions14dSameSKU",
        "attributedConversions30dSameSKU",
        "attributedUnitsOrdered1d",
        "attributedUnitsOrdered7d",
        "attributedUnitsOrdered14d",
        "attributedUnitsOrdered30d",
        "attributedSales1d",
        "attributedSales7d",
        "attributedSales14d",
        "attributedSales30d",
        "attributedSales1dSameSKU",
        "attributedSales7dSameSKU",
        "attributedSales14dSameSKU",
        "attributedSales30dSameSKU",
        "attributedUnitsOrdered1dSameSKU",
        "attributedUnitsOrdered7dSameSKU",
        "attributedUnitsOrdered14dSameSKU",
        "attributedUnitsOrdered30dSameSKU",
    ],
    "adGroups": [
        "campaignName",
        "campaignId",
        "adGroupName",
        "adGroupId",
        "impressions",
        "clicks",
        "cost",
        "attributedConversions1d",
        "attributedConversions7d",
        "attributedConversions14d",
        "attributedConversions30d",
        "attributedConversions1dSameSKU",
        "attributedConversions7dSameSKU",
        "attributedConversions14dSameSKU",
        "attributedConversions30dSameSKU",
        "attributedUnitsOrdered1d",
        "attributedUnitsOrdered7d",
        "attributedUnitsOrdered14d",
        "attributedUnitsOrdered30d",
        "attributedSales1d",
        "attributedSales7d",
        "attributedSales14d",
        "attributedSales30d",
        "attributedSales1dSameSKU",
        "attributedSales7dSameSKU",
        "attributedSales14dSameSKU",
        "attributedSales30dSameSKU",
        "attributedUnitsOrdered1dSameSKU",
        "attributedUnitsOrdered7dSameSKU",
        "attributedUnitsOrdered14dSameSKU",
        "attributedUnitsOrdered30dSameSKU",
    ],
    "keywords": [
        "campaignName",
        "campaignId",
        "adGroupName",
        "adGroupId",
        "keywordId",
        "keywordText",
        "matchType",
        "impressions",
        "clicks",
        "cost",
        "attributedConversions1d",
        "attributedConversions7d",
        "attributedConversions14d",
        "attributedConversions30d",
        "attributedConversions1dSameSKU",
        "attributedConversions7dSameSKU",
        "attributedConversions14dSameSKU",
        "attributedConversions30dSameSKU",
        "attributedUnitsOrdered1d",
        "attributedUnitsOrdered7d",
        "attributedUnitsOrdered14d",
        "attributedUnitsOrdered30d",
        "attributedSales1d",
        "attributedSales7d",
        "attributedSales14d",
        "attributedSales30d",
        "attributedSales1dSameSKU",
        "attributedSales7dSameSKU",
        "attributedSales14dSameSKU",
        "attributedSales30dSameSKU",
        "attributedUnitsOrdered1dSameSKU",
        "attributedUnitsOrdered7dSameSKU",
        "attributedUnitsOrdered14dSameSKU",
        "attributedUnitsOrdered30dSameSKU",
    ],
    "productAds": [
        # "bidPlus",
        "campaignName",
        "campaignId",
        "adGroupName",
        "adGroupId",
        "impressions",
        "clicks",
        "cost",
        "currency",
        "asin",
        "sku",
        "attributedConversions1d",
        "attributedConversions7d",
        "attributedConversions14d",
        "attributedConversions30d",
        "attributedConversions1dSameSKU",
        "attributedConversions7dSameSKU",
        "attributedConversions14dSameSKU",
        "attributedConversions30dSameSKU",
        "attributedUnitsOrdered1d",
        "attributedUnitsOrdered7d",
        "attributedUnitsOrdered14d",
        "attributedUnitsOrdered30d",
        "attributedSales1d",
        "attributedSales7d",
        "attributedSales14d",
        "attributedSales30d",
        "attributedSales1dSameSKU",
        "attributedSales7dSameSKU",
        "attributedSales14dSameSKU",
        "attributedSales30dSameSKU",
        "attributedUnitsOrdered1dSameSKU",
        "attributedUnitsOrdered7dSameSKU",
        "attributedUnitsOrdered14dSameSKU",
        "attributedUnitsOrdered30dSameSKU",
    ],
    "targets": [
        "campaignName",
        "campaignId",
        "adGroupName",
        "adGroupId",
        "targetId",
        "targetingExpression",
        "targetingText",
        "targetingType",
        "impressions",
        "clicks",
        "cost",
        "attributedConversions1d",
        "attributedConversions7d",
        "attributedConversions14d",
        "attributedConversions30d",
        "attributedConversions1dSameSKU",
        "attributedConversions7dSameSKU",
        "attributedConversions14dSameSKU",
        "attributedConversions30dSameSKU",
        "attributedUnitsOrdered1d",
        "attributedUnitsOrdered7d",
        "attributedUnitsOrdered14d",
        "attributedUnitsOrdered30d",
        "attributedSales1d",
        "attributedSales7d",
        "attributedSales14d",
        "attributedSales30d",
        "attributedSales1dSameSKU",
        "attributedSales7dSameSKU",
        "attributedSales14dSameSKU",
        "attributedSales30dSameSKU",
        "attributedUnitsOrdered1dSameSKU",
        "attributedUnitsOrdered7dSameSKU",
        "attributedUnitsOrdered14dSameSKU",
        "attributedUnitsOrdered30dSameSKU",
    ],
    "asins": [
        "campaignName",
        "campaignId",
        "adGroupName",
        "adGroupId",
        "keywordId",
        "keywordText",
        "asin",
        "otherAsin",
        "sku",
        "currency",
        "matchType",
        "attributedUnitsOrdered1d",
        "attributedUnitsOrdered7d",
        "attributedUnitsOrdered14d",
        "attributedUnitsOrdered30d",
        "attributedUnitsOrdered1dOtherSKU",
        "attributedUnitsOrdered7dOtherSKU",
        "attributedUnitsOrdered14dOtherSKU",
        "attributedUnitsOrdered30dOtherSKU",
        "attributedSales1dOtherSKU",
        "attributedSales7dOtherSKU",
        "attributedSales14dOtherSKU",
        "attributedSales30dOtherSKU",
    ]
}


DEFAULT_REPORT_DIMENSIONAL = {
    "keywords": "query",
    "campaigns": "placement"
}

class SpReport(ZADOpenAPI):
    def request(self, record_type, report_date, metrics, segment=None):
        if record_type == 'asins':
            path = '/v2/{record_type}/report'.format(record_type=record_type)
        else:
            path = '/v2/sp/{record_type}/report'.format(record_type=record_type)

        if self._client.account_type == "vendor" and record_type in ["productAds", "asins"]:
            if 'sku' in metrics:
                metrics.remove("sku")

        if isinstance(metrics, (list, tuple)):
            metrics = ','.join(metrics)

        data = {
           'reportDate': report_date,
           'metrics': metrics
        }

        if record_type == 'asins':
            data['campaignType'] = 'sponsoredProducts'

        if segment:
            data['segment'] = segment
        return self.post(path, data)


    def _get_metrics(self, metrics, default):
        if not metrics:
            metrics = default

        return metrics

    def campaigns(self, report_date, metrics=None):

        metrics = self._get_metrics(metrics, DEFAULT_REPORT_METRICS.get('campaigns'))

        return self.request('campaigns', report_date, metrics)

    def placements(self, report_date, metrics=None):

        segment = DEFAULT_REPORT_DIMENSIONAL.get('campaigns')

        metrics = self._get_metrics(metrics, DEFAULT_REPORT_METRICS.get('campaigns'))

        return self.request('campaigns', report_date, metrics, segment)

    def ad_groups(self, report_date, metrics=None):

        metrics = self._get_metrics(metrics, DEFAULT_REPORT_METRICS.get('adGroups'))

        return self.request('adGroups', report_date, metrics)

    def keywords(self, report_date, metrics=None):

        metrics = self._get_metrics(metrics, DEFAULT_REPORT_METRICS.get('keywords'))

        return self.request('keywords', report_date, metrics)

    def queries(self, report_date, metrics=None):

        segment = DEFAULT_REPORT_DIMENSIONAL.get('keywords')

        metrics = self._get_metrics(metrics, DEFAULT_REPORT_METRICS.get('keywords'))

        return self.request('keywords', report_date, metrics, segment)

    def product_ads(self, report_date, metrics=None):

        metrics = self._get_metrics(metrics, DEFAULT_REPORT_METRICS.get('productAds'))

        return self.request('productAds', report_date, metrics)

    def targets(self, report_date, metrics=None):

        metrics = self._get_metrics(metrics, DEFAULT_REPORT_METRICS.get('targets'))

        return self.request('targets', report_date, metrics)

    def asins(self, report_date, metrics=None):

        metrics = self._get_metrics(metrics, DEFAULT_REPORT_METRICS.get('asins'))

        return self.request('asins', report_date, metrics)
