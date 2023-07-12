from sqlalchemy.orm import Session

from core.db import models
from core.utils.elasticsearch import es


def create_keywords(contents: str, db: Session): 
    result = es.indices.analyze(
        index="postgres",
        body={
            "char_filter": ["html_strip"],
            "tokenizer": {
                "type": "nori_tokenizer",
                "decompound_mode": "mixed"
            },
            "filter": [
                "lowercase",
                {
                    "type": "nori_part_of_speech",
                    "stoptags": ["E",
                                "IC",
                                "J",
                                "MAG", "MAJ", "MM",
                                "UNA", "NA", 
                                "SP", "SSC", "SSO", "SC", "SE",
                                "XPN", "XSA", "XSN", "XSV",
                                "VA", "VCN", "VCP", "VSV", "VV", "VX",
                                "XPN", "XR", "XSA", "XSN", "XSV"]
                },
            ],
            "text": contents,
        }
    )


    response = es.indices.analyze(
            index="keyword",
            body={
                "char_filter": ["html_strip"],
                "tokenizer": {
                    "type": "standard"
                },
                "filter": [
                    "lowercase",
                    "word_delimiter_graph",
                    {
                        "type": "shingle",
                        "min_shingle_size": 2,
                        "max_shingle_size": 2
                    },
                ],
                "text": contents
            }
        )
    result['tokens'].extend(response['tokens'])
    
    for token in result['tokens']:
        keyword = models.Keyword(keyword=token['token'])
        if db.query(models.Keyword).filter(models.Keyword.keyword == keyword.keyword).all():
            continue
        else:
            db.add(keyword)
            db.commit()
            db.refresh(keyword)
    return
        
