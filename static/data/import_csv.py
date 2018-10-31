#Import CSV to Postgresql

import psycopg2
import pandas as pd

conn = psycopg2.connect("host=localhost dbname=midterm_db user=postgres password=Winchester110283")
cur = conn.cursor()

df_condos = pd.read_csv('midterm.csv', encoding='ISO-8859-1')
for idx, c in df_condos.iterrows():
	cur.execute('''INSERT INTO condos (mlsnum, display_x, display_y, beds, baths, sqft, ppsf, photo_url, list_price, predicted_price, remarks) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (c.mlsnum, c.display_x, c.display_y, c.beds, c.baths, c.sqft, c.ppsf, c.photo_url, c.list_price, c.predicted_price, c.remarks))

	conn.commit()

cur.close()
conn.close()