CREATE OR REPLACE VIEW competitor_sentiment_gap AS

SELECT
    product,
    average_sentiment,

    ROUND(
        (
            SUM(average_sentiment) OVER ()
            - average_sentiment
        )
        /
        (COUNT(*) OVER () - 1),
        3
    ) AS competitor_avg_sentiment,

    ROUND(
        average_sentiment
        -
        (
            (
                SUM(average_sentiment) OVER ()
                - average_sentiment
            )
            /
            (COUNT(*) OVER () - 1)
        ),
        3
    ) AS competitor_sentiment_gap

FROM product_metrics;