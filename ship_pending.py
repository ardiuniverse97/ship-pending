from modules.handle_conversation import handle_conversation
from modules.contact_buyer import contact_buyer
from modules.get_headers import get_headers
from modules.payload import payload
from modules.params import params
import requests
import os

# AFTER SALES
def after_sales(headers, shop, shop_id, buyer_user_id, order_sn, _uid, request_id, part):
  if part == 0: content=f'Halo Kak! 😊 Bantu info email untuk pengiriman produk digital kakak yaa. Terimakasih! 🙏'
  elif part == 1: content=f'Halo Kak! 😊 Terimakasih sudah order di {shop}\n\nNo. Pesanan: {order_sn}\n\nUntuk pesanan ini sudak kami kirim ke email kakak yaa 🎁'
  elif part == 2: content='Jika tidak ada di emai, tolong bantu cek di folder spam/sampah kak. Terimakasih! 🙏'
  conversation_id=contact_buyer(headers=headers, shop_id=shop_id, buyer_user_id=buyer_user_id, _uid=_uid)
  requests.post(
    url='https://seller.shopee.co.id/webchat/api/v1.2/messages',
    headers=headers,
    params=params(headers=headers, _uid=_uid),
    json=payload(shop_id=shop_id, buyer_user_id=buyer_user_id, content=content, request_id=request_id)
  )
  if part in [0,2]: handle_conversation(headers=headers, shop_id=shop_id, conversation_id=conversation_id, status='closed', _uid=_uid)

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
  for order_sn in content:
    # TRIGGER (SHIP PENDING)
    if (content[order_sn]['sent_email'] == False) and (content[order_sn]['trigger'] == False):
      for part in [0]:
        after_sales(
          headers=dict(headers),
          shop=str(content[order_sn]['shop']).title(),
          shop_id=int(content[order_sn]['shop_id']),
          buyer_user_id=int(content[order_sn]['buyer_user_id']),
          order_sn=str(order_sn),
          _uid=str(_uid),
          request_id=str(request_id),
          part=int(part)
        )
      content[order_sn]['trigger']=True
      update_ship_pending(ship_pending_url=ship_pending_url, ship_pending_key=ship_pending_key, content=content)
      print(f"[{content[order_sn]['shop']}] [trigger] [0] - {order_sn}")
    # DELETE (SHIP PENDING)
    elif content[order_sn]['sent_email'] == True:
      for part in [1,2]:
        after_sales(
          headers=dict(headers),
          shop=str(content[order_sn]['shop']).title(),
          shop_id=int(content[order_sn]['shop_id']),
          buyer_user_id=int(content[order_sn]['buyer_user_id']),
          order_sn=str(order_sn),
          _uid=str(_uid),
          request_id=str(request_id),
          part=int(part)
        )
      del content[order_sn]
      update_ship_pending(ship_pending_url=ship_pending_url, ship_pending_key=ship_pending_key, content=content)
      print(f"[{content[order_sn]['shop']}] [after sales] [0] - {order_sn}")
