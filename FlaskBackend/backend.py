from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from web3 import Web3
from web3_input_decoder import InputDecoder
import json
abi_file = open("abi.json")
abi = json.load(abi_file)
app = Flask(__name__)
CORS(app)


@app.route('/streams', methods=["POST"])
def streams():
    # moralis send two diffrent API one is confirmed is true another is false first we recieve false transaction and after 10
    # blocks passes after our transaction minedblock it sends us another  confirmed is true same transaction so we only save confirmed is true transaction
    # link -----------> https://docs.moralis.io/docs/streams-api-frequently-asked-questions
    if request.json['confirmed']:
        try:
            # Provide Signature
            provided_signature = request.headers.get("x-signature")
            if not provided_signature:
                raise ValueError("Signature not provided")
            print("Provided Signature:", provided_signature)

            data = request.data + \
                "jUQ3ILfqPNO3OKHAlTPqsyc5y9xbVhlOcWtt5GZj6IfN2iykUxDEoP0IpcBp14pM".encode()
            signature = Web3.sha3(data).hex()
            print("Generated Signature:", signature)
            if provided_signature != signature:
                raise TypeError(f"Invalid Signature!!")
            print("Valid Signature")

            data = request.json["txs"][0]
            hash = data["hash"]

            decoder = InputDecoder(abi)
            result = decoder.decode_function(data["input"])

            if result.name == "createInstantTransfer":
                print("Wrong function to save")
                return

            payroll_id = result.arguments[0][2]
            tokenAddress = result.arguments[1][2]

            return payroll_id, tokenAddress, hash

        except Exception as e:
            print("Error:", e)
            return str(e)
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=True)
