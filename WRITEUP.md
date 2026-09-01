# Data issues found and handling

- Exact duplicate rows, fully identical across every column, dropped via drop_duplicates()
- Status = 'test' - test data which was excluded
- Customer id null, excluded from orders_clean
- Category null, also excluded from orders_clean
- Negative quantities
- Unit price <1 (also the upper margin of 99999)

After removing all those I was left wth 8693 rows in orders_clean.

When first creating orders_clean too many rows have been removed. This had me checking the data manually and finding that some order dupes are fully duped (like 2 identical orders for earbuds), while some others have the same order id, customer, time, but different products and quantities. I assume those are valid orders as well but without a possibility to store 2 products in the same column the order gets duped.
Triple checked from all directions just to find out it was a terminal problem.

# How I'd monitor this in production

If the daily job  failed, I'd want to know without having to check manually.

I'd put my faith in the github failure notifications, and maybe create some other daily jobs to keep the rates updated and monitor any of the listed above problems.


# AI usage

I used Claude to renew some SQL syntax that has left my brain due to me not using it, mostly on point 4, and to automate the daily job which was pretty new to me. Besides that It was more like a debugging help, pulling some tips and tricks out of its hat every now and then.