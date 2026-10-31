from modules.spc_cds_chat import spc_cds_chat
import requests

# HANDLE CONVERSATION
def handle_conversation(headers, shop_id, conversation_id, status, _uid):
  requests.put(
    url=f'https://seller.shopee.co.id/webchat/api/v1.2/conversations/{conversation_id}/status',
    headers=headers,
    params={"_uid": _uid, "_v": "9.1.17", "SPC_CDS_CHAT": spc_cds_chat(headers=headers), "x-shop-region": "ID", "_api_source": "sc"},
    json={"shop_id": shop_id, "status": status, "biz_id": 0}
  )