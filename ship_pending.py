from modules.handle_conversation import handle_conversation
from modules.contact_buyer import contact_buyer
from modules.get_headers import get_headers
from modules.payload import payload
from modules.params import params
import requests
import os

# AFTER SALES
def after_sales(headers, shop_id, buyer_user_id, _uid, request_id, type):
  if type == 'trigger': content=f'Halo Kak! 😊 Bantu info email untuk pengiriman produk digital kakak yaa. Terimakasih! 🙏'
  elif type == 'after sales': content="Halo Kak! 😊 Terimakasih sudah berbelanja di toko kami. Pesanan sudah dikirimkan ya. Jika belum menerima, tolong bantu cek di folder spam/sampah kak. Terimakasih! 🙏"
  conversation_id=contact_buyer(headers=headers, shop_id=shop_id, buyer_user_id=buyer_user_id, _uid=_uid)
  requests.post(
    url='https://seller.shopee.co.id/webchat/api/v1.2/messages',
    headers=headers,
    params=params(headers=headers, _uid=_uid),
    json=payload(shop_id=shop_id, buyer_user_id=buyer_user_id, content=content, request_id=request_id)
  )
  handle_conversation(headers=headers, shop_id=shop_id, conversation_id=conversation_id, status='closed', _uid=_uid)

# UPDATE SHIP PENDING
def update_ship_pending(ship_pending_url, ship_pending_key, content):
  requests.patch(url=ship_pending_url, headers={'Content-Type': 'application/json', 'X-Edit-Key': ship_pending_key}, json=content)  

# RUNNING
if __name__ == '__main__':
  # (1) CONFIGURATION
  auth_headers_url=os.environ["AUTH_HEADERS_URL"]; request_id=os.environ["REQUEST_ID"]; _uid=os.environ["_UID"]
  ship_pending_url=os.environ["SHIP_PENDING_URL"]; ship_pending_key=os.environ["SHIP_PENDING_KEY"]
  # (2) SHIP PENDING
  headers=get_headers(auth_headers_url=auth_headers_url); content=requests.get(ship_pending_url).json()['content']
  for order_sn in list(content):
    # TRIGGER (SHIP PENDING)
    if (content[order_sn]['sent_email'] == False) and (content[order_sn]['trigger'] == False):
      after_sales(
        headers=dict(headers),
        shop_id=int(content[order_sn]['shop_id']),
        buyer_user_id=int(content[order_sn]['buyer_user_id']),
        _uid=str(_uid),
        request_id=str(request_id),
        type=str('trigger')
      )
      content[order_sn]['trigger']=True
      update_ship_pending(ship_pending_url=ship_pending_url, ship_pending_key=ship_pending_key, content=content)
      print(f"[trigger] - {order_sn}")
    # DELETE (SHIP PENDING)
    elif content[order_sn]['sent_email'] == True:
      after_sales(
        headers=dict(headers),
        shop_id=int(content[order_sn]['shop_id']),
        buyer_user_id=int(content[order_sn]['buyer_user_id']),
        _uid=str(_uid),
        request_id=str(request_id),
        type=str('after sales')
      )
      del content[order_sn]
      update_ship_pending(ship_pending_url=ship_pending_url, ship_pending_key=ship_pending_key, content=content)
      print(f"[after sales] - {order_sn}")
