from modules.handle_conversation import handle_conversation
from modules.spc_cds_chat import spc_cds_chat
import requests

# CONTACT BUYER
def contact_buyer(headers, shop_id, buyer_user_id, _uid):
  response=requests.post(
    url='https://seller.shopee.co.id/webchat/api/v1.2/mini/conversation/redirection',
    headers=headers,
    params={"_uid": _uid, "_v": "9.1.17", "SPC_CDS_CHAT": spc_cds_chat(headers=headers), "x-shop-region": "ID", "_api_source": "sc"},
    json={"user_id": buyer_user_id, "shop_id": shop_id, "biz_id": 0, "on_message_received": True, "entry_point": "seller_contact_buyer", "redirection_source": "order_page"}
  )
  conversation_id=response.json()['id']; status=response.json()['status']
  if status == 'closed': handle_conversation(headers=headers, shop_id=shop_id, conversation_id=conversation_id, status='activated', _uid=_uid)
  return conversation_id