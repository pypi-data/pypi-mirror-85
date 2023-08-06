import os

from configparser import ConfigParser


class Progress():
    """An object for keeping track of progress in case a process gets interupted.  It creates and saves progress to a file.
    
     Args:
            fp (str): file path of file to save progress into
            vars (list(str)): list of variables to include in progress file and keep track of.
    """

    def __init__(self, fp, vars=['last_index_processed']):
        self.fp = fp
        self.vars = vars
        self.name = 'PROGRESS'
        self.values = {}
        self.cp = ConfigParser()
        # Read config file, if not exists then create one.
        if not os.path.exists(fp):
            for var in vars:
                self.cp[self.name] = {var: 0}
                self.values[var] = 0
            self.__save()
        else:
            for var in vars:
                self.values[var] = int(self.cp.get(self.name, var))


    def increment(self, var='last_index_processed'):
        """Increment progress of 'var' by 1

        Args:
            var (str, optional): Variable to increment. Defaults to 'last_index_processed'.
        """

        try:
            self.values[var] += 1
            self.cp.set(self.name, var, str(self.values[var]))
            self.__save()
        except KeyError:
            print(f'KeyError: {var} does not exist in progress object.')


    def reset(self, var='last_index_processed'):
        """Reset progress to 0
        
        Args:
            var (str, optional): Variable to reset. Defaults to 'last_index_processed'.
        """

        try:
            self.values[var] = 0
            self.cp.set(self.name, var, str(self.values[var]))
            self.__save()
        except KeyError:
            print(f'KeyError: {var} does not exist in progress object.')


    def delete(self):
        """Delete file where progress is stored.
        """
        try:
            os.remove(self.fp)
        except Exception as e:
            print(e)


    def __save(self):
        try:
            with open(self.fp, 'w') as configfile:
                self.cp.write(configfile)
        except Exception as e:
            print(e)
