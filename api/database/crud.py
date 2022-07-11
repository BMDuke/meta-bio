from sqlalchemy import select, or_
from sqlalchemy.orm import Session, Query
from sqlalchemy.sql import exists
from sqlalchemy.sql.expression import Select

from database.models import DataRelease, Genome, GenomeDatabase, Organism
from database.schemas import MetaDataResponseList


'''
This file contains commonly used database queries and subqueries.

'''


def get_metadata(   
    db: Session,
    organism: str = None, 
    db_type: str = None, 
    release: int = None,
    offset: int = 0,
    limit: int = 20,
        ) -> MetaDataResponseList:

    '''
    Takes SQLAlchemy session and values from query parameters as inputs.
    It builds the query, queries tha database and returns the results to the 
    user.
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
    results = db.query(query.subquery()).offset(offset).limit(limit)
    
    # Return results
    return [r._asdict() for r in results]


def get_genome_subq(

    organism: str = None,
    release: int = None

        ) -> Select:

    '''
    Builds the subquery that joins the data_release and organism
    tables to the genome table, with optional filtering.
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
    Joins the data_release table to the genome table
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
    Filter the genome:data_release table for release version
    '''

    subq = subq.where(

        DataRelease.c.ensembl_version == release

    )    

    return subq

def join_organism_subq_on_organism_id(subq: Select) -> Select:
    '''
    Joins the organism table to the genome table
    '''

    subq = subq.join(
            
            Organism, 
            Organism.c.organism_id == Genome.c.organism_id
            
        )   

    return subq 

def filter_subq_on_organism(subq: Select, organism: str) -> Select:
    '''
    Filter the genome:data_release:organism table for organism name
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
    Joins the results of the genome subquery with the genome_dataset table
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
    Filter the subquery:genome_dataset on db_type
    '''

    query = query.where(

        GenomeDatabase.c.type == dbtype

    )    

    return query

def check_organism_exists_in_db(db: Session, organism: str) -> bool:
    '''
    Takes a SQLAlchemy session and an organism name and checks to see whether
    it is present in the Organism table. Returns a boolean value.
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



