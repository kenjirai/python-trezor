# This file is part of the TREZOR project.
#
# Copyright (C) 2017 Saleem Rashid <trezor@saleemrashid.com>
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library.  If not, see <http://www.gnu.org/licenses/>.

from .common import *

from trezorlib import messages as proto
from trezorlib import nem
import time


# assertion data from T1
@pytest.mark.nem
@pytest.mark.skip_t1
@pytest.mark.xfail  # to be removed when nem is merged
class TestMsgNEMSignTxMosaics(TrezorTest):

    def test_nem_signtx_mosaic_supply_change(self):
        self.setup_mnemonic_nopin_nopassphrase()

        with self.client:
            tx = self.client.nem_sign_tx(self.client.expand_path("m/44'/1'/0'/0'/0'"), {
                "timeStamp": 74649215,
                "fee": 2000000,
                "type": nem.TYPE_MOSAIC_SUPPLY_CHANGE,
                "deadline": 74735615,
                "message": {
                },
                "mosaicId": {
                    "namespaceId": "hellom",
                    "name": "Hello mosaic"
                },
                "supplyType": 1,
                "delta": 1,
                "version": (0x98 << 24),
                "creationFeeSink": "TALICE2GMA34CXHD7XLJQ536NM5UNKQHTORNNT2J",
                "creationFee": 1500,
            })

            assert hexlify(tx.data) == b'02400000010000987f0e730420000000edfd32f6e760648c032f9acb4b30d514265f6a5b5f8a7154f2618922b406208480841e0000000000ff5f74041a0000000600000068656c6c6f6d0c00000048656c6c6f206d6f73616963010000000100000000000000'
            assert hexlify(tx.signature) == b'928b03c4a69fff35ecf0912066ea705895b3028fad141197d7ea2b56f1eef2a2516455e6f35d318f6fa39e2bb40492ac4ae603260790f7ebc7ea69feb4ca4c0a'

    def test_nem_signtx_mosaic_creation(self):
        self.setup_mnemonic_nopin_nopassphrase()

        test_suite = {
            "timeStamp": 74649215,
            "fee": 2000000,
            "type": nem.TYPE_MOSAIC_CREATION,
            "deadline": 74735615,
            "message": {
            },
            "mosaicDefinition": {
                "id": {
                    "namespaceId": "hellom",
                    "name": "Hello mosaic"
                },
                "levy": {},
                "properties": {},
                "description": "lorem"
            },
            "version": (0x98 << 24),
            "creationFeeSink": "TALICE2GMA34CXHD7XLJQ536NM5UNKQHTORNNT2J",
            "creationFee": 1500,
        }

        # not using client.nem_sign_tx() because of swiping
        tx = self._nem_sign(2, test_suite)
        assert hexlify(tx.data) == b'01400000010000987f0e730420000000edfd32f6e760648c032f9acb4b30d514265f6a5b5f8a7154f2618922b406208480841e0000000000ff5f7404c100000020000000edfd32f6e760648c032f9acb4b30d514265f6a5b5f8a7154f2618922b40620841a0000000600000068656c6c6f6d0c00000048656c6c6f206d6f73616963050000006c6f72656d04000000150000000c00000064697669736962696c6974790100000030160000000d000000696e697469616c537570706c7901000000301a0000000d000000737570706c794d757461626c650500000066616c7365190000000c0000007472616e7366657261626c650500000066616c7365000000002800000054414c49434532474d4133344358484437584c4a513533364e4d35554e4b5148544f524e4e54324adc05000000000000'
        assert hexlify(tx.signature) == b'537adf4fd9bd5b46e204b2db0a435257a951ed26008305e0aa9e1201dafa4c306d7601a8dbacabf36b5137724386124958d53202015ab31fb3d0849dfed2df0e'

    def test_nem_signtx_mosaic_creation_properties(self):
        self.setup_mnemonic_nopin_nopassphrase()

        test_suite = {
            "timeStamp": 74649215,
            "fee": 2000000,
            "type": nem.TYPE_MOSAIC_CREATION,
            "deadline": 74735615,
            "message": {
            },
            "mosaicDefinition": {
                "id": {
                    "namespaceId": "hellom",
                    "name": "Hello mosaic"
                },
                "levy": {},
                "properties": [
                    {
                        "name": "divisibility",
                        "value": "4"
                    },
                    {
                        "name": "initialSupply",
                        "value": "200"
                    },
                    {
                        "name": "supplyMutable",
                        "value": "false"
                    },
                    {
                        "name": "transferable",
                        "value": "true"
                    }
                ],
                "description": "lorem"
            },
            "version": (0x98 << 24),
            "creationFeeSink": "TALICE2GMA34CXHD7XLJQ536NM5UNKQHTORNNT2J",
            "creationFee": 1500,
        }

        # not using client.nem_sign_tx() because of swiping
        tx = self._nem_sign(2, test_suite)
        assert hexlify(tx.data) == b'01400000010000987f0e730420000000edfd32f6e760648c032f9acb4b30d514265f6a5b5f8a7154f2618922b406208480841e0000000000ff5f7404c200000020000000edfd32f6e760648c032f9acb4b30d514265f6a5b5f8a7154f2618922b40620841a0000000600000068656c6c6f6d0c00000048656c6c6f206d6f73616963050000006c6f72656d04000000150000000c00000064697669736962696c6974790100000034180000000d000000696e697469616c537570706c79030000003230301a0000000d000000737570706c794d757461626c650500000066616c7365180000000c0000007472616e7366657261626c650400000074727565000000002800000054414c49434532474d4133344358484437584c4a513533364e4d35554e4b5148544f524e4e54324adc05000000000000'
        assert hexlify(tx.signature) == b'f17c859710060f2ea9a0ab740ef427431cf36bdc7d263570ca282bd66032e9f5737a921be9839429732e663be2bb74ccc16f34f5157ff2ef00a65796b54e800e'

    def test_nem_signtx_mosaic_creation_levy(self):
        self.setup_mnemonic_nopin_nopassphrase()

        test_suite = {
            "timeStamp": 74649215,
            "fee": 2000000,
            "type": nem.TYPE_MOSAIC_CREATION,
            "deadline": 74735615,
            "message": {
            },
            "mosaicDefinition": {
                "id": {
                    "namespaceId": "hellom",
                    "name": "Hello mosaic"
                },
                "properties": [
                    {
                        "name": "divisibility",
                        "value": "4"
                    },
                    {
                        "name": "initialSupply",
                        "value": "200"
                    },
                    {
                        "name": "supplyMutable",
                        "value": "false"
                    },
                    {
                        "name": "transferable",
                        "value": "true"
                    }
                ],
                "levy": {
                    "type": 1,
                    "fee": 2,
                    "recipient": "TALICE2GMA34CXHD7XLJQ536NM5UNKQHTORNNT2J",
                    "mosaicId": {
                        "namespaceId": "hellom",
                        "name": "Hello mosaic"
                    },
                },
                "description": "lorem"
            },
            "version": (0x98 << 24),
            "creationFeeSink": "TALICE2GMA34CXHD7XLJQ536NM5UNKQHTORNNT2J",
            "creationFee": 1500,
        }

        tx = self._nem_sign(6, test_suite)
        assert hexlify(tx.data) == b'01400000010000987f0e730420000000edfd32f6e760648c032f9acb4b30d514265f6a5b5f8a7154f2618922b406208480841e0000000000ff5f74041801000020000000edfd32f6e760648c032f9acb4b30d514265f6a5b5f8a7154f2618922b40620841a0000000600000068656c6c6f6d0c00000048656c6c6f206d6f73616963050000006c6f72656d04000000150000000c00000064697669736962696c6974790100000034180000000d000000696e697469616c537570706c79030000003230301a0000000d000000737570706c794d757461626c650500000066616c7365180000000c0000007472616e7366657261626c65040000007472756556000000010000002800000054414c49434532474d4133344358484437584c4a513533364e4d35554e4b5148544f524e4e54324a1a0000000600000068656c6c6f6d0c00000048656c6c6f206d6f7361696302000000000000002800000054414c49434532474d4133344358484437584c4a513533364e4d35554e4b5148544f524e4e54324adc05000000000000'
        assert hexlify(tx.signature) == b'b87aac1ddf146d35e6a7f3451f57e2fe504ac559031e010a51261257c37bd50fcfa7b2939dd7a3203b54c4807d458475182f5d3dc135ec0d1d4a9cd42159fd0a'

    def _nem_sign(self, num_of_swipes, test_suite):
        n = self.client.expand_path("m/44'/1'/0'/0'/0'")
        n = self.client._convert_prime(n)
        msg = nem.create_sign_tx(test_suite)
        assert msg.transaction is not None
        msg.transaction.address_n = n

        # Sending NEMSignTx message
        self.client.transport.write(msg)
        ret = self.client.transport.read()

        # Confirm action
        assert isinstance(ret, proto.ButtonRequest)
        self.client.debug.press_yes()
        self.client.transport.write(proto.ButtonAck())
        time.sleep(1)
        for i in range(num_of_swipes):
            self.client.debug.swipe_down()
            time.sleep(1)
        self.client.debug.press_yes()
        ret = self.client.transport.read()

        # Confirm action
        assert isinstance(ret, proto.ButtonRequest)
        self.client.debug.press_yes()
        self.client.transport.write(proto.ButtonAck())
        ret = self.client.transport.read()

        # Confirm tx
        assert isinstance(ret, proto.ButtonRequest)
        self.client.debug.press_yes()
        self.client.transport.write(proto.ButtonAck())
        return self.client.transport.read()
