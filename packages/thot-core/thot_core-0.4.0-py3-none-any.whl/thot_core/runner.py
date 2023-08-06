
# coding: utf-8

# # Runner Core

# In[ ]:


import os
import sys
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

from .classes.container import Container


# In[ ]:


class Runner:
    """
    For performing analysis on a Thot project.
    
    Hooks are:
        + get_container: Method to retrieve the Container being run. 
            Provided the root id, should return the Container.
            [Siganture: ( root ) => ( Container )]
            [Required]
            
        + get_script_info: Method to retrieve require information about the Script being run.
            [Signature: ( ScriptAssociation.script ) => ( script id, script path ) ]
            [Required]
        
        + script_error: Runs when a Script creates an error.
            [Signature: ( error, ignore_errors ) => ()]
            
        + assets_added: Run after a Script analysis is complete, passed ids of the added Assets.
            [Signature: ( added_assets ) => ()]
            
        + complete: Run after a subtree completes.
            [Signature: () => ()]
    """
    
    def __init__( self ):
        """
        Initializes a new Runner.
        """
        self.hooks = {
            'get_container':   None,
            'get_script_info': None,
            'script_error':    self._default_script_error_handler,
            'assets_added':    None,
            'complete':        None
        }
    
    
    def register( self, hook, method ):
        """
        Registers a hook method.
        
        :param hook: Name of the hook to register.
        :param method: Method to run.
        """
        if hook not in self.hooks:
            # hook is invalid,
            # all hook names are defined in constructor
            raise ValueError( 'Invalid hook name.' )
        
        self.hooks[ hook ] = method
    
    
    
    def run_script( self, script_id, script_path, container_id ):
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
        self,
        root, 
        scripts = None,
        ignore_errors = False, 
        multithread = False, 
        verbose = False,
    ):
        """
        Runs scripts on the Container tree.
        Uses DFS, running from bottom up.

        :param root: Container.
        :param scripts: List of scripts to run, or None for all. [Default: None]
        :param ignore_errors: Continue running if an error is encountered. [Default: False]
        :param multithread: Evaluate tree using multiple threads. 
            True to use default number of threads, or an integer 
            to specify how many threads to use. 
            If interpreted as boolean is False, will use a single thread.
            CAUTION: May decrease runtime, but also locks system and can not kill.
            [Default: False] [Default Threads: 5]
        :param verbose: Print evaluation information. [Default: False]
        """
        self._check_hooks()
        
        root = self.hooks[ 'get_container' ]( root )
        if not isinstance( root, Container ):
            root = Container( **root )

        # eval children
        kwargs = {
            'scripts': scripts,
            'ignore_errors': ignore_errors,
            'multithread': multithread,
            'verbose': verbose
        }
        
        if multithread:
            max_workers = (
                5 # default
                if multithread is True else
                multithread
            )
            
            with ThreadPoolExecutor( max_workers = max_workers ) as executer:
                # only enable threading at top level
                kwargs[ 'multithread' ] = False
                
                executer.map( 
                    lambda child: self.eval_tree( child, **kwargs ), 
                    root.children 
                )

        else:
            for child in root.children:
                # recurse
                self.eval_tree( child, **kwargs )

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

            ( script_id, script_path ) = self.hooks[ 'get_script_info' ]( association.script )

            if verbose:
                print( 'Running script {} on container {}'.format( script_id, root._id )  )

            try:
                script_assets = self.run_script( 
                    str( script_id ), # convert ids if necessary
                    script_path, 
                    str( root._id ) 
                ) 

            except Exception as err:
                self.hooks[ 'script_error' ]( err, ignore_errors )

            if self.hooks[ 'assets_added' ]:
                script_assets = [ 
                    json.loads( asset ) for asset
                    in script_assets.decode().split( '\n' )
                    if asset
                ]

                self.hooks[ 'assets_added' ]( script_assets )


        if self.hooks[ 'complete' ]:
            self.hooks[ 'complete' ]()
            
            
    def _check_hooks( self ):
        """
        Verifies registered hooks.
        
        :throws: Error if registered hook is invalid.
        """
        if not self.hooks[ 'get_container' ]:
            raise Error( 'Required hook get_container is not set.' )
        
        if not self.hooks[ 'get_script_info' ]:
            raise Error( 'Required hook get_script_info is not set.' )
    
    
    @staticmethod
    def _default_script_error_handler( err, ignore_errors = False ):
        """
        
        """
        if ignore_errors:
            # TODO [2]: Only return errors after final exit.
            # collect errors for output at end
            print( '[{}] {}'.format( root._id, err ) )

        else:
            raise err


# # Work
