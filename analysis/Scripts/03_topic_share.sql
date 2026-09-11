CREATE OR REPLACE VIEW topic_share AS

SELECT
    product,
    category,

    COUNT(*) AS topic_review_count,

    ROUND(
        100.0 * COUNT(*)
        / SUM(COUNT(*)) OVER (
            PARTITION BY product
        ),
        2
    ) AS topic_share_pct

FROM all_reviews

GROUP BY
    product,
    category;