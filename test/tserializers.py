from bitpeer import serializers
from io import BytesIO

b = serializers.Block ()
t = serializers.Tx ()
#txi = serializers.TxIn ()
#txi.previous_output = 0x0000000000000000037fb2555bff59aeff86f53e9733096288445b6f7f287f38
#t.tx_in.append (txi)
b.txns.append (t)


h1 = b.calculate_hash ()

deserializer = serializers.BlockSerializer ()
bb = deserializer.serialize(b)

print (bb)

b2 = deserializer.deserialize(BytesIO (bb))
h2 = b2.calculate_hash ()

print (h1 == h2)
