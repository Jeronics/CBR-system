CBR-system
==========

Task List
---------
- [x] **Data Structure**
- [x] **Read fast the data**
- [x] **Retrieve**
 - [x] Create abstract Retrieve.
 - [x] Match Iosu's implementation with the abstract case.
- [ ] **Reuse**
 - [ ] Create abstract Reuse.
 - [ ] Match Iosu's implementation with the abstract case.
- [ ] **Revise**
 - [x] Create abstract Revise.
 - [ ] Adapt the abstract case to our problem.
- [ ] **Retain**
 - [ ] Create abstract Retain.
 - [ ] Adapt the abstract case to our problem.

0. Data
-------
   - We have csv-s of first and second division of spain from 1996/97 til now. And lot of more information.
                        http://www.football-data.co.uk/spainm.php

   - Here we have history of 'quinielas': http://www.resultados-futbol.com/quiniela/historico/18
   
   - Here we have the statistics of the 2014-15: http://www.lfp.es/estadisticas/liga-bbva/goles/
   
   - Here we can get everything!!: http://www.marca.com/estadisticas/futbol/primera/2010_11/

1. Data Structure
-----------------
Consists in three classes:

### CBRclass:
Is an abstraction of an object class, which can contain other instances of CBRclass 
in a dictionary of classes and can also contain other data structures in the attributes 
dictionary.

```python
 def __init__(self, name, **kwargs):
```

### Case:
The Case class is a subclass of the CBRclass with an attribute called solution and a CBRclass
called problem.

```python
def __init__(self, name, problem, **kwargs):
```

### CaseBase:
This class contains basically a dictionary with all the cases in our Case Base. 

```python
def __init__(self):
```

2. Retrieve
-----------

3. Reuse
--------

4. Revise
---------

5. Retain
---------
