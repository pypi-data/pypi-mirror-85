# ms_thermo

![logo_msthermo](http://cerfacs.fr/coop/whatwedo/logo_msthermo.gif). This is the CERFACS minimal package for multispecies reactive operations. 

*It is available on [pipy](https://pypi.org/project/ms-thermo/), 
documentation is on [readtthedocs](https://ms-thermo.readthedocs.io/en/latest/), sources are mirrored on [gitlab.com](https://gitlab.com/cerfacs/ms_thermo)*

## Installation 

Install from Python Package index:

```
pip install ms_thermo
```

## Command line tools 

Once the package is installed, you have acces in your terminal to a CLI from the command `ms_thermo`:

```bash
Usage: ms_thermo [OPTIONS] COMMAND [ARGS]...

  ---------------    MS_THERMO  --------------------

  You are now using the Command line interface of MS-Thermo, a Python3
  helper for reactive multispecies computation, created at CERFACS
  (https://cerfacs.fr).

  This is a python package currently installed in your python environement.
  See the full documentation at : https://ms-
  thermo.readthedocs.io/en/latest/.

Options:
  --help  Show this message and exit.

Commands:
  fresh-gas    description of a non-reacted kero-air mixture.
  gasout       Apply GASOUT actions to a CFD field.
  hp-equil     HP equilibrium using Cantera.
  tadia        adiabatic flame temperature for Kerosene.
  yk-from-phi  Mass fractions of a fuel-air mixture.
```


### The `tadia` command

This returns the burnt gas temperature and mass fractions using a tabulation on Kerosene.
The tabulation was created using [CANTERA](https://cantera.org/).

A typical usage is, for a stoechiometric fresh gas mixture at ambiant conditions:

```
>ms_thermo tadia 300. 101325 1.


The adiabatic flame temperature of a mix C10H22-air from tables is : 2312.99 K.

Species     |    Mass fraction
------------------------------
N2          |       0.718
fuel        |       0.000
O2          |       -0.000
CO2         |       0.200
H2O         |       0.082
```

### The `hp-equil` command

This returns the burnt gas temperature and mass fractions using a CANTERA `.cti` file.

A typical usage is, for a stoechiometric fresh gas mixture at ambiant conditions:

```
>ms_thermo hp_equil 300 101325 1 NC10H22 ../../Desktop/Luche1.cti


**** WARNING ****
For species C5H4O, discontinuity in cp/R detected at Tmid = 1000
	Value computed using low-temperature polynomial:  22.0928
	Value computed using high-temperature polynomial: 22.1544

The adiabatic flame temperature of a mix C10H22-air from cantera is : 2277.41 K.

Species     |    Mass fraction
------------------------------
CO          |       0.014
CO2         |       0.172
H2O         |       0.084
N2          |       0.718
NO          |       0.003
O2          |       0.007
OH          |       0.002
+ 82 others |       0.000
```
**WARNING**: If you do not have CERFACS's CANTERA installed in your virtual environment, this function will not be available!!

### The `yk_from_phi` command

This returns the mass fractions of fresh gases according to chemical composition of the fuel and equivalence ratio.

Typical usage is :

```
>ms_thermo yk-from-phi 0.5 10. 22. 

Species     |    Mass fraction
------------------------------
fuel        |       0.466
N2          |       0.410
O2          |       0.125
```
### The `fresh_gas`command
This calculates the conservative variables of a Kerosene/air fresh gas mixture from primitive variables P, T and phi (equivalence ratio).

Typical usage is:

```
>ms_thermo fresh-gas 300 101325. 1.

rho       |  1.232 kg/m3
rhoE      |  266054.682 J.kg/m3
rhoYk     |
 N2       |  0.886 mol.kg/m3
 O2       |  0.269 mol.kg/m3
 KERO     |  0.077 mol.kg/m3
```


### The `gasout`command

This command is an example of a tool build on ms-thermo package for the setup of a CFD computation. It can apply several local alteration to a CFD field.
The typical input file is :

```yaml

#This is the tentative input file of a python Gasout.
# Enable YAML syntax highlighting in you IDE for the best experience.

# input files
inst_solut: ./solut_0003.sol.h5
mesh: ./solut_0003.mesh.h5
inst_solut_output: ./gasouted.sol.h5

# list (each - block) of actions to take
actions:
- type: directional_linear_mask
  direction: "x"             #direction x, y, or z
  max_abcissa: 0.11        #If None, takes  70% of CAO size
  min_abcissa: 0.1         #If None, takes  30% of CAO size
  new_pressure: null       #use null if you dont want to edit this field
  new_temperature: 2000.0  # Temp in K.
  new_yk: null

- type: spherical_tanh_mask
  center: [0.1, 0.1, 0]    # center sphere. If None, takes CAO center.
  radius: 0.01              # radius sphere [m]. If None, takes from CAO size
  delta: 0.05              # transition thickness [m], If None, takes half rad
  new_pressure: null
  new_temperature: 1600.
  new_yk:                  # dictionnary of species Yk
    N2: 0.8                # order and competion does not matter
    O2: 0.2                # Sum MUST be 1!

- type: fraction_z_mask
  specfuel: KERO_LUCHE     # Fuel spec name
  atom_ref: C              # reference atom for Z computation
  oxyd_mass_fracs:                 # Mixture oxidizer, for Z computation.
    O2: 0.233              #   If None, takes AIR
    N2: 0.767
  fuel_mass_fracs:  None          # Mixture fuel. dict of Yk.
  zmax: 0.02              #   If None, takes the mix at the Higesh Yk fuel
  zmin: 0.01
  new_pressure: 103000.0  # Pressure in Pa
  new_temperature: null
  new_yk: null

- type: fraction_z_mask    # You can repeat several treatments
  specfuel: KERO_LUCHE
  atom_ref: C
  oxyd_mass_fracs:
    O2: 0.233
    N2: 0.767
  fuel_mass_fracs:  None
  zmax: 0.05
  zmin: 0.04
  new_pressure: 103000.0
```



## Packages usage

The `ms_thermo` is also meant to be used in lager scripts/packages.

### The `state` class

The state class handles a mixture of gases.

Typical usage for this class . The following script creates an initial mixture of fresh gases, then changes a subset of the field into hot gases.

```
>>> import ms_thermo as ms
>>> case = ms.State()
>>> print(case)

Current primitive state of the mixture

		        | Most Common |    Min    |    Max 
----------------------------------------------------
             rho| 1.17192e+00 | 1.172e+00 | 1.172e+00 
          energy| 2.16038e+05 | 2.160e+05 | 2.160e+05 
     temperature| 3.00000e+02 | 3.000e+02 | 3.000e+02 
        pressure| 1.01325e+05 | 1.013e+05 | 1.013e+05 
            Y_O2| 2.32500e-01 | 2.325e-01 | 2.325e-01 
            Y_N2| 7.67500e-01 | 7.675e-01 | 7.675e-01 

>>> case.temperature = 1200
>>> print(case)

Current primitive state of the mixture 
			   	| Most Common |    Min    |    Max 
----------------------------------------------------
             rho| 2.92980e-01 | 2.930e-01 | 2.930e-01 
          energy| 9.41143e+05 | 9.411e+05 | 9.411e+05 
     temperature| 1.20000e+03 | 1.200e+03 | 1.200e+03 
        pressure| 1.01325e+05 | 1.013e+05 | 1.013e+05 
            Y_O2| 2.32500e-01 | 2.325e-01 | 2.325e-01 
            Y_N2| 7.67500e-01 | 7.675e-01 | 7.675e-01 


```


