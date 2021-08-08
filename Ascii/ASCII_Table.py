# Title: Python ASCII Table
# Description: Create ASCII Table with Pyhton from CSV file
# More info:http://buymeacoffee.com/alteredadmin/posts/python-print_tables_with_python_and_csvs/
# =====================================================
# Name: Altered Admin
# Website: https://alteredadmin.github.io/
# If you found this helpful Please consider:
# Buymeacoffee: http://buymeacoffee.com/alteredadmin
# BTC: bc1qhkw7kv9dtdk8xwvetreya2evjqtxn06cghyxt7
# LTC: ltc1q2mrh9s8sgmh8h5jtra3gqxuhvy04vuagpm3dk9
# ETH: 0xef053b0d936746Df00C9CCe0454b7b8afb1497ac


from prettytable import from_csv

with open("/path/to/CSV/file/file.csv", "r") as csvfile:
    x = from_csv(csvfile)
print(x)
