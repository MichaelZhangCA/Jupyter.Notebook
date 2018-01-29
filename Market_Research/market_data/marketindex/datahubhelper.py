from datapackage import Package

def get_sp500_constituent():

    package = Package('http://datahub.io/core/s-and-p-500-companies/datapackage.json')

    # get list of resources:
    resources = package.descriptor['resources']
    resourceList = [resources[x]['name'] for x in range(0, len(resources))]
    
    # grab the constituent from package
    lst = package.resources[1].read()
    # conver to a dict list, to keep compatibilty of WIKI page helper function
    dic = []
    for row in lst:
        dic.append({'symbol': row[0], 'company': row[1]})
    
    return dic


