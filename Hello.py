import streamlit as st

# Initialize connection.
conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from actor;', ttl=600)

# Print results.
for row in df.itertuples():
    st.write(f"{row.first_name} {row.last_name}")