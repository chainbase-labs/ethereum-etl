# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import itertools
from collections import defaultdict

from ethereumetl.mappers.trace_mapper import EthTraceMapper
from ethereumetl.service.trace_id_calculator import calculate_trace_ids
from ethereumetl.service.trace_status_calculator import calculate_trace_statuses


def join(left, right, join_fields, left_fields, right_fields):
    left_join_field, right_join_field = join_fields

    def field_list_to_dict(field_list):
        result_dict = {}
        for field in field_list:
            if isinstance(field, tuple):
                result_dict[field[0]] = field[1]
            else:
                result_dict[field] = field
        return result_dict

    left_fields_as_dict = field_list_to_dict(left_fields)
    right_fields_as_dict = field_list_to_dict(right_fields)

    left_map = defaultdict(list)
    for item in left: left_map[item[left_join_field]].append(item)

    right_map = defaultdict(list)
    for item in right: right_map[item[right_join_field]].append(item)

    for key in left_map.keys():
        for left_item, right_item in itertools.product(left_map[key], right_map[key]):
            result_item = {}
            for src_field, dst_field in left_fields_as_dict.items():
                result_item[dst_field] = left_item.get(src_field)
            for src_field, dst_field in right_fields_as_dict.items():
                result_item[dst_field] = right_item.get(src_field)

            yield result_item


def enrich_l2_transactions(transactions, receipts):
    result = list(join(
        transactions, receipts, ('hash', 'transaction_hash'),
        left_fields=[
            'type',
            'hash',
            'nonce',
            'transaction_index',
            'from_address',
            'to_address',
            'value',
            'gas',
            'gas_price',
            'input',
            'block_timestamp',
            'block_number',
            'block_hash',
            'max_fee_per_gas',
            'max_priority_fee_per_gas',
            'transaction_type',
            'l1_block_number',
            'l1_times_stamp',
            'l1_tx_origin',
            'max_fee_per_blob_gas',
            'blob_versioned_hashes',
            'access_list',
            'y_parity'
        ],
        right_fields=[
            ('cumulative_gas_used', 'receipt_cumulative_gas_used'),
            ('gas_used', 'receipt_gas_used'),
            ('contract_address', 'receipt_contract_address'),
            ('root', 'receipt_root'),
            ('status', 'receipt_status'),
            ('effective_gas_price', 'receipt_effective_gas_price'),
            ('l1_fee', 'receipt_l1_fee'),
            ('l1_gas_used', 'receipt_l1_gas_used'),
            ('l1_gas_used_paid', 'receipt_l1_gas_used_paid'),
            ('l1_gas_price', 'receipt_l1_gas_price'),
            ('l1_fee_scalar', 'receipt_l1_fee_scalar'),
            ('blob_gas_used', 'receipt_blob_gas_used'),
            ('blob_gas_price', 'receipt_blob_gas_price')
        ]))

    if len(result) != len(transactions):
        raise ValueError('The number of transactions is wrong ' + str(result))

    return result


def enrich_transactions(transactions, receipts):
    result = list(join(
        transactions, receipts, ('hash', 'transaction_hash'),
        left_fields=[
            'type',
            'hash',
            'nonce',
            'transaction_index',
            'from_address',
            'to_address',
            'value',
            'gas',
            'gas_price',
            'input',
            'block_timestamp',
            'block_number',
            'block_hash',
            'max_fee_per_gas',
            'max_priority_fee_per_gas',
            'transaction_type',
            'max_fee_per_blob_gas',
            'blob_versioned_hashes',
            'access_list',
            'y_parity'
        ],
        right_fields=[
            ('cumulative_gas_used', 'receipt_cumulative_gas_used'),
            ('gas_used', 'receipt_gas_used'),
            ('contract_address', 'receipt_contract_address'),
            ('root', 'receipt_root'),
            ('status', 'receipt_status'),
            ('effective_gas_price', 'receipt_effective_gas_price'),
            ('blob_gas_used', 'receipt_blob_gas_used'),
            ('blob_gas_price', 'receipt_blob_gas_price')
        ]))

    if len(result) != len(transactions):
        raise ValueError('The number of transactions is wrong ' + str(result))

    return result


def enrich_logs(blocks, logs):
    result = list(join(
        logs, blocks, ('block_number', 'number'),
        [
            'type',
            'log_index',
            'transaction_hash',
            'transaction_index',
            'address',
            'data',
            'topics',
            'block_number'
        ],
        [
            ('timestamp', 'block_timestamp'),
            ('hash', 'block_hash'),
        ]))

    if len(result) != len(logs):
        raise ValueError('The number of logs is wrong ' + str(result))

    return result


