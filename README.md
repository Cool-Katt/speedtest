# speedtest scraper and ETL
Scrapes data from the speedtest server and imports to DB.

## Prerequisites:
- pandas, numpy, sqlalchemy, pymssql, dotenv for Python
- pyinstaller and pkg to compile 
- node, puppeteer for JS part

## To compile and use:
`pkg -t win speedtest.js` for JS part

`pyinstaller --onefile --hidden-import "pymssql" --hidden-import "numpy"  main.py` for Python part

## To run:
1. compile .exe files
2. make sure your .env contains the nescesarry credentials (see example file)
3. put .exe files in the same dirrectory as your .env file
4. run main.exe 
