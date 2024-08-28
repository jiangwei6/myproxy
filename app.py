from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)

@app.route('/proxy', methods=['GET', 'POST'])
def proxy():
    try:
        if request.method == 'POST':
            data = request.json
            url = data.get('url')
            method = data.get('method', 'GET')
            headers = data.get('headers', {})
            payload = data.get('data', {})
        elif request.method == 'GET':
            url = request.args.get('url')
            method = request.args.get('method', 'GET')
            headers = request.args.get('headers', {})
            payload = request.args.get('data', {})

        # 发起 HTTP 请求到目标 API
        response = requests.request(method, url, headers=headers, json=payload)

        # 根据响应的内容类型做出不同的处理
        content_type = response.headers.get('Content-Type', '')

        if 'application/json' in content_type:
            return jsonify(response.json()), response.status_code
        elif 'text/html' in content_type:
            return Response(response.content, status=response.status_code, content_type='text/html')
        elif 'image' in content_type:
            return Response(response.content, status=response.status_code, content_type=content_type)
        else:
            # 对于其他类型的数据，直接返回原始内容
            return Response(response.content, status=response.status_code, content_type=content_type)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
