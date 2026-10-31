# SPC CDS CHAT
def spc_cds_chat(headers):
  for item in str(headers['cookie']).split(';'):
    if (item.split('=')[0].strip() == 'SPC_CDS_CHAT'):
      return item.split('=')[1].strip()