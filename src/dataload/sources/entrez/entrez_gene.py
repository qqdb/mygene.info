from .entrez_base import GeneInfoParser
from .entrez_base import get_geneid_d
import biothings.dataload.uploader as uploader
import biothings.dataload.uploader as uploader

class EntrezGeneUploader(uploader.MergerSourceUploader):

    name = "entrez_gene"
    main_source = "entrez"
    ENTREZ_GENEDOC_ROOT = True

    def load_data(self, data_folder):
        self.parser = GeneInfoParser(data_folder)
        self.parser.set_all_species()
        genedoc_d = self.parser.load()
        return genedoc_d

    def get_mapping(self):
        mapping = {
            "entrezgene": {
                "type": "long"
            },
            "taxid": {
                "type": "integer",
                "include_in_all": False
            },
            "alias": {
                "type": "string"
            },
            "name": {
                "type": "string",
                "boost": 0.8    # downgrade name field a little bit
            },
            "symbol": {
                "type": "string",
                "analyzer": "string_lowercase",
                "boost": 5.0
            },
            "locus_tag": {
                "type": "string",
                "analyzer": "string_lowercase"
            },
    
            # do not index map_location and type_of_gene
            "map_location": {
                "index": "no",
                "type": "string",
                "include_in_all": False
            },
            "type_of_gene": {
                # "index": "no",
                "index": "not_analyzed",
                "type": "string",
                "include_in_all": False
            },
            "AnimalQTLdb": {
                "index": "no",
                "type": "string",
                "include_in_all": False
            },
            "Vega": {
                "index": "no",
                "type": "string",
                "include_in_all": False
            },
    
            # convert index_name to lower-case, and excluded from "_all"
            "HGNC": {
                "type": "string",              # 1771
                "index": "not_analyzed",
                "include_in_all": False,
                "copy_to": 'hgnc'
            },
            "HPRD": {
                "type": "string",              # 00310
                "index": "not_analyzed",
                "include_in_all": False,
                "copy_to": 'hprd'
            },
            "MIM": {
                "type": "string",              # 116953
                "index": "not_analyzed",
                "include_in_all": False,
                "copy_to": 'mim'
            },
            "MGI": {
                "type": "string",              # MGI:104772
                "index": "not_analyzed",
                "include_in_all": False,
                "copy_to": 'mgi'
            },
            "RATMAP": {
                "type": "string",
                "index": "not_analyzed",
                "include_in_all": False,
                "copy_to": 'ratmap'
            },
            "RGD": {
                "type": "string",             # 70486
                "index": "not_analyzed",
                "include_in_all": False,
                "copy_to": 'rgd'
            },
            "FLYBASE": {
                "type": "string",            # FBgn0004107
                "analyzer": "string_lowercase",
                "include_in_all": False,
                "copy_to": 'flybase'
            },
            "WormBase": {
                "type": "string",         # WBGene00000871
                "analyzer": "string_lowercase",
                "include_in_all": False,
                "copy_to": 'wormbase'
            },
            "TAIR": {
                "type": "string",             # AT3G48750
                "analyzer": "string_lowercase",
                "include_in_all": False,
                "copy_to": 'tair'
            },
            "ZFIN": {
                "type": "string",             # ZDB-GENE-040426-2741
                "analyzer": "string_lowercase",
                "include_in_all": False,
                "copy_to": 'zfin'
            },
            "Xenbase": {
                "type": "string",
                "analyzer": "string_lowercase",
                "include_in_all": False,
                "copy_to": 'xenbase'
            },
            "miRBase": {
                "type": "string",
                "analyzer": "string_lowercase",
                "include_in_all": True,
                "copy_to": 'mirbase'
            },
        }
        return mapping

    def get_geneid_d(self):
        return get_geneid_d()

    def generate_doc_src_master(self):
        # TODO: not sure this ENTREZ_GENEDOC_ROOT is actually useful now we're using class inheritance
        _doc = super(uploader.MergerSourceUploader,self).generate_doc_src_master()
        _doc["ENTREZ_GENEDOC_ROOT"] = True

    def post_update_data(self):
        self.logger.info('Uploading "geneid_d" to GridFS...')
        geneid_d = self.get_geneid_d()
        dump2gridfs(geneid_d, self.name + '__geneid_d.pyobj', self.db)
