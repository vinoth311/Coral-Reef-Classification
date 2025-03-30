# **Hi everyone,,,**

Just added my code for final year project on my Bachelors in Computer Science :)

# **Coral Reef Classification with VGG16net and Finetuned deepseek-r1 1.5b LLM**

Research paper of oour project is added below. Please do cite if you find it useful


# **Research paper link:** https://ieeexplore.ieee.org/document/10847426


# **IEEE xplore DOI(10.1109/CICN63059.2024.10847426):** 
https://doi.org/10.1109/CICN63059.2024.10847426 

This Project covers a total of 4 modules

# **1: Collecting the dataset for coral classification and global coral map data**
We used 14 classes of coral structure data to classifiy the type of coral reef based on their structure


Dataset Link: https://universe.roboflow.com/giang-ha/rsmas-structure


For segementatation of the areas that classifies the corals on map the data is taken from allen coral maps 


Dataset link: https://allencoralatlas.org/atlas/#4.63/8.8971/71.7274

# **2: Training VGG16net DL model with the classification dataset**


We used VGG16net architecture to train the model and achieved the accuracy of 98.64% using data augumentation 
and the results are shown below 
![Screenshot 2024-10-31 184342](https://github.com/user-attachments/assets/91903459-ea7b-4ee1-b251-cbd5769bed49)
![Screenshot 2024-10-31 184308](https://github.com/user-attachments/assets/bb3d53a2-5dd0-4b7e-b108-6496d6cf27ea)
![Screenshot 2024-10-31 184247](https://github.com/user-attachments/assets/9a0f5bd0-8104-49f7-8a63-eff1e5f6849b)

# **3: Finetuning of Deepseek r1 1.5b model**


We used ollama to download the model and fine tune it suin sloth with the coral reef characteristics dataset to create a LLM which explains about the characteristics and other infromation related to coral reefs
and additionally we used RAG to increase the performance of the model and the results are added below
![Screenshot 2025-02-13 110602](https://github.com/user-attachments/assets/dfbe8cdf-3de3-4940-afc3-591182d7a323)
![Screenshot 2025-02-13 113107](https://github.com/user-attachments/assets/d93d4e41-ed25-4dce-8d31-e0015dd079b7)


# **4: Web interface for the project**


We used streamlit to develop the interface for the project mongodb is used as database and the main motive behind the web interface is to create awareness about coral reef and sustainability which helps to connect with other organisations .
Pictures are added below
![image](https://github.com/user-attachments/assets/42c7da44-03c5-41c5-9f5a-68b90938820a)
![image](https://github.com/user-attachments/assets/8d163ae8-713e-43c5-967a-a871a4469aa9)
![image](https://github.com/user-attachments/assets/efee916f-737e-4ff4-8368-5ec0c6f213af)
