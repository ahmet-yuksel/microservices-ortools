# microservices-ortools

#Docker Container da çalıştırmak için

Docker container da çalıştırmak için proje dizinde iken aşağıdaki komutu çalıştırarak servis ayağa kaldırabilirsiniz.

`docker-compose up -d`

Docker container kurulumları tamamlandıktan servise 
http://localhost:8002/calc_optimal_route erişilebilinir.

Test için aşağıdaki komut çalıştırılmalıdır.

`docker-compose exec web pytest .`

Proje folder ındaki MicroServices Call .postman_collection.json dosyası kullanarak Postman Request oluşturulabilir.

#lokal de  çalıştırmak için

`python3.7.3` kurulu bilgisayarda veya enviroment'a aşağıdaki komut ile gerekli lib ler kurulmalı

`pip install -r /usr/src/app/requirements.txt \`

proje dizinindeki src/app/main.py dosyasındaki aşağıdaki satırların yorum satırı karakterini(#) kaldırmak gerekli

`#from vrp_ortools import get_optimal_routes`

ve 

`#if __name__ == "__main__":`

`#uvicorn.run(app, host="0.0.0.0", port=8000)`

son olarak aşağıdaki satırın yorum satırı yapılmalıdır.

`from .vrp_ortools import get_optimal_routes`

aşağıdaki komut ile webservis lokal bilgisayarda çalıştırılabilir.

`python src/app/main.py`

