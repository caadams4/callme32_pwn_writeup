# Callme32
Description and Writeup of the ROPEmporium's Callme32 challenge. 

The ROP Emporium callme32 challenge is a problem which requires the use of a gadget to solve. To produce the decrypted flag, one must call each function callme_one, callme_two, and callme_three with the parameters 0xdeadbeef, 0xcafebabe and 0xd00df00d. 

#Solving the problem
We start by running a 'checksec callme32' command and find there is no PIE enabled, so the addresses of the functions we need to call are static. 

![image](https://user-images.githubusercontent.com/79220528/156766257-f56597b9-8255-4774-bd08-f31336b86651.png)

Next, we want to check to see which functions the binary imports with the command: 'rabin2 -i callme32'. Note the addresses of the callme_one/two/three functions.

![image](https://user-images.githubusercontent.com/79220528/156766177-9eb6b4a0-0bf6-4138-a421-644a1f20021d.png)

Open the binary with rabin2 with the command 'r2 callme32' and observe the pwnme function. We want to hijack the ret/leave to point to our desired callme_one/two/three functions.

![image](https://user-images.githubusercontent.com/79220528/156766003-22a5aa5f-fbe7-4ca8-9fae-c79a1a95a5ee.png)

We know var_28h in 0x28 bytes away from the base pointer, and 0x28+0x4 bytes away from the return to main address. Our payload must begin with 0x2c bytes of junk followed by the callme_one address to hijack the instruction pointer.

At this stage, our payload is: 0x2c x b'a' + callme_one_address

After hijacking the instruction pointer, we check out the ROPgadgets. We are looking to pop three variables off the stack to send call the next callme function at the next return address. 

![image](https://user-images.githubusercontent.com/79220528/156765393-0ebe6c71-34f4-4843-8664-8a8d0baf3994.png)

The ROPgadget for our situation is 0x080487f8 : pop ebx ; pop esi ; pop edi ; pop ebp ; ret and we will call it ROPPOP. 

So we know the offset, ROPgedet, variables and function addresses. Now we craft our payload. 

payload = b'a' * junkOffset + callme1 + ROPPOP + variables + callme2 + ROPPOP + variables + callme3 + ROPPOP + variables

Using pwntools, we create the process, send the payload, and print the output. 



