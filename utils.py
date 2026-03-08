from wit import Wit

access_token = "CXJKOMJHNPQ2V2BJFJIJEYB6MUO6XJAJ"

client = Wit(access_token = access_token)

def wit_response(message_text):
    resp = client.message(message_text)
    print("Wit.ai Response:", resp)

    entity = None
    value = None

    try:
        entity = list(resp['entities'])[0]
        value = resp['entities'][entity][0]['value']
    except:
        pass

    return (entity, value)

print(wit_response("je veux un pantalon"))
