import hashlib
import json
from textwrap import dedent
from time import time
from urllib.perse import urplarse
from uuid import uuid4

import requests
from flask import Flask, jeonify,request

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set[]

        self.new_block(previous_hash=1,proof=100)

    def register_node(self,address):
        """
        ノードリストに新しいノードを加える
        :param address: <str>ノードのアドレス　例:'http://192.168.0.5:5000'
        :return: None
        """

        parsed_url = urlparse(address)
        #新しいジェネシスブロックを作る
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self,chain):
        """ブロックチェーンが正しいかを確認する
        :param chain:<list> ブロックチェーン
        :return:<bool> True であれば正しく、 False　であればそうではない
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n--------------\n")

            #ブロックのハッシュが正しいがを確認
            if not self.valid_proof(last_block['proof'],block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        これがコンセンサスアルゴリズム、ネットワーク上の長いチェーンで自らのチェーンを
        置き換えることでコンフリクトを解消する。
        :return: <bool> 自らのチェーンが置き換えられると True 、そうでなければ False
        """

        neighbours = self.nodes
        new_chain = None

        #他のすべてのノードのチェーンを確認
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                #その自らのチェーンがより長いか、有効かを確認
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = new_chain

        # もし自らのチェーンより長く、かつ有効なチェーンを見つけた場合それで置き換える
        if new_chain:
            self.chain = new_chain
            return True

        return False


    def new_block(self,proof,previous_hash=None):
        #新しいブロックを作り、チェーンに加える
        """
        ブロックチェーンに新しいブロックを作る
        :param proof:<int>プルーフ・オブ・ワークアルゴリズムから得られるプルーフ
        :param previous_hash:（オプション）<str>前のブロックのハッシュ
        :return:<dict>新しいブロック
        ”””

        block = {'index':len(self.chain)+1,
                 'timestamp': time()
                 'transactions':self.current_transactions,
                'proof':proof,
                'previous_hash':previous_hash or self.hash(self.chain[-1]),
        }

        # 現在のトランザクションリストをリセット
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self,sender,recipient,amount):

        #新しいトランザクションをリストに加える
        """
        次に発掘されるブロックに加える新しいトランザクションを作る
        :param sender:<str>送信者のアドレス
        :param amount:<int>受信者のアドレス
        :param amount:<int> 量
        :return:<int>このトランザクションを含むブロックのアドレス
        """

        self.current_transactions.append({
            'sender':sender,
            'recipient':recipient,
            'amount':amount,
        })

        return self.last_block['index']+1



    @property
    def last_block(self):
        #チェーンの最後のブロックをリターン
        return self.chain[-1]


    @staticmethod
    def hash(block):
        """ブロックの　SHA-256　ハッシュを作る
        :param block: <dict>ブロック
        :return:<str>
        """

        # 必ずディクショナリ（辞書型のオブジェクト）がソートされている必要がある。そうでないと、一貫性がないハッシュとなってしまう。
        block_string = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        シンプルなプルーフ・オブ・ワークのアルゴリズム:
         - hash(pp')　の最初の４つが０となるような p' を探す
         - p は前のプルーフ、 p' は新しいプルーフ
         :param last_proof: <int>
         :return: <int>
         """

         proof = 0
         while self.valid_proof(last_proof,proof) is False:
             proof += 1


            return proof

    @staticmenthod
    def valid_proof(last_proof,proof):
        """
        プルーフが正しいかを確認する:hash(last_proof, proof)の最初の４つが０となっているかどうか？
        :param last_proof: <int> 前のプルーフ
        :param proof: <int>現在のプルーフ
        :return: <bool> 正しければ　true 、そうでなければ false
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"

＃　ノードを作る
app = Flask(__name__)

#このノードのグローバルにユニークなアドレスを作る
node_identifire = str(uuid4()).replace('_', '')

#　ブロックチェーンクラスをインスタンス化する
blockchain = Blockchain()

#　メソッドはGETで/mineエンドポイントを作る
@app.route('/mine', methods=['GET'])
def mine():
    #次のプルーフを見つけるためにプルーフ・オブ・ワークアルゴリズムを使用する
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    #プルーフを見つけたことに対する報酬を得る
    ＃送信者は、採掘者が新しいコインを採掘したことを表すためにブロックを採掘する
    blockchain.new_transaction(
        sender='0'
        recipient=node_indentfire,
        amount=1,
    )

    #チェーンに新しいブロックを加えることで、新しいブロックを採掘する
    block = blockchain.new_block(proof)

    response = {
        'message':'新しいブロックを採掘しました',
        'index': block['index'],
        'transactions': block['transactions']
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    reurn jsonify(response),200
