import os

from configparser import ConfigParser

class Progress():
    """An object for keeping track of progress in case a process gets interupted.  It creates and saves progress to a file.
    """    
    
    def __init__(self, name, fp):
        """Create new progress file if none exists and sets the initial value progress to 0.

        Args:
            name (str): Name of progress variable
            fp (str): file path of file to save progress into.
        """        
        self.name = name
        self.fp = fp
        
        self.cp = ConfigParser()
        # Read config file, if not exists then create one.
        if not os.path.exists(fp):
            self.cp[name] = {'last_index_processed': 0}
            self.__save()
        else:
            self.cp.read(fp)
            if not self.cp.has_section(name):
                self.cp[name] = {'last_index_processed': 0}
                self.__save()
        
        self.value = int(self.cp.get(name, 'last_index_processed'))
    
    def increment(self):
        """Increment progress by 1
        """        
        self.value += 1
        self.cp.set(self.name, 'last_index_processed', str(self.value))
        self.__save()
    
    def reset(self):
        """Reset progress to 0
        """        
        self.value = 0
        self.cp.set(self.name, 'last_index_processed', str(self.value))
        self.__save()
        
    def delete(self):
        """Delete file where progress is stored.
        """        
        os.remove(self.fp)

    def __save(self):
        try:
            with open(self.fp, 'w') as configfile:
                self.cp.write(configfile)
        except Exception as e:
            print(e)
        

# p = Progress('TEST_VAR3', 'D:/projects_2019/06-data-eng/02-coursework/de-nanodegree/de-nano-projects/de-nano-final-project/austin-micromobility-data-lake/src/smci_tool_etl/utils/test_progress.cfg')
