class nearest_square:
    def __init__(num):
        self.num=num

    def find_nearest_square(self,num):

        """Function to calculate nearest square of any number.
            
        Args: 
            num (int): Any integer
        
        Returns: 
            Int: Nearest Square of num
        """

        answer = 0
        while (answer+1)**2 < self.num:
            answer += 1
        return answer**2