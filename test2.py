from ASGSConstants import ASGSConstants

ASGSConstants_inst = ASGSConstants()

site_id = [10,2]
print(site_id[0])

renci = ASGSConstants_inst.getLuId('RENCI', 'site')
tacc = ASGSConstants_inst.getLuId('TACC', 'site')
lsu = ASGSConstants_inst.getLuId('LSU', 'site')
penguin = ASGSConstants_inst.getLuId('Penguin', 'site')
loni = ASGSConstants_inst.getLuId('LONI', 'site')
seahorse = ASGSConstants_inst.getLuId('Seahorse', 'site')
qb2 = ASGSConstants_inst.getLuId('QB2', 'site')
cct = ASGSConstants_inst.getLuId('CCT', 'site')
psc = ASGSConstants_inst.getLuId('PSC', 'site')

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
