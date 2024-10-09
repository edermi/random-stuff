import re
import requests
import sys
import traceback

def get_tenant_domains(domain, sub_scope=None):
    def get_tenant_subscope(domain):
        return "Commercial"  # Example default, can return "DOD" or "DODCON"
    
    # Get Tenant Region subscope from Open ID configuration if not provided
    if not sub_scope:
        sub_scope = get_tenant_subscope(domain)

# Determine the correct URL based on subscope
    if sub_scope == "DOD":
        uri = "https://autodiscover-s-dod.office365.us/autodiscover/autodiscover.svc"
    elif sub_scope == "DODCON":
        uri = "https://autodiscover-s.office365.us/autodiscover/autodiscover.svc"
    else:
        uri = "https://autodiscover-s.outlook.com/autodiscover/autodiscover.svc"

    # Create the SOAP request body
    body = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:exm="http://schemas.microsoft.com/exchange/services/2006/messages" xmlns:ext="http://schemas.microsoft.com/exchange/services/2006/types" xmlns:a="http://www.w3.org/2005/08/addressing" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <soap:Header>
        <a:Action soap:mustUnderstand="1">http://schemas.microsoft.com/exchange/2010/Autodiscover/Autodiscover/GetFederationInformation</a:Action>
        <a:To soap:mustUnderstand="1">{uri}</a:To>
        <a:ReplyTo>
            <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>
        </a:ReplyTo>
    </soap:Header>
    <soap:Body>
        <GetFederationInformationRequestMessage xmlns="http://schemas.microsoft.com/exchange/2010/Autodiscover">
            <Request>
                <Domain>{domain}</Domain>
            </Request>
        </GetFederationInformationRequestMessage>
    </soap:Body>
</soap:Envelope>"""

    # Create the headers
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": '"http://schemas.microsoft.com/exchange/2010/Autodiscover/Autodiscover/GetFederationInformation"',
    }

# Use a prepared request to capture the final request details
    session = requests.Session()
    req = requests.Request('POST', uri, data=body, headers=headers)
    prepared_request = session.prepare_request(req)

    try:
        # Send the POST request
        response = session.send(prepared_request)
        response_text = response.content.decode('utf-8', errors='ignore')

        domain_pattern = re.compile(r'<Domain>(.*?)</Domain>')
        domains = domain_pattern.findall(response_text)

        # Add the original domain if it's not already in the list
        if domain not in domains:
            domains.append(domain)

        # Return the sorted list of domains
        return sorted(domains)

    except requests.exceptions.HTTPError as http_err:
        print("HTTP error occurred:", http_err)
    except Exception as e:
        print(f"Error fetching tenant domains: {e}")
        traceback.print_exc()


if __name__ == '__main__':
    domains = get_tenant_domains(sys.argv[1])
    print('\n'.join(domains))

