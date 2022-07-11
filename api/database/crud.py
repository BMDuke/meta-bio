from typing import List

from sqlalchemy import select, or_
from sqlalchemy.orm import Session, Query
from sqlalchemy.sql import exists
from sqlalchemy.sql.expression import Select

from database.models import DataRelease, Genome, GenomeDatabase, Organism
from database.schemas import MetaDataResponse, MetaDataResponseList


'''
This file contains commonly used database queries and subqueries.

'''


def get_metadata(   
    db: Session,
    organism: str = None, 
    db_type: str = None, 
    release: int = None
        ) -> MetaDataResponseList:

    '''
    '''

    # Create subquery by joining the data_release and organism tables 
    # to the genome table. Filter results based on organism and release.
    subq = get_genome_subq(organism, release)

    # Create a full query using the intermediate genome table and
    # the genome_database table
    query = join_genome_subq_genome_database_in_full(subq.subquery())

    # Filter results for a specific organism if provided
    if db_type:

        query = filter_query_on_dbtype(query, db_type)

    # Submit DB transation
    results = db.query(query.subquery()).limit(20)
    
    # Return results
    return [r._asdict() for r in results]


def get_genome_subq(

    organism: str = None,
    release: int = None

        ) -> Select:

    '''
    '''

    # Join Data Release table onto Genome table 
    subq = join_data_release_genome_on_release_id()

    # Filter results for specific release if provided 
    if release: 

        subq = filter_subq_on_release(subq, release)
    
    # Join Organism table onto intermediate results
    subq = join_organism_subq_on_organism_id(subq)

    # Filter results for a specific organism if provided
    if organism:

        subq = filter_subq_on_organism(subq, organism)       
 

    return subq



def join_data_release_genome_on_release_id() -> Select:
    '''
    '''

    subq = select(
        
        # Define the columns to return and give labels
        Genome.c.genome_id.label('genome_id'), 
        DataRelease.c.ensembl_version.label('release'), 
        Organism.c.name.label('organism')
        
        ).join(
            
            DataRelease, 
            DataRelease.c.data_release_id == Genome.c.data_release_id
            
        )    
    
    return subq

def filter_subq_on_release(subq: Select, release: int) -> Select:
    '''
    '''

    subq = subq.where(

        DataRelease.c.ensembl_version == release

    )    

    return subq

def join_organism_subq_on_organism_id(subq: Select) -> Select:
    '''
    '''

    subq = subq.join(
            
            Organism, 
            Organism.c.organism_id == Genome.c.organism_id
            
        )   

    return subq 

def filter_subq_on_organism(subq: Select, organism: str) -> Select:
    '''
    '''    

    subq = subq.where(

        or_(
            
            Organism.c.name == organism,
            Organism.c.scientific_name == organism

        )

    )    

    return subq

def join_genome_subq_genome_database_in_full(subq: Query) -> Select:
    '''
    '''
    
    query = select (

        # Define the columns to return and give labels
        GenomeDatabase.c.dbname.label('dbname'),
        GenomeDatabase.c.type.label('dbtype'),
        subq.c.release,
        subq.c.organism

    ).join (

        subq,
        subq.c.genome_id == GenomeDatabase.c.genome_id

    )

    return query

def filter_query_on_dbtype(query: Select, dbtype: str) -> Select: 
    '''
    '''

    query = query.where(

        GenomeDatabase.c.type == dbtype

    )    

    return query

def check_organism_exists_in_db(db: Session, organism: str) -> bool:
    '''
    '''

    does_exist = db.query(
        
        exists().where(
        
            or_(
                
                Organism.c.name == organism,
                Organism.c.scientific_name == organism
                
                )
                
            )
        
        ).scalar()
    
    return does_exist



