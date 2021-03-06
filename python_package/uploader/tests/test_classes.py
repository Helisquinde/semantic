__author__ = 'Stephen Kan'

import unittest
import mock
from superphy.uploader import classes
from rdflib import Graph, Namespace

n = Namespace("https://github.com/superphy#")
owl = Namespace("http://www.w3.org/2002/07/owl#")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
xml = Namespace("http://www.w3.org/XML/1998/namespace")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
gfvo = Namespace("http://www.biointerchange.org/gfvo#")

class ClassesTestCase(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()

    def tearDown(self):
        self.graph.remove((None, None, None))

    def check_triples(self, fields, outputs):
        self.assertTrue(len(outputs) is len(fields))
        for item in fields:
            self.assertTrue(item in str(outputs))

    # used for generating results for test to compare against (please manually confirm validity before using)
    def temp_print(self, name):
        print list(self.graph.objects(n[name]))
        print list(self.graph.subjects(object=n[name]))
        print self.graph.serialize(format="turtle")

    def test_NamedIndividual(self):
        instance = classes.NamedIndividual(self.graph, "foobar")
        instance.rdf()

        fields = ["http://www.w3.org/2002/07/owl#NamedIndividual"]
        objects = list(self.graph.objects(n["foobar"]))

        self.check_triples(fields, objects)

    def test_User(self):
        user = classes.User(self.graph, "test@test.com")
        user.rdf()

        fields = ["http://www.w3.org/2002/07/owl#NamedIndividual",
                  "test@test.com",
                  "https://github.com/superphy#User"]
        objects = list(self.graph.objects(n["test@test.com"]))

        self.check_triples(fields, objects)

    def test_Organism(self):
        organism = classes.Organism(self.graph, "ecoli", "Escherichia coli (E. coli)", "Escherichia coli", "E. coli", 562)
        organism.rdf()

        fields = ["E. coli",
                  "Escherichia coli",
                  "562",
                  "Escherichia coli (E. coli)",
                  "http://www.w3.org/2002/07/owl#NamedIndividual",
                  "https://github.com/superphy#Organism"]
        objects = list(self.graph.objects(n["ecoli"]))

        self.check_triples(fields, objects)

    def test_Host(self):
        host = classes.Host(self.graph, "hsapiens", "Homo sapiens (human)", "Homo sapiens", "human", "human", 9606)
        host.rdf()

        fields = ["http://www.w3.org/2002/07/owl#NamedIndividual",
                  "https://github.com/superphy#Host",
                  "Homo sapiens (human)",
                  "9606",
                  "https://github.com/superphy#human",
                  "Homo sapiens",
                  "https://github.com/superphy#Organism",
                  "https://github.com/superphy#from_hsapiens",
                  "human"]
        objects = list(self.graph.objects(n["hsapiens"]))

        self.check_triples(fields, objects)

        fields = ["https://github.com/superphy#from_hsapiens",
                  "https://github.com/superphy#human"]
        subjects = list(self.graph.subjects(object=n["hsapiens"]))

        self.check_triples(fields, subjects)

    def test_Microbe(self):
        microbe = classes.Microbe(self.graph, "ecoli", "Escherichia coli (E. coli)", "Escherichia coli", "E. coli", 562)
        microbe.rdf()

        fields = ["https://github.com/superphy#Organism",
                  "Escherichia coli",
                  "E. coli",
                  "http://www.w3.org/2002/07/owl#NamedIndividual",
                  "562",
                  "Escherichia coli (E. coli)",
                  "https://github.com/superphy#Microbe"]
        objects = list(self.graph.objects(n["ecoli"]))

        self.check_triples(fields, objects)

    def test_Attribute(self):
        attribute = classes.Attribute(self.graph, "attribute")
        attribute.rdf()

        fields = ["http://www.w3.org/2002/07/owl#NamedIndividual",
                  "https://github.com/superphy#Attribute"]
        objects = list(self.graph.objects(n["attribute"]))

        self.check_triples(fields, objects)

    def test_HostCategory(self):
        hostcategory = classes.HostCategory(self.graph, "human", "Human")
        hostcategory.rdf()

        fields = ["Human",
                  "http://www.w3.org/2002/07/owl#NamedIndividual",
                  "https://github.com/superphy#host_category"]
        objects = list(self.graph.objects(n["human"]))

        self.check_triples(fields, objects)

    def test_IsolationAttribute(self):
        isolation_attribute = classes.IsolationAttribute(self.graph, "from_hsapiens")
        isolation_attribute.rdf()

        fields = ["https://github.com/superphy#Attribute",
                  "https://github.com/superphy#isolation_attribute",
                  "http://www.w3.org/2002/07/owl#NamedIndividual"]
        objects = list(self.graph.objects(n["from_hsapiens"]))

        self.check_triples(fields, objects)

    def test_FromHost(self):
        from_host = classes.FromHost(self.graph, "hsapiens", "human")
        from_host.rdf()

        fields = ["http://www.w3.org/2002/07/owl#NamedIndividual",
                  "https://github.com/superphy#Attribute",
                  "https://github.com/superphy#isolation_attribute",
                  "https://github.com/superphy#isolation_from_host",
                  "https://github.com/superphy#human",
                  "https://github.com/superphy#hsapiens"]
        objects = list(self.graph.objects(n["from_hsapiens"]))

        self.check_triples(fields, objects)

        fields = ["https://github.com/superphy#human",
                  "https://github.com/superphy#hsapiens"]
        subjects = list(self.graph.subjects(object=n["from_hsapiens"]))

        self.check_triples(fields, subjects)

    def test_FromSource(self):
        from_source = classes.FromSource(self.graph, "stool", "Stool", "human")
        from_source.rdf()

        fields = ["https://github.com/superphy#Attribute",
                  "https://github.com/superphy#human",
                  "http://www.w3.org/2002/07/owl#NamedIndividual",
                  "Stool",
                  "https://github.com/superphy#isolation_from_source",
                  "https://github.com/superphy#isolation_attribute"]
        objects = list(self.graph.objects(n["stool"]))

        self.check_triples(fields, objects)

        fields = ["https://github.com/superphy#human"]
        subjects = list(self.graph.subjects(object=n["stool"]))

        self.check_triples(fields, subjects)

    def test_IsolationSyndrome(self):
        isolation_syndrome = classes.IsolationSyndrome(self.graph, "meningitis", "Meningitis", "human")
        isolation_syndrome.rdf()

        fields = ["https://github.com/superphy#isolation_attribute",
                  "https://github.com/superphy#Attribute",
                  "https://github.com/superphy#human",
                  "Meningitis",
                  "http://www.w3.org/2002/07/owl#NamedIndividual",
                  "https://github.com/superphy#isolation_syndrome"]
        objects = list(self.graph.objects(n["meningitis"]))

        self.check_triples(fields, objects)

        fields = ["https://github.com/superphy#human"]
        subjects = list(self.graph.subjects(object=n["meningitis"]))

        self.check_triples(fields, subjects)

    def test_Serotype(self):
        serotype = classes.Serotype(self.graph, "OUnknown")
        serotype.rdf()

        fields = ["http://www.w3.org/2002/07/owl#NamedIndividual",
                  "https://github.com/superphy#serotype",
                  "https://github.com/superphy#Attribute"]
        objects = list(self.graph.objects(n["OUnknown"]))

        self.check_triples(fields, objects)

    def test_Otype(self):
        otype = classes.Otype(self.graph, 157)
        otype.rdf()

        fields =["http://www.w3.org/2002/07/owl#NamedIndividual",
                 "https://github.com/superphy#serotype",
                 "https://github.com/superphy#Attribute",
                 "https://github.com/superphy#Otype"]
        objects = list(self.graph.objects(n["O157"]))

        self.check_triples(fields, objects)

    def test_Htype(self):
        htype = classes.Htype(self.graph, 7)
        htype.rdf()

        fields =["http://www.w3.org/2002/07/owl#NamedIndividual",
                 "https://github.com/superphy#serotype",
                 "https://github.com/superphy#Attribute",
                 "https://github.com/superphy#Htype"]
        objects = list(self.graph.objects(n["H7"]))

        self.check_triples(fields, objects)

    @mock.patch('superphy.uploader.classes.sparql')
    def test_Genome(self, mock_sparql):

        mock_sparql.find_from_host.return_value = "https://github.com/superphy#from_hsapiens"
        mock_sparql.find_source.return_value = "https://github.com/superphy#feces"
        mock_sparql.find_syndrome.return_value = "https://github.com/superphy#uti"

        kwargs = {"date": {"2013-06-24"},
                  "location": {"United States, California, Santa Clara"},
                  "accession": {"JNOG00000000"},
                  "bioproject": {"251898"},
                  "biosample": {"2841129"},
                  "strain": {"CS03"},
                  "organism": "ecoli",
                  "host": {"Homo sapiens (human)"},
                  "source": {"Feces"},
                  "syndrome": {"Urinary tract infection (cystitis)"},
                  "Htype": "-",
                  "Otype": None,
                  }

        genome = classes.Genome(self.graph, "JNOG00000000", **kwargs)
        genome.rdf()

        field = {"https://github.com/superphy#H-",
                 "https://github.com/superphy#from_hsapiens",
                 "United States, California, Santa Clara",
                 "JNOG00000000",
                 "https://github.com/superphy#ecoli",
                 "https://github.com/superphy#OUnknown",
                 "https://github.com/superphy#feces",
                 "2841129",
                 "https://github.com/superphy#uti",
                 "251898",
                 "http://www.w3.org/2002/07/owl#NamedIndividual",
                 "CS03",
                 "2013-06-24",
                 "http://www.biointerchange.org/gfvo#Genome"}
        objects = list(self.graph.objects(n["JNOG00000000"]))

        self.check_triples(field, objects)

        field = {"https://github.com/superphy#uti",
                 "https://github.com/superphy#from_hsapiens",
                 "https://github.com/superphy#H-",
                 "https://github.com/superphy#feces",
                 "https://github.com/superphy#OUnknown",
                 "https://github.com/superphy#ecoli"}
        subjects = list(self.graph.subjects(object=n["JNOG00000000"]))

        self.check_triples(field, subjects)

    @mock.patch('superphy.uploader.classes.sparql')
    def test_PendingGenome(self, mock_sparql):

        mock_sparql.find_from_host.return_value = "https://github.com/superphy#from_hsapiens"
        mock_sparql.find_source.return_value = "https://github.com/superphy#feces"
        mock_sparql.find_syndrome.return_value = "https://github.com/superphy#uti"

        kwargs = {"date": {"2013-06-24"},
                  "location": {"United States, California, Santa Clara"},
                  "accession": {"JNOG00000000"},
                  "bioproject": {"251898"},
                  "biosample": {"2841129"},
                  "strain": {"CS03"},
                  "organism": "ecoli",
                  "host": {"Homo sapiens (human)"},
                  "source": {"Feces"},
                  "syndrome": {"Urinary tract infection (cystitis)"},
                  "Htype": "-",
                  "Otype": None,
                  }

        pending_genome = classes.PendingGenome(self.graph, "JNOG00000000", **kwargs)
        pending_genome.rdf()

        field = {"https://github.com/superphy#H-",
                 "https://github.com/superphy#from_hsapiens",
                 "United States, California, Santa Clara",
                 "JNOG00000000",
                 "https://github.com/superphy#ecoli",
                 "https://github.com/superphy#OUnknown",
                 "https://github.com/superphy#feces",
                 "2841129",
                 "https://github.com/superphy#uti",
                 "251898",
                 "http://www.w3.org/2002/07/owl#NamedIndividual",
                 "CS03",
                 "2013-06-24",
                 "http://www.biointerchange.org/gfvo#Genome",
                 "https://github.com/superphy#pending_genome"}
        objects = list(self.graph.objects(n["JNOG00000000"]))

        self.check_triples(field, objects)

        field = {"https://github.com/superphy#uti",
                 "https://github.com/superphy#from_hsapiens",
                 "https://github.com/superphy#H-",
                 "https://github.com/superphy#feces",
                 "https://github.com/superphy#OUnknown",
                 "https://github.com/superphy#ecoli"}
        subjects = list(self.graph.subjects(object=n["JNOG00000000"]))

        self.check_triples(field, subjects)

    @mock.patch('superphy.uploader.classes.sparql')
    def test_CompletedGenome(self, mock_sparql):

        mock_sparql.find_from_host.return_value = "https://github.com/superphy#from_hsapiens"
        mock_sparql.find_source.return_value = "https://github.com/superphy#feces"
        mock_sparql.find_syndrome.return_value = "https://github.com/superphy#uti"

        kwargs = {"date": {"2013-06-24"},
                  "location": {"United States, California, Santa Clara"},
                  "accession": {"JNOG00000000"},
                  "bioproject": {"251898"},
                  "biosample": {"2841129"},
                  "strain": {"CS03"},
                  "organism": "ecoli",
                  "host": {"Homo sapiens (human)"},
                  "source": {"Feces"},
                  "syndrome": {"Urinary tract infection (cystitis)"},
                  "Htype": "-",
                  "Otype": None,
                  }

        completed_genome = classes.CompletedGenome(self.graph, "JNOG00000000", **kwargs)
        completed_genome.rdf()

        field = {"https://github.com/superphy#H-",
                 "https://github.com/superphy#from_hsapiens",
                 "United States, California, Santa Clara",
                 "JNOG00000000",
                 "https://github.com/superphy#ecoli",
                 "https://github.com/superphy#OUnknown",
                 "https://github.com/superphy#feces",
                 "2841129",
                 "https://github.com/superphy#uti",
                 "251898",
                 "http://www.w3.org/2002/07/owl#NamedIndividual",
                 "CS03",
                 "2013-06-24",
                 "http://www.biointerchange.org/gfvo#Genome",
                 "https://github.com/superphy#completed_genome"}
        objects = list(self.graph.objects(n["JNOG00000000"]))

        self.check_triples(field, objects)

        field = {"https://github.com/superphy#uti",
                 "https://github.com/superphy#from_hsapiens",
                 "https://github.com/superphy#H-",
                 "https://github.com/superphy#feces",
                 "https://github.com/superphy#OUnknown",
                 "https://github.com/superphy#ecoli"}
        subjects = list(self.graph.subjects(object=n["JNOG00000000"]))

        self.check_triples(field, subjects)

