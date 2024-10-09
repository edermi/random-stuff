import requests
import sys

def get_tenant_id(domain=None):
    try:
        response = requests.get(f"https://odc.officeapps.live.com/odc/v2.1/federationprovider?domain={domain}")
        response.raise_for_status()
        tenant_id = response.json().get('tenantId')
    except Exception as e:
        print(f"Error fetching tenant ID: {e}")
        return None

    return tenant_id

if __name__ == '__main__':
    print(get_tenant_id(sys.argv[1]))
