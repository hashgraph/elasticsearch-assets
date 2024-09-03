import os
import sys

# Add the path to the utils module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from metrics.utils.common import BaseScript
import metrics.utils.mirrornode_helper as mirrornode_helper
from model import Token


class TokenBalances(BaseScript):
    def __init__(self):
        super().__init__(log_filename="token_balances")
        # Your HTS-specific initialization code here
        self.script_name = os.path.basename(__file__[:-3])
    
    # get token balances from Mirror Node
    def get_token_balances(self, tokens):
        token_balances = []
        count = 0
        for token in tokens:
            token['balance'] = mirrornode_helper.get_mirrornode_token_balance(self.logger, token["token_id"])
            token_balances.append(token)
            count += 1
            if count > 100:
                import pdb; pdb.set_trace()
            # if token_balances is not None:
            #     token_balances_df = self.rcdstreams_to_pd_df(token_balances)
            #     self.write_df_to_file(token_balances_df, f"token_balances_{token_id}")
            # else:
            #     self.logger.error(f"Failed to get token balances for {token_id}")
    
    def run(self):
        self.logger.info(f"Reading data from {self.options.input_file} ...")
        records = self.read_data(self.options.input_file, Token)
        if records is not None:
            token_balances = self.get_token_balances(records)
            if token_balances is not None:
                token_balances_df = self.rcdstreams_to_pd_df(token_balances)
                self.write_df_to_file(token_balances_df, "token_balances")
            else:
                self.logger.error("Failed to get token balances")
        else:
            self.logger.error("Failed to read data from input file")

if __name__ == "__main__":
    myObject = TokenBalances()
    myObject.run()