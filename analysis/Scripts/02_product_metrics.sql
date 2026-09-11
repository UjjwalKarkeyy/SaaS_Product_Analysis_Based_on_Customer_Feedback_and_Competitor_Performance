/*
 - Average Rating
 - Average Sentiment
 - Review Volume
 - Negative Review %
 - Complaint Rate
 - Feature Request Rate
 */

CREATE OR REPLACE VIEW product_metrics AS

SELECT
    product,

    ROUND(AVG(rating), 2) AS average_rating,

    ROUND(
        AVG(
            CASE
                WHEN LOWER(sentiment_label) = 'positive' THEN 1
                WHEN LOWER(sentiment_label) = 'negative' THEN -1
                ELSE 0
            END
        ),
        3
    ) AS average_sentiment,

    COUNT(*) AS review_volume,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE LOWER(sentiment_label) = 'negative'
        )
        / COUNT(*),
        2
    ) AS negative_review_pct,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE LOWER(complaint_flag) = 'complaint'
        )
        / COUNT(*),
        2
    ) AS complaint_rate,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE is_feature_request = TRUE
        )
        / COUNT(*),
        2
    ) AS feature_request_rate

FROM all_reviews

GROUP BY product;

