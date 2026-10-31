# PAYLOAD
def payload(shop_id, buyer_user_id, content, request_id):
  return {
    "request_id": request_id,
    "to_id": buyer_user_id,
    "type": "text",
    "content": {"text": content},
    "shop_id": shop_id,
    "chat_send_option": {"force_send_cancel_order_warning": False, "comply_cancel_order_warning": False},
    "source_content": {},
    "entry_point": "direct_chat_entry_point",
    "choice_info": {"real_shop_id": None},
    "biz_id": 2
  }