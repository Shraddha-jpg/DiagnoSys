### Storage System Simulator

The **Storage System Simulator** is an intuitive and interactive web-based tool designed to simulate the working of storage systems efficiently. 

### System Object

The first core entity in this simulator is the **System** object, which allows users to specify key performance parameters including 
**Max Throughput (in MB/s)** and **Max Capacity (in GB)**. 
With a sleek user interface, users can easily create new systems, view all configured systems, or delete them as needed. 

![Storage System Simulator UI](images/system.png)

On successfully creating a system, the following response will be displayed with port number assigned to the system along with a unique ID using the following python function: **str(uuid.uuid4())**, which ensures that no two UUID's collide across systems.

![System creation response](images/response.png)

The storage system handles duplicate system creation efficiently by displaying the following error when user tries to create a system in the same instance. 

![System creation response error](images/responseerror.png)

The view all button displays all systems created under the current instance along with their attributes(max capacity,max throughput and name) as shown below. There are also update and delete functionalities that allow users to alter the attribute values or delete the system permanently. 

![System creation response view all](images/viewall.png)


### Volume Object

The **Volume** object represents an individual storage unit that can be created within a specific system in the Storage System Simulator. Each volume requires a unique **Volume Name**, a defined **Volume Size (in GB)**, and an association with an existing setting through the **Select Volume** dropdown. This feature allows users to simulate multiple volumes within storage systems, enabling better testing and modeling of storage allocation scenarios like system utilization.

![Storage System Simulator UI for Volume](images/volume.png)

Shown below is the response for successful creation of a volume, along with settings(to be applied as of the picture) and other attributes. 

![Storage System Simulator UI for Volume](images/volumecreationresponse.png)



















