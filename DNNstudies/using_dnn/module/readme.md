## Gardener

Common tools to modify tree variables, add new variables, add weights, ...

### 1. First copy an existing module :
```
cd LatinoAnalysis/Gardener/python/variables
cp AnyVariable.py NewVariable.py
```
### 2. Import the new module in gardener.py :
* https://github.com/latinos/LatinoAnalysis/blob/master/Gardener/scripts/gardener.py
```diff
+ from LatinoAnalysis.Gardener.variables.newVariable      import newVariableTreeMaker
```
### 3. Add it to the list of nuisnaces in gardener.py :
```diff
+ modules['newVariable']=NewVariableTreeMaker()
```
### 4. Document how-to use it in Gardener/test/README.md :
```
gardener.py  newVariable  input.root  output.root
```
