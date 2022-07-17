from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, SmallInteger
from sqlalchemy.orm import relationship

from .database import Base, engine

from sqlalchemy import MetaData

'''
This file instantiates the database models which are used by SQL Alchemy 
to perform ORM.

Based on the following table schema:
 > https://raw.githubusercontent.com/Ensembl/ensembl-metadata/release/106/sql/table.png

we have two options to create our models. We could
 - Create them declaratively - implementing the schema above
 - Reflect the tables - use the database schema to generate our python objects

I will use the reflection option for this project.
However, in a real life project I would avoid this due to the 
network overhead.

I will also provide an example using a declarative approach commented out 
below for inspection.
'''

# Create a metadata object
metadata_obj = MetaData()

# Bind the database engine and reflect the tables
metadata_obj.reflect(bind=engine)

# Define the tables 
DataRelease = metadata_obj.tables['data_release']
Genome = metadata_obj.tables['genome']
GenomeDatabase = metadata_obj.tables['genome_database']
Organism = metadata_obj.tables['organism']



# class DataRelease(Base):
#     __tablename__ = "data_release"

#     # Primary key
#     data_release_id = Column(Integer(10), primary_key=True)

#     # Columns
#     ensembl_version = Column(Integer(10))
#     ensembl_genomes_version = Column(Integer(10))
#     release_date = Column(Date)
#     is_current = Column(SmallInteger)

# class Genome(Base):
#     __tablename__ = "genome"

#     # Primary key
#     genome_id = Column(Integer(10), primary_key=True)

#     # Foreign keys
#     data_release_id = Column(Integer(10))
#     assembly_id = Column(Integer(10))
#     organism_id = Column(Integer(10))
#     division_id = Column(Integer(10))

#     # Columns
#     genebuild = Column(String(64))
#     has_pan_compara = Column(SmallInteger) 
#     has_variations = Column(SmallInteger)
#     has_peptide_compara = Column(SmallInteger)
#     has_genome_alignments = Column(SmallInteger)
#     has_synteny = Column(SmallInteger)
#     has_other_alignments = Column(SmallInteger)

#     # Relations
#     relationship("data_release")
#     relationship("assembly_id")
#     relationship("organism_id")
#     relationship("division_id")





