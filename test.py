site_id = [3,2]
renci = 0
tacc = 1
lsu = 2
penguin = 5
loni = 6
seahorse = 7
qb2 = 8
cct = 9
psc = 10
print(site_id[0])
print(lsu)
if (
    (site_id[0] == renci) or
    (site_id[0] == tacc) or
    (site_id[0] == lsu) or
    (site_id[0] == penguin) or
    (site_id[0] == loni) or
    (site_id[0] == seahorse) or
    (site_id[0] == qb2) or
    (site_id[0] == cct) or
    (site_id[0] == psc)
):
    print("accepted run")
else:
    print("run not accepted")

status = "new"
if (
    (site_id[0] != renci) and
    (site_id[0] != tacc) and
    (site_id[0] != penguin) and
    (site_id[0] != psc)
):
    status = "hazus"

print(status)
