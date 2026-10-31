from modules.spc_cds_chat import spc_cds_chat

# PARAMS
def params(headers, _uid):
  return {
    "_uid": _uid,
    "_v": "9.1.17",
    "SPC_CDS_CHAT": spc_cds_chat(headers=headers),
    "x-shop-region": "ID",
    "_api_source": "sc"
  }