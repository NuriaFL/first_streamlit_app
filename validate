import snowflake.connector

# Gets the version
ctx = snowflake.connector.connect(
    user='nuriafl',
    password='Snownfl08',
    account='NL57057'
    )
cs = ctx.cursor()
try:
    cs.execute("SELECT current_version()")
    one_row = cs.fetchone()
    print(one_row[0])
finally:
    cs.close()
ctx.close()
