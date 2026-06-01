-- 1. Количество полисов, сумма премий и страховая сумма по видам страхования.
SELECT
    product_type,
    COUNT(*) AS policies_count,
    ROUND(SUM(premium), 2) AS total_premium,
    ROUND(SUM(insured_amount), 2) AS total_insured_amount
FROM policies
GROUP BY product_type
ORDER BY total_premium DESC;

-- 2. Портфель клиентов: количество полисов и общая сумма страховых премий.
SELECT
    c.id,
    c.full_name,
    COUNT(p.id) AS policies_count,
    COALESCE(ROUND(SUM(p.premium), 2), 0) AS total_premium
FROM clients c
LEFT JOIN policies p ON p.client_id = c.id
GROUP BY c.id, c.full_name
ORDER BY total_premium DESC;

-- 3. Статистика страховых случаев по статусам.
SELECT
    status,
    COUNT(*) AS claims_count,
    ROUND(SUM(amount), 2) AS total_claim_amount
FROM claims
GROUP BY status
ORDER BY total_claim_amount DESC;

-- 4. Убыточность по видам страхования.
SELECT
    p.product_type,
    ROUND(SUM(COALESCE(policy_claims.total_claims, 0)), 2) AS total_claims,
    ROUND(SUM(p.premium), 2) AS total_premium,
    ROUND(
        SUM(COALESCE(policy_claims.total_claims, 0)) * 100.0 / SUM(p.premium),
        2
    ) AS loss_ratio_percent
FROM policies p
LEFT JOIN (
    SELECT policy_id, SUM(amount) AS total_claims
    FROM claims
    GROUP BY policy_id
) policy_claims ON policy_claims.policy_id = p.id
GROUP BY p.product_type
ORDER BY loss_ratio_percent DESC;
