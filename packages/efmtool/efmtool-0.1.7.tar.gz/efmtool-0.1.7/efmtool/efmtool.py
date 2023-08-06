import glob
import jpype
import logging
import numpy as np
import os
import scipy.io
import tempfile
from typing import Dict, List

logger = logging.getLogger(__name__)
package_directory = os.path.dirname(os.path.abspath(__file__))
CalculateFluxModes : jpype.JClass = None

def _relative_filename(folder : str, file : str) -> str:
    return os.path.relpath(os.path.join(folder, file), '.')

def _read_efms_from_mat(folder : str) -> np.array:
    # efmtool stores the computed EFMs in one or more .mat files. This function
    # finds them and loads them into a single numpy array.
    efm_parts : List[np.array] = []
    files_list = sorted(glob.glob(os.path.join(folder, 'efms_*.mat')))
    for f in files_list:
        mat = scipy.io.loadmat(f, verify_compressed_data_integrity=False)
        efm_parts.append(mat['mnet']['efms'][0, 0])

    if len(efm_parts) == 1:
        return efm_parts
    else:
        return np.concatenate(efm_parts, axis=1)

def calculate_efms(
    stoichiometry : np.array,
    reversibilities : List[int],
    reaction_names : List[str],
    metabolite_names : List[str],
    options : Dict = None,
    jvm_options : List[str] = None
) -> np.array:
    """Calculates all the Elementary Flux Modes (EFMs) in a reaction network. 

    Parameters
    ----------
    stoichiometry : np.array
        m-by-n array describing the stoichiometry of the network.
    reversibilities : List[int]
        n-elements list specifying whether each reaction is reversible (1) or
        not (0).
    reaction_names : List[str]
        n-elements list of reaction names.
    metabolite_names : List[str]
        m-elements list of metabolite names.
    options : Dict, optional
        List of options to pass to efmtool. Defaults can be obtained with
        get_default_options().
    jvm_options : List[str], optional
        List of arguments to be passed to the JVM.

    Returns
    -------
    np.array
        n-by-e array containing the e EFMs found in the network.
    """
    options = options or get_default_options()

    # Create temporary directory for efmtool and input/output files.
    tmp_dir = tempfile.TemporaryDirectory()
    options['tmpdir'] = os.path.relpath(tmp_dir.name, '.')
    options['stoich'] = _relative_filename(tmp_dir.name, 'stoich.txt')
    options['rev'] = _relative_filename(tmp_dir.name, 'revs.txt')
    options['meta'] = _relative_filename(tmp_dir.name, 'mnames.txt')
    options['reac'] = _relative_filename(tmp_dir.name, 'rnames.txt')
    out_file = _relative_filename(tmp_dir.name, 'efms.mat')

     # Convert options dictionary to list of flags.
    options_list = [['-' + k, v] for _, (k, v) in enumerate(options.items())]
    args = [s for pair in options_list for s in pair] 
    args += ['-out', 'matlab', out_file]
    
    # Write inputs to temporary files.
    np.savetxt(options['stoich'], stoichiometry)
    with open(options['rev'], 'w') as file:
        file.write(' '.join(str(x) for x in reversibilities))
    with open(options['meta'], 'w') as file:
        file.write(' '.join('"' + x + '"' for x in metabolite_names))
    with open(options['reac'], 'w') as file:
        file.write(' '.join('"' + x + '"' for x in reaction_names))

    # Call efmtool, read result and clean up temporary directory.
    try:
        call_efmtool(args, jvm_options)
        efms = _read_efms_from_mat(tmp_dir.name)
    except:
        logger.error('EFM computation failed.')
        raise
    finally:    
        try:
            tmp_dir.cleanup()
        except:
            logger.warning(
                f'Unable to clean up temporary directory {tmp_dir.name}')

    return efms

def call_efmtool(
    args : List[str],
    jvm_options : List[str] = None
):
    """Wrapper for the ch.javasoft.metabolic.efm.main.CalculateFluxModes.matlab
    call. Note that we use matlab() instead of main() because the latter would
    terminate the process. This function is meant for advance usage. It does not
    perform any initialization and only calls efmtool with the given arguments.

    Parameters
    ----------
    args : List[str]
        List of arguments to be passed to efmtool.
    jvm_options : List[str], optional
        List of arguments to be passed to the JVM.
    """
    # Start JVM adding efmtool and its dependencies to the classpath
    global CalculateFluxModes
    if CalculateFluxModes is None:
        jvm_options = jvm_options or []
        libs_path = os.path.join(package_directory, 'lib/*')
        jpype.startJVM(*jvm_options, classpath = [libs_path])
        CalculateFluxModes = \
            jpype.JClass("ch.javasoft.metabolic.efm.main.CalculateFluxModes")

    # Call efmtool. We use the matlab call so that it doesn't kill the process.
    CalculateFluxModes.matlab(args)

def get_default_options() -> Dict:
    """Gets a dictionary containing default options for efmtool.

    Returns
    -------
    Dict
        The default options.
    """
    options = {
        'kind': 'stoichiometry',
        'arithmetic': 'double',
        'zero': '1e-10',
        'compression': 'default',
        'log': 'console',
        'level': 'INFO',
        'maxthreads': '-1',
        'normalize': 'min',
        'adjacency-method': 'pattern-tree-minzero',
        'rowordering': 'MostZerosOrAbsLexMin'
    }
    return options