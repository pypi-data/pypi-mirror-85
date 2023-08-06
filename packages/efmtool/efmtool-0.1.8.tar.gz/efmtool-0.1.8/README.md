# Python wrapper for efmtool
efmtool is a Java software for the enumeration of Elementary Flux Modes (EFMs)
developed by Marco Terzer at ETH Zurich. This package provides a simple Python
wrapper.

## Installation
`pip install efmtool`

## Usage
The wrapper provides two ways of calling efmtool:
1.  Through a simplified interface: 
    
    ```Python
    efms = efmtool.calculate_efms(
        stoichiometry : np.array,
        reversibilities : List[int],
        reaction_names : List[str],
        metabolite_names : List[str],
        options : Dict = None,
        jvm_options : List[str] = None)
    ```
    
    This function directly returns a NumPy array containing all the EFMs of the
    specified network ([example](./examples/small_network.py)).
    `reversibilities` is a list indicating whether a reaction is reversible (1)
    or not (0). Note that irreversibilities are assumed to be in forward
    directions. If a reaction is irreversible in the backward direction, it
    should be reversed before calling efmtool. Default options can be obtained
    through `get_default_options()`.


1.  Through a generic wrapper:
    
    ```Python
    efmtool.call_efmtool(
        args : List[str],
        jvm_options : List[str] = None)
    ```

    The wrapper simply calls efmtool passing the specified arguments.
    Specifying, writing and reading input/output temporary files is
    responsibility of the user.

See `config/metabolic-efm.xml`, the documentation, or run `java -cp
lib/metabolic-efm-all.jar ch.javasoft.metabolic.efm.main.CalculateFluxModes
--help` for more information about the available options.

## Cite us

If you use efmtool in a scientific publication, please cite our paper:

Terzer, M., Stelling, J., 2008. "Large-​scale computation of elementary flux
modes with bit pattern trees". *Bioinformatics*. -
[link](http://doi.org/10.1093/bioinformatics/btn401)


## Credits
efmtool is a software written by Marco Terzer (ETH Zurich).

Python wrapper by Mattia Gollub (ETH Zurich).