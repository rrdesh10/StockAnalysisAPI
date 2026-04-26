from flask import Blueprint, jsonify, request
from .services import get_company_data, get_market_data, get_historical_data, analyse_stock_data
import yfinance  as yf

api_bp = Blueprint('api', __name__)

@api_bp.route('/company/<string:symbol>', methods = ['GET'])
def company_info(symbol):
    data = get_company_data(symbol)

    if not data:
        return jsonify({"error": "Symbol not found", "symbol" : symbol}), 404
    
    return jsonify(data), 200


@api_bp.route('/market_data/<string:symbol>', methods = ['GET'])
def market_data(symbol):
    data = get_market_data(symbol)

    if not data:
        return jsonify({"error": "Symbol not found", "symbol" : symbol}), 404
    
    return jsonify(data), 200


@api_bp.route('/history/<string:symbol>', methods = ['POST'])
def historical_data(symbol):
    data = request.get_json()

    start = data.get('start_date')
    end = data.get('end_date')
    interval = data.get('interval', '1d')

    if not start or not end:
        return jsonify({"error": "Please provide start_date and end_date"}), 400
    
    history = get_historical_data(symbol, start, end, interval)
    
    if history is None:
        return jsonify({"Error": "No data found for this range", "symbol":symbol}), 404
    
    return jsonify(
        {
            "symbol":symbol,
            "range": {"start":start, "end":end},
            "data": history
        }), 200

@api_bp.route('/analytics/<string:symbol>', methods=['GET'])
def get_analytics(symbol):
    ticker = yf.Ticker(symbol)
    
    # Fetch 6 months of data to have enough room for 50-day SMA
    df = ticker.history(period="6mo")
    
    if df.empty:
        return jsonify({"error": "Could not fetch data for analysis"}), 404
        
    analysis = analyse_stock_data(df)
    
    return jsonify({
        "symbol": symbol.upper(),
        "analysis_period": "6 Months",
        "insights": analysis
    }), 200