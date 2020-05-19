This repository contains supplementary material to the paper *Key Mismatch Attack on NewHope Revisited*  



All functions are contained in the file *attack.py*, we make few comments on the most important ones:

- Attack():
  - this function is called when *Attack.py* is executed (at the end of this file)
  - the input parameter is how many secret keys we want to attack (default value is 5)
  - secret keys are generated independently following the centered binomial distribution according to the NewHope specification
  - the function prints the average number of queries used to recover the secret keys

- Oracle():
  - this function implements the key mismatch oracle
  - the oracle is already implemented for the inputs we are using, this has no effect on the correctness of the attack 
  - it is also possible to implement the oracle using the full NewHope decapsulation, but it is slower and not necessary for our testing purposes

- RecoverSecretKey():
  - this function is the main building block in the function *Attack*
  - it recovers one whole secret key
  - when one wants to test our attack on some concrete secret key (instead of randomly chosen secret keys following the centered binomial distribution), then he can change the secret key manually (stored in the global variable) and then call this function

- T1_RecoverQuadruplet():
  - this function recovers one quadruplet of secret coefficients using tree T1
  - the recovered quadruplets is always correct

- T2_RecoverQuadruplet():
  - this functions recovers one quadruplet of secret coefficients using tree T2 or detects a problem with Hypothesis 1

Beside the *attack.py* file, there is a file called *NodeTree.py*. It is used only for reading json data from *T1.txt* and *T2.txt*.
