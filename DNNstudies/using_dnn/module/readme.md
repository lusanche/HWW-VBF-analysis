## Gardener

Common tools to modify tree variables, add new variables, add weights, ...

### 1. First copy an existing module :
```
- cd LatinoAnalysis/Gardener/python/variables
cp AnyVariable.py NewVariable.py
```
### 2. Import the new module in gardener.py :
* https://github.com/latinos/LatinoAnalysis/blob/master/Gardener/scripts/gardener.py
```
from LatinoAnalysis.Gardener.variables.anotherUncertainty        import AnotherUncertaintyTreeMaker
```

