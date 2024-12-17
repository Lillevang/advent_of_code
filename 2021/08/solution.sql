-- Setup table
CREATE TABLE day8(line_number integer NOT NULL GENERATED ALWAYS AS IDENTITY, line text);

-- Imported data in dbeaver from a csv file with 1 column
-- vacuum analyze day8;

-- Debug:
--select * from day8, split_part(line, ' | ', 2) display, regexp_split_to_table(display, ' ') digit;

-- Part one:
select count(*) from day8, split_part(line, ' | ', 2) display, regexp_split_to_table(display, ' ') digit where length(digit) = any(array[2,3,4,7]);

-- Part two

select
  sum(number_map.figure) as "Answer!!"
from
  day8,
  split_part(line, ' | ', 1) raw,
  split_part(line, ' | ', 2) digits,
  lateral (
    -- this part assigns numbers
    with parsed as (
      select
        array_agg(signal_char order by signal_char) as signal
      from
        regexp_split_to_table(raw, ' ') signal,
        regexp_split_to_table(signal, '') signal_char
      group by signal
    ),
    easy_ones as (
      select
        signal,
        case
        when cardinality(signal) = 2 then
          '1'
        when cardinality(signal) = 3 then
          '7'
        when cardinality(signal) = 4 then
          '4'
        when cardinality(signal) = 7 then
          '8'
        else
          null
        end figure
      from
        parsed
      ),
    with_3_6_9_0 as (
      select
        *
      from
        easy_ones
      where figure is not null
      union
      select
        signal,
        case
        -- 3 is the only number with 5 segments that "contains" 1
        when cardinality(signal) = 5 and exists (
            select
            from easy_ones e
            where
              figure = '1'
              and ea.signal @> e.signal
          )
        then
          '3'
        -- for 6 segments numbers
        when cardinality(signal) = 6 then
          case
            -- 6 is the only one not containing segments from 1
            when not exists (select from easy_ones e where figure = '1' and ea.signal @> e.signal) then
              '6'
            -- 9 contains 4
            when exists (select from easy_ones e where figure = '4' and ea.signal @> e.signal) then
              '9'
            else
              '0'
          end
        else
          null
        end
      from easy_ones ea
      where figure is null
    ), complete_map as (
      select
        *
      from
        with_3_6_9_0 wi
      where figure is not null

      union

      select
        signal,
        case
          -- 5 is contained into 6
          when exists (select signal from with_3_6_9_0 w where figure='6' and w.signal @> wi.signal) then
            '5'
          else
            '2'
        end
      from
        with_3_6_9_0 wi
      where figure is null
    ),
    -- let's parse the digits
    digits as (
      select
        idx, array_agg(digit_char order by digit_char) digits
      from
        regexp_split_to_table(digits, ' ') with ordinality _(digit, idx),
        regexp_split_to_table(digit, '') digit_char
      group by idx, digit
    )
    -- and finally do the translation
    select
      string_agg(figure, '' order by idx)::int as figure
    from
      digits
      join complete_map on digits.digits = complete_map.signal
  ) number_map
