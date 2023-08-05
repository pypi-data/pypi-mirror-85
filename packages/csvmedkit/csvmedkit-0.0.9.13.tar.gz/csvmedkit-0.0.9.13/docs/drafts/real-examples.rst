

**********
csvflatten
**********

- Stop-n-frisk/police data: combine with csvgrep to pick specific rows by id or by category, e.g.

    - csvgrep -c 'race' -m 'W' | csvflatten -P -L 45


**********
csvreplace
**********

::
    $  cat examples/realdata/fec-independent-exp.csv \
        | csvswitch -c candidate_last_name -r '(?i)trump' 'TRUMP' \
            -r '(?i)biden' 'BIDEN' \
            --else 'OTHER' \
        | csvpivot -r candidate_last_name,support_oppose_indicator -a sum:expenditure_amount

