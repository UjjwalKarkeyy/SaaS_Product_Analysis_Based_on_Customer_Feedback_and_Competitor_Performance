CREATE OR REPLACE VIEW all_reviews AS

SELECT
    'Zoom' AS product,
    reviewId,
    rating,
    body,
    timestamp,
    sentiment_label,
    complaint_flag,
    category,
    TRY_CAST(is_feature_request AS BOOLEAN) AS is_feature_request
FROM 'd:/GitHub/SaaS_Product_Analysis/data/export_data/zoom.csv'

UNION ALL

SELECT
    'Teams' AS product,
    reviewId,
    rating,
    body,
    timestamp,
    sentiment_label,
    complaint_flag,
    category,
    TRY_CAST(is_feature_request AS BOOLEAN) AS is_feature_request
FROM 'd:/GitHub/SaaS_Product_Analysis/data/export_data/teams.csv'


UNION ALL

SELECT
    'Meet' AS product,
    reviewId,
    rating,
    body,
    timestamp,
    sentiment_label,
    complaint_flag,
    category,
    TRY_CAST(is_feature_request AS BOOLEAN) AS is_feature_request
FROM 'd:/GitHub/SaaS_Product_Analysis/data/export_data/meet.csv'


UNION ALL

SELECT
    'Webex' AS product,
    reviewId,
    rating,
    body,
    timestamp,
    sentiment_label,
    complaint_flag,
    category,
    TRY_CAST(is_feature_request AS BOOLEAN) AS is_feature_request
FROM 'd:/GitHub/SaaS_Product_Analysis/data/export_data/webex.csv';

