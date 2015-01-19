This is a general readme file for the "CBR Bet Assistant" application.
Following is a description package structure:

 1. The file "README.md" is provided to display relevant information on the GitHub hosting page of this project:
    https://github.com/Jeronics/CBR-system

 2. "Technical manual" and "User manual" are located in the folder "report/"

 3. Source code of the CBR Bet Assistant can be found under "cbr/"

 4. Datasets (obtained from http://www.football-data.co.uk/spainm.php) are stored in the directories "data/[Test|Train]/".

 5. Description of the main files:
    * cbr/core/main.py -- this is the main application file that serves as an entry point to run the CBR
    * cbr/core/internal_repr/* -- contains definition of the entities to represent Case, CaseBase and individual phases in a generic way
    * cbr/core/wrapper.py -- serves to provide a domain-targeted implementation of the generic entities
    * cbr/core/utils.py -- numerous utility functions that are used throughout the system
    * cbr/web/* -- web interface for the CBR system