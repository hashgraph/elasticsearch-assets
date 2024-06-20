import os
import sys

# Add the path to the utils module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from metrics.utils.common import BaseScript
import metrics.utils.mirrornode_helper as mirrornode_helper


class TokenList(BaseScript):
    def __init__(self):
        super().__init__(log_filename="token_list")
        # Your HTS-specific initialization code here
        self.script_name = os.path.basename(__file__[:-3])

    def get_token_list(self):
            """
            Retrieves the token list from the Mirror Node.

            Returns:
                list: A list of tokens.
                None: If an exception occurs during the retrieval process.
            """
            self.logger.info("Getting token list")
            try:
                tokens = mirrornode_helper.get_mirrornode_token_list(self.logger)
                return tokens
            except Exception as e:
                self.logger.error(f"Exception: {e}")
                return None
    
    def run(self):
        """
        Executes the token list retrieval process.
        
        This method retrieves the token list, converts it to a pandas DataFrame,
        and writes the data to a file. If the token list retrieval fails, an error
        message is logged.
        """
        self.logger.info("Getting token list")
        tokens = self.get_token_list()
        if tokens is not None:
            token_df = self.rcdstreams_to_pd_df(tokens)
            output_filename_type = f"{self.options.output_folder}/{self.script_name}"
            self.logger.info(f"Writing data to {output_filename_type} ...")
            self.write_df_to_file(output_filename_type, token_df)
        else:
            self.logger.error("Failed to get token list")


if __name__ == "__main__":
    myObject = TokenList()
    myObject.run()
