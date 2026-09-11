CREATE OR REPLACE VIEW competitor_rating_gap AS

SELECT
    product,
    average_rating,

    ROUND(
        (
            SUM(average_rating) OVER ()
            - average_rating
        )
        /
        (COUNT(*) OVER () - 1),
        2
    ) AS competitor_avg_rating,

    ROUND(
        average_rating
        -
        (
            (
                SUM(average_rating) OVER ()
                - average_rating
            )
            /
            (COUNT(*) OVER () - 1)
        ),
        2
    ) AS competitor_rating_gap

FROM product_metrics;