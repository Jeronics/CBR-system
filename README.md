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


Deadlines
----------

- 19/01/2015 Delivery 2: Project Documentation and software code.

- 22/01/2015 Delivery 3: Project work presentation and public exposition.
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
class CBRclass(object):
    """
    The class CBRclass defines in a general way the cases of the CBR.

    """
    def __init__(self, name, **kwargs):
```

| Method | Description |
| ------ | ----------- |
| add_class | Adds a class to the classes dictionary. |
| get_class | Gets a class from the classes dictionary. |
| pop_class | Removes the class 'name' from the dictionary of classes and returns it. |
| add_feature | These method adds a new attribute to the CBRclass. |
| get_feature | These method sets the values of an attribute from the CBRclass. |
| pop_feature | Removes and returns the element 'name' from the dictionary of attributes. |

### Case:
The Case class is a subclass of the CBRclass with an attribute called solution and a CBRclass
called problem. This class is the base of our CBR system.

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
