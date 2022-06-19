import json
import os.path

scenario_number = '۱'

with open(os.path.dirname(__file__) + "/../output/report{}.json".format(scenario_number)) as f:
    data = json.load(f)
    result = {
        "start_simulation_time": data['start_simulation_time'],
        "end_simulation_time": data['end_simulation_time'],
        "created_transactions": data['created_transactions'],
        "tx_propagation": {},
        "block_propagation": {}
    }

    # calculate tx propagation
    result['tx_propagation']['sum'] = 0
    result['tx_propagation']['length'] = 0
    result['tx_propagation']['average'] = 0
    for pair in data['tx_propagation']:
        for tx in data['tx_propagation'][pair]:
            result['tx_propagation']['sum'] += data['tx_propagation'][pair][tx]
            result['tx_propagation']['length'] += 1

    if result['tx_propagation']['length'] != 0:
        result['tx_propagation']['average'] = result['tx_propagation']['sum'] / result['tx_propagation']['length']

    # calculate block propagation
    result['block_propagation']['sum'] = 0
    result['block_propagation']['length'] = 0
    result['block_propagation']['average'] = 0
    for pair in data['block_propagation']:
        for block in data['block_propagation'][pair]:
            result['block_propagation']['sum'] += data['block_propagation'][pair][block]
            result['block_propagation']['length'] += 1

    if result['block_propagation']['length'] != 0:
        result['block_propagation']['average'] = result['block_propagation']['sum'] / result['block_propagation']['length']

    # output
    path = 'output-processed/report{}.json'.format(scenario_number)
    with open(path, 'w') as f:
        f.write(json.dumps(result))
