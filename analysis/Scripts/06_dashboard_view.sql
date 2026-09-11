CREATE OR REPLACE VIEW dashboard_metrics AS

SELECT
    pm.product,

    pm.average_rating,
    pm.average_sentiment,
    pm.review_volume,
    pm.negative_review_pct,
    pm.complaint_rate,
    pm.feature_request_rate,

    rg.competitor_avg_rating,
    rg.competitor_rating_gap,

    sg.competitor_avg_sentiment,
    sg.competitor_sentiment_gap

FROM product_metrics AS pm

LEFT JOIN competitor_rating_gap AS rg
    ON pm.product = rg.product

LEFT JOIN competitor_sentiment_gap AS sg
    ON pm.product = sg.product;