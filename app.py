from flask import Flask
from flask import request
import pymongo
import json
import urllib.parse

app = Flask(__name__)
@app.route("/",methods = ['GET', 'POST'])
#{"query_type": "discounted_products_list","filters": [{"operand1": "discount","operator": ">","operand2": 5}]}
def hello():
  
  myclient = pymongo.MongoClient("mongodb+srv://maheswarreddyperam:M%40hi1432@cluster0-r0ygt.mongodb.net/test?retryWrites=true&w=majority")
  
  #myclient = pymongo.MongoClient("mongodb+srv://maheswarreddyperam:M@hi1432@cluster0-r0ygt.mongodb.net/test?retryWrites=true&w=majority")
  mydb = myclient["Dproject"]
  mytable = mydb['Lpu']
  all_records = mytable.find({})
  if request.method == 'POST':
    post_request = request.get_json(force=True)
    query_type = post_request['query_type']
    print(query_type)
    filters = post_request['filters']
    discounted_products_list = list()
    operand1 = filters[0]['operand1']
    operator = filters[0]['operator']
    if operator == '>' and query_type == 'discounted_products_list':
      operand2 = int(filters[0]['operand2'])
      for record in all_records:
        regular_price = int(record['price']['regular_price']['value'])
        offer_price = int(record['price']['offer_price']['value'])
        discount_percentage = ((regular_price - offer_price)/regular_price) * 100
        if discount_percentage > operand2 :
          discounted_products_list.append(record['_id'])
      return {
      query_type : str(discounted_products_list)   
    }
    #Test 1: POST { "query_type": "discounted_products_count|avg_discount", 
    # "filters": [{ "operand1": "brand.name", "operator": "==", "operand2": "gucci" }] }
    if operator == '==' and query_type == 'discounted_products_count|avg_discount' :
      operand2 = filters[0]['operand2']
      discounted_products_count_list = list()
      discount_percentage_add = 0
      for record in all_records:
        if record['brand']['name'] == operand2:
          regular_price = int(record['price']['regular_price']['value'])
          offer_price = int(record['price']['offer_price']['value'])
          discount_percentage = ((regular_price - offer_price)/regular_price) * 100
          discount_percentage_add = discount_percentage_add + discount_percentage
          discounted_products_count_list.append(record['_id'])
      avg_discount = discount_percentage_add / len(discounted_products_count_list)
      return{
        query_type : str(len(discounted_products_count_list)),
        "avg_dicount" : avg_discount
      }
      #{ "query_type": "expensive_list","filters": [{ "operand1": "brand.name", "operator": "==", "operand2": "balenciaga" }] }
    if operator == '==' and query_type == 'expensive_list' :
      operand2 = filters[0]['operand2']
      expensive_list = list()
      for record in all_records:
        if record['brand']['name'] == operand2 :
          regular_price_A = int(record['price']['regular_price']['value'])
          basket_price_A = int(record['price']['basket_price']['value'])
          if regular_price_A > basket_price_A :

            expensive_list.append(record['_id'])
      return{
        query_type : str(expensive_list)
      }
      #{ "query_type": "competition_discount_diff_list", "filters": [{ "operand1": "discount_diff", "operator": ">", "operand2": 10 },{ "operand1": "competition", "operator": "==", "operand2": "5d0cc7b68a66a100014acdb0"}] } 
    if operator == '>' and query_type == 'competition_discount_diff_list' :
      competition_discount_diff_list = list()
      discount_percentage_A = 0
      count = 0
      web_avg = 0
      operand2_A = int(filters[0]['operand2'])
      operator_A = filters[0]['operator']
      operand1_A = filters[0]['operand1']
      operand1_B = filters[1]['operand1']
      operator_B = filters[1]['operator']
      operand2_B = str(filters[1]['operand2'])
      for record in all_records:
        basket_price_A = int(record['price']['basket_price']['value'])
        web_avg = record['similar_products']['website_results'][operand2_B]['meta']['avg_price']['basket']
        discount_percentage_A = ((web_avg-basket_price_A)/basket_price_A)*100
        if discount_percentage_A > operand2_A :
         competition_discount_diff_list.append(record['_id'])
      return{
        query_type : str(competition_discount_diff_list)
      }
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)