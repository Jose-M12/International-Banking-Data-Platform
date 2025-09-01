{% macro get_market_tz(col) -%}
case
  when {{ col }} = 'MX' then 'America/Mexico_City'
  when {{ col }} = 'CO' then 'America/Bogota'
  when {{ col }} = 'PE' then 'America/Lima'
  else 'UTC'
end
{%- endmacro %}
