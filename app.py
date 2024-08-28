from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/proxy', methods=['POST'])
def proxy():
    try:
        data = request.json
        url = data.get('url')
        method = data.get('method', 'GET')
        headers = data.get('headers', {})
        payload = data.get('data', {})

        # 发起 HTTP 请求到目标 API
        response = requests.request(method, url, headers=headers, json=payload)

        # 返回目标 API 的响应给客户端
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
