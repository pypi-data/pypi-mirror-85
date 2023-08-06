# -*- coding: utf-8 -*-
"""
Rest API Documentation
    https://algomojo.com/docs/
"""

import requests
import json


class api:

    """
    A class Which has methods to handle all the api calls to algomojo

    """

    def __init__(self, api_key, api_secret, broker, version=1.0):

        """
         Function used to initialize object of class api.
         ...

         Attributes
         ----------
         api_key : str
             User Api key (logon to algomojo account to find api credentials)
         api_secret : str
             User Api secret (logon to algomojo account to find api credentials)
         Broker : str
             This takes broker it generally consists 2 letters , EX: alice blue--> ab, tradejini-->tj, zebu-->zb

         ----------
         Example:
        ab=api(api_key="20323f062bb71ca6fbb178b4df8ac5z6",api_secret="686786a302d7364d81badc233f1d22e3",broker="ab")
         """


        self.api_key = api_key.lower()
        self.api_secret = api_secret.lower()
        self.burl = "https://" + broker + 'api.algomojo.com/' + str(version) + '/'
        self.headers = {
            'Content-Type': 'application/json'
        }

    def place_order(self, ticker, exchange, action, qty, order_type="MKT", price=0, discqty=0, trig_price=0,
                    product_type="MIS", strategy_name="Test Strategy", api_key="default", api_secret="default"):



        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "strg_name": strategy_name,
                    "s_prdt_ali": "BO:BO||CNC:CNC||CO:CO||MIS:MIS||NRML:NRML",
                    "Tsym": ticker,
                    "exch": exchange,
                    "Ttranstype": action,
                    "Ret": "DAY",
                    "prctyp": order_type,
                    "qty": str(qty),
                    "discqty": str(discqty),
                    "MktPro": "NA",
                    "Price": str(price),
                    "TrigPrice": str(trig_price),
                    "Pcode": product_type,
                    "AMO": "NO"
                }
        }
        url = self.burl + "PlaceOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    def place_bracket_order(self, token, exchange, action, qty, target, stoploss, trailingSL=0, tSLticks=1, price=0,
                            trig_price="LTP", discqty=0, SqrOffAbsOrticks="Absolute", SLAbsOrticks="Absolute",
                            strategy_name="Test Strategy", api_key="default", api_secret="default"):



        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "strg_name": strategy_name,
                    "s_prdt_ali": "BO:BO||CNC:CNC||CO:CO||MIS:MIS||NRML:NRML",
                    "TokenNo": str(token),
                    "exch": exchange,
                    "Ttranstype": action,
                    "Ret": "DAY",
                    "qty": str(qty),
                    "discqty": str(discqty),
                    "Price": str(price),
                    "ltpOratp": str(trig_price),
                    "SqrOffAbsOrticks": SqrOffAbsOrticks,
                    "SqrOffvalue": str(target),
                    "SLAbsOrticks": str(SLAbsOrticks),
                    "SLvalue": str(stoploss),
                    "trailingSL": str(trailingSL),
                    "tSLticks": str(tSLticks)
                }
        }
        url = self.burl + "PlaceBOOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    def place_option_order(self, spot_sym, expiry, opt_type, action, qty, order_type="MKT", product_type="MIS", price=0,
                           trig_price=0, strike_int=50, offset=10, strategy_name="Test Strategy", api_key="default",
                           api_secret="default"):
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "strg_name": strategy_name,
                    "spot_sym": spot_sym,
                    "expiry_dt": expiry,
                    "opt_type": opt_type,
                    "Ttranstype": action,
                    "prctyp": order_type,
                    "qty": str(qty),
                    "Price": str(price),
                    "TrigPrice": str(trig_price),
                    "Pcode": product_type,
                    "strike_int": str(strike_int),
                    "offset": str(offset)
                }
        }
        url = self.burl + "PlaceFOOptionsOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    def cancel_bo(self, client_id, nestordernumber, status="pending", api_key="default", api_secret="default"):
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "uid": str(client_id),
                    "nestordernumber": str(nestordernumber),
                    "SyomOrderId": "",
                    "status": status
                }

        }
        url = self.burl + "ExitBOOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    def cancel_co(self, client_id, nestordernumber, api_key="default", api_secret="default"):
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "uid": str(client_id),
                    "nestordernumber": str(nestordernumber),
                    "s_prdt_ali": "BO:BO||CNC:CNC||CO:CO||MIS:MIS||NRML:NRML"
                }

        }
        url = self.burl + "ExitCOOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    def modify_order(self, client_id, nestordernumber, ticker, exchange, action, order_type, price, qty, symbol_token,
                     filled_qty="0", product_type="MIS", disc_qty=0, trig_price=0, api_key="default",
                     api_secret="default"):
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "uid": str(client_id),
                    "Actid": str(client_id),
                    "Exchangeseg": str(exchange),
                    "Tsym": str(ticker),
                    "Nstordno": str(nestordernumber),
                    "Ttranstype": str(action),
                    "Prctype": str(order_type),
                    "Price": str(price),
                    "Qty": str(qty),
                    "Dscqty": str(disc_qty),
                    "Trgprc": str(trig_price),
                    "Validity": "DAY",
                    "Symbol": str(symbol_token),
                    "Filledqty": str(filled_qty),
                    "Pcode": product_type,
                    "Mktpro": "NA",
                    "DateDays": "NA",
                    "s_prdt_ali": "BO:BO||CNC:CNC||CO:CO||MIS:MIS||NRML:NRML"
                }
        }
        url = self.burl + "ModifyOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    def cancelorder(self, client_id, nestordernumber, ticker, exchange, api_key="default", api_secret="default"):
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "uid": str(client_id),
                    "NestOrd": str(nestordernumber),
                    "sTradeSymbol": str(ticker),
                    "s_prdt_ali": "BO:BO||CNC:CNC||CO:CO||MIS:MIS||NRML:NRML",
                    "sExch": str(exchange)

                }

        }
        url = self.burl + "CancelOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    def order_book(self, client_id, api_key="default", api_secret="default"):
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "s_prdt_ali": "BO:BO||CNC:CNC||CO:CO||MIS:MIS||NRML:NRML",
                    "uid": str(client_id)
                }

        }
        url = self.burl + "OrderBook"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)

        return (r.json())

    def order_history(self, client_id, nestordernumber, api_key="default", api_secret="default"):
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "uid": str(client_id),
                    "NOrdNo": str(nestordernumber),
                    "s_prdt_ali": "BO:BO||CNC:CNC||CO:CO||MIS:MIS||NRML:NRML"
                }

        }
        url = self.burl + "OrderHistory"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return ((r.json()))

    def position_book(self, client_id, prod_type="DAY", api_key="default", api_secret="default"):
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "uid": str(client_id),
                    "actid": str(client_id),
                    "type": prod_type,
                    "s_prdt_ali": "BO:BO||CNC:CNC||CO:CO||MIS:MIS||NRML:NRML"
                }

        }
        url = self.burl + "PositionBook"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    def place_multi_order(self, order_list):
        l = order_list

        def rename(dictn, old, new):
            dictn[new] = dictn.pop(old)
            return dictn

        for i in range(len(l)):
            if "api_key" not in l[i].keys():
                l[i]["api_key"] = self.api_key
                l[i]["api_secret"] = self.api_secret
            if "strategy_name" not in l[i].keys():
                l[i]["strategy_name"] = "Test"
            if "order_type" not in l[i].keys():
                l[i]["order_type"] = "MKT"
            if "MktPro" not in l[i].keys():
                l[i]["MktPro"] = "NA"
            if "Ret" not in l[i].keys():
                l[i]["Ret"] = "DAY"
            if "price" not in l[i].keys():
                l[i]["price"] = "0"
            if "trig_price" not in l[i].keys():
                l[i]["trig_price"] = "0"
            if "product_type" not in l[i].keys():
                l[i]["product_type"] = "CNC"
            if "s_prdt_ali" not in l[i].keys():
                l[i]["s_prdt_ali"] = "BO:BO||CNC:CNC||CO:CO||MIS:MIS||NRML:NRML"
            if "AMO" not in l[i].keys():
                l[i]["AMO"] = "NO"
            if "discqty" not in l[i].keys():
                l[i]["discqty"] = "0"

            l[i]["qty"] = str(l[i]["qty"])
            l[i]["price"] = str(l[i]["price"])
            l[i]["discqty"] = str(l[i]["discqty"])
            l[i]["discqty"] = str(l[i]["discqty"])
            l[i] = rename(l[i], "api_key", "user_apikey")
            l[i] = rename(l[i], "ticker", "Tsym")
            l[i] = rename(l[i], "exchange", "exch")
            l[i] = rename(l[i], "action", "Ttranstype")
            l[i] = rename(l[i], "order_type", "prctyp")
            l[i] = rename(l[i], "price", "Price")
            l[i] = rename(l[i], "trig_price", "TrigPrice")
            l[i] = rename(l[i], "product_type", "Pcode")
            l[i] = rename(l[i], "strategy_name", "strg_name")

        data = {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "data":
                {
                    "orders": l
                }
        }
        # return l
        url = self.burl + "PlaceMultiOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)

        return (r.json())

    def place_multi_bo(self, order_list):
        l = order_list

        def rename(dictn, old, new):
            dictn[new] = dictn.pop(old)
            return dictn

        for i in range(len(l)):
            if "api_key" not in l[i].keys():
                l[i]["api_key"] = self.api_key
                l[i]["api_secret"] = self.api_secret
            if "strategy_name" not in l[i].keys():
                l[i]["strategy_name"] = "Test"
            if "Ret" not in l[i].keys():
                l[i]["Ret"] = "DAY"
            if "price" not in l[i].keys():
                l[i]["price"] = "0"
            if "trig_price" not in l[i].keys():
                l[i]["trig_price"] = "LTP"
            if "s_prdt_ali" not in l[i].keys():
                l[i]["s_prdt_ali"] = "BO:BO||CNC:CNC||CO:CO||MIS:MIS||NRML:NRML"
            if "discqty" not in l[i].keys():
                l[i]["discqty"] = "0"
            if "trailingSL" not in l[i].keys():
                l[i]["trailingSL"] = "0"
            if "tSLticks" not in l[i].keys():
                l[i]["tSLticks"] = "1"
            if "SqrOffAbsOrticks" not in l[i].keys():
                l[i]["SqrOffAbsOrticks"] = "Absolute"
            if "SLAbsOrticks" not in l[i].keys():
                l[i]["SLAbsOrticks"] = "Absolute"
            l[i]["qty"] = str(l[i]["qty"])
            l[i]["profit"] = str(l[i]["profit"])
            l[i]["stoploss"] = str(l[i]["stoploss"])
            l[i]["trailingSL"] = str(l[i]["trailingSL"])
            l[i]["price"] = str(l[i]["price"])
            l[i] = rename(l[i], "api_key", "user_apikey")
            l[i] = rename(l[i], "ticker", "TokenNo")
            l[i] = rename(l[i], "exchange", "exch")
            l[i] = rename(l[i], "action", "Ttranstype")
            l[i] = rename(l[i], "price", "Price")
            l[i] = rename(l[i], "trig_price", "ltpOratp")
            l[i] = rename(l[i], "profit", "SqrOffvalue")
            l[i] = rename(l[i], "stoploss", "SLvalue")
            l[i] = rename(l[i], "strategy_name", "strg_name")
        data = {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "data":
                {
                    "orders": l
                }
        }
        url = self.burl + "PlaceMultiBOOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        # return l
        return (r.json())

    def squareoff(self, client_id, ticker, symbol_token, qty, exchange_seg="nse_cm", product_type="MIS",
                  api_key="default", api_secret="default"):
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "uid": str(client_id),
                    "actid": str(client_id),
                    "s_prdt_ali": "BO:BO||CNC:CNC||CO:CO||MIS:MIS||NRML:NRML",
                    "Exchangeseg": exchange_seg,
                    "Pcode": product_type,
                    "Netqty": str(qty),
                    "Token": str(symbol_token),
                    "Symbol": ticker,
                    "orderSource": "NEST_REST"
                }
        }
        url = self.burl + "SquareOffPosition"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    def partial_convert(self, client_id, ticker, symbol_token, qty, exchange_seg="nse_cm", product_type="MIS",
                        api_key="default", api_secret="default"):
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "uid": str(client_id),
                    "actid": str(client_id),
                    "s_prdt_ali": "BO:BO||CNC:CNC||CO:CO||MIS:MIS||NRML:NRML",
                    "Exchangeseg": exchange_seg,
                    "Pcode": product_type,
                    "Netqty": str(qty),
                    "Token": str(symbol_token),
                    "Symbol": ticker,
                    "orderSource": "NEST_REST"
                }
        }
        url = self.burl + "PartialPositionconvertion"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    def ltp_cover(self, symbol_token, exchange, action, api_key="default", api_secret="default"):
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "Exchange": exchange,
                    "Symbol": str(symbol_token),
                    "Transtype": action

                }
        }
        url = self.burl + "LTPCoverpercentage"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    def symbol_info(self, symbol, api_key="default", api_secret="default"):
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "s": symbol
                }
        }
        url = self.burl + "fetchsymbol"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    def security_info(self, security_dict, api_key="default", api_secret="default"):
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data": security_dict
        }
        url = self.burl + "SecurityInfo"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    def limits(self, client_id,exchange, segment="ALL" ,product_type="", api_key="default", api_secret="default"):
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "uid": str(client_id),
                    "actid": str(client_id),
                    "segment": segment,
                    "Exchange": exchange,
                    "product": product_type
                }
        }
        url = self.burl + "Limits"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())