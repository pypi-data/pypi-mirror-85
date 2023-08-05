import json
import pandas as pd
from . import feature_generation_utils as fgu

class json_to_table:
    def __init__(self, document_str):
        self.json_documents = json.loads(document_str)
        if not isinstance(self.json_documents, list):
            self.json_documents = [self.json_documents]
            
        self.utils = fgu.FeatureGenerationUtils()
        
    def to_frame(self, columns, prefix=None):
        if isinstance(columns, dict):
            table = self.to_table(list(columns.keys()), prefix=prefix)
            df = pd.DataFrame.from_records(table, columns=list(columns.values()))
        else:
            table = self.to_table(columns, prefix=prefix)
            df = pd.DataFrame.from_records(table, columns=columns)
        
        return df
            
    def to_table(self, columns, prefix=None):
        table = []
        for document in self.json_documents:
            record = []
            for column in columns:
                if prefix != None:
                    column = prefix + '.' + column
                    
                property_value = self.utils.get_document_property(document, column)
                record.append(property_value)
            
            table.append(record)
        
        return table