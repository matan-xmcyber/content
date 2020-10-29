#first section copies over from context to incident fields

fields = {
    'entityId': 'xmcyberentityid',
    'averageComplexity': 'xmcyberaveragecomplexity',
    'averageComplexityLevel': 'xmcyberaveragecomplexitylevel',
    'affectedEntities': 'xmcyberaffectedentities',
    'entitiesAtRiskList': 'xmcyberaffectedentitieslist',
    'compromisingTechniques': 'xmcybercompromisingtechniques',
    'criticalAssetsAtRisk': 'xmcybercriticalassetsatrisk',
    'criticalAssetsAtRiskLevel': 'xmcybercriticalassetsatrisklevel',
    'criticalAssetsAtRiskList':'xmcybercriticalassetsatrisklist',
    'isAsset': 'xmcybercriticalasset',
    'entityType': 'xmcyberentitytype',
    'name': 'xmcyberhostname',
    'entityReport': 'xmcyberentityreport'
}
context = demisto.context()
xmcyber_obj = None
try:
    xmcyber_obj = context['XMCyber']
except KeyError:
    pass
if isinstance(xmcyber_obj, list):
    for i in xmcyber_obj:
        try:
            xmcyber_obj = i
            entity_id = xmcyber_obj['entityId']
            break
        except (KeyError, AttributeError):
            continue
context_values = {}
missing_keys = []
if xmcyber_obj:
    for key in fields.keys():
        try:
            context_values[key] = xmcyber_obj[key]
        except KeyError:
            missing_keys.append(key)
    for key in missing_keys:
        fields.pop(key)
    res = demisto.executeCommand('setIncident', {fields[key]: context_values[key] for key in fields.keys() if context_values[key]})

#this next section copies from incident fields to context

def set_field(field, context_path):
    value = "${incident." + field+ "}"
    res = demisto.executeCommand("Print", {"value": value})
    res_value = res[0]['Contents']
    demisto.log(f'{field} {context_path} {res_value}')
    if res_value and res_value.find('Missing argument') == -1:
        demisto.setContext(context_path, res_value)

try:
    if context['IP']['Address']:
        demisto.executeCommand('setIncident', {'xmcyberipaddress': context['IP']['Address']})
except KeyError:
    set_field('xmcyberipaddress', 'IP.Address')

try:
    if context['Entity']['Hostname']:
        demisto.executeCommand('setIncident', {'xmcyberhostname': context['IP']['Hostname']})
except KeyError:
    set_field('xmcyberhostname', 'Entity.Hostname')

try:
    if xmcyber_obj and xmcyber_obj['entityId']:
        pass
    else:
        set_field('xmcyberentityid', 'XMCyber.entityId')
except KeyError:
    set_field('xmcyberentityid', 'XMCyber.entityId')


demisto.log('Completed mapping.')