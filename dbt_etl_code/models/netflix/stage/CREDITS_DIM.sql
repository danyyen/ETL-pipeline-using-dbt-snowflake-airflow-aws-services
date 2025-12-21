{{ config(
    pre_hook="ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE = true",
    tags=[var('TAG_DIMENSION')]
) }}

SELECT *
FROM {{ source('netflix', 'CREDITS') }}
WHERE ROLE IN ('ACTOR', 'DIRECTOR')
