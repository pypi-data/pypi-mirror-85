
# coding: utf-8

# # Runner

# In[ ]:


import os
import sys
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

from .classes.container import Container


# In[ ]:


def run_script( script_id, script_path, container_id ):
    """
    Runs the given program form the given Container.
    
    :param script_id: Id of the script.
    :param script_path: Path to the script.
    :param container: Id of the container to run from.
    :returns: Script output. Used for collecting added assets.
    """
    # setup environment
    env = os.environ.copy()
    env[ 'THOT_CONTAINER_ID' ] = container_id # set root container to be used by thot library
    env[ 'THOT_SCRIPT_ID' ]    = script_id    # used in project for adding Assets
    
    # TODO [0]: Ensure safely run
    # run program
    try:
        return subprocess.check_output(
            'python {}'.format( script_path ),
            shell = True,
            env = env
        )
        
    except subprocess.CalledProcessError as err:
        err.cmd = '[{}] '.format( container_id ) + err.cmd
        raise err
    
    
# TODO [2]: Allow running between certain depths.
def eval_tree( 
    root, 
    db, 
    script_info,
    scripts = None,
    ignore_errors = False, 
    multithread = False, 
    verbose = False,
    driver = None
):
    """
    Runs scripts on the Container tree.
    Uses DFS, running from bottom up.
    
    :param root: Container.
    :param db: Database.
    :param script_info: Function accepting <script id> as a parameter 
        and returning a tuple ( <script_id>, <script_path> ).
    :param scripts: List of scripts to run, or None for all. [Default: None]
    :param ignore_errors: Continue running if an error is encountered. [Default: False]
    :param multithread: Evaluate tree using multiple threads. [Default: False]
        CAUTION: May decrease runtime, but also locks system and can not kill.
    :param verbose: Print evaluation information. [Default: False]
    :param driver: Driver used to modify script retrieval. [Default: None]
    """
    if isinstance( root, str ):
        root = db.containers.find_one( { '_id': root } )
    
    if not isinstance( root, Container ):
        root = Container( **root )
            
    # eval children
    if multithread:
        with ThreadPoolExecutor( max_workers = 10 ) as executer:
            executer.map( 
                lambda child: eval_tree( child, db, verbose = verbose ), 
                root.children 
            )
        
    else:
        for child in root.children:
            eval_tree( 
                child, 
                db, 
                script_info,
                scripts       = scripts,
                ignore_errors = ignore_errors,
                multithread   = multithread,
                verbose       = verbose,
                driver        = driver
            )

    # TODO [1]: Check filtering works for local projects.
    # filter scripts to run
    root.scripts.sort()
    run_scripts = (
        root.scripts
        if scripts is None else
        filter( lambda assoc: assoc.script in scripts, root.scripts ) # filter scripts
    )
    
    # eval self
    added_assets = []
    for association in run_scripts:
        if not association.autorun:
            continue
        
        
        ( script_id, script_path ) = script_info( association.script )
        
        if verbose:
            print( 'Running script {} on container {}'.format( script_id, root._id )  )
            
        try:
            script_assets = run_script( 
                str( script_id ), # convert ids from ObjectId, if necessary
                script_path, 
                str( root._id ) 
            ) 
            
        except Exception as err:
            if ignore_errors:
                # TODO [2]: Only return errors after final exit.
                # collect errors for output at end
                print( '[{}] {}'.format( root._id, err ) )
                
            else:
                raise err
                
        if driver:
            script_assets = [ 
                json.loads( asset ) for asset
                in script_assets.decode().split( '\n' )
                if asset
            ]
            
            driver.added_assets += script_assets
            

    if driver:
        driver.flush_added_assets()


# # Work
