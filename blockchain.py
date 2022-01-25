#Muhammad Usama Azam
#Implementation of blockChain

import hashlib
from flask import Flask, jsonify
import datetime
import json

class blockChain:
    def __init__(self):
        self.chain = []
        self.createBlock('0000')
    
    def createBlock(self, prevHash):
        newBlock = {'blockNumber': len(self.chain) + 1,
                    'timeStamp': str(datetime.datetime.now()),
                    'Nounce':1,
                    'prevHash':prevHash}
        newBlock = self.hash(newBlock)
        self.chain.append(newBlock)
        return newBlock
    
    def getPrevBlock(self):
        return self.chain[-1]
    
    def hash(self, block):
        checkNounce = True
        while checkNounce:
            encodedBlock = json.dumps(block, sort_keys = True).encode()
            hashValue = hashlib.sha256(encodedBlock).hexdigest()
            if hashValue[:5] == '00000':
                checkNounce = False
            else:
                block['Nounce'] += 1
        block['Hash'] = hashValue
        return block
    
    def isChainValid(self):
        prevBlock = self.chain[0]
        blockNumber = 1
        while blockNumber < len(self.chain):
            currentBlock = self.chain[blockNumber]
            if prevBlock['Hash'] != currentBlock['prevHash']:
                return False
            prevBlock = currentBlock
            blockNumber += 1
        return True

blckchain = blockChain()

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

@app.route("/")
def hello():
    return "Hello, World!"

@app.route('/getChain', methods = ['GET'])
def getChain():
    response = {'chain': blckchain.chain,
                'length': len(blckchain.chain)}
    return jsonify(response)

# Checking if the Blockchain is valid
@app.route('/isValid', methods = ['GET'])
def isValid():
    isValid = blckchain.isChainValid()
    if isValid:
        response = {'message': 'The block chain is valid.'}
    else:
        response = {'message': 'The block chain is not valid.'}
    return jsonify(response)

@app.route('/mineBlock', methods = ['GET'])
def mineBlock():
    prevBlock = blckchain.getPrevBlock()
    prevHash = prevBlock['Hash']
    block = blckchain.createBlock(prevHash)
    response = {'newBlock':{'blockNumber': block['blockNumber'],
                'timestamp': block['timeStamp'],
                'Nounce': block['Nounce'],
                'prevHash': block['prevHash'],
                'Hash': block['Hash']}}
    return jsonify(response)
    
app.run(host = '0.0.0.0', port = 5000)