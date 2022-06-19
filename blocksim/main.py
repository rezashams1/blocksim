import time
import os
from json import dumps as dump_json
from blocksim.world import SimulationWorld
from blocksim.node_factory import NodeFactory
from blocksim.transaction_factory import TransactionFactory
from blocksim.models.network import Network
from datetime import datetime

scenario_number = '12'


def write_report(world):
    world.env.data['end_simulation_time'] = datetime.now().strftime('%y-%m-%d %H:%M:%S')

    path = 'output/report{}.json'.format(scenario_number)
    with open(path, 'w') as f:
        f.write(dump_json(world.env.data))


def report_node_chain(world, nodes_list):
    for node in nodes_list:
        head = node.chain.head
        chain_list = []
        num_blocks = 0
        for i in range(head.header.number):
            b = node.chain.get_block_by_number(i)
            chain_list.append(str(b.header))
            num_blocks += 1
        chain_list.append(str(head.header))
        key = f'{node.address}_chain'
        world.env.data[key] = {
            'head_block_hash': f'{head.header.hash[:8]} #{head.header.number}',
            'number_of_blocks': num_blocks,
            'chain_list': chain_list
        }


def run_model():
    now = int(time.time())  # Current time
    duration = 3600  # seconds

    world = SimulationWorld(
        duration,
        now,
        'input-parameters/config.json',
        'input-parameters/latency.json',
        'input-parameters/throughput-received.json',
        'input-parameters/throughput-sent.json',
        'input-parameters/delays.json')

    # Create the network
    network = Network(world.env, 'NetworkXPTO')

    miners = {
        'Tehran': {
            'how_many': 5,
            'mega_hashrate_range': "(25, 40)"
        },
        'Helsinki': {
            'how_many': 5,
            'mega_hashrate_range': "(25, 40)"
        },
        'Nuremberg': {
            'how_many': 8,
            'mega_hashrate_range': "(25, 40)"
        }
    }
    non_miners = {
        'Tehran': {
            'how_many': 8
        },
        'Helsinki': {
            'how_many': 6
        },
        'Nuremberg': {
            'how_many': 5
        }
    }

    node_factory = NodeFactory(world, network)
    # Create all nodes
    nodes_list = node_factory.create_nodes(miners, non_miners)
    # Start the network heartbeat
    world.env.process(network.start_heartbeat())
    # Full Connect all nodes
    for node in nodes_list:
        node.connect(nodes_list)

    transaction_factory = TransactionFactory(world)
    transaction_factory.broadcast(100, 80, 15, nodes_list)

    world.start_simulation()

    report_node_chain(world, nodes_list)
    write_report(world)


if __name__ == '__main__':
    run_model()
