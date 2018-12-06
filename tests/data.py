FILE_BEFORE_PROCESSING = """
import math
    
# ▼▼▼ MY TEMP CODE. DELETE ME ▼▼▼
import pdb; pdb.set_trace()
# ▲▲▲ MY TEMP CODE. DELETE ME ▲▲▲
    
for x in range(10):
    print(x)
    
"""

FILE_WITHOUT_CLOSING_TAG = """
import math
    
# ▼▼▼ MY TEMP CODE. DELETE ME ▼▼▼
import pdb; pdb.set_trace()
    
for x in range(10):
    print(x)
    
"""

FILE_AFTER_DELETE_PROCESSOR = """
import math
    
    
for x in range(10):
    print(x)
    
"""

FILE_AFTER_COMMENT_PROCESSOR = """
import math
    
# # ▼▼▼ MY TEMP CODE. DELETE ME ▼▼▼
# import pdb; pdb.set_trace()
# # ▲▲▲ MY TEMP CODE. DELETE ME ▲▲▲
    
for x in range(10):
    print(x)
    
"""
