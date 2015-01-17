This is a general readme file for the "CBR Bet Assistant" application.
Following is a description package structure:
 1. The file "README.md" is provided to display relevant information on the GitHub hosting page of this project:
    https://github.com/Jeronics/CBR-system
 2. Technical and user manuals are located in the folder "report/"
 3. Source code of the CBR Bet Assistant can be found under "src/"
 4. Datasets (obtained from http://www.football-data.co.uk/spainm.php) are stored in the directories "data/[Test|Train]/".
 5. Description of the main files:
    * src/main.py -- this is the main application file that serves as an entry point to run the CBR
    * src/internal_repr/* -- contains definition of the entities to represent Case, CaseBase and individual phases in a generic way
    * src/wrapper.py -- serves to provide a domain-targeted implementation of the generic entities
    * src/utils.py -- numerous utility functions that are used throughout the system