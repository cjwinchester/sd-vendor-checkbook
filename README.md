# South Dakota vendor checkbook data
Some Python to poke at the state of South Dakota's [checkbook-level vendor payment data](https://open.sd.gov/vendor.aspx).

`fetch_latest_data.py` grabs the three files offered on the state website and combines them into one local file, `sd-vendor-checkbook.csv`. (Thereafter, the data fetched from the website is also combined with data cached in the local file, which is tracked with [`git-lfs`](https://git-lfs.github.com/).)

`fetch_agency_codes.py` scrapes [a table of agency codes mapped to agency names](https://bfm.sd.gov/vendor/contactinfo.asp) and saves them to file, `sd-agency-codes.csv`.

`Find duplicate vendor numbers.ipynb` is a Jupyter notebook with code to discover `vendor_number`s that map to more than one `vendor_name`. (A preliminary look suggests they point to the same entity, just entered inconsistently.)

`Analyze checkbook data.ipynb` is a Jupyter notebook with some scaffolding to work with the data in pandas.
