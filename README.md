# ALU Regex Data Extraction

A small Python script that reads a raw text log and pulls out useful data
using regex: emails, Rwanda phone numbers, times (12h/24h), and credit card
numbers. It also checks the text for anything unsafe before trusting it.

## Folder structure

```
input/    -> raw-text.txt (the sample log file)
main.py   -> all the code
output/   -> sample-output.json (result of running main.py)
```

## How to run it

```bash
python3 main.py
```

This reads `input/raw-text.txt` and writes the results to
`output/sample-output.json`.

## What it extracts

- **Emails** – found with a regex, then sorted into `official`, `alumni`,
  `si`, or `non_alu` based on the domain. A hidden version (e.g.
  `k***@alueducation.com`) is saved so full addresses aren't exposed.
- **Phone numbers** – only Rwanda numbers were used in `+250XXXXXXXXX` format.
- **Times** – both 24-hour (`14:30`) and 12-hour (`2:30 PM`) formats,
  kept in separate lists.
- **Credit cards** – matched whether written with spaces, dashes, or no
  separator, then masked to show only the last 4 digits.

## Security check

The script never treats anything in the input file as an instruction. It
also scans the text for signs of script/HTML injection or SQL-style
attacks (like `<script>` tags or `DROP TABLE`) and flags this in the
output as `threat_detected`, instead of acting on it.

## AI usage note

AI was used to help generate the realistic sample input text for testing.
All regex patterns and logic were written by me.