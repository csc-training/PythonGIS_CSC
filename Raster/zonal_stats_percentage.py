
def get_zonal_stats_percentage(zstats):

    zstat_perc = {}
    sum = 0
    total = zstats[0]['count']
    for key in zstats[0].keys():
        if not key == 'count':
            amount = zstats[0][key]
            perc=  round(amount/total *100)
            zstat_perc[key] = perc
            sum += perc
    
    return zstat_perc