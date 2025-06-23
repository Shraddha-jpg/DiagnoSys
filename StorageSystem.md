### Storage System Simulator

The **Storage System Simulator** is an intuitive and interactive web-based tool designed to simulate the working of storage systems efficiently. 
The first core entity in this simulator is the **System** object, which allows users to specify key performance parameters including 
**Max Throughput (in MB/s)** and **Max Capacity (in GB)**. 
With a sleek user interface, users can easily create new systems, view all configured systems, or delete them as needed. 

![Storage System Simulator UI](images/system.png)

On successfully creating a system, the following response will be displayed with port number assigned to the system along with a unique ID using the following python function: **str(uuid.uuid4())**, which ensures that no two UUID's collide across systems.

![System creation response](images/response.png)

The storage system handles duplicate system creation efficiently by displaying the following error when user tries to create a system in the same instance. 

![System creation response error](images/responseerror.png)




