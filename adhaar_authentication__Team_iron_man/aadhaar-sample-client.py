import logging
import sys, os, os.path
from config import Config
log = logging.getLogger("SampleClient")

from AadhaarAuth.request import AuthRequest
from AadhaarAuth.data import AuthData
from AadhaarAuth.command import AuthConfig

if __name__ == '__main__':

   cmd = AuthConfig()
   cfg = cmd.update_config()

   logging.getLogger().setLevel(cfg.common.loglevel)
   logging.basicConfig()

   # => Force only demographic authentication
   cfg.request.demographics = ["Pi"]
   cfg.request.biometrics = []
   
   # => Simulate a POS site and generate the request data
   data = AuthData(cfg=cfg)
   data.generate_client_xml()
   exported_data = data.export_request_data()

   # Create the request object and execute the auth request
   req = AuthRequest(cfg)
   req.import_request_data(exported_data)
   req.execute()

   # Extract the response
   data = json.loads(req.export_response_data())
   res = AuthResponse(cfg=cfg, uid=cfg.request.uid)
   res.load_string(data['xml'])

   #Print the response
   bits = res.lookup_usage_bits()
   print "[%.3f] (%s) -> %s " % (data['latency'], bits, data['ret'])
   if data['err'] is not None and data['err'] != -1:
         print( "Err %s: %s "% ( data['err'], data['err_message']))