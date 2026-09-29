import os
import base64
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 환경 변수에서 시크릿 키를 읽어옴. 없으면 기본값 사용.
TOSS_SECRET_KEY = os.environ.get("TOSS_SECRET_KEY", "test_gsk_docs_OaPz8L5KdmQXkzRz3y47BMw6")

def get_auth_header():
    """토스페이먼츠 API를 위한 Basic Auth 헤더 생성"""
    auth_str = f"{TOSS_SECRET_KEY}:"
    encoded_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
    return {"Authorization": f"Basic {encoded_auth}", "Content-Type": "application/json"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    # 1. 쿼리 파라미터 받기
    payment_key = request.args.get('paymentKey')
    order_id = request.args.get('orderId')
    amount_str = request.args.get('amount')

    # 2. amount 검증 (1000이어야 함)
    try:
        amount = int(amount_str)
        if amount != 1000:
            return render_template('fail.html', code="INVALID_AMOUNT", message=f"결제 금액이 올바르지 않습니다. (요청: {amount}, 기대값: 1000)", error_details={"requested_amount": amount}), 400
    except (ValueError, TypeError):
        return render_template('fail.html', code="INVALID_AMOUNT_FORMAT", message="결제 금액 형식이 올바르지 않습니다.", error_details={"amount": amount_str}), 400

    # 3. 토스페이먼츠 결제 승인 API 호출
    api_url = "https://api.tosspayments.com/v1/payments/confirm"
    payload = {
        "paymentKey": payment_key,
        "orderId": order_id,
        "amount": amount
    }

    try:
        response = requests.post(api_url, json=payload, headers=get_auth_header())
        response_data = response.json()

        if response.status_code == 200:
            # 승인 성공
            return render_template('success.html', 
                                   status=response_data.get('status'),
                                   orderName=response_data.get('orderName'),
                                   totalAmount=response_data.get('totalAmount'),
                                   method=response_data.get('method'),
                                   approvedAt=response_data.get('approvedAt'),
                                   json_response=response_data)
        else:
            # 승인 실패 (API 레벨에서의 에러)
            return render_template('fail.html', 
                                   code=response_data.get('code', 'UNKNOWN_ERROR'),
                                   message=response_data.get('message', '알 수 없는 에러가 발생했습니다.'),
                                   error_details=response_data), response.status_code

    except Exception as e:
        return render_template('fail.html', code="SERVER_ERROR", message=str(e), error_details={}), 500

@app.route('/fail')
def fail():
    # 쿼리에서 에러 정보 받기
    code = request.args.get('code', 'UNKNOWN')
    message = request.args.get('message', '알 수 없는 오류가 발생했습니다.')
    
    # 혹시 모를 추가 에러 디테일을 위해 쿼리 전체를 전달할 수도 있지만, 
    # 스펙에는 code와 message를 보여준다고 되어 있음.
    return render_template('fail.html', code=code, message=message, error_details={})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
