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


from ethereumetl.domain.transaction import EthTransaction
from ethereumetl.utils import hex_to_dec, to_normalized_address


class EthTransactionMapper(object):
    def json_dict_to_transaction(self, json_dict, **kwargs):
        transaction = EthTransaction()
        transaction.hash = json_dict.get('hash')
        transaction.nonce = hex_to_dec(json_dict.get('nonce'))
        transaction.block_hash = json_dict.get('blockHash')
        transaction.block_number = hex_to_dec(json_dict.get('blockNumber'))
        transaction.block_timestamp = kwargs.get('block_timestamp')
        transaction.transaction_index = hex_to_dec(json_dict.get('transactionIndex'))
        transaction.from_address = to_normalized_address(json_dict.get('from'))
        transaction.to_address = to_normalized_address(json_dict.get('to'))
        transaction.value = hex_to_dec(json_dict.get('value'))
        transaction.gas = hex_to_dec(json_dict.get('gas'))
        transaction.gas_price = hex_to_dec(json_dict.get('gasPrice'))
        transaction.input = json_dict.get('input')
        transaction.max_fee_per_gas = hex_to_dec(json_dict.get('maxFeePerGas'))
        transaction.max_priority_fee_per_gas = hex_to_dec(json_dict.get('maxPriorityFeePerGas'))
        transaction.transaction_type = hex_to_dec(json_dict.get('type'))

        transaction.max_fee_per_blob_gas = hex_to_dec(json_dict.get('maxFeePerBlobGas'))
        transaction.blob_versioned_hashes = json_dict.get('blobVersionedHashes')
        transaction.access_list = self.parse_access_list(json_dict.get('accessList'))
        transaction.y_parity = hex_to_dec(json_dict.get('yParity'))

        transaction.r = json_dict.get('r')
        transaction.s = json_dict.get('s')
        transaction.v = json_dict.get('v')
        transaction.chain_id = hex_to_dec(json_dict.get('chainId'))
        transaction.method_id = json_dict.get('input')[0:10]

        # OP Stack
        transaction.source_hash = json_dict.get('sourceHash')
        transaction.mint = json_dict.get('mint')

        return transaction

    def parse_access_list(self, access_list):
        if access_list is None:
            return None

        return [
            {
                'address': to_normalized_address(access['address']),
                'storage_keys': access['storageKeys']
            }
            for access in access_list
        ]

    def transaction_to_dict(self, transaction):
        return {
            'type': 'transaction',
            'hash': transaction.hash,
            'nonce': transaction.nonce,
            'block_hash': transaction.block_hash,
            'block_number': transaction.block_number,
            'block_timestamp': transaction.block_timestamp,
            'transaction_index': transaction.transaction_index,
            'from_address': transaction.from_address,
            'to_address': transaction.to_address,
            'value': transaction.value,
            'gas': transaction.gas,
            'gas_price': transaction.gas_price,
            'input': transaction.input,
            'max_fee_per_gas': transaction.max_fee_per_gas,
            'max_priority_fee_per_gas': transaction.max_priority_fee_per_gas,
            'transaction_type': transaction.transaction_type,

            'max_fee_per_blob_gas': transaction.max_fee_per_blob_gas,
            'blob_versioned_hashes': transaction.blob_versioned_hashes,
            'access_list': transaction.access_list,
            'y_parity': transaction.y_parity,

            'r': transaction.r,
            's': transaction.s,
            'v': transaction.v,
            'chain_id': transaction.chain_id,
            'method_id': transaction.method_id,
            'source_hash': transaction.source_hash,
            'mint': transaction.mint,
        }