def enrich_token_transfers(blocks, token_transfers):
    result = list(join(
        token_transfers, blocks, ('block_number', 'number'),
        [
            'type',
            'token_address',
            'from_address',
            'to_address',
            'value',
            'transaction_hash',
            'log_index',
            'block_number'
        ],
        [
            ('timestamp', 'block_timestamp'),
            ('hash', 'block_hash'),
        ]))

    if len(result) != len(token_transfers):
        raise ValueError('The number of token transfers is wrong ' + str(result))

    return result


def enrich_traces(blocks, traces):
    result = list(join(
        traces, blocks, ('block_number', 'number'),
        [
            'type',
            'transaction_index',
            'from_address',
            'to_address',
            'value',
            'input',
            'output',
            'trace_type',
            'call_type',
            'reward_type',
            'gas',
            'gas_used',
            'subtraces',
            'trace_address',
            'error',
            'status',
            'transaction_hash',
            'block_number',
            'trace_id',
            'trace_index'
        ],
        [
            ('timestamp', 'block_timestamp'),
            ('hash', 'block_hash'),
        ]))

    if len(result) != len(traces):
        raise ValueError('The number of traces is wrong ' + str(result))

    return result


def enrich_traces_with_blocks_transactions(blocks, traces, transactions):
    blocks_and_traces = list(join(
        traces, blocks, ('block_number', 'number'),
        [
            'type',
            'transaction_index',
            'from_address',
            'to_address',
            'value',
            'input',
            'output',
            'trace_type',
            'call_type',
            'reward_type',
            'gas',
            'gas_used',
            'subtraces',
            'trace_address',
            'error',
            'status',
            'transaction_hash',
            'block_number',
            'trace_id'
        ],
        [
            ('timestamp', 'block_timestamp'),
            ('hash', 'block_hash'),
        ]))

    for bt in blocks_and_traces:
        bt['block_number_transaction_index'] = str(bt['block_number']) + '-' + str(bt['transaction_index'])
    for t in transactions:
        t['block_number_transaction_index'] = str(t['block_number']) + '-' + str(t['transaction_index'])

    result = list(join(
        blocks_and_traces, transactions, ('block_number_transaction_index', 'block_number_transaction_index'),
        [
            'type',
            'transaction_index',
            'from_address',
            'to_address',
            'value',
            'input',
            'output',
            'trace_type',
            'call_type',
            'reward_type',
            'gas',
            'gas_used',
            'subtraces',
            'trace_address',
            'error',
            'status',
            'block_number',
            'trace_id'
        ],
        [
            ('block_timestamp', 'block_timestamp'),
            ('block_hash', 'block_hash'),
            ('hash', 'transaction_hash')
        ]))

    if len(result) != len(traces):
        raise ValueError('The number of traces is wrong ' + str(result))
    trace_mapper = EthTraceMapper()
    trs = [trace_mapper.dict_to_trace(tr) for tr in result]
    calculate_trace_statuses(trs)
    calculate_trace_ids(trs)
    enriched_traces = []
    # calculate trace index
    for ind, trace in enumerate(trs):
        trace.trace_index = ind
        trace_item = trace.__dict__
        trace_item.update({
            'type': 'trace'
        })
        enriched_traces.append(trace_item)

    return enriched_traces


def enrich_contracts(blocks, contracts):
    result = list(join(
        contracts, blocks, ('block_number', 'number'),
        [
            'type',
            'address',
            'bytecode',
            'function_sighashes',
            'is_erc20',
            'is_erc721',
            'block_number',
            'from_address',
            'transaction_hash',
            'transaction_index',
        ],
        [
            ('timestamp', 'block_timestamp'),
            ('hash', 'block_hash'),
        ]))

    if len(result) != len(contracts):
        raise ValueError('The number of contracts is wrong ' + str(result))

    return result


def enrich_tokens(blocks, tokens):
    result = list(join(
        tokens, blocks, ('block_number', 'number'),
        [
            'type',
            'address',
            'symbol',
            'name',
            'decimals',
            'total_supply',
            'block_number'
        ],
        [
            ('timestamp', 'block_timestamp'),
            ('hash', 'block_hash'),
        ]))

    if len(result) != len(tokens):
        raise ValueError('The number of tokens is wrong ' + str(result))

    return result
