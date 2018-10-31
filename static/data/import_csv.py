#Import CSV to Postgresql

import psycopg2
import pandas as pd
import os

#conn = psycopg2.connect("host=localhost dbname=midterm_db user=postgres password=Winchester110283")
#DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL = "postgres://spajdxucccmxnr:c02e9213c4168046fb6c5097341661c4d28dd265a9d6830f5950b0e46ad10621@ec2-23-23-153-145.compute-1.amazonaws.com:5432/ddlqkveshrq9mv"
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

df_condos = pd.read_csv('midterm.csv', encoding='ISO-8859-1')
for idx, c in df_condos.iterrows():
	cur.execute('''INSERT INTO condos (mlsnum, display_x, display_y, beds, baths, sqft, ppsf, photo_url, list_price, predicted_price, remarks) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (c.mlsnum, c.display_x, c.display_y, c.beds, c.baths, c.sqft, c.ppsf, c.photo_url, c.list_price, c.predicted_price, c.remarks))

	conn.commit()

cur.close()
conn.close()